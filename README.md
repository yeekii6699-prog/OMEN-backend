# OMEN · Backend

OMEN 塔罗牌项目的后端服务，基于 FastAPI 构建，预留 LangChain / LangGraph 用于后续 AI 编排能力。

> 前端仓库：[OMEN-frontend](https://github.com/yeekii6699-prog/OMEN-frontend)

## 技术栈

- **框架**：FastAPI + Uvicorn
- **AI（预留）**：LangChain、LangGraph、OpenAI

## 快速开始

```bash
# 1. 安装依赖（建议先创建虚拟环境）
pip install -r requirements.txt

# 2. 启动开发服务器
uvicorn app.main:app --reload --port 8000
```

服务启动后访问 http://localhost:8000 ，应返回：

```json
{ "message": "OMEN Backend is active." }
```

## API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 健康检查，返回服务状态 |

> 更多业务端点开发中。

## Docker

```bash
docker build -t omen-backend .
docker run -p 8000:8000 omen-backend
```

## 工具脚本

- `app/download_tarot_images.py` — 从 CDN 批量下载塔罗牌图片到本地的开发辅助脚本。

## License

[MIT](./LICENSE)
