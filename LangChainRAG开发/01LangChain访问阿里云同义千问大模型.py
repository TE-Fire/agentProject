from langchain_community.chat_models import ChatTongyi
import os

# 检查环境变量
api_key = os.getenv("DASHSCOPE_API_KEY")
print(f"API Key: {api_key}")
print(f"API Key exists: {api_key is not None}")

model = ChatTongyi(
    model="qwen-turbo",  # 使用更通用的模型名称
    api_key=api_key,
    base_url="https://dashscope.aliyuncs.com/api/v1"  # 使用标准API地址
)

# res = model.invoke("你是谁，能够完成什么任务?") # invoke调用模型，一次返回完整结果
res = model.stream("你是谁，能够完成什么任务?") # stream调用模型，返回流式结果
for chunk in res:
    print(chunk.content, end="", flush=True)
