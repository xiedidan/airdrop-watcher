# WebMon Docker Image
# 多阶段构建：前端构建 + Python运行时

# ============================================
# 阶段1: 前端构建
# ============================================
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# 复制前端依赖文件
COPY frontend/package.json frontend/package-lock.json ./

# 安装依赖
RUN npm ci

# 复制前端源码
COPY frontend/ ./

# 构建前端（输出到 dist 目录）
RUN npm run build

# ============================================
# 阶段2: Python运行时
# ============================================
FROM python:3.11-slim-bookworm

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# 安装系统依赖（Playwright需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Playwright 依赖
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxkbcommon0 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    # 字体支持
    fonts-noto-cjk \
    # 网络工具
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制Python依赖文件
COPY requirements.txt ./

# 安装Python依赖（增加超时和重试机制）
RUN pip install --no-cache-dir --timeout 300 --retries 5 -r requirements.txt

# 安装Playwright浏览器
RUN playwright install chromium

# 复制应用代码
COPY webmon/ ./webmon/
COPY webmon.py ./

# 从前端构建阶段复制静态文件
COPY --from=frontend-builder /app/frontend/dist ./webmon/web/static/

# 创建必要的目录
RUN mkdir -p /app/config /app/data /app/logs

# 创建非root用户
RUN groupadd -r webmon && useradd -r -g webmon webmon \
    && chown -R webmon:webmon /app /ms-playwright

# 切换到非root用户
USER webmon

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "webmon.web.app:app", "--host", "0.0.0.0", "--port", "8000"]
