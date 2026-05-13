# Spring AI Alibaba 学习总结

## 为什么要学 Spring AI Alibaba

你有没有遇到过这种情况：想给自己的应用加上 AI 能力，结果被各种 API 文档、认证方式、响应格式搞得一头雾水？或者写了一段 AI 调用的代码，下次换了个模型又要重写一大半？

Spring AI Alibaba 就是来解决这些问题的。它是阿里云对 Spring AI 框架的深度适配，让你可以用统一的写法，调用通义千问、OpenAI、DashScope 等各种大模型，而不用关心底层到底是谁在干活。

换句话说：学一次，到处能用。

## 学习路线图

下面这张图展示了整个学习路径，从最基础的"Hello World"开始，逐步深入到高级的 RAG 和 MCP 应用：

```
┌─────────────────────────────────────────────────────────────────┐
│                      Spring AI Alibaba 学习路线                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   第一阶段：Hello World        →  掌握基础对话和流式响应           │
│         ↓                                                        │
│   第二阶段：Tool Calling       →  让 AI 调用外部工具和函数          │
│         ↓                                                        │
│   第三阶段：MCP               →  使用 Model Context Protocol     │
│         ↓                                                        │
│   第四阶段：RAG               →  构建检索增强生成系统              │
│         ↓                                                        │
│   第五阶段：综合实战           →  将所有技术融会贯通               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 第一阶段：Hello World（入门基础）

**教学目标**：掌握 Spring AI Alibaba 的基本用法，包括简单对话、流式响应、多轮对话记忆。

**对应模块**：`spring-ai-alibaba-helloworld`

### 你会学到什么

1. **最简单的 AI 对话**
   
   只需要几行代码，就能让 AI 回答你的问题：

   ```java
   @GetMapping("/simple/chat")
   public String simpleChat() {
       return chatClient.prompt()
           .user("你好，请介绍一下自己")
           .call()
           .content();
   }
   ```

2. **流式响应（像 ChatGPT 一样打字效果）**
   
   不再等待漫长的加载，显示 AI 正在"思考"的过程：

   ```java
   @GetMapping("/stream/chat")
   public Flux<String> streamChat() {
       return chatClient.prompt()
           .user("请讲一个关于春天的故事")
           .stream()
           .content();
   }
   ```

3. **多轮对话记忆（让 AI 记住上下文）**
   
   这是智能客服的基础——AI 能记住你们之前聊了什么：

   ```java
   // 第一轮
   curl "http://localhost:8080/advisor/chat/session123?message=我叫小明"
   
   // 第二轮 - AI 能记住我叫小明
   curl "http://localhost:8080/advisor/chat/session123?message=你还记得我叫什么吗？"
   ```

### 快速启动

```bash
# 设置 API Key
export AI_DASHSCOPE_API_KEY=your_api_key_here

# 启动项目
mvn -pl spring-ai-alibaba-helloworld spring-boot:run
```

### 核心配置

```yaml
spring:
  ai:
    dashscope:
      api-key: ${AI_DASHSCOPE_API_KEY}
      chat:
        model: qwen-plus
        options:
          temperature: 0.7
          max-tokens: 2000
```

### 学完这个能做什么

- 简单的 AI 问答机器人
- 带打字效果的实时对话界面
- 需要记忆上下文的多轮对话系统（比如智能客服）

---

## 第二阶段：Tool Calling（工具调用）

**教学目标**：让 AI 能够调用外部工具和 API，真正完成实际任务，比如查天气、翻译、查地址等。

**对应模块**：`spring-ai-alibaba-tool-calling-example`

### 你会学到什么

这是 AI 从"会说话"到"会做事"的关键一步。Tool Calling 让 AI 能够：

1. **理解自己能力的边界**——知道什么时候需要调用外部工具
2. **调用真实的 API**——查天气、翻译、搜索等
3. **整合多个工具**——完成复杂任务

### 四种实现方式

| 方式 | 控制器 | 说明 | 场景 |
|------|--------|------|------|
| Methods as Tools | TimeController | 直接把 Java 方法暴露给 AI | 简单的本地计算 |
| MethodToolCallback | AddressController | 使用回调方式调用方法 | 需要处理复杂逻辑 |
| Function as Tools | BaiduTranslateController | 按函数名调用 | 需要外部服务 |
| FunctionCallBack | WeatherController | 完整的函数回调 | 需要参数验证 |

### 实际案例：天气查询

**传统方式**：你问 AI "北京今天天气怎么样"，AI 只能瞎猜或者"我不知道"。

**Tool Calling 方式**：
```java
// AI 识别到需要查天气 → 自动调用天气 API → 返回真实数据
@GetMapping("/weather/chat-tool-function-name")
public String chatWithWeather(String message) {
    // AI 会自动调用 WeatherService.getCurrentWeather()
    return chatClient.prompt()
        .user(message)
        .tools("getCurrentWeather")  // 声明可用的工具
        .call()
        .content();
}
```

### 核心配置

```yaml
spring:
  ai:
    alibaba:
      toolcalling:
        weather:
          enabled: true
          api-key: ${WEATHER_API_KEY}
    dashscope:
      api-key: ${AI_DASHSCOPE_API_KEY}
```

### 学完这个能做什么

- 天气查询机器人
- 翻译工具
- 地图/位置服务
- 任何需要调用外部 API 的场景

---

## 第三阶段：MCP（Model Context Protocol）

**教学目标**：理解并使用 MCP 协议，实现标准化的 AI 工具调用。

**对应模块**：`spring-ai-alibaba-mcp-example`

### 你会学到什么

MCP 是一种新的协议标准，让 AI 能够以统一的方式调用各种工具。类似于 USB 接口——不管什么牌子的设备，插上就能用。

**MCP 的优势**：
- **标准化**：不同工具用同一套调用方式
- **可扩展**：轻松添加新工具
- **可复用**：一次开发，多处使用

### 快速启动

```bash
# 启动 MCP 服务器（本地或远程）
# 配置环境变量
export AI_DASHSCOPE_API_KEY=your_key

