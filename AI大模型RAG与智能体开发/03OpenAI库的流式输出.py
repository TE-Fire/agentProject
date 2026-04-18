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
            { "role": "system", "content": "你是一位诗人，可以根据我提供的意象和景物来写一首五言律诗，只生成诗即可"},
            { "role": "assistant", "content": "好的，我是一位诗人，将为你提供最简洁的诗文，你要什么类型的诗文？"},
            { "role": "user", "content": "意象：明月、友人、离别，为我生成一首五言律诗"}
        ],
        stream=True
    )

# 3.处理结果
for chunk in response:
    content = chunk.choices[0].delta.content
    if content:  # 检查content是否存在
        print(content, end="", flush=True)

print()  # 最后换行，使输出更美观