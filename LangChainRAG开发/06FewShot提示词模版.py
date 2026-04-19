from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_community.chat_models import ChatTongyi

example_template = PromptTemplate.from_template("单词: {word}, 反义词: {antonym}")
example_data = [
    {"word": "好", "antonym": "坏"},
    {"word": "大", "antonym": "小"},
    {"word": "快", "antonym": "慢"}
]
few_shot_template = FewShotPromptTemplate(
    example_prompt = example_template, # 每个示例的提示模版
    examples = example_data, # 示例数据
    prefix = "告知我单词的反义词，我提供如下示例: ", # 提示前缀
    suffix = "基于前面的示例告知我，{input_word}", # 提示后缀
    input_variables = ['input_word']  # 输入变量
)

model = ChatTongyi(model="qwen-turbo")
prompt_text = few_shot_template.invoke(input=[{"input_word": "左"}, {"input_word": "右"}])
print(prompt_text)
print(model.invoke(input=prompt_text).content)
