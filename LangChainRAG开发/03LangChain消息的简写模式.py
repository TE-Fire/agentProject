from langchain_community.chat_models import ChatTongyi

model = ChatTongyi(model="qwen-turbo")

messages = [
    # 使用元组表示消息角色和内容，角色为system、ai、human
    ("system", "你是一位边塞诗人。"),
    ("ai", "你好，我是一个专业的边塞诗人。"),
    ("human", "写一首唐诗")
]


res = model.stream(input=messages)

for chunk in res:
    print(chunk.content, end="", flush=True)
