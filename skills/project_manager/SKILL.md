# 项目管理技能

## 技能信息
- **name**: project_manager
- **description**: 管理Java和Python项目结构
- **version**: 1.0.0
- **author**: Developer

## 功能描述
- 生成项目结构
- 管理项目依赖
- 配置项目构建工具
- 生成项目配置文件

## 输入参数
- **language**: 项目语言 (Java/Python)
- **project_type**: 项目类型 (web/application/library)
- **name**: 项目名称
- **dependencies**: 依赖项列表
- **features**: 项目功能需求

## 输出格式
- **structure**: 项目结构
- **configuration_files**: 配置文件
- **build_commands**: 构建命令
- **setup_instructions**: 设置说明

## 示例
### 输入
```json
{
  "language": "Java",
  "project_type": "web",
  "name": "springboot-demo",
  "dependencies": ["Spring Boot", "Spring Security", "MyBatis"],
  "features": "用户管理和订单管理模块"
}
```

### 输出
```json
{
  "structure": "springboot-demo/\n├── src/\n│   ├── main/\n│   │   ├── java/\n│   │   │   └── com/\n│   │   │       └── example/\n│   │   │           ├── controller/\n│   │   │           ├── service/\n│   │   │           ├── repository/\n│   │   │           └── model/\n│   │   └── resources/\n│   └── test/\n├── pom.xml
└── README.md",
  "configuration_files": ["pom.xml", "application.properties"],
  "build_commands": ["mvn clean install", "mvn spring-boot:run"],
  "setup_instructions": "1. 安装Maven\n2. 执行mvn clean install\n3. 执行mvn spring-boot:run"
}
```