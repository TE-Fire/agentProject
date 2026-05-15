# Spring AI 架构与类继承体系详解

## 一、整体架构概览

### 1.1 Spring AI 定位与核心价值

**Spring AI** 是 Spring 官方推出的 AI 应用开发框架，旨在简化 Java 开发者与 AI 模型的交互。其核心价值在于：

- **统一抽象层**：屏蔽不同 AI 模型的 API 差异
- **声明式编程**：通过配置而非代码实现 AI 集成
- **生态整合**：无缝对接 Spring Boot、Spring Cloud 等生态

**Spring AI Alibaba** 是阿里巴巴基于 Spring AI 的扩展实现，提供对阿里云 DashScope（通义千问）等国内 AI 服务的支持。

### 1.2 架构层次图

```
┌─────────────────────────────────────────────────────────────┐
│                    用户应用层                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ ChatClient  │  │  ReactAgent │  │  RAG Chain  │        │
│  │   (高级API) │  │  (智能体)    │  │  (检索增强) │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
└─────────┼────────────────┼────────────────┼─────────────────┘
          │                │                │
┌─────────▼────────────────▼────────────────▼─────────────────┐
│                    核心抽象层                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              ChatModel (核心接口)                    │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │  call(Prompt) → ChatResponse               │    │    │
│  │  │  stream(Prompt) → Flux<ChatResponse>       │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────┘    │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                    模型实现层                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │OpenAIChat│  │DashScope │  │  Ollama  │  │  Bedrock │   │
│  │  Model   │  │ChatModel │  │ChatModel │  │ChatModel │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 二、核心接口体系

### 2.1 ChatModel 接口（核心）

`ChatModel` 是 Spring AI 中最核心的接口，定义了与 AI 模型交互的标准方式：

```java
public interface ChatModel {
    
    // 同步调用：一次性返回完整结果
    ChatResponse call(Prompt prompt);
    
    // 异步调用：流式返回（响应式编程）
    default Flux<ChatResponse> stream(Prompt prompt) {
        return Flux.just(call(prompt));
    }
    
    // 批量调用：一次处理多个 Prompt
    default List<ChatResponse> call(List<Prompt> prompts) {
        return prompts.stream().map(this::call).toList();
    }
}
```

**设计要点**：
- `stream()` 默认委托给 `call()`，子类可选择性重写以实现真正的流式输出
- 提供批量调用能力，适合批量处理场景

### 2.2 Prompt 接口

`Prompt` 代表发送给 AI 的完整提示：

```java
public interface Prompt {
    List<Message> getMessages();
    Map<String, Object> getMetadata();
    
    static Prompt create(Message... messages) {
        return new DefaultPrompt(List.of(messages));
    }
}
```

### 2.3 Message 接口体系

| 消息类型 | 说明 | 用途 |
|---------|------|------|
| `SystemMessage` | 系统提示词 | 设定 AI 角色和行为规则 |
| `UserMessage` | 用户消息 | 用户的实际问题 |
| `AssistantMessage` | AI 回复 | 对话历史记录 |
| `ToolResponseMessage` | 工具调用结果 | 工具执行后的返回数据 |

---

## 三、类继承体系

### 3.1 ChatModel 实现继承链

```
ChatModel (接口)
    │
    ├── AbstractChatModel (抽象类，提供通用实现)
    │       │
    │       ├── OpenAiChatModel (OpenAI 实现)
    │       │
    │       ├── DashScopeChatModel (阿里云 DashScope 实现)
    │       │
    │       ├── OllamaChatModel (本地 Ollama 实现)
    │       │
    │       └── BedrockChatModel (AWS Bedrock 实现)
    │
    └── StreamingChatModel (流式专用接口)
            │
            └── AbstractStreamingChatModel (流式抽象实现)
```

### 3.2 AbstractChatModel 核心实现

```java
public abstract class AbstractChatModel implements ChatModel {
    
    // 模型配置选项
    protected ChatOptions defaultOptions;
    
