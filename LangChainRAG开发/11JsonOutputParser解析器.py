from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import PromptTemplate

model = ChatTongyi(model="qwen-turbo")
parser = StrOutputParser()
jsonParser = JsonOutputParser()


firstPromptTemplate = PromptTemplate.from_template(
    '我的领居姓{last_name}, 刚生了{gender}'
    '帮我起个名字，封装json格式为: {{"name": "value"}}，value是你起的名字'

)

second_prompt = PromptTemplate.from_template(
    "姓名: {name}, 帮我解析含义"
)
chain = firstPromptTemplate | model | jsonParser | second_prompt | model | parser

for chunk in chain.stream({ "last_name": "张", "gender": "女儿" }):
    print(chunk, end="", flush=True)
# chain = firstPromptTemplate | model | jsonParser

# res = chain.invoke({"last_name": "王", "gender": "女儿"}) #{'name': '王雨桐'} <class 'dict'>
# print(res)
# print(type(res))