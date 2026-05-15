package com.example.springaialibaba.controller;

import java.util.List;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.messages.AssistantMessage;
import org.springframework.ai.chat.messages.SystemMessage;
import org.springframework.ai.chat.messages.ToolResponseMessage;
import org.springframework.ai.chat.messages.UserMessage;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import reactor.core.publisher.Flux;

@RestController
@RequestMapping("/stram")
public class StreamController {
    
    @Autowired
    private ChatClient chatClient;

    @Autowired
    private ChatModel chatModel;


    // ===============流式调用方式===================

    /**
     * 基础流式调用
     * @param msg
     * @return
     */
    @GetMapping("/basic")
    public Flux<String> basicStream(@RequestParam(defaultValue = "你好") String msg) {
        return chatClient.prompt()
            .user(msg)
            .stream()
            .content();
    }

    /**
     * SSE 流式调用（指定 Content-Type）
     * @param msg
     * @return
     */
    @GetMapping(value = "/sse", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<String> sseStream(@RequestParam(defaultValue = "你好") String msg) {
        return chatClient.prompt()
            .system("你是一位专业助手，回答简洁明了")
            .user(msg)
            .stream()
            .content();
    }

    /**
     * 方式二：使用底层 Message 对象（更底层灵活）
     * 
     * 创建 SystemMessage 和 UserMessage 对象
     * 组合成 Prompt 进行调用
     * 
     */
    @GetMapping("/basicMessage")
    public Flux<ChatResponse> basicMessage(String question) {
        SystemMessage systemMessage = new SystemMessage(
            "你是一个讲故事的助手,每个故事控制在300字以内"
        );
        UserMessage userMessage = new UserMessage(question);

        // Prompt是Message的容器，可以包含多个消息
        Prompt prompt = new Prompt(systemMessage, userMessage);
        
        return chatModel.stream(prompt);
    }

    
    /**
     * 方式三：提取响应中的文本
     * 
     * 获取 ChatResponse 对象后，需要手动提取内容
     * 
     */
    @GetMapping("/prompt/chat1")
    public Flux<String> chat1(String question) {
         SystemMessage systemMessage = new SystemMessage(
            "你是一个讲故事的助手,每个故事控制在600字以内且以HTML格式返回"
        );

        UserMessage userMessage = new UserMessage(question);
        Prompt prompt = new Prompt(userMessage, systemMessage);

        // 使用 map 转换响应，提取文本内容
        // getResults().get(0) 获取第一个结果块
        // getOutput().getText() 获取生成的文本
        return chatModel.stream(prompt)
            .map(response -> response.getResults().get(0).getOutput().getText());
    }

     /**
     * 方式四：获取 AssistantMessage 对象
     * 
     * 如果需要获取 AI 回复的完整对象（包含元数据）
     * 可以获取 AssistantMessage
     * 
     */
    @GetMapping("/prompt/chat2")
    public String chat2(String question) {
        AssistantMessage assistantMessage = chatClient.prompt()
                .user(question)
                .call()
                .chatResponse()
                .getResult()
                .getOutput();

        return assistantMessage.getText();
    }

    
    /**
     * 方式五：模拟工具调用场景（ToolResponseMessage）
     * 
     * 这个示例展示了 ToolResponseMessage 的使用场景
     * 实际使用会在 ToolCalling 章节详细讲解
     * 
     */
    @GetMapping("/prompt/chat3")
    public String chat3(String city) {
        String answer = chatClient.prompt()
            .user(city + "今天天气如何")
            .call()
            .chatResponse()
            .getResult()
            .getOutput()
            .getText();
        
        // 模拟工具返回结果（实际是外部工具调用的返回值）
        // 1. 创建 ToolResponse 对象（使用内部类）
        // 创建工具响应
        ToolResponseMessage.ToolResponse toolResponse = new ToolResponseMessage.ToolResponse(
            "call_abc123",
            "getWeather",
            "{\"city\":\"Shanghai\",\"temperature\":\"28°C\",\"humidity\":\"65%\"}"
        );

        // 使用 Builder 模式创建 ToolResponseMessage
        ToolResponseMessage message = ToolResponseMessage.builder()
            .responses(List.of(toolResponse))
            .build();

        String response = message.getText();
        String res = answer + response;

        return res;
    }
    
}