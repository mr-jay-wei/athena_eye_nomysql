# backend/Dockerfile (已修复构建时文件缺失问题)

# --- Stage 1: 使用官方的Python 3.12 slim镜像作为基础 ---
    FROM python:3.12-slim

    # --- 设置环境变量 ---
    ENV PYTHONUNBUFFERED=1
    ENV PATH="/root/.local/bin:${PATH}"
    
    # --- 设置工作目录 ---
    WORKDIR /app
    
    # --- 【核心修复】调整文件复制顺序 ---
    
    # 1. 先复制项目定义文件
    COPY pyproject.toml ./
    
    # 2. 接着，把所有项目代码和相关文件都复制过来
    #    这样，在下一步安装时，构建工具就能找到所有需要的文件了
    COPY . .
    
    # 3. 最后，在文件齐全的情况下，安装所有依赖
    #    这个指令包含了多个步骤，以确保健壮性和镜像体积
    RUN apt-get update && \
        apt-get install -y curl && \
        # 安装uv
        curl -LsSf https://astral.sh/uv/install.sh | sh && \
        # 使用uv安装项目依赖（包括我们自己的包）
        uv pip install . --system && \
        # 清理工作
        apt-get purge -y --auto-remove curl && \
        rm -rf /var/lib/apt/lists/*
    
    RUN mkdir logs
    
    # --- 暴露端口 ---
    EXPOSE 8000
    
    # --- 默认启动命令 ---
    CMD ["uvicorn", "athena_eye_project.main_api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]