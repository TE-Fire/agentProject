# ReactAgent 学习笔记

---

## 一、什么是 ReactAgent

### 1.1 核心概念

ReactAgent 是 Spring AI Alibaba 框架提供的核心智能体组件，基于 **ReAct（Reasoning + Acting）范式** 设计。

> **ReAct 范式**：让智能体在执行任务时，进行"思考→行动→观察"的循环迭代，直到完成任务。

**核心思想**：
- **思考（Reasoning）**：分析问题，决定下一步该做什么
- **行动（Acting）**：执行具体操作，可能是调用工具或直接回答
- **观察（Observation）**：获取行动结果，作为下一次思考的输入

### 1.2 为什么需要 ReactAgent

在传统的 AI 应用中，我们通常直接调用模型获取答案。但在复杂场景下，这种方式存在以下问题：

| 问题 | 传统方式 | ReactAgent 方式 |
|------|---------|----------------|
| **信息时效性** | 依赖模型训练数据 | 可调用实时工具获取最新信息 |
| **任务复杂性** | 单次调用难以完成复杂任务 | 可分解任务，分步执行 |
| **逻辑推理** | 单次推理 | 多步推理，逐步逼近答案 |
| **工具使用** | 需要手动集成 | 自动选择和调用工具 |

### 1.3 ReactAgent 的核心组件

一个完整的 ReactAgent 包含以下核心组件：

```
┌─────────────────────────────────────────────────────────────┐
│                      ReactAgent                            │
├──────────────┬──────────────┬──────────────┬──────────────┤
│   Model      │   Tools      │   Memory     │   Prompt     │
│  (大语言模型) │  (工具集)    │  (记忆系统)  │  (提示词)    │
└──────────────┴──────────────┴──────────────┴──────────────┘
         │              │              │              │
         ▼              ▼              ▼              ▼
    生成回答        调用工具        存储状态        指导行为
```

---

## 二、环境准备与依赖配置

### 2.1 前置条件

在开始使用 ReactAgent 之前，您需要：

1. **Java 环境**：JDK 21 或更高版本
2. **Maven 环境**：Maven 3.8+
3. **DashScope API Key**：在阿里云控制台获取

### 2.2 Maven 依赖配置

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    
    <modelVersion>4.0.0</modelVersion>
    
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.5</version>
        <relativePath/>
    </parent>
    
    <groupId>com.example</groupId>
    <artifactId>reactagent-demo</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <packaging>jar</packaging>
    
    <properties>
        <java.version>21</java.version>
        <spring-ai-alibaba.version>1.1.2.2</spring-ai-alibaba.version>
        <spring-ai.version>1.0.0-SNAPSHOT</spring-ai.version>
    </properties>
    
    <dependencies>
        <!-- Spring Boot Starter Web -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        
        <!-- Spring Boot Starter WebFlux (用于流式响应) -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-webflux</artifactId>
        </dependency>
        
        <!-- Spring AI Core -->
        <dependency>
            <groupId>org.springframework.ai</groupId>
            <artifactId>spring-ai-core</artifactId>
            <version>${spring-ai.version}</version>
        </dependency>
        
        <!-- Spring AI Alibaba DashScope Starter -->
        <dependency>
            <groupId>com.alibaba.cloud.ai</groupId>
            <artifactId>spring-ai-alibaba-starter-dashscope</artifactId>
            <version>${spring-ai-alibaba.version}</version>
        </dependency>
        
        <!-- Spring AI Alibaba Agent Framework -->
        <dependency>
            <groupId>com.alibaba.cloud.ai</groupId>
            <artifactId>spring-ai-alibaba-agent-framework</artifactId>
            <version>${spring-ai-alibaba.version}</version>
        </dependency>
        
        <!-- Lombok (可选，简化代码) -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
    </dependencies>
    
    <repositories>
        <!-- Spring Snapshots 仓库 -->
        <repository>
            <id>spring-snapshots</id>
            <name>Spring Snapshots</name>
            <url>https://repo.spring.io/snapshot</url>
            <releases>
                <enabled>false</enabled>
            </releases>
            <snapshots>
                <enabled>true</enabled>
            </snapshots>
        </repository>
        
        <!-- Spring Milestones 仓库 -->
        <repository>
            <id>spring-milestones</id>
            <name>Spring Milestones</name>
            <url>https://repo.spring.io/milestone</url>
        </repository>
        
        <!-- 阿里云 Maven 仓库 -->
        <repository>
            <id>aliyunmaven</id>
            <name>Aliyun Maven</name>
            <url>https://maven.aliyun.com/repository/public</url>
        </repository>
    </repositories>
    
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```

### 2.3 API Key 配置

在使用 ReactAgent 之前，需要配置 DashScope API Key：

**方式一：环境变量**（推荐）

```bash
# Linux/Mac
export AI_DASHSCOPE_API_KEY=your_api_key_here

