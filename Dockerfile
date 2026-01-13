# 使用官方轻量级 Python 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 先拷贝依赖文件（利用 Docker 缓存层）
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 拷贝代码
COPY . .

# 启动命令 (直接用 FastAPI CLI)
CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