    // 响应解析器
    protected ChatResponseParser responseParser;
    
    @Override
    public ChatResponse call(Prompt prompt) {
        // 1. 预处理 Prompt
        Prompt processedPrompt = preProcess(prompt);
        
        // 2. 调用底层 API
        ChatResponse response = generateResponse(processedPrompt);
        
        // 3. 后处理响应
        return postProcess(response);
    }
    
    // 子类必须实现的核心方法
    protected abstract ChatResponse generateResponse(Prompt prompt);
    
    // 模板方法：可被子类重写
    protected Prompt preProcess(Prompt prompt) { return prompt; }
    protected ChatResponse postProcess(ChatResponse response) { return response; }
}
```

### 3.3 DashScopeChatModel 实现分析

```java
public class DashScopeChatModel extends AbstractChatModel {
    
    private final DashScopeApi dashScopeApi;
    
    public DashScopeChatModel(DashScopeApi dashScopeApi) {
        this.dashScopeApi = dashScopeApi;
    }
    
    @Override
    protected ChatResponse generateResponse(Prompt prompt) {
        // 1. 将 Spring AI Prompt 转换为 DashScope 请求格式
        GenerationParam param = convertToDashScopeParam(prompt);
        
        // 2. 调用 DashScope API
        GenerationResult result = dashScopeApi.call(param);
        
        // 3. 将 DashScope 响应转换为 Spring AI 格式
        return convertToChatResponse(result);
    }
    
    @Override
    public Flux<ChatResponse> stream(Prompt prompt) {
        // 真正的流式实现
        return dashScopeApi.stream(param)
            .map(this::convertToChatResponse);
    }
}
```

### 3.4 ChatClient 高级封装

`ChatClient` 是对 `ChatModel` 的高级封装，提供更简洁的 API：

```java
public interface ChatClient {
    
    // 链式 API 入口
    PromptBuilder prompt();
    
    // 直接调用
    String generate(String message);
    
    // 流式调用
    Flux<String> stream(String message);
    
    // 构建器模式
    static Builder builder(ChatModel chatModel) {
        return new DefaultBuilder(chatModel);
    }
    
    interface PromptBuilder {
        PromptBuilder system(String systemMessage);
        PromptBuilder user(String userMessage);
        PromptBuilder options(ChatOptions options);
        ChatResponse call();
        Flux<String> stream();
        String content();
    }
}
```

---

## 四、智能体（Agent）架构

### 4.1 Agent 核心接口

```java
public interface Agent {
    
    // 核心调用方法
    Response call(Request request);
    
    // 带上下文的调用
    Response call(Request request, Context context);
    
    // 流式调用
    default Flux<Response> stream(Request request) {
        return Flux.just(call(request));
    }
}
```

### 4.2 ReactAgent 继承体系

```
Agent (接口)
    │
    └── AbstractAgent (抽象类)
            │
            └── ReactAgent (ReAct 范式实现)
                    │
                    ├── Builder (构建器)
                    ├── Memory (记忆系统)
                    ├── ToolRegistry (工具注册)
                    └── PromptTemplate (提示词模板)
```

### 4.3 ReactAgent 核心组件

| 组件 | 职责 | 实现类 |
|------|------|--------|
| **Memory** | 存储对话历史 | `ConversationMemory` |
| **ToolRegistry** | 管理可用工具 | `DefaultToolRegistry` |
| **Planner** | 规划执行步骤 | `ReActPlanner` |
| **Executor** | 执行工具调用 | `ToolExecutor` |
| **OutputParser** | 解析输出格式 | `StructuredOutputParser` |

### 4.4 ReactAgent 执行流程

```
用户输入
    │
    ▼
┌─────────────────────────────────┐
│  1. 构建 Prompt               │
│     (System + History + User)  │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  2. 调用大模型                 │
│     (决定思考或调用工具)       │
└─────────────────────────────────┘
    │
    ├── 思考 → 更新记忆 → 继续
    │
    └── 工具调用 → 执行工具 → 获取结果 → 更新记忆 → 继续
                    │
                    ▼
