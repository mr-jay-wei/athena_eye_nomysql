# Athena Eye - GCP服务器Docker化部署权威手册 (SOP V2.2 - SQLite版)

本文档是 `Athena Eye` 项目在全新的Google Cloud Platform (GCP) Linux服务器上，使用Docker进行**生产环境**容器化部署的**最终标准操作规程**。它凝聚了项目部署过程中的所有实战经验，旨在提供一个从零开始、一站式、高可靠性的部署指南。

---

## 目录
1.  [**服务器首次配置 (One-Time Setup)**](#1-服务器首次配置-one-time-setup)
    *   [1.1. 前提条件与实例创建建议](#11-前提条件与实例创建建议)
    *   [1.2. 【核心】安装核心工具 (Docker, Git, Screen)](#12-核心安装核心工具-docker-git-screen)
    *   [1.3. 优化SSH连接 (可选但强烈推荐)](#13-优化ssh连接-可选但强烈推荐)
2.  [**项目部署 (Initial Deployment)**](#2-项目部署-initial-deployment)
    *   [2.1. 克隆项目代码](#21-克隆项目代码)
    *   [2.2. 创建生产环境变量 (`.env`)](#22-创建生产环境变量-env)
    *   [2.3. 【关键】后台构建并启动系统](#23-关键后台构建并启动系统)
3.  [**日常运维 (Daily Operations)**](#3-日常运维-daily-operations)
    *   [3.1. 验证系统状态](#31-验证系统状态)
    *   [3.2. 查看服务日志](#32-查看服务日志)
    *   [3.3. 停止/重启系统](#33-停止重启系统)
4.  [**更新与维护 (Updates & Maintenance)**](#4-更新与维护-updates--maintenance)
5.  [**故障排查手册 (Troubleshooting FAQ)**](#5-故障排查手册-troubleshooting-faq)

---

## 1. 服务器首次配置 (One-Time Setup)

在全新的GCP服务器上，严格按照以下步骤操作一遍。

### 1.1. 前提条件与实例创建建议
*   **创建实例**: 在GCP控制台 **Compute Engine -> 虚拟机实例 -> 创建实例**。
*   **机器类型 (重要)**: 推荐 **`e2-small` (2 vCPU, 2 GB 内存)** 或更高配置。`e2-micro` (1 GB 内存) 现在有了运行的可能性，但仍建议从`e2-small`开始以保证稳定。
*   **启动磁盘**: 推荐使用 **`Ubuntu 22.04 LTS` (x86/64架构)** 镜像。
*   **防火墙**: 在创建实例时，务必**勾选“允许HTTP流量”和“允许HTTPS流量”**。

### 1.2. 【核心】安装核心工具 (Docker, Git, Screen)

**在新创建的服务器终端中，执行以下操作：**

1.  **等待系统更新完成**: 新服务器后台会自动运行安全更新。运行 `sudo apt install -y screen`，如果提示 `Waiting for cache lock...`，请耐心等待5-10分钟。
2.  **安装工具**:
    ```bash
    # 更新系统包列表
    sudo apt update
    # 安装 Git 和 Screen
    sudo apt install -y git screen
    # 使用Docker官方一键安装脚本
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    # 将当前用户添加到docker组以实现免sudo操作
    sudo usermod -aG docker $USER
    # 完成提示
    echo "✅ 核心工具已全部安装！请执行 'exit' 退出并重新登录SSH，使Docker权限生效。"
    ```
3.  **重新登录**: `exit` 退出并重新登录SSH。验证`docker ps`不报错。

### 1.3. 优化SSH连接 (可选但强烈推荐)
为防止SSH因空闲而自动断开，请在**您的本地电脑**上配置SSH KeepAlive。编辑 `~/.ssh/config` 文件并添加：
```
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

---

## 2. 项目部署 (Initial Deployment)

(确保您已经重新登录SSH，并获得了Docker权限)

### 2.1. 克隆项目代码
```bash
git clone https://your-git-repository-url/athena_eye.git
cd athena_eye_nomysql
```

### 2.2. 创建生产环境变量 (`.env`)
```bash
nano .env
```
将您本地电脑上`.env`文件的**全部内容**复制并粘贴进来。按 `Ctrl+X` -> `Y` -> `Enter` 保存。

### 2.3. 【关键】后台构建并启动系统
使用`screen`来防止SSH断开导致构建中断。

1.  **创建新的`screen`会话**: `screen -S athena`
2.  **在`screen`会话中，执行构建和启动命令**:
    ```bash
    # --build: 首次部署时必须使用，以构建镜像
    # -d: 后台运行
    sudo docker compose -f docker-compose.prod.yml up --build -d
    ```
    > **注意**: 如果免sudo配置成功，`sudo`不是必需的，但加上更保险。
3.  **脱离会话**: 按下组合键 **`Ctrl+A`**，然后松开，再按 **`d`**。构建需要一些时间，脱离后可安全断开SSH。

---

## 3. 日常运维 (Daily Operations)

### 3.1. 验证系统状态```bash
sudo docker compose -f docker-compose.prod.yml ps
```
### 3.2. 查看服务日志
```bash
# 查看后端实时日志
sudo docker compose -f docker-compose.prod.yml logs -f backend

# 查看前端Nginx实时日志
sudo docker compose -f docker-compose.prod.yml logs -f frontend
```
### 3.3. 停止/重启系统
```bash
# 停止
sudo docker compose -f docker-compose.prod.yml down

# 启动
sudo docker compose -f docker-compose.prod.yml up -d
```
---

## 4. 更新与维护 (Updates & Maintenance)
1.  `cd ~/athena_eye`
2.  `git pull`
3.  `sudo docker compose -f docker-compose.prod.yml up --build -d`
4.  (可选) `sudo docker image prune -f`

---

## 5. 故障排查手册 (Troubleshooting FAQ)

*   **问题**: `apt`命令提示`Waiting for cache lock...`
    *   **解决**: 耐心等待5-10分钟，让后台自动更新完成。

*   **问题**: 运行`docker`命令提示`permission denied`。
    *   **解决**: 确保已执行`sudo usermod -aG docker $USER`，并且**必须 `exit` 退出并重新登录SSH**。

*   **问题**: `backend`容器无法启动或不断重启。
    *   **原因**: 通常是`.env`文件配置错误或缺失。
    *   **解决**: 仔细检查`.env`文件是否存在且内容正确。使用`sudo docker compose -f docker-compose.prod.yml logs backend`查看详细的错误日志。

*   **问题**: `screen -r`提示会话`(Attached)`。
    *   **解决**: 先运行`screen -d <会话名>`强制脱离，再运行`screen -r <会ta名>`重新连接。