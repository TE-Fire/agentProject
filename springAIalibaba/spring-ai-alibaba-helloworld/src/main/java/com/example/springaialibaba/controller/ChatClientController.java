package com.example.springaialibaba.controller;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import reactor.core.publisher.Flux;

@RestController
@RequestMapping("/chat")
public class ChatClientController {
    
    @Autowired
    private ChatClient chatClient;

    @GetMapping("/simpleClient")
    public String doChat(@RequestParam(name = "msg", defaultValue = "今天新郑市的天气如何,给出游玩建议") String msg) {
        return chatClient.prompt()
            .system("你是一位准备周全的导游")
            .user(msg)
            .call()
            .content();
    }

    @GetMapping("/streamClient")
    public Flux<String> stream(@RequestParam(name = "msg", defaultValue = "今天新郑市的天气如何") String msg) {
        return chatClient.prompt()
            .user(msg)
            .stream()
            .content();
    }

    

}
