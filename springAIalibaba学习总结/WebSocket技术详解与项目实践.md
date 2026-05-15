# WebSocket 技术详解与项目实践

## 一、WebSocket 技术概述

### 1.1 什么是 WebSocket

WebSocket 是一种**全双工通信协议**，它允许客户端和服务器之间建立持久连接，实现实时双向数据传输。

**核心特点：**

| 特性 | 说明 |
|------|------|
| **全双工** | 客户端和服务器可同时发送和接收数据 |
| **持久连接** | 连接建立后保持打开状态，直到主动关闭 |
| **低延迟** | 避免 HTTP 请求的握手开销 |
| **原生支持** | 现代浏览器原生支持 |

### 1.2 WebSocket 与 HTTP 的对比

| 对比维度 | HTTP | WebSocket |
|---------|------|-----------|
| **通信方向** | 单向（客户端发起） | 双向（全双工） |
| **连接方式** | 短连接（每次请求建立） | 长连接（持续保持） |
| **延迟** | 高（每次请求需握手） | 低（连接建立后即时通信） |
| **适用场景** | 普通网页请求 | 实时聊天、实时监控、推送通知 |

### 1.3 WebSocket 协议握手过程

WebSocket 连接建立需要经过一次 HTTP 握手：

1. **客户端发起请求**：发送带有 `Upgrade: websocket` 头部的 HTTP 请求
2. **服务器响应**：返回 101 状态码，表示协议切换成功
3. **建立连接**：后续数据通过 WebSocket 协议传输

```http
# 客户端请求
GET /ws/chat HTTP/1.1
Host: localhost:18080
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13

# 服务器响应
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

---

## 二、Spring Boot 中的 WebSocket 实现

### 2.1 核心组件

Spring Boot 提供了完整的 WebSocket 支持，主要组件包括：

| 组件 | 作用 |
|------|------|
| `@EnableWebSocket` | 启用 WebSocket 支持 |
| `WebSocketConfigurer` | 注册 WebSocket 处理器 |
| `WebSocketHandler` | 处理 WebSocket 消息 |
| `TextWebSocketHandler` | 文本消息处理器（抽象类） |

### 2.2 依赖配置

```xml
<!-- pom.xml -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-websocket</artifactId>
</dependency>
```

---

## 三、项目中的 WebSocket 配置

### 3.1 WebSocketConfig 配置类

```java
package com.example.springaialibaba.config;

import com.example.springaialibaba.websocket.ChatWebSocketHandler;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.socket.config.annotation.EnableWebSocket;
import org.springframework.web.socket.config.annotation.WebSocketConfigurer;
import org.springframework.web.socket.config.annotation.WebSocketHandlerRegistry;

@Configuration
@EnableWebSocket  // 启用 WebSocket 功能
public class WebSocketConfig implements WebSocketConfigurer {

    private final ChatWebSocketHandler chatWebSocketHandler;

    // 构造注入 Handler
    public WebSocketConfig(ChatWebSocketHandler chatWebSocketHandler) {
        this.chatWebSocketHandler = chatWebSocketHandler;
    }

    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
        registry.addHandler(chatWebSocketHandler, "/ws/chat")  // 注册处理器，映射路径 /ws/chat
                .setAllowedOriginPatterns("*");  // 允许所有来源（生产环境需限制）
    }
}
```

**配置要点：**

1. **`@EnableWebSocket`**：启用 WebSocket 自动配置
2. **`registerWebSocketHandlers`**：注册自定义处理器
3. **路径映射**：`/ws/chat` 是 WebSocket 连接端点
4. **跨域配置**：`setAllowedOriginPatterns("*")` 允许跨域

### 3.2 ChatWebSocketHandler 消息处理器

```java
package com.example.springaialibaba.websocket;

import org.springframework.ai.chat.messages.SystemMessage;
import org.springframework.ai.chat.messages.UserMessage;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import java.util.List;

@Component
public class ChatWebSocketHandler extends TextWebSocketHandler {

    private final ChatModel chatModel;

