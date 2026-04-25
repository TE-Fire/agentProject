from langchain_community.chat_models import ChatTongyi
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser

strParser = StrOutputParser()
model = ChatTongyi(model="qwen-turbo")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你需要根据历史会话回答用户问题。对话历史: "),
        MessagesPlaceholder("chat_history"),
        ("human", "请回答如下问题: {input}")
    ]
)

def print_prompt(full_prompt):
    print("="*20, full_prompt.to_string(), "="*20)
    return full_prompt

base_chain = prompt | print_prompt | model | strParser
print(type(base_chain)) # <class 'langchain_core.runnables.base.RunnableSequence'>

store = {} # key就是session，value就是InMemoryChatMessageHistory对象，根据sessionId获取该用户的历史会话，该历史会话临时存在于内存中

def get_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# 通过RunnableWithMessageHistory获取一个带有新的历史记录功能的chain
conversation_chain = RunnableWithMessageHistory(
    base_chain, # 被附加历史消息的Runnable，用于加强一个新的chain
    get_history, # 获取历史会话的函数
    input_messages_key="input", # 用户提问
    history_messages_key="chat_history"
)

if __name__ == "__main__":
    # 固定配置，配置当前会话id
    session_config = {"configurable": {"session_id": "user_001"}}
    print(conversation_chain.invoke({"input": "小明有一只猫"}, session_config))
    print(conversation_chain.invoke({"input": "小刚有2只狗"}, session_config))
    print(conversation_chain.invoke({"input": "一共有几只宠物"}, session_config))
