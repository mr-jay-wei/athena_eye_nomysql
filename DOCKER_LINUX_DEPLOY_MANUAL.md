# Athena Eye - GCP服务器Docker化部署权威手册 (SOP V2.1)

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
    *   [2.3. 创建MySQL低内存配置 (`my.cnf`)](#23-创建mysql低内存配置-mycnf)
    *   [2.4. 【关键】后台构建并启动系统](#24-关键后台构建并启动系统)
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
*   **机器类型 (重要)**: 强烈推荐 **`e2-small` (2 vCPU, 2 GB 内存)** 或更高配置。
    *   **教训**: `e2-micro` (1 GB 内存) 经实践证明**资源不足**，会导致系统服务（如SSH、MySQL）随机启动失败或运行崩溃。
*   **启动磁盘**: 推荐使用 **`Ubuntu 22.04 LTS` (x86/64架构)** 镜像。它比Debian有更好的开箱即用兼容性。
*   **防火墙**: 在创建实例时，务必**勾选“允许HTTP流量”和“允许HTTPS流量”**。这会自动为您配置好80和443端口的防火墙规则。
*   **登录**: 实例创建后，通过GCP控制台的“SSH”按钮连接到服务器。

### 1.2. 【核心】安装核心工具 (Docker, Git, Screen)

**在新创建的服务器终端中，执行以下操作：**

**第一步：处理系统自动更新 (非常重要)**
新创建的服务器会立即在后台运行安全更新，这会锁住`apt`。我们需要等待或手动处理它。

1.  运行 `sudo apt install -y screen`。
2.  如果提示 `Waiting for cache lock...`，请**耐心等待5-10分钟**，让后台更新自动完成。
3.  如果等待后依然被锁，请**打开一个新的SSH窗口**，执行以下命令找到并终止更新进程：
    ```bash
    # 在新窗口中查找进程ID (PID)
    ps aux | grep apt
    # 记下 apt upgrade 那个进程的PID，然后终结它
    sudo kill <PID>
    # 修复可能的中断状态
    sudo dpkg --configure -a
    ```
4.  回到第一个窗口，`apt install screen`命令现在应该可以成功执行。

**第二步：安装所有工具**
在`apt`锁解除后，运行以下命令块完成所有安装。

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
> **操作**: 复制并执行上述命令块。完成后，**务必 `exit` 退出并重新登录SSH**。重新登录后，运行 `docker ps` 和 `groups`，若不报错且`groups`输出中包含`docker`，则表示配置成功。

### 1.3. 优化SSH连接 (可选但强烈推荐)
为防止SSH因空闲而自动断开，请在**您的本地电脑**上配置SSH KeepAlive。
1.  在本地电脑上找到或创建 `~/.ssh/config` 文件。
2.  添加以下内容并保存：
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
cd athena_eye
```

### 2.2. 创建生产环境变量 (`.env`)
```bash
nano .env
```
> **操作**: 将您本地电脑上`.env`文件的**全部内容**复制并粘贴进来。按 `Ctrl+X` -> `Y` -> `Enter` 保存。

### 2.3. 创建MySQL低内存配置 (`my.cnf`)
```bash
nano my.cnf
```
> **操作**: 将以下**内容**完整复制并粘贴进来。确保`[mysqld]`是文件的第一行。
> ```ini
> [mysqld]
> performance_schema = off
> innodb_buffer_pool_size = 128M
> innodb_log_file_size = 32M
> innodb_flush_log_at_trx_commit = 2
> innodb_flush_method = O_DIRECT
> max_connections = 50
> thread_cache_size = 8
> skip-log-bin
> skip-name-resolve
> ```
> 按 `Ctrl+X` -> `Y` -> `Enter` 保存。

### 2.4. 【关键】后台构建并启动系统
使用`screen`来防止SSH断开导致构建中断。

1.  **杀死可能残留的旧`screen`会话**: `screen -X -S athena quit`
2.  **创建新的、拥有正确权限的`screen`会话**: `screen -S athena`
3.  **在`screen`会话中，执行构建和启动命令**:
    ```bash
    # --build: 首次部署时必须使用，以构建镜像
    # -d: 后台运行
    sudo docker compose -f docker-compose.prod.yml up --build -d
    ```
    > **注意**: 如果您严格按照1.2节的步骤并重新登录，`sudo`可能不是必需的。但为了100%成功，加上`sudo`是最稳妥的选择。

4.  **脱离会话**: 按下组合键 **`Ctrl+A`**，然后松开，再按 **`d`**。
> **操作**: 构建过程需要5-15分钟。脱离后可安全断开SSH。稍后可使用`screen -r athena`重新连接回去查看日志，或直接访问网站验证。

---

## 3. 日常运维 (Daily Operations)

### 3.1. 验证系统状态
```bash
sudo docker compose -f docker-compose.prod.yml ps
```
### 3.2. 查看服务日志
```bash
sudo docker compose -f docker-compose.prod.yml logs -f backend

# 查看前端Nginx实时日志
sudo docker compose -f docker-compose.prod.yml logs -f frontend

# 查看数据库实时日志
sudo docker compose -f docker-compose.prod.yml logs -f db
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
    *   **原因**: 服务器后台正在自动运行安全更新。
    *   **解决**: **耐心等待5-10分钟**，它会自动结束。如果长时间不结束，参考 **1.2节** 的方法手动处理。

*   **问题**: 运行`docker`命令提示`permission denied`。
    *   **原因**: 当前用户不在`docker`用户组，或者权限未在当前SSH会话生效。
    *   **解决**:
        1.  确保您已执行`sudo usermod -aG docker $USER`。
        2.  **必须 `exit` 退出并重新登录SSH**。
        3.  如果在新会话中`groups`命令输出仍不含`docker`，说明`usermod`未生效，请在所有`docker`命令前加上`sudo`。

*   **问题**: `screen -r`提示会话`(Attached)`。
    *   **原因**: 上一个SSH连接异常断开。
    *   **解决**: 先运行`screen -d <会话名>`强制脱离，再运行`screen -r <会话名>`重新连接。

*   **问题**: `db`容器`unhealthy`或`backend`无法启动。
    *   **原因**: 绝大多数情况是`e2-micro`的**内存不足**。
    *   **解决**: 强烈建议**使用`e2-small`或更高配置的实例**。同时，请确保`my.cnf`文件已正确创建且格式无误（`[mysqld]`在第一行）。