# Windows PowerShell
$env:AI_DASHSCOPE_API_KEY="your_api_key_here"
```

**方式二：配置文件**

在 `application.yml` 中配置：

```yaml
spring:
  ai:
    dashscope:
      api-key: ${AI_DASHSCOPE_API_KEY}
```

---

## 三、基础使用：创建第一个 ReactAgent

### 3.1 最简单的例子

```java
import com.alibaba.cloud.ai.dashscope.api.DashScopeApi;
import com.alibaba.cloud.ai.dashscope.chat.DashScopeChatModel;
import com.alibaba.cloud.ai.graph.agent.ReactAgent;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.chat.messages.AssistantMessage;

public class FirstAgentExample {
    
    public static void main(String[] args) {
        // 步骤1：创建 DashScope API 实例
        DashScopeApi dashScopeApi = DashScopeApi.builder()
                .apiKey(System.getenv("AI_DASHSCOPE_API_KEY"))
                .build();
        
        // 步骤2：创建 ChatModel
        ChatModel chatModel = DashScopeChatModel.builder()
                .dashScopeApi(dashScopeApi)
                .build();
        
        // 步骤3：创建 ReactAgent
        ReactAgent agent = ReactAgent.builder()
                .name("my_first_agent")
                .model(chatModel)
                .systemPrompt("你是一个乐于助人的AI助手。")
                .build();
        
        // 步骤4：调用 Agent
        AssistantMessage response = agent.call("你好，请问你是谁？");
        
        // 步骤5：输出结果
        System.out.println("Agent 回复：");
        System.out.println(response.getText());
    }
}
```

### 3.2 运行结果

```
Agent 回复：
你好！我是一个基于 ReactAgent 构建的 AI 助手。我可以帮助你解答问题、提供信息和完成各种任务。有什么我可以帮助你的吗？
```

### 3.3 代码解释

让我们逐行解析这段代码：

```java
// 1. 创建 DashScope API 实例
DashScopeApi dashScopeApi = DashScopeApi.builder()
        .apiKey(System.getenv("AI_DASHSCOPE_API_KEY"))
        .build();
```

这一步创建了与阿里云 DashScope 服务的连接，需要提供 API Key。

```java
// 2. 创建 ChatModel
ChatModel chatModel = DashScopeChatModel.builder()
        .dashScopeApi(dashScopeApi)
        .build();
```

`ChatModel` 是 Spring AI 提供的统一接口，封装了与大语言模型的交互细节。

```java
// 3. 创建 ReactAgent
ReactAgent agent = ReactAgent.builder()
        .name("my_first_agent")
        .model(chatModel)
        .systemPrompt("你是一个乐于助人的AI助手。")
        .build();