    public ChatWebSocketHandler(ChatModel chatModel) {
        this.chatModel = chatModel;
    }
}
```

---

## 四、消息处理流程详解

### 4.1 连接建立阶段

```java
@Override
public void afterConnectionEstablished(WebSocketSession session) {
    try {
        // 连接建立成功后发送欢迎消息
        session.sendMessage(new TextMessage("Connected successfully! You can start chatting."));
    } catch (Exception e) {
        e.printStackTrace();
    }
}
```

**流程说明：**

1. 客户端通过 `new WebSocket('ws://localhost:18080/ws/chat')` 发起连接
2. 服务器接收连接请求，完成握手
3. 触发 `afterConnectionEstablished` 方法
4. 向客户端发送连接成功消息

### 4.2 消息处理阶段

```java
@Override
protected void handleTextMessage(WebSocketSession session, TextMessage message) {
    String userMessage = message.getPayload();  // 获取用户消息

    try {
        // 构建 Prompt
        SystemMessage systemMessage = new SystemMessage("你是一位专业助手，回答简洁明了");
        UserMessage userMsg = new UserMessage(userMessage);
        Prompt prompt = new Prompt(List.of(systemMessage, userMsg));

        // 流式调用 AI 模型
        chatModel.stream(prompt)
            .doOnNext(response -> {
                // 处理每个响应块
                String content = response.getResults().get(0).getOutput().getText();
                if (content != null && !content.isEmpty()) {
                    synchronized (session) {
                        if (session.isOpen()) {
                            session.sendMessage(new TextMessage(content));
                        }
                    }
                }
            })
            .doOnError(error -> {
                // 处理错误
                session.sendMessage(new TextMessage("Error: " + error.getMessage()));
            })
            .doOnComplete(() -> {
                // 完成标志
                synchronized (session) {
                    if (session.isOpen()) {
                        session.sendMessage(new TextMessage("[DONE]"));
                    }
                }
            })
            .subscribe();  // 订阅流
    } catch (Exception e) {
        session.sendMessage(new TextMessage("Error: " + e.getMessage()));
    }
}
```

**核心流程：**

```
┌─────────────────────────────────────────────────────────────────┐
│                    WebSocket 消息处理流程                       │
├─────────────────────────────────────────────────────────────────┤
│  1. 用户发送消息                                               │
│     └─> WebSocketSession.receive()                            │
│                                                               │
│  2. handleTextMessage() 处理                                   │
│     └─> 解析用户消息                                            │
│     └─> 构建 Prompt (SystemMessage + UserMessage)              │
│                                                               │
│  3. AI 模型流式调用                                            │
│     └─> chatModel.stream(prompt)                              │
│     └─> Flux<ChatResponse> 响应流                             │
│                                                               │
│  4. 流式响应处理                                               │
│     ├─> doOnNext: 每收到一个响应块                             │
│     │     └─> 获取文本内容                                      │
│     │     └─> 发送到客户端                                      │
│     ├─> doOnError: 处理错误                                    │
│     │     └─> 发送错误消息                                      │
│     └─> doOnComplete: 完成时                                   │
│           └─> 发送 [DONE] 标志                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3 连接关闭阶段

```java
@Override
public void afterConnectionClosed(WebSocketSession session, CloseStatus status) {
    System.out.println("WebSocket connection closed: " + status);
    // 可以在此处清理资源、记录日志等
}
```

**关闭原因：**
- 客户端主动关闭连接
- 服务器主动断开连接
- 网络中断

---

## 五、并发安全处理

### 5.1 线程安全问题

WebSocket 会话在多线程环境下存在并发问题：
- 多个响应块可能同时发送
- 会话可能在发送过程中关闭

### 5.2 同步处理

```java
synchronized (session) {
    if (session.isOpen()) {
        session.sendMessage(new TextMessage(content));
    }
}
```

**同步机制说明：**

| 措施 | 作用 |
|------|------|
| `synchronized (session)` | 确保同一会话的消息顺序发送 |
| `session.isOpen()` | 发送前检查连接状态 |
| 响应式流 | 保证消息顺序性 |

---

## 六、前端调用示例

### 6.1 WebSocket 客户端代码

