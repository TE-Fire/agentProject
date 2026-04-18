import json

# 字典或列表序列化为JSON字符串 ： json.dumps()
   
# 使用列表存储多个字典
exampleList = [
    {
        "name": "小明",
        "age": 18,
        "gender": "男",
        "workExperience": [
            {
                "company": "公司A",
                "position": "开发人员",
                "duration": "2020-01-2022-01"
            }
        ]
    },
    {
        "name": "小红",
        "age": 19,
        "gender": "女",
        "workExperience": [
            {
                "company": "公司B",
                "position": "测试人员",
                "duration": "2022-01-2024-01"
            }
        ]
    },
    {
        "name": "小绿",
        "age": 20,
        "gender": "女",
        "workExperience": [
            {
                "company": "公司C",
                "position": "产品管理",
                "duration": "2024-01-2026-01"
            }
        ]
    }
]

exampleJson = json.dumps(exampleList, ensure_ascii=False, indent=4) #ensure_ascii=False 表示不使用ASCII编码，保留中文字符, indent=4 表示缩进4个空格
print(exampleJson)


strExampleJson = '''
[
    {"name":"小明","age":18,"gender":"男","workExperience":[{"company":"公司A","position":"开发人员","duration":"2020-01-2022-01"}]},
    {"name":"小红","age":19,"gender":"女","workExperience":[{"company":"公司B","position":"测试人员","duration":"2022-01-2024-01"}]},
    {"name":"小绿","age":20,"gender":"女","workExperience":[{"company":"公司C","position":"产品管理","duration":"2024-01-2026-01"}]}
]
'''

print(json.loads(strExampleJson)) # json字符串对于key和value的类型是字符串,需要使用""引起来
