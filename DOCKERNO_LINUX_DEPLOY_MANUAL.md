# Athena Eye - Linux 服务器操作手册 (SOP)

本文档是`Athena Eye`项目在Linux服务器（Debian/Ubuntu on Google Cloud）上的标准操作规程（Standard Operating Procedure）。它涵盖了从首次部署到日常维护的所有关键命令和流程。

---

## 目录
1.  [首次部署](#1-首次部署)
2.  [日常管理](#2-日常管理)
3.  [更新与维护 (标准流程)](#3-更新与维护-标准流程)
4.  [故障排查](#4-故障排查)
5.  [`screen` 快捷键备忘录](#5-screen-快捷键备忘录)

---

## 1. 首次部署

当你在一个全新的、干净的Linux服务器上部署本项目时，请严格按照以下步骤操作。

### 1.1 登录服务器
通过SSH客户端或云服务商提供的Web Shell，登录到你的服务器。

### 1.2 更新系统并安装核心工具
```bash
# 更新软件包列表和已安装的软件
sudo apt update && sudo apt upgrade -y

# 安装Git, Python虚拟环境工具, 和Screen
sudo apt install -y git python3-venv screen
```

### 1.3 安装 `uv` 包管理器
```bash
# 下载并执行安装脚本
curl -LsSf https://astral.sh/uv/install.sh | sh
#curl -LsSf https://astral.sh/uv/install.sh -o install.sh
#sh install.sh
# 重新加载Shell配置以使uv命令生效
source ~/.profile

# 验证安装
uv --version
```

### 1.4 克隆项目代码
从你的Git仓库克隆项目。建议使用私有仓库。
```bash
git clone https://your-git-repository-url/athena_eye.git

# 进入项目目录
cd athena_eye/backend
```

### 1.5 创建并配置 `.env` 文件
`.env`文件包含了所有密钥和配置，**绝不能**上传到Git仓库。你需要在服务器上手动创建它。
```bash
# 使用nano文本编辑器创建文件
nano .env
```
将你本地的`.env`文件内容**完整地复制并粘贴**到编辑器中。按 `Ctrl+X` -> `Y` -> `Enter` 保存并退出。

### 1.6 创建并激活Python虚拟环境
这是一个至关重要的步骤，它为项目提供了一个隔离、干净的运行环境。
```bash
# 在项目根目录(~/athena_eye/backend)下，创建一个名为.venv的虚拟环境
uv venv

# 激活该虚拟环境
source .venv/bin/activate
```
激活后，你的命令行提示符前会出现`(.venv)`字样。

### 1.7 安装项目依赖
在激活的虚拟环境中，安装`pyproject.toml`中定义的所有依赖。
```bash
# -e . 表示以可编辑模式安装当前目录下的项目
uv pip install -e .
```
至此，首次部署全部完成！

---

## 2. 日常管理

### 2.1 启动 Athena Eye (后台运行)
```bash
# 1. 确保你处于激活的虚拟环境中
# (如果提示符前没有(.venv)，请先运行: source .venv/bin/activate)

# 2. 创建一个名为 athena 的 screen 后台会话
screen -S athena

# 3. 在新会话中，启动主程序
uv run -m athena_eye_project.main

# 4. 脱离会话，让它在后台运行
# 按下组合键: Ctrl+A, 然后松开, 再按 d
```

### 2.2 检查运行状态

#### 方法A：查看后台会话列表
```bash
screen -ls
```
-   如果看到 `(Detached)`，说明程序正在后台正常运行。
-   如果看到 `(Attached)`，说明你当前的终端正连接着该会话。
-   如果看到 `No Sockets found...`，说明没有任何程序在后台运行。

#### 方法B：连接到会话，查看实时日志
```bash
screen -r athena
```
执行后，你会“进入”程序的运行界面，看到实时的日志输出。看完后，按`Ctrl+A`, `d`再次脱离。

### 2.3 安全停止 Athena Eye
```bash
# 1. 连接回正在运行的会话
screen -r athena

# 2. 在程序日志滚动的界面，按下 Ctrl+C 来中断Python程序
# 你会看到命令行提示符重新出现

# 3. 输入 exit 并按回车，彻底关闭这个screen会话
exit
```

---

## 3. 更新与维护 (标准流程)

当你需要**修改配置**或**更新代码**时，请严格遵循以下SOP：

1.  **回去**: `screen -r athena`
2.  **停止**: `Ctrl+C`
3.  **关闭**: `exit`
4.  **进目录**: `cd ~/athena_eye/backend`
5.  **激活环境**: `source .venv/bin/activate`
6.  **修改**: `nano .env` (修改配置) 或 `git pull` (更新代码)
7.  **新建**: `screen -S athena`
8.  **启动**: `uv run -m athena_eye_project.main`
9.  **离开**: `Ctrl+A`, `d`

---

## 4. 故障排查

### 4.1 问题：`screen -ls` 显示有多个同名会话
**原因**: 重复执行了`screen -S athena`而没有关闭旧会话。
**解决方案**:
```bash
# 1. 查看所有会话及其ID
screen -ls

# 2. 假设你想杀死ID为 83675.athena 的旧会话
screen -X -S 83675.athena quit
```

### 4.2 问题：`screen -ls` 显示 `(Attached)`，但无法 `Ctrl+A, d` 脱离
**原因**: 当前SSH连接“卡”在了会话里，无法通过常规快捷键脱离。
**解决方案**:
1.  **保持当前SSH窗口不动。**
2.  **打开一个全新的SSH窗口**，登录到同一台服务器。
3.  在新窗口中，执行强制脱离命令：
    ```bash
    screen -d athena
    ```
4.  回到原来的窗口，你会发现它已经被踢回了主终端。

---

## 5. `screen` 快捷键备忘录

所有命令都以“唤醒词” **`Ctrl+A`** 作为前缀。

-   **`Ctrl+A` `d`**: **D**etach，脱离当前会话（最常用）。
-   **`Ctrl+A` `c`**: **C**reate，在当前会话中创建新窗口（标签页）。
-   **`Ctrl+A` `n`**: **N**ext，切换到下一个窗口。
-   **`Ctrl+A` `p`**: **P**revious，切换到上一个窗口。
-   **`Ctrl+A` `k`**: **K**ill，杀死当前窗口。
-   **`Ctrl+A` `[`**: 进入滚动/复制模式，可以用方向键上翻查看历史日志，按`Esc`退出。
-   **`Ctrl+A` `?`**: 显示帮助信息。