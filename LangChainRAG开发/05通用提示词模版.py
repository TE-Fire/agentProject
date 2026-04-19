from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatTongyi



model = ChatTongyi(model="qwen-turbo")

prompt_template = PromptTemplate.from_template(
    "我的领居姓{last_name}, 刚生了{gender}的孩子，帮我起个名字，简单回答。"
)

# prompt_text = prompt_template.format(last_name="王", gender="男")
# print(model.invoke(prompt_text).content)

# 构建LangChain的链式调用
chain = prompt_template | model
print(chain.invoke(input={"last_name": "王", "gender": "女"}).content)
