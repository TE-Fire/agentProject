from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

model = ChatTongyi(model="qwen-turbo")

messages = [
    SystemMessage(content="你是一位边塞诗人。"),
    HumanMessage(content="写一首唐诗")
]


res = model.stream(input=messages)

for chunk in res:
    print(chunk.content, end="", flush=True)
