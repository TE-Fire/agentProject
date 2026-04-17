import os
from openai import OpenAI

# - 华北2（北京）: https://dashscope.aliyuncs.com/compatible-mode/v1
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.6-plus",
    messages=[{'role': 'system', 'content': '你是一个专业的问答机器人,答复要十分简洁'},
              {'role': 'user', 'content': '你是谁，能够完成什么任务?'}]
)
print(completion.choices[0].message.content)