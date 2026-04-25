from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

func = RunnableLambda(lambda ai_msg : {"name": ai_msg.content})

model = ChatTongyi(model="qwen-turbo")
parser = StrOutputParser()


firstPromptTemplate = PromptTemplate.from_template(
    '我的领居姓{last_name}, 刚生了{gender}'
    '帮我起个名字，封装json格式为: {{"name": "value"}}，value是你起的名字'

)

second_prompt = PromptTemplate.from_template(
    "姓名: {name}, 帮我解析含义, 简单概述即可"
)
# AIMessage --> func --> dict
# 也可直接传入lambda对象，会自动把函数转换为RunnableLambda对象
chain = firstPromptTemplate | model | func | second_prompt | model | parser

for chunk in chain.stream({ "last_name": "李", "gender": "女儿" }):
    print(chunk, end="", flush=True)