┌─────────────────────────────────┐
│  3. 生成最终回复               │
│     (总结思考过程)             │
└─────────────────────────────────┘
    │
    ▼
 用户输出
```

---

## 五、RAG（检索增强生成）架构

### 5.1 RAG 核心组件

```java
public interface VectorStore {
    void add(List<Document> documents);
    void delete(List<String> ids);
    List<Document> similaritySearch(String query, int topK);
    List<Document> similaritySearch(SearchRequest request);
}
```

### 5.2 RAG 执行流程

```
用户问题
    │
    ▼
┌─────────────────────────────────┐
│  1. 查询向量化                 │
│     (将问题转换为向量)         │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  2. 向量检索                   │
│     (从知识库查找相关文档)     │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  3. 构建增强 Prompt            │
│     (文档 + 问题)              │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│  4. 调用大模型                 │
│     (基于文档生成回答)         │
└─────────────────────────────────┘
    │
    ▼
 最终回答
```

### 5.3 RAG 常用实现

| 组件 | Spring AI 实现 | 说明 |
|------|--------------|------|
| **向量数据库** | `ChromaVectorStore`, `PineconeVectorStore`, `MilvusVectorStore` | 多种向量库支持 |
| **嵌入模型** | `OpenAiEmbeddingModel`, `DashScopeEmbeddingModel` | 将文本转为向量 |
| **文档加载** | `FileSystemDocumentReader`, `WebDocumentReader` | 支持多种格式 |
| **文本分割** | `RecursiveCharacterTextSplitter` | 长文档分割策略 |

---

## 六、Spring AI Alibaba 扩展架构

### 6.1 DashScope 集成层次

```
┌─────────────────────────────────────────────────────────────┐
│                    Spring AI 标准层                        │
│  ChatModel, Prompt, Message, ChatClient                   │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│              Spring AI Alibaba 适配层                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  DashScopeChatModel (实现 ChatModel)                │   │
│  │  DashScopeEmbeddingModel (实现 EmbeddingModel)      │   │
│  │  DashScopeChatOptions (模型配置选项)                │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                    DashScope SDK 层                       │
│  Generation, Embedding, DashScopeApi                     │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 DashScopeChatOptions 配置

```java
public class DashScopeChatOptions implements ChatOptions {
    
    // 模型名称
    private String model = "qwen-plus";
    
    // 温度参数
    private Double temperature = 0.7;
    
    // 最大输出长度
    private Integer maxTokens;
    
    // 核采样参数
    private Double topP = 0.9;
    
    // 自定义参数
    private Map<String, Object> extraOptions;
    
    // Builder 模式
    public static DashScopeChatOptionsBuilder builder() {
        return new DashScopeChatOptionsBuilder();
    }
}
```

### 6.3 Agent Framework 扩展

Spring AI Alibaba 提供了专门的 Agent 框架：

```java
public interface GraphAgent extends Agent {
    
    // 执行图推理
    Response execute(Graph graph);
    
    // 注册工具
    void registerTool(Tool tool);
    
    // 设置系统提示词
    void setSystemPrompt(String prompt);
}
```

---

## 七、自动配置机制

### 7.1 Spring Boot AutoConfiguration

Spring AI 通过自动配置简化集成：

```java
@Configuration
@ConditionalOnClass(ChatModel.class)
@EnableConfigurationProperties(SpringAiProperties.class)
public class DashScopeChatAutoConfiguration {
    
    @Bean
    @ConditionalOnMissingBean
    @ConditionalOnProperty(prefix = "spring.ai.dashscope", name = "api-key")
    public DashScopeApi dashScopeApi(SpringAiProperties properties) {
        return DashScopeApi.builder()
            .apiKey(properties.getDashscope().getApiKey())
            .build();
    }
    
    @Bean
    @ConditionalOnMissingBean
    public ChatModel chatModel(DashScopeApi dashScopeApi) {
        return DashScopeChatModel.builder()
            .dashScopeApi(dashScopeApi)
            .build();
    }
    
    @Bean
    @ConditionalOnMissingBean
    public ChatClient chatClient(ChatModel chatModel) {
        return ChatClient.builder(chatModel).build();
    }
}
```

