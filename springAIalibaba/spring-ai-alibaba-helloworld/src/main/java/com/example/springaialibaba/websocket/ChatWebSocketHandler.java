package com.example.springaialibaba.websocket;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.messages.AssistantMessage;
import org.springframework.ai.chat.messages.SystemMessage;
import org.springframework.ai.chat.messages.UserMessage;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import java.util.List;

@Component
public class ChatWebSocketHandler extends TextWebSocketHandler {

    private final ChatClient chatClient;
    private final ChatModel chatModel;

    public ChatWebSocketHandler(ChatClient chatClient, ChatModel chatModel) {
        this.chatClient = chatClient;
        this.chatModel = chatModel;
    }

    @Override
    protected void handleTextMessage(WebSocketSession session, TextMessage message) {
        String userMessage = message.getPayload();

        try {
            SystemMessage systemMessage = new SystemMessage("你是一位专业助手，回答简洁明了");
            UserMessage userMsg = new UserMessage(userMessage);
            Prompt prompt = new Prompt(List.of(systemMessage, userMsg));

            chatModel.stream(prompt)
                .doOnNext(response -> {
                    AssistantMessage output = response.getResults().get(0).getOutput();
                    String content = output.getText();
                    if (content != null && !content.isEmpty()) {
                        try {
                            synchronized (session) {
                                if (session.isOpen()) {
                                    session.sendMessage(new TextMessage(content));
                                }
                            }
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    }
                })
                .doOnError(error -> {
                    try {
                        session.sendMessage(new TextMessage("Error: " + error.getMessage()));
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                })
                .doOnComplete(() -> {
                    try {
                        synchronized (session) {
                            if (session.isOpen()) {
                                session.sendMessage(new TextMessage("[DONE]"));
                            }
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                })
                .subscribe();
        } catch (Exception e) {
            try {
                session.sendMessage(new TextMessage("Error: " + e.getMessage()));
            } catch (Exception ex) {
                ex.printStackTrace();
            }
        }
    }

    @Override
    public void afterConnectionEstablished(WebSocketSession session) {
        try {
            session.sendMessage(new TextMessage("Connected successfully! You can start chatting."));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) {
        System.out.println("WebSocket connection closed: " + status);
    }
}
