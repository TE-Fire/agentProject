import os
from openai import OpenAI


# 创建client对象，OpenAI类对象
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 2.调用模型
response = client.chat.completions.create(
        model="qwen3.6-plus",
        messages=[
            { "role": "system", "content": "你是一位专业的机器人，能帮我处理各项事务，回答要十分简洁。"},
            { "role": "user", "content": "小明有两只宠物狗。"},
            { "role": "assistant", "content": "好的"},
            { "role": "user", "content": "小红有两只宠物猫"},
            { "role": "assistant", "content": "好的"},
            { "role": "user", "content": "一共有几只宠物?"}
        ],
        stream=True
    )

# 3.处理结果
for chunk in response:
    content = chunk.choices[0].delta.content
    if content:  # 检查content是否存在
        print(content, end="", flush=True)

print()  # 最后换行，使输出更美观