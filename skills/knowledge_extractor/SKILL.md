# 知识点提取技能

## 技能信息
- **name**: knowledge_extractor
- **description**: 提取响应中的主要知识点并生成Markdown格式
- **version**: 1.0.0
- **author**: Developer

## 功能描述
- 分析响应内容，识别主要知识点
- 将知识点组织成结构化的Markdown格式
- 确保知识点覆盖核心内容
- 保持Markdown格式清晰易读

## 输入参数
- **response**: 原始响应内容
- **question**: 用户的原始问题（可选）
- **language**: 输出语言（中文/English，默认中文）

## 输出格式
- **markdown**: 生成的Markdown文本
- **key_points**: 提取的关键知识点列表
- **structure**: 文档结构

## 示例
### 输入
```json
{
  "response": "Java中的多线程可以通过继承Thread类或实现Runnable接口来实现。线程池可以提高性能，减少线程创建和销毁的开销。常见的线程池包括FixedThreadPool、CachedThreadPool和ScheduledThreadPool。",
  "question": "Java多线程的实现方式和线程池类型",
  "language": "中文"
}
```

### 输出
```json
{
  "markdown": "# Java多线程知识点\n\n## 实现方式\n- 继承Thread类\n- 实现Runnable接口\n\n## 线程池\n- **作用**：提高性能，减少线程创建和销毁的开销\n- **类型**：\n  - FixedThreadPool\n  - CachedThreadPool\n  - ScheduledThreadPool\n",
  "key_points": ["Java多线程实现方式", "线程池作用", "常见线程池类型"],
  "structure": ["Java多线程知识点", "实现方式", "线程池"]
}
```