```

这里创建了 ReactAgent 实例：
- `name`：Agent 的名称，用于标识和日志记录
- `model`：指定使用的大语言模型
- `systemPrompt`：系统提示词，定义 Agent 的角色和行为准则

```java
// 4. 调用 Agent
AssistantMessage response = agent.call("你好，请问你是谁？");
```

`call()` 方法是最常用的调用方式，接收字符串输入并返回 `AssistantMessage`。

---

## 四、深入理解 ReactAgent 的工作机制

### 4.1 ReactAgent 的执行流程

ReactAgent 的核心是一个循环执行过程：

```
┌──────────────────────────────────────────────────────────────────┐
│                     ReactAgent 执行流程                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                │
│   用户输入                                                      │
│      │                                                         │
│      ▼                                                         │
│   ┌──────────────┐                                             │
│   │  思考阶段    │ ←── 分析问题，决定下一步行动                  │
│   └──────┬───────┘                                             │
│          │                                                     │
│          ▼                                                     │
│   ┌──────────────┐                                             │
│   │  判断是否需要 │                                             │
│   │  调用工具？  │                                             │
│   └──────┬───────┘                                             │
│          │                                                     │
│     ┌────┴────┐                                                │
│     │         │                                                │
│     ▼         ▼                                                │
│   是         否                                                │
│     │         │                                                │
│     ▼         ▼                                                │
│   ┌──────────────┐    ┌──────────────┐                         │
│   │  调用工具    │    │  直接回答    │                         │
│   │  获取结果    │    │  返回答案    │                         │
│   └──────┬───────┘    └──────────────┘                         │
│          │                                                     │
│          ▼                                                     │
│   ┌──────────────┐                                             │
│   │  观察结果    │ ←── 获取工具返回的信息                        │
│   └──────┬───────┘                                             │
│          │                                                     │
│          ▼                                                     │
│   ┌──────────────┐                                             │
│   │  判断任务    │                                             │
│   │  是否完成？  │                                             │
│   └──────┬───────┘                                             │
│          │                                                     │
│     ┌────┴────┐                                                │
│     │         │                                                │
│     ▼         ▼                                                │
│   否         是                                                │
│     │         │                                                │
│     └────┬────┘                                                │
│          ▼                                                     │
│   返回最终答案                                                  │
│                                                                │
└──────────────────────────────────────────────────────────────────┘
```

### 4.2 核心方法说明

ReactAgent 提供了三种主要的调用方法：

| 方法 | 功能 | 返回值 | 使用场景 |
|------|------|--------|----------|
| `call()` | 简单调用 | `AssistantMessage` | 简单对话场景 |
| `invoke()` | 完整状态调用 | `Optional<OverAllState>` | 需要访问完整状态 |
| `stream()` | 流式调用 | `Flux<NodeOutput>` | 需要实时响应 |

### 4.3 调用示例对比

#### 4.3.1 call() - 简单调用

```java
// 字符串输入
AssistantMessage response = agent.call("杭州今天天气怎么样？");
System.out.println(response.getText());

// UserMessage 输入
UserMessage userMessage = new UserMessage("帮我推荐一本好书");
AssistantMessage response2 = agent.call(userMessage);

// 多轮对话（包含历史消息）
List<Message> messages = List.of(
        new UserMessage("我想学 Java"),
        new AssistantMessage("好的，Java 是一门非常流行的编程语言..."),
        new UserMessage("那我应该从哪里开始学起？")
);
AssistantMessage response3 = agent.call(messages);
```

#### 4.3.2 invoke() - 完整状态调用

```java
// 使用 Map 输入
Map<String, Object> inputs = Map.of(
        "input", "帮我写一首诗",
        "topic", "春天"
);

Optional<OverAllState> result = agent.invoke(inputs);

if (result.isPresent()) {
    OverAllState state = result.get();
    
    // 获取消息历史
    Optional<Object> messages = state.value("messages");
    if (messages.isPresent()) {
        List<Message> messageList = (List<Message>) messages.get();
        Message lastMessage = messageList.get(messageList.size() - 1);
        
        if (lastMessage instanceof AssistantMessage) {
            System.out.println("Agent 回复：" + ((AssistantMessage) lastMessage).getText());
        }
    }
    
    // 获取自定义状态
    Optional<Object> customData = state.value("custom_key");
    if (customData.isPresent()) {
        System.out.println("自定义数据：" + customData.get());
    }
}
```

#### 4.3.3 stream() - 流式调用

```java
// 基础流式调用
Flux<NodeOutput> stream = agent.stream("帮我写一篇关于人工智能的短文");

stream.subscribe(
        // 处理每个节点输出
        output -> {
            System.out.println("===== 节点 " + output.node() + " =====");
            
            // 检查是否有 token 使用信息
            if (output.tokenUsage() != null) {
                System.out.println("Token 使用: " + output.tokenUsage());
            }
            
            // 获取状态中的消息
            Optional<Object> messages = output.state().value("messages");
            if (messages.isPresent()) {
                List<Message> messageList = (List<Message>) messages.get();
                if (!messageList.isEmpty()) {
                    Message lastMsg = messageList.get(messageList.size() - 1);
                    if (lastMsg instanceof AssistantMessage) {
                        System.out.println("当前内容: " + ((AssistantMessage) lastMsg).getText());
                    }
                }
            }
        },
        // 处理错误
        error -> System.err.println("发生错误: " + error.getMessage()),
        // 处理完成
        () -> System.out.println("\n流式输出完成！")
);
```

---

## 五、模型配置详解

### 5.1 基础配置

```java
DashScopeApi dashScopeApi = DashScopeApi.builder()
        .apiKey(System.getenv("AI_DASHSCOPE_API_KEY"))
        .build();

