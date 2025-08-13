# frontend/Dockerfile
# 使用多阶段构建（Multi-stage build），保持最终镜像的轻量

# --- 第一阶段: 构建阶段 (Build Stage) ---
# 使用一个包含完整Node.js环境的镜像来构建我们的Vue项目
FROM node:20-alpine AS build-stage

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 package-lock.json (或 yarn.lock / pnpm-lock.yaml)
COPY package*.json ./

# 安装项目依赖
RUN npm install

# 复制所有前端源代码
COPY . .

# 执行构建命令，生成静态文件到 /app/dist 目录
RUN npm run build


# --- 第二阶段: 生产阶段 (Production Stage) ---
# 使用一个超轻量级的Nginx官方镜像作为我们的生产环境基础
FROM nginx:stable-alpine

# 将构建阶段生成的静态文件，复制到Nginx的默认网站根目录
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 【核心】复制我们自定义的Nginx配置文件
# 这个文件将告诉Nginx如何处理请求和反向代理
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露80端口
EXPOSE 80

# Nginx镜像的默认CMD就是启动Nginx服务，我们无需重写