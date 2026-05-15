package com.example.springaialibaba.controller;

import org.springframework.ai.chat.model.ChatModel;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import reactor.core.publisher.Flux;

@RestController
@RequestMapping("/hello")
public class ChatHelloController {
    
    @Autowired
    private ChatModel chatModel;

    /**
     * 普通调用方式：发送消息，获取完成回复
     * @param msg
     * @return
     */
    @GetMapping(value = "/dochat")
    public String doChat(@RequestParam(name = "msg", defaultValue = "你是谁?") String msg) {
        String response = chatModel.call(msg);
        return response;
    }

    @GetMapping(value = "/streamChat")
    public Flux<String> stram(@RequestParam(name = "msg", defaultValue = "你是谁?") String msg) {
        return chatModel.stream(msg); // stream返回一个响应式流Flux
    }
}
