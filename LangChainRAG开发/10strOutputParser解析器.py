from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatTongyi
from langchain_core.output_parsers import StrOutputParser 


model = ChatTongyi(model="qwen-turbo")
parser = StrOutputParser()

prompt_template = PromptTemplate.from_template(
    "我的领居姓{last_name}, 刚生了{gender}，帮我起个名字，简单回答。"
)

# 将AIMessage解析为字符串，同时StrOutputParser又继承自runnable接口可以加入chain进行链式调用
chain = prompt_template | model | parser | model

res = chain.invoke(input={"last_name": "王", "gender": "女儿"}).content

print(res)

print(type(res))