```javascript
// 创建 WebSocket 连接
const socket = new WebSocket('ws://localhost:18080/ws/chat');

// 连接建立
socket.onopen = function() {
    console.log('WebSocket connected');
};

// 接收消息
socket.onmessage = function(event) {
    if (event.data === '[DONE]') {
        console.log('Response completed');
        return;
    }
    console.log('Received:', event.data);
};

// 发送消息
function sendMessage(message) {
    socket.send(message);
}

// 连接关闭
socket.onclose = function(event) {
    console.log('WebSocket closed:', event.code, event.reason);
};
```

---

## 七、完整架构图

```
┌──────────────────────────────────────────────────────────────────┐
│                      架构流程图                                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────┐      WebSocket      ┌────────────────────┐    │
│   │   Browser    │ ──────────────────> │   WebSocketConfig │    │
│   │   (Client)   │      /ws/chat       │  注册 Handler     │    │
│   └──────┬───────┘                     └─────────┬──────────┘    │
│          │                                        │               │
│          │                                        ▼               │
│          │                              ┌─────────────────────┐   │
│          │                              │ ChatWebSocketHandler│   │
│          │                              │                     │   │
│          │                              │ 1. handleTextMessage│   │
│          │                              │ 2. 构建 Prompt     │   │
│          │                              │ 3. 调用 ChatModel  │   │
│          │                              │ 4. 流式返回结果    │   │
│          │                              └─────────┬───────────┘   │
│          │                                        │               │
│          │                                        ▼               │
│          │                              ┌─────────────────────┐   │
│          │◄─────────────────────────────│     ChatModel      │   │
│          │         Stream Response       │   (AI 模型)       │   │
│          │                              └─────────────────────┘   │
│                                                                 │
└──────────────────────────────────────────────────────────────────┘
```

---

## 八、技术要点总结

### 8.1 WebSocket 核心优势

1. **实时性**：低延迟双向通信
2. **效率**：避免 HTTP 重复握手开销
3. **全双工**：服务器可主动推送

### 8.2 实现注意事项

1. **线程安全**：使用同步机制保护会话状态
2. **资源管理**：及时清理关闭的连接
3. **错误处理**：完善的异常捕获和错误消息返回
4. **跨域配置**：生产环境应限制允许的来源

### 8.3 适用场景

| 场景 | 说明 |
|------|------|
| **实时聊天** | 即时消息、在线客服 |
| **实时监控** | 数据仪表盘、告警推送 |
| **协作编辑** | 多人协同文档编辑 |
| **游戏通信** | 实时游戏状态同步 |

---

## 九、代码优化建议

### 9.1 异常处理增强

```java
@Override
protected void handleTextMessage(WebSocketSession session, TextMessage message) {
    String userMessage = message.getPayload();
    
    // 消息长度限制
    if (userMessage.length() > 1000) {
        sendError(session, "Message too long");
        return;
    }
    
    // 空消息检查
    if (userMessage.trim().isEmpty()) {
        sendError(session, "Empty message");
        return;
    }
    
    // 业务处理...
}

private void sendError(WebSocketSession session, String errorMessage) {
    try {
        session.sendMessage(new TextMessage("[ERROR] " + errorMessage));
    } catch (Exception e) {
        // 日志记录
    }
}
```

### 9.2 连接管理优化

```java
// 维护活跃连接列表
private final Set<WebSocketSession> activeSessions = new CopyOnWriteArraySet<>();

@Override
public void afterConnectionEstablished(WebSocketSession session) {
    activeSessions.add(session);
    // 发送欢迎消息
}

@Override
public void afterConnectionClosed(WebSocketSession session, CloseStatus status) {
    activeSessions.remove(session);
    // 清理资源
}

// 广播消息到所有连接
public void broadcast(String message) {
    for (WebSocketSession session : activeSessions) {
        try {
            if (session.isOpen()) {
                session.sendMessage(new TextMessage(message));
            }
        } catch (Exception e) {
            // 处理异常
        }
    }
}
```

---

## 十、参考资料

1. [Spring WebSocket 官方文档](https://docs.spring.io/spring-framework/docs/current/reference/html/web.html#websocket)
2. [WebSocket 协议规范](https://datatracker.ietf.org/doc/html/rfc6455)
3. [Spring Boot WebSocket 教程](https://spring.io/guides/gs/messaging-stomp-websocket/)
