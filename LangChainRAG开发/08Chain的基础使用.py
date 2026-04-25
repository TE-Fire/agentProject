from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatTongyi

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个山水田园诗人"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "请再来一首诗")
    ]
)

history_data = [
    ("human", "请写一首关于山水的诗"),
    ("ai", "天门中断楚江开，碧水东流至此回。两岸青山相对出，孤帆一片日边来。"),
    ("human", "请再来一首关于山水的诗"),
    ("ai","湖光秋月两相和，潭面无风镜未磨。遥望洞庭山水翠，白银盘里一青螺。")
]

model = ChatTongyi(model="qwen-turbo")

chain = chat_prompt_template | model #重 载|运算符进行实现
print(type(chain)) # <class 'langchain_core.runnables.base.RunnableSequence'> 

for chunk in chain.stream({"history": history_data}): # 将history_data--> 注入chat_prompt_template --> 注入model 链式调用都必须满足继承自Runnable接口
    print(chunk.content, end="", flush=True)