ChatModel chatModel = DashScopeChatModel.builder()
        .dashScopeApi(dashScopeApi)
        .build();
```

### 5.2 高级配置

```java
ChatModel chatModel = DashScopeChatModel.builder()
        .dashScopeApi(dashScopeApi)
        .defaultOptions(DashScopeChatOptions.builder()
                .model("qwen-plus")           // 指定模型
                .temperature(0.7)             // 控制随机性（0-1）
                .maxToken(2000)              // 最大输出长度
                .topP(0.9)                   // 核采样参数
                .enableThinking(true)         // 启用思考模式
                .apiTimeout(Duration.ofSeconds(60))  // API 超时时间
                .build())
        .build();
```

### 5.3 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `model` | String | qwen-plus | 模型名称 |
| `temperature` | double | 0.7 | 随机性控制，0 表示确定性，1 表示最大随机性 |
| `maxToken` | int | 2000 | 最大输出 token 数 |
| `topP` | double | 0.9 | 核采样参数，控制生成的多样性 |
| `enableThinking` | boolean | false | 是否启用思考模式 |
| `apiTimeout` | Duration | 30s | API 调用超时时间 |

---

## 六、工具调用机制

### 6.1 为什么需要工具调用

在实际应用中，AI 模型的知识是有限的，且可能不是最新的。通过工具调用，我们可以：

1. **获取实时信息**：如天气、新闻、股票价格
2. **执行计算**：如数学运算、数据分析
3. **访问外部系统**：如数据库、API
4. **执行操作**：如发送邮件、创建文件

### 6.2 创建自定义工具

```java
import org.springframework.ai.tool.ToolCallback;
import org.springframework.ai.tool.function.FunctionToolCallback;

// 定义工具类
public class WeatherTool {
    
    public String getWeather(String city) {
        // 模拟获取天气信息
        return "城市：" + city + "\n天气：晴\n温度：25°C\n湿度：60%";
    }
}

// 创建工具回调
ToolCallback weatherTool = FunctionToolCallback
        .builder("get_weather", new WeatherTool())
        .description("获取指定城市的天气信息")
        .inputType(String.class)
        .build();

// 使用工具
ReactAgent agent = ReactAgent.builder()
        .name("weather_agent")
        .model(chatModel)
        .tools(weatherTool)
        .systemPrompt("你是一个天气查询助手。当用户询问天气时，使用 get_weather 工具获取信息。")
        .build();

// 调用
AssistantMessage response = agent.call("北京今天天气怎么样？");
System.out.println(response.getText());
```

### 6.3 多工具使用

```java
// 创建多个工具
ToolCallback searchTool = FunctionToolCallback
        .builder("search", new SearchTool())
        .description("搜索网络信息")
        .inputType(String.class)
        .build();

ToolCallback calculatorTool = FunctionToolCallback
        .builder("calculate", new CalculatorTool())
        .description("进行数学计算")
        .inputType(String.class)
        .build();

// 同时使用多个工具
ReactAgent agent = ReactAgent.builder()
        .name("multi_tool_agent")
        .model(chatModel)
        .tools(searchTool, calculatorTool)
        .build();

// Agent 会根据问题自动选择合适的工具
AssistantMessage response = agent.call("2024 年世界杯冠军是谁？");
```

---

## 七、提示词工程

### 7.1 System Prompt 的重要性

System Prompt 定义了 Agent 的角色、行为准则和知识范围。一个好的 System Prompt 可以：

1. **定义身份**：告诉 AI 它是什么角色
2. **设定规则**：告诉 AI 应该怎么做
3. **提供知识**：给 AI 提供特定领域的知识

### 7.2 编写有效的 System Prompt

```java
String systemPrompt = """
        你是一个专业的软件架构师助手。
        
        你的职责是：
        1. 帮助用户设计软件架构
        2. 提供技术选型建议
        3. 解答技术问题
        4. 审查代码质量
        
        回答要求：
        - 使用中文回答
        - 保持专业但易懂的语言
        - 提供具体的示例
        - 如果不确定，明确说明
        
        禁止：
        - 编造信息
        - 使用攻击性语言
        - 回答与技术无关的问题
        """;

ReactAgent agent = ReactAgent.builder()
        .name("architecture_agent")
        .model(chatModel)
        .systemPrompt(systemPrompt)
        .build();
