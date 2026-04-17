# 文档生成技能

## 技能信息
- **name**: doc_generator
- **description**: 生成技术文档
- **version**: 1.0.0
- **author**: Developer

## 功能描述
- 生成API文档
- 生成项目文档
- 生成技术架构文档
- 生成用户手册

## 输入参数
- **doc_type**: 文档类型 (api/architecture/project/user_manual)
- **content**: 文档内容来源
- **format**: 输出格式 (markdown/html/pdf)
- **language**: 文档语言 (中文/English)

## 输出格式
- **document**: 生成的文档内容
- **format**: 文档格式
- **sections**: 文档章节

## 示例
### 输入
```json
{
  "doc_type": "api",
  "content": "public class UserController {\n    @GetMapping(\"/users\")\n    public List<User> getUsers() {\n        return userService.getUsers();\n    }\n    \n    @PostMapping(\"/users\")\n    public User createUser(@RequestBody User user) {\n        return userService.createUser(user);\n    }\n}",
  "format": "markdown",
  "language": "中文"
}
```

### 输出
```json
{
  "document": "# UserController API 文档\n\n## 接口列表\n\n### GET /users\n- **功能**: 获取所有用户\n- **返回值**: List<User>\n\n### POST /users\n- **功能**: 创建新用户\n- **请求体**: User对象\n- **返回值**: 创建的User对象\n",
  "format": "markdown",
  "sections": ["接口列表", "GET /users", "POST /users"]
}
```