package com.example.springaialibaba.helloworld.controller;

import com.alibaba.cloud.ai.dashscope.chat.DashScopeChatOptions;

import jakarta.servlet.http.HttpServletResponse;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;


/**
 * 聊天控制器
 * 提供简单聊天、流式响应、多轮对话记忆功能
 */
@RestController
@RequestMapping("/helloworld")
public class ChatController {

    private static final String DEFAULT_PROMPT = "你是一个博学的智能聊天助手，请根据用户提问回答！";

    private final ChatClient dashScopeChatClient;

    private ChatController(ChatClient.Builder chatClientBuilder) {
        this.dashScopeChatClient = chatClientBuilder
                .defaultSystem(DEFAULT_PROMPT)
                .defaultOptions(
                    DashScopeChatOptions.builder()
                            .withTopP(0.7)
                            .build()
                )
                .build();
    } 

    /**
     * 简单调用
     * @param query
     * @return
     */
    @GetMapping("/simple/chat")
    public String simpleChat(@RequestParam(value = "query", defaultValue = "你好，能简单介绍一下自己吗?") String query) {
        return dashScopeChatClient.prompt(query).call().content();
    }

    /**
     * 流式调用
     * @param query
     * @param response
     * @return
     */
    public Flux<String> streanChat(@RequestParam(value = "query", defaultValue = "你好，能简单介绍一下自己吗?") String query,
            HttpServletResponse response) {
        response.setCharacterEncoding("UTF-8");
        return dashScopeChatClient.prompt(query).stream().content();
    }

    @GetMapping("/options/chat")
     public Flux<String> optionsChat(
            HttpServletResponse response,
            @RequestParam(value = "query", defaultValue = "你好，很高兴认识你，能简单介绍一下自己吗？") String query,
            @RequestParam(value = "topP", required = false) Double topP,
            @RequestParam(value = "temperature", required = false) Double temperature) {

        response.setCharacterEncoding("UTF-8");
        DashScopeChatOptions.DashScopeChatOptionsBuilder optionsBuilder = DashScopeChatOptions.builder();
        if (topP != null) {
            optionsBuilder.withTopP(topP);
        }
        if (temperature != null) {
            optionsBuilder.withTemperature(temperature);
        }

        return this.dashScopeChatClient.prompt(query)
                        .options(optionsBuilder.build())
                        .stream()
                        .content();
    }

}