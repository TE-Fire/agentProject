# MCP 配置文件

## 智能体信息
- **name**: DevAssistant
- **description**: 一个专为Java和Python开发者设计的智能开发助手
- **version**: 1.0.0
- **author**: Developer

## 核心功能
- 代码生成与优化
- 项目结构设计
- 技术文档生成
- 代码质量分析
- 依赖管理

## 工作流程
1. 接收用户输入
2. 分析用户需求
3. 选择合适的Skill处理任务
4. 执行Skill并获取结果
5. 整合结果并返回给用户

## 技能列表
- code_generator: 代码生成技能
- code_analyzer: 代码分析技能
- project_manager: 项目管理技能
- doc_generator: 文档生成技能
- dependency_manager: 依赖管理技能

## 配置参数
- **timeout**: 300s
- **max_retries**: 3
- **default_language**: Java
- **supported_languages**: ["Java", "Python"]