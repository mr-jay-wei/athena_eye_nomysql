# Athena Eye 项目：云端部署实战复盘报告

**文档目的**: 本文档旨在系统性地记录`Athena Eye`项目从本地开发环境迁移至Google Cloud Platform (GCP)生产环境的全过程中，所遇到的所有关键问题、错误、诊断过程及最终解决方案。其目的是提炼经验与教训，形成知识资产，为未来项目的维护、扩展和新项目的部署提供权威参考。

---

## 目录
1.  [**核心经验与教训总结**](#1-核心经验与教训总结)
2.  [**详细问题复盘 (Case Study)**](#2-详细问题复盘-case-study)
    *   [2.1. 环境配置问题：GCP服务器初始化失败](#21-环境配置问题gcp服务器初始化失败)
    *   [2.2. 权限问题：Docker `permission denied`](#22-权限问题docker-permission-denied)
    *   [2.3. 容器启动问题：数据库服务 (`db`) 不健康](#23-容器启动问题数据库服务db不健康)
    *   [2.4. 应用内部错误：后端服务 (`backend`) 崩溃重启](#24-应用内部错误后端服务backend崩溃重启)
    *   [2.5. 网络访问问题：前端无法连接](#25-网络访问问题前端无法连接)
3.  [**最终架构与关键决策**](#3-最终架构与关键决策)

---

## 1. 核心经验与教训总结

*   **教训1：永远不要低估生产环境对资源的基础需求。**
    *   **摘要**: 1GB内存的`e2-micro`实例是导致一系列连锁问题的根源。低内存不仅影响应用本身，更会严重拖慢甚至破坏基础的系统服务（如`apt`、`sshd`）。
    *   **经验**: 对于包含数据库的现代化全栈应用，**2GB内存应被视为最低稳定运行的起点**。在项目规划初期，资源评估应优先保证稳定性，而非追求极致的零成本。

*   **教训2：权限问题必须在根源上解决，并理解其生效机制。**
    *   **摘要**: `docker`用户组权限的变更，必须在新登录的Shell会话中才能生效。已存在的`screen`会话会保持其创建时的“旧权限”，导致行为不一致。
    *   **经验**: 解决Linux权限问题，必须遵循“**授权 -> 重新登录 -> 验证**”的三步曲。对于`screen`等会话管理工具，必须杀死旧会话并创建新会话，才能继承新权限。当常规权限配置失效时，`sudo`是最后的、最可靠的保障。

*   **教训3：日志是通往真相的唯一路径。**
    *   **摘要**: 无论是GPG密钥错误、`db`不健康、`backend`崩溃，还是Nginx的`502`错误，最终的答案都清晰地写在对应服务（`apt`, `docker logs`, `串行端口`）的日志中。
    *   **经验**: 必须建立“**日志驱动**”的调试思维。遇到问题时，第一反应永远是“**去看日志**”。熟练使用`docker logs <container>`和`journalctl -u <service>`等命令，是云端运维的核心技能。

*   **教训4：必须为不同环境（开发/生产）提供差异化、隔离的配置。**
    *   **摘要**: 生产环境应移除代码热加载(`volumes`)，使用更健壮的进程管理器(`gunicorn`)，并针对低资源环境进行服务调优（如`my.cnf`）。
    *   **经验**: 使用独立的`docker-compose.prod.yml`文件是管理环境差异的最佳实践。必须清醒地认识到，在`Dockerfile`中，因为`.gitignore`的存在，**开发环境下的文件结构不等于生产镜像中的文件结构**（如此次`logs`目录的缺失）。

---

## 2. 详细问题复盘 (Case Study)

### 2.1. 环境配置问题：GCP服务器初始化失败

*   **错误表现**:
    1.  执行`apt-get update`或`apt-get install`时，报告GPG错误：`NO_PUBKEY 7EA0A9C3F273FCD8`，`repository ... is not signed`。
    2.  执行`apt`命令时，长时间卡在`Waiting for cache lock...`，或报告`dpkg was interrupted`。

*   **原因分析**:
    1.  **GPG错误**: GCP服务器的网络环境或基础镜像配置，导致无法通过标准流程正确下载并信任Docker官方的GPG公钥。
    2.  **Apt锁死**: 新创建的GCP虚拟机会在后台自动运行`apt upgrade`安全更新，这个进程会长时间占用`apt`锁，与我们手动的`apt`命令发生冲突。强行中断后会导致`dpkg`状态损坏。

*   **解决方法**:
    1.  **GPG问题**: 放弃通过`apt`源安装的方式，改用**Docker官方一键安装脚本** (`curl -fsSL https://get.docker.com | sh`)。该脚本绕过了系统的包管理签名验证，直接下载二进制文件进行安装，成功率最高。
    2.  **Apt锁问题**:
        *   **首选**: 耐心等待5-10分钟，让后台进程自动完成。
        *   **备选**: 打开新SSH窗口，使用`ps aux | grep apt`找到进程PID，用`sudo kill <PID>`终止进程，最后运行`sudo dpkg --configure -a`修复中断状态。

*   **总结**: 云平台初始环境并非100%纯净，其后台的自动化任务可能会与手动操作冲突。遇到顽固的环境配置问题时，应果断切换到更底层的、官方推荐的“通用”安装方案。

### 2.2. 权限问题：Docker `permission denied`

*   **错误表现**:
    1.  直接运行`docker ps`或`docker compose`命令，提示`permission denied while trying to connect to the Docker daemon socket`。
    2.  在`screen`会话中运行时出现权限错误，但在主终端中正常。

*   **原因分析**:
    1.  执行`docker`命令的当前用户（`xiaofeng_0209`）不在`docker`用户组中。
    2.  虽然执行了`sudo usermod -aG docker $USER`，但**没有退出并重新登录SSH**，导致权限变更未在当前会话生效。
    3.  `screen`会话**继承了其创建时刻的用户组权限**。如果在权限变更前创建了`screen`会话，那么即使主终端重登后获得了新权限，旧的`screen`会话内部依然是“旧身份”。

*   **解决方法**:
    1.  **标准流程**:
        *   执行`sudo usermod -aG docker $USER`。
        *   **必须 `exit` 退出并重新登录SSH**。
        *   在新会话中运行`groups`命令，确认输出包含`docker`。
    2.  **`screen`会话处理**:
        *   杀死所有旧的、以“旧身份”运行的`screen`会话 (`screen -X -S <会话名> quit`)。
        *   用拥有新权限的SSH会话，创建全新的`screen`会话。
    3.  **最终保障**: 如果以上步骤因某些系统原因依然无效，在所有`docker`和`docker compose`命令前添加`sudo`，以`root`权限执行。

*   **总结**: Linux的用户组权限管理有其特定的生效机制，必须严格遵守“授权后重新登录”的原则。要理解`screen`等工具的会话隔离特性。

### 2.3. 容器启动问题：数据库服务 (`db`) 不健康

*   **错误表现**:
    1.  `docker compose up`启动后，`backend`和`frontend`无法启动，最终报错`dependency failed to start: container athena_eye_db is unhealthy`。
    2.  `docker logs athena_eye_db`显示日志在初始化中途无错误地戛然而止。
    3.  `docker logs athena_eye_db`显示`unknown variable 'query_cache_type=0'`或`Found option without preceding group`错误。

*   **原因分析**:
    1.  **无声的死亡**: 服务器内存不足（1GB `e2-micro`），导致MySQL初始化时被系统OOM Killer（Out-of-Memory Killer）强制杀死。
    2.  **配置不兼容**: `my.cnf`中包含了已被MySQL 8.0移除的旧配置项（`query_cache_type`）。
    3.  **配置文件格式错误**: `my.cnf`文件开头存在注释或空行，导致严格的MySQL 8.0解析器无法识别文件格式。

*   **解决方法**:
    1.  **内存问题**:
        *   **治标**: 创建一个为低内存环境优化的`my.cnf`文件，关闭`performance_schema`并大幅降低`innodb_buffer_pool_size`。
        *   **治本**: 将服务器实例**升级到`e2-small`（2GB内存）**。
    2.  **配置兼容性**: 移除`my.cnf`中所有MySQL 8.0不再支持的配置项。
    3.  **格式问题**: 确保`.cnf`配置文件的**第一行必须是有效的组声明**（如`[mysqld]`），不能有任何前导注释或空行。

*   **总结**: 容器服务的健康，不仅取决于应用本身，更严重依赖于宿主机的资源。必须为数据库等内存密集型服务提供充足的资源，并确保配置文件与服务版本严格兼容。

### 2.4. 应用内部错误：后端服务 (`backend`) 崩溃重启

*   **错误表现**: 前端访问API时，Nginx日志报告`connect() failed (111: Connection refused)`或`502 Bad Gateway`。`docker logs backend`显示`FileNotFoundError: [Errno 2] No such file or directory: '/app/logs/athena_eye.log'`，并伴有`Worker failed to boot.`的Gunicorn错误。

*   **原因分析**:
    *   `backend/logs`目录被写入了`.gitignore`，因此没有被Git提交和克隆到服务器上。
    *   `Dockerfile`中的`COPY . .`指令，在构建镜像时，因为源目录（服务器上的`backend`目录）不存在`logs`文件夹，所以最终构建的生产镜像里也没有`/app/logs`这个目录。
    *   后端应用启动时，`logger.py`尝试在不存在的目录中创建日志文件，导致`FileNotFoundError`，使Gunicorn的worker进程启动失败并崩溃。

*   **解决方法**:
    *   在`backend/Dockerfile`中，`COPY . .`指令之后，明确添加一行`RUN mkdir logs`。这保证了无论源目录结构如何，最终的生产镜像中都必定存在一个空的`/app/logs`目录。

*   **总结**: 必须清醒地意识到开发环境和生产镜像之间的文件系统差异，特别是那些被`.gitignore`忽略的、但应用运行时又必需的空目录结构，必须在`Dockerfile`中显式创建。

### 2.5. 网络访问问题：前端无法连接

*   **错误表现**:
    1.  浏览器访问`http://<IP地址>`，提示`ERR_CONNECTION_TIMED_OUT`。
    2.  浏览器访问`http://<IP地址>`，提示`ERR_CONNECTION_CLOSED`，Nginx日志显示`"\x16\x03\x01\x01" 400`错误。

*   **原因分析**:
    1.  **超时**: GCP的VPC防火墙默认阻止了所有外部流量，没有创建允许`80`和`443`端口入站的规则。
    2.  **连接关闭**: 浏览器自动尝试使用`HTTPS`协议访问，而Nginx当时只配置了监听`80 (HTTP)`端口，无法处理`HTTPS`的加密握手请求，因此直接关闭了连接。

*   **解决方法**:
    1.  **防火墙**:
        *   **最佳实践**: 在创建GCP实例时，直接勾选“允许HTTP流量”和“允许HTTPS流量”。
        *   **手动配置**: 在VPC网络 -> 防火墙中，创建一条允许来自`0.0.0.0/0`对`tcp:80,443`端口入站流量的规则。
    2.  **协议问题**: 在浏览器地址栏中，**明确、完整地输入`http://`**，强制浏览器使用HTTP协议进行访问。

*   **总结**: 云端部署必须考虑“网络入口”问题。应用内部的端口监听（`ports`指令）和云平台外部的防火墙规则，必须协同工作，才能打通访问链路。

---

## 3. 最终架构与关键决策

经过这场部署实战，我们最终确定了`Athena Eye`项目的最佳实践架构：
*   **云主机**: GCP `e2-small` (2GB RAM) Ubuntu 22.04 LTS。
*   **部署技术**: Docker + Docker Compose。
*   **部署单元**: 使用`docker-compose.prod.yml`编排`db (MySQL)`, `backend (Gunicorn)`, `frontend (Nginx)`三个核心服务。
*   **运维模式**: 通过`screen`执行长时间部署，日常管理通过前端Web界面和`docker compose`命令进行。
*   **配置管理**: 通过`.env`和`my.cnf`等外部配置文件，实现了应用与配置的完全分离。

这份文档将作为项目的核心资产，指导我们未来的每一步。