# 使用官方 Python 轻量级镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 更新 pip
RUN pip install --upgrade pip

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
# --no-cache-dir 减小镜像体积
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 暴露 Streamlit 默认端口
EXPOSE 8501

# 设置 Streamlit 配置环境变量
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
ENV STREAMLIT_SERVER_ENABLE_WEBSOCKET_COMPRESSION=false
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# 启动命令
# 注意：移除了 healthcheck 中的 curl 依赖，改用 streamlit 原生配置
ENTRYPOINT ["sh", "-c", "streamlit run main.py --server.address 0.0.0.0 --server.port ${PORT:-8501}"]
