from langchain_community.embeddings import DashScopeEmbeddings

# 初始化DashScopeEmbeddings, 默认模型为text-embedding-v1
model = DashScopeEmbeddings()

print(model.embed_query("你好, 我是alex"))
print(model.embed_documents(["你好, 我是alex", "你好, 我是bobby"]))
