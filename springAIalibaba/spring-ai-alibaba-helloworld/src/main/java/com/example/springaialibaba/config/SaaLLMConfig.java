package com.example.springaialibaba.config;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * 基于自动注入的ChatModel构建ChatCline
 */
@Configuration
public class SaaLLMConfig {
    
    @Bean("dashScopeChatClinet")
    public ChatClient dashScopeChatClient(ChatModel dashScopeChatModel) {
        return ChatClient.builder(dashScopeChatModel).build();
    }
}