```

### 7.3 Instruction 的使用

Instruction 提供更详细的任务说明，与 System Prompt 互补：

```java
String instruction = """
        用户正在询问关于微服务架构的问题。
        
        请按照以下结构回答：
        1. 核心概念解释
        2. 优势与挑战
        3. 适用场景
        4. 最佳实践
        
        确保回答结构清晰，便于理解。
        """;

ReactAgent agent = ReactAgent.builder()
        .name("microservice_agent")
        .model(chatModel)
        .systemPrompt("你是一个微服务架构专家。")
        .instruction(instruction)
        .build();
```

---

## 八、记忆系统

### 8.1 为什么需要记忆

在多轮对话中，记忆系统可以：

1. **记住上下文**：让 Agent 记住之前的对话内容
2. **保持一致性**：确保回答与之前的对话一致
3. **支持复杂任务**：支持需要多步骤完成的任务

### 8.2 配置记忆

```java
import com.alibaba.cloud.ai.graph.checkpoint.savers.MemorySaver;

// 使用内存存储（适合开发和测试）
ReactAgent agent = ReactAgent.builder()
        .name("memory_agent")
        .model(chatModel)
        .saver(new MemorySaver())
        .build();

// 多轮对话示例
AssistantMessage response1 = agent.call("我叫张三");
System.out.println("回复1：" + response1.getText());

AssistantMessage response2 = agent.call("你还记得我叫什么吗？");
System.out.println("回复2：" + response2.getText());
```

### 8.3 使用线程 ID 管理会话

```java
import com.alibaba.cloud.ai.graph.RunnableConfig;

// 创建配置
String threadId = "user_session_123";
RunnableConfig config = RunnableConfig.builder()
        .threadId(threadId)
        .addMetadata("user_id", "1001")
        .addMetadata("session_start", "2024-01-01 10:00:00")
        .build();

// 使用配置调用
AssistantMessage response = agent.call("你好", config);

// 在另一个调用中使用相同的 threadId 保持会话
AssistantMessage response2 = agent.call("继续刚才的话题", config);
```

---

## 九、高级特性

### 9.1 拦截器机制

拦截器允许在模型调用或工具调用前后执行自定义逻辑：

```java
import com.alibaba.cloud.ai.graph.agent.interceptor.ModelInterceptor;
import com.alibaba.cloud.ai.graph.agent.interceptor.ModelRequest;
import com.alibaba.cloud.ai.graph.agent.interceptor.ModelResponse;
import com.alibaba.cloud.ai.graph.agent.interceptor.ModelCallHandler;

// 创建模型拦截器
ModelInterceptor loggingInterceptor = new ModelInterceptor() {
    @Override
    public ModelResponse intercept(ModelRequest request, ModelCallHandler handler) {
        // 在调用前执行
        System.out.println("准备调用模型，输入：" + request.getInput());
        long startTime = System.currentTimeMillis();
        
        // 调用模型
        ModelResponse response = handler.handle(request);
        
        // 在调用后执行
        long endTime = System.currentTimeMillis();
        System.out.println("模型调用完成，耗时：" + (endTime - startTime) + "ms");
        System.out.println("输出：" + response.getOutput());
        
        return response;
    }
};

// 使用拦截器
ReactAgent agent = ReactAgent.builder()
        .name("interceptor_agent")
        .model(chatModel)
        .interceptors(loggingInterceptor)
        .build();
```

### 9.2 钩子机制

钩子提供了更细粒度的控制，可以在 Agent 执行的不同阶段插入自定义逻辑：

```java
import com.alibaba.cloud.ai.graph.agent.hook.AgentHook;
import com.alibaba.cloud.ai.graph.agent.hook.HookPosition;
import com.alibaba.cloud.ai.graph.agent.hook.HookPositions;

// 创建钩子
AgentHook myHook = new AgentHook() {
    @Override
    public HookPosition getPosition() {
        // 在模型调用前执行
        return HookPositions.BEFORE_MODEL_CALL;
    }
    
    @Override
    public void apply(OverAllState state) {
        // 自定义逻辑，比如修改提示词
        System.out.println("在模型调用前执行自定义逻辑");
    }
};

// 使用钩子
ReactAgent agent = ReactAgent.builder()
        .name("hook_agent")
        .model(chatModel)
        .hooks(List.of(myHook))
        .build();
