# 扫地机器人智能客服

基于 **LangChain Agent + RAG** 的产品客服实践项目：以 Streamlit 提供聊天界面，智能体可检索产品知识库回答问题，也能调用工具查询使用记录并生成月度使用报告。

## 功能

- **RAG 知识库问答**：产品知识文档切分后存入 Chroma 向量库，检索后由大模型总结回答
- **工具调用（ReAct Agent）**：检索资料、查询天气 / 用户位置 / 用户 ID / 当前月份 / 指定月份的使用记录
- **报告模式**：当智能体调用 `fill_context_for_report` 工具时，中间件动态切换提示词，转而生成结构化的使用报告
- **流式输出**：回答通过 Streamlit 聊天界面逐字显示

## 技术栈

- [Streamlit](https://streamlit.io/) — Web 聊天界面
- [LangChain](https://python.langchain.com/) — `create_agent`、middleware、tools
- [Chroma](https://www.trychroma.com/) — 本地向量数据库（`chroma_db/`）
- 通义千问（DashScope）— 对话模型 `qwen3.7-max` 与向量模型 `text-embedding-v4`

## 目录结构

```
.
├── app.py                     # Streamlit 应用入口
├── agent/
│   ├── react_agent.py         # ReactAgent：组装模型、工具、中间件，流式输出
│   ├── agent_tools.py         # 工具定义：RAG 检索、天气、位置、使用记录等
│   └── middleware.py          # 中间件：报告模式提示词切换、工具监控
├── rag/
│   ├── rag_service.py         # 检索 + 总结链
│   └── vector_store.py        # 向量库构建与检索（可单独运行建库）
├── model/factory.py           # 对话 / 向量模型工厂
├── prompt_template/           # 系统提示词、RAG 总结提示词、报告提示词
├── utils/                     # 文件加载、提示词加载
├── knowledge_database/        # 产品知识文档（txt）
└── usage_data/records.csv     # 演示用使用记录数据
```

## 快速开始

1. 安装依赖（建议 Python 3.10+）：

   ```bash
   pip install -r requirements.txt
   ```

2. 配置 DashScope API Key（[阿里云百炼](https://bailian.console.aliyun.com/) 获取）：

   ```powershell
   # PowerShell
   $env:DASHSCOPE_API_KEY="sk-xxx"

   # Bash
   export DASHSCOPE_API_KEY="sk-xxx"
   ```

3. 首次运行先构建向量库（`chroma_db/` 与 `md5_hex.txt` 为生成物，已被 .gitignore 排除，会在首次建库时自动生成）：

   ```bash
   python -m rag.vector_store
   ```

4. 启动应用：

   ```bash
   streamlit run app.py
   ```

浏览器打开后即可在侧边栏点击推荐问题，或直接输入问题对话；试试"帮我生成我 2026-10 月的使用报告"。

## 说明

- 新增或修改 `knowledge_database/` 中的文档后，重新运行 `python -m rag.vector_store` 即可增量入库（已按文件 MD5 去重）。
- `usage_data/records.csv` 为演示数据，用户 ID 固定为 `1001`。