# 启动
mvn -pl spring-ai-alibaba-mcp-example spring-boot:run
```

### 和 Tool Calling 的区别

| 特性 | Tool Calling | MCP |
|------|-------------|-----|
| 标准化程度 | 依赖具体实现 | 统一协议 |
| 扩展性 | 需要代码修改 | 配置文件即可 |
| 适用场景 | 单个项目 | 跨项目复用 |

### 学完这个能做什么

- 构建企业级 AI 工具平台
- 快速集成各种 AI 能力
- 构建自己的 AI 应用生态

---

## 第四阶段：RAG（检索增强生成）

**教学目标**：掌握 RAG 系统的构建，让 AI 能够基于私有知识库回答问题。

**对应模块**：`spring-ai-alibaba-rag-example`

### 你会学到什么

RAG 是目前最实用的 AI 应用架构之一。它的核心思想是：不让 AI 凭空编造，而是先从知识库检索相关信息，再让 AI 基于这些信息生成答案。

### 解决什么问题

**没有 RAG 时**：
- AI 不知道你的公司有什么产品
- AI 不知道你个人的资料或文档
- AI 回答可能瞎编（幻觉问题）

**有 RAG 时**：
```java
// 用户问：你们公司最新的优惠政策是什么？
// 1. 先从知识库检索相关内容
// 2. 把检索到的内容发给 AI
// 3. AI 基于真实资料回答
```

### RAG 工作流程

```
┌──────────┐    ┌──────────────┐    ┌─────────┐    ┌────────┐
│  用户问题 │ → │  向量检索     │ → │  增强   │ → │  生成  │
└──────────┘    └──────────────┘    └─────────┘    └────────┘
                   ↓                                    ↓
              ┌─────────┐                         ┌─────────┐
              │ 知识库   │                         │  大模型  │
              └─────────┘                         └─────────┘
```

### 快速启动

```bash
# 启动（可选：配置向量数据库）
mvn -pl spring-ai-alibaba-rag-example spring-boot:run
```

### 核心配置

```yaml
spring:
  ai:
    dashscope:
      api-key: ${AI_DASHSCOPE_API_KEY}
    # 向量数据库配置（可选）
    vectorstore:
      chroma:
        enabled: true
```

### 学完这个能做什么

- 企业知识库问答系统
- 产品手册/文档智能助手
- 基于私有数据的 AI 查询

---

## 第五阶段：综合实战

### 对应模块

根据官方 Quickstart Matrix，还包括：

| 模块 | 用途 | 启动命令 |
|------|------|---------|
| dashscope-chat | DashScope 聊天基础 | `mvn -pl spring-ai-alibaba-chat-example/dashscope-chat spring-boot:run` |
| dashscope-image | DashScope 图片生成 | `mvn -pl spring-ai-alibaba-image-example/dashscope-image spring-boot:run` |
| deepseek-chat | DeepSeek 模型示例 | 需要 DeepSeek API Key |
| minimax-chat | MiniMax 模型示例 | 需要 MiniMax API Key |
| zhipuai-chat | 智谱模型示例 | 需要智谱 API Key |
| openai-chat | OpenAI 兼容接口 | 需要 OpenAI API Key |

### 实战项目建议

1. **智能客服系统**
   - 第一阶段：基础对话
   - 第二阶段：工具调用（查订单、查物流）
   - 第四阶段：RAG（基于产品知识库）

2. **个人知识助手**
   - 第一阶段：基础对话
   - 第四阶段：RAG（基于你的笔记/文档）

3. **多模型对比工具**
   - 同时对接多个模型
   - 对比不同模型的回答效果

---

## 环境变量速查

| 变量名 | 适用模块 | 说明 |
|--------|---------|------|
| `AI_DASHSCOPE_API_KEY` | 大部分模块 | 阿里云 DashScope API Key |
| `OPENAI_API_KEY` | openai-chat、openai-image | OpenAI API Key |
| `AI_DEEPSEEK_API_KEY` | deepseek-chat | DeepSeek API Key |
| `MINIMAX_API_KEY` | minimax-chat | MiniMax API Key |
| `ZHIPUAI_API_KEY` | zhipuai-chat | 智谱 API Key |
| `BAIDU_MAP_API_KEY` | tool-calling-example | 百度地图 API Key |

---

## 常见问题

### 1. API Key 从哪来

- **DashScope**：阿里云控制台 →  DashScope API-KEY
- **OpenAI**：OpenAI Platform
- **DeepSeek**：DeepSeek Platform
- **智谱**：智谱 AI 开放平台

### 2. 端口被占用

检查 `application.yml` 中的 `server.port`，释放端口或修改配置。

### 3. 向量数据库连接失败

RAG 示例支持可选的向量数据库。暂时没有数据库也能运行，但检索功能不可用。

---

## 学习资源

- **官方文档**：https://java2ai.com/
- **GitHub 仓库**：https://github.com/spring-ai-alibaba/examples
- **Spring AI 文档**：https://docs.spring.io/spring-ai/reference/

---

## 总结

Spring AI Alibaba 提供了一条清晰的学习路径，从 Hello World 到 RAG 实战，每一步都有完整的示例代码。只要跟着这条路走，你就能掌握现代 AI 应用开发的核心技能。

记住：不要急于求成，每一阶段都要亲手实践、跑通代码、理解原理。这样才能真正把知识变成自己的能力。