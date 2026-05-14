package com.example.springaialibaba;

import com.alibaba.cloud.ai.dashscope.api.DashScopeApi;
import com.alibaba.cloud.ai.dashscope.chat.DashScopeChatModel;
import com.alibaba.cloud.ai.graph.agent.ReactAgent;
import com.alibaba.cloud.ai.graph.exception.GraphRunnerException;

import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.chat.messages.AssistantMessage;

public class AgentsExample {
    
    public static void main(String[] args) throws GraphRunnerException {
        // 步骤1：创建 DashScope API 实例
        DashScopeApi dashScopeApi = DashScopeApi.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
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