```

### 9.3 结构化输出

ReactAgent 支持将输出格式化为特定的结构：

```java
import org.springframework.ai.converter.BeanOutputConverter;

// 定义输出结构
public class WeatherOutput {
    private String city;
    private String weather;
    private int temperature;
    private String recommendation;
    
    // 构造函数、getter、setter
}

// 创建转换器
BeanOutputConverter<WeatherOutput> converter = 
    new BeanOutputConverter<>(WeatherOutput.class);

// 使用结构化输出
ReactAgent agent = ReactAgent.builder()
        .name("structured_agent")
        .model(chatModel)
        .outputSchema(converter.getFormat())
        .build();

// 调用
AssistantMessage response = agent.call("查询北京天气，并给出出行建议");

// 解析结果
WeatherOutput output = converter.convert(response.getText());
System.out.println("城市：" + output.getCity());
System.out.println("天气：" + output.getWeather());
System.out.println("温度：" + output.getTemperature() + "°C");
System.out.println("建议：" + output.getRecommendation());
```

---

## 十、实际应用场景

### 10.1 智能客服

```java
// 创建客服 Agent
ReactAgent customerServiceAgent = ReactAgent.builder()
        .name("customer_service_agent")
        .model(chatModel)
        .systemPrompt("你是一个友好的客服助手。请帮助用户解决问题。")
        .tools(orderTool, refundTool, faqTool)
        .saver(new MemorySaver())
        .build();

// 对话流程
customerServiceAgent.call("您好，我想查询我的订单状态");
customerServiceAgent.call("订单号是 123456");
customerServiceAgent.call("什么时候能发货？");
```

### 10.2 代码助手

```java
// 创建代码助手 Agent
ReactAgent codeAgent = ReactAgent.builder()
        .name("code_agent")
        .model(chatModel)
        .systemPrompt("你是一个专业的 Java 开发助手。")
        .instruction("请提供完整的代码示例，并解释关键部分。")
        .build();

// 使用
AssistantMessage response = codeAgent.call("请写一个 Spring Boot REST API 示例");
```

### 10.3 数据分析助手

```java
// 创建数据分析 Agent
ReactAgent dataAgent = ReactAgent.builder()
        .name("data_agent")
        .model(chatModel)
        .tools(databaseTool, chartTool, exportTool)
        .build();

// 使用
AssistantMessage response = dataAgent.call("分析上个月的销售数据，生成报表");
```

---

## 十一、常见问题与解决方案

### 11.1 依赖冲突

**问题**：`NoClassDefFoundError` 或 `ClassNotFoundException`

**解决方案**：
1. 检查 Maven 依赖版本是否兼容
2. 确保 `spring-ai-alibaba.version` 和 `spring-ai.version` 版本匹配
3. 使用 `mvn dependency:tree` 检查依赖树

### 11.2 API Key 错误

**问题**：`Invalid API Key` 或认证失败

**解决方案**：
1. 确认 API Key 正确
2. 检查环境变量是否正确设置
3. 确认 API Key 有足够的权限

### 11.3 工具调用失败

**问题**：工具调用返回错误或无响应

**解决方案**：
1. 检查工具的 `description` 是否清晰
2. 确保工具方法的参数类型正确
3. 添加适当的错误处理

### 11.4 性能问题

**问题**：响应时间过长

**解决方案**：
1. 调整 `apiTimeout` 参数
2. 考虑使用流式调用
3. 优化提示词长度

---

## 十二、总结

ReactAgent 是 Spring AI Alibaba 框架的核心组件，提供了强大的智能体能力。通过本教程，您应该掌握：

1. **基本概念**：ReAct 范式、核心组件
2. **环境配置**：Maven 依赖、API Key 设置
3. **基础使用**：创建 Agent、调用方法
4. **高级特性**：工具调用、记忆系统、拦截器、结构化输出
5. **实际应用**：智能客服、代码助手、数据分析等场景

**下一步建议**：
1. 尝试创建一个简单的智能客服应用
2. 集成自定义工具
3. 探索多智能体协作模式

---

## 参考资料

- **官方文档**：https://java2ai.com/
- **GitHub 仓库**：https://github.com/alibaba/spring-ai-alibaba
- **菜鸟教程**：https://www.runoob.com/ai-agent/
- **Spring AI 文档**：https://docs.spring.io/spring-ai/reference/

---

**创建时间**：2026-05-14  
**版本**：v2.0  
**作者**：Spring AI Alibaba 学习笔记