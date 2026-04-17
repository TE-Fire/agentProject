# 代码分析技能

## 技能信息
- **name**: code_analyzer
- **description**: 分析Java和Python代码质量
- **version**: 1.0.0
- **author**: Developer

## 功能描述
- 分析代码质量
- 检测代码中的问题和潜在错误
- 提供代码优化建议
- 评估代码复杂度
- 检查代码风格和规范

## 输入参数
- **language**: 代码语言 (Java/Python)
- **code**: 要分析的代码
- **analysis_type**: 分析类型 (quality/style/complexity)

## 输出格式
- **issues**: 发现的问题列表
- **suggestions**: 优化建议
- **metrics**: 代码度量指标
- **complexity**: 复杂度分析

## 示例
### 输入
```json
{
  "language": "Java",
  "code": "public class Calculator {\n    public int add(int a, int b) {\n        int result = a + b;\n        return result;\n    }\n}\n",
  "analysis_type": "quality"
}
```

### 输出
```json
{
  "issues": [],
  "suggestions": ["考虑添加参数验证"],
  "metrics": {
    "lines": 6,
    "methods": 1,
    "cyclomatic_complexity": 1
  },
  "complexity": "低"
}
```