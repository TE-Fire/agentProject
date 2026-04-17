# 依赖管理技能

## 技能信息
- **name**: dependency_manager
- **description**: 管理Java和Python项目依赖
- **version**: 1.0.0
- **author**: Developer

## 功能描述
- 分析项目依赖
- 检查依赖版本冲突
- 推荐依赖版本
- 生成依赖配置文件

## 输入参数
- **language**: 项目语言 (Java/Python)
- **dependencies**: 依赖项列表
- **project_type**: 项目类型
- **build_tool**: 构建工具 (maven/gradle/pip)

## 输出格式
- **dependency_config**: 依赖配置
- **version_conflicts**: 版本冲突
- **recommendations**: 依赖建议
- **setup_commands**: 设置命令

## 示例
### 输入
```json
{
  "language": "Java",
  "dependencies": ["Spring Boot", "Spring Security", "MyBatis"],
  "project_type": "web",
  "build_tool": "maven"
}
```

### 输出
```json
{
  "dependency_config": "<dependencies>\n    <dependency>\n        <groupId>org.springframework.boot</groupId>\n        <artifactId>spring-boot-starter-web</artifactId>\n        <version>3.2.0</version>\n    </dependency>\n    <dependency>\n        <groupId>org.springframework.boot</groupId>\n        <artifactId>spring-boot-starter-security</artifactId>\n        <version>3.2.0</version>\n    </dependency>\n    <dependency>\n        <groupId>org.mybatis.spring.boot</groupId>\n        <artifactId>mybatis-spring-boot-starter</artifactId>\n        <version>3.0.3</version>\n    </dependency>\n</dependencies>",
  "version_conflicts": [],
  "recommendations": ["建议添加spring-boot-starter-test依赖用于测试"],
  "setup_commands": ["mvn dependency:resolve"]
}
```