### 7.2 配置属性

```yaml
spring:
  ai:
    dashscope:
      api-key: ${DASHSCOPE_API_KEY}
      chat:
        model: qwen-plus
        temperature: 0.7
        max-tokens: 2048
```

---

## 八、设计模式应用

### 8.1 核心设计模式

| 模式 | 应用场景 | 实现类 |
|------|---------|--------|
| **策略模式** | 不同 AI 模型切换 | `ChatModel` 接口 |
| **模板方法** | 统一调用流程 | `AbstractChatModel` |
| **构建器模式** | 复杂对象创建 | `ChatClient.Builder`, `ReactAgent.Builder` |
| **工厂模式** | 对象实例化 | `ChatModelAutoConfiguration` |
| **代理模式** | 请求预处理/后处理 | `ChatClient` 封装 |

### 8.2 架构设计原则

1. **开闭原则**：通过接口扩展，无需修改现有代码即可支持新模型
2. **单一职责**：每个组件只负责一个功能
3. **依赖倒置**：高层模块依赖抽象，不依赖具体实现
4. **里氏替换**：子类可替换父类使用

---

## 九、资料引用

### 9.1 官方文档

| 资源 | 链接 |
|------|------|
| Spring AI 官方文档 | [https://docs.spring.io/spring-ai/reference/](https://docs.spring.io/spring-ai/reference/) |
| Spring AI GitHub | [https://github.com/spring-projects/spring-ai](https://github.com/spring-projects/spring-ai) |
| Spring AI Alibaba GitHub | [https://github.com/alibaba/spring-ai-alibaba](https://github.com/alibaba/spring-ai-alibaba) |
| DashScope 官方文档 | [https://help.aliyun.com/document_detail/611472.html](https://help.aliyun.com/document_detail/611472.html) |

### 9.2 教程文章

| 资源 | 链接 |
|------|------|
| Spring AI Alibaba 新手村系列 | [https://developer.aliyun.com/article/1720012](https://developer.aliyun.com/article/1720012) |
| Spring AI 官方教程 | [https://spring.io/guides/gs/spring-ai](https://spring.io/guides/gs/spring-ai) |
| Spring AI Agent 框架教程 | [https://java2ai.com/docs/frameworks/agent-framework/tutorials/agents](https://java2ai.com/docs/frameworks/agent-framework/tutorials/agents) |

### 9.3 学习资源

| 资源 | 链接 |
|------|------|
| Project Reactor 官方文档 | [https://projectreactor.io/docs/core/release/reference/](https://projectreactor.io/docs/core/release/reference/) |
| Spring WebFlux 文档 | [https://docs.spring.io/spring-framework/reference/web/reactive.html](https://docs.spring.io/spring-framework/reference/web/reactive.html) |

---

## 十、总结

### 核心架构要点

1. **抽象层设计**：通过 `ChatModel` 接口统一不同 AI 模型的调用方式
2. **响应式编程**：使用 `Flux` 实现流式输出，提升用户体验
3. **智能体扩展**：`ReactAgent` 提供 ReAct 范式的实现，支持工具调用和记忆系统
4. **RAG 集成**：完整的检索增强生成支持，提升回答准确性
5. **自动配置**：Spring Boot 自动配置简化集成流程

### 学习路径建议

1. **基础阶段**：掌握 `ChatModel` 和 `ChatClient` 的使用
2. **进阶阶段**：学习 `ReactAgent` 智能体开发
3. **高级阶段**：深入 RAG 和自定义工具开发
4. **实战阶段**：构建完整的 AI 应用系统

通过理解这些架构设计和类继承关系，你可以更好地掌握 Spring AI 的使用，构建高效、可扩展的 AI 应用。