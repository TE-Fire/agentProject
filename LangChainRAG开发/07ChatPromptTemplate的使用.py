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

prompt_text = chat_prompt_template.invoke(input={"history": history_data}).to_string()
print(prompt_text)
print(model.invoke(input= prompt_text).content)
