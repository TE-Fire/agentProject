# 代码生成技能

## 技能信息
- **name**: code_generator
- **description**: 生成Java和Python代码
- **version**: 1.0.0
- **author**: Developer

## 功能描述
- 生成Java类和方法
- 生成Python模块和函数
- 根据需求生成完整的代码结构
- 支持代码模板和最佳实践

## 输入参数
- **language**: 目标语言 (Java/Python)
- **type**: 代码类型 (class/function/module)
- **name**: 代码名称
- **requirements**: 功能需求描述
- **parameters**: 输入参数（如果需要）
- **return_type**: 返回类型（如果需要）

## 输出格式
- **code**: 生成的代码
- **explanation**: 代码解释
- **dependencies**: 依赖项

## 示例
### 输入
```json
{
  "language": "Java",
  "type": "class",
  "name": "UserService",
  "requirements": "用户服务类，包含用户创建、查询、更新和删除方法"
}
```

### 输出
```json
{
  "code": "public class UserService {\n    public User createUser(User user) {\n        // 创建用户逻辑\n        return user;\n    }\n    \n    public User getUserById(long id) {\n        // 查询用户逻辑\n        return null;\n    }\n    \n    public User updateUser(User user) {\n        // 更新用户逻辑\n        return user;\n    }\n    \n    public void deleteUser(long id) {\n        // 删除用户逻辑\n    }\n}",
  "explanation": "生成了一个UserService类，包含基本的CRUD操作方法",
  "dependencies": ["User类"]
}
```