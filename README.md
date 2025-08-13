# Athena Eye V3 - 智能美股异动监控系统 (全栈容器化版)

**Athena Eye** 是一个基于Docker容器化部署的全栈、高度可配置的智能监控系统。它旨在实时分析美股市场的**量、价、情绪**三维信息，捕捉潜在的机构投资者活动，并通过邮件向用户发送即时警报。

该项目已完成从本地开发到云端生产环境的完整部署，融合了专业的软件工程实践、量化交易策略和大型语言模型（LLM）的认知能力，形成了一套稳定、可靠、可扩展的自动化交易信号解决方案。

---

## 核心架构
```
athena_eye/
├── backend
│   ├── archive
│   │   └── 2025-08-04
│   │       └── 20250804_084829_PERFECTCO_主力入场（强烈看涨）.json
│   ├── athena_eye_project
│   │   ├── analysis
│   │   │   ├── __init__.py
│   │   │   ├── decision_engine.py
│   │   │   ├── sentiment.py
│   │   │   └── volume_price.py
│   │   ├── archiving
│   │   │   └── archiver.py
│   │   ├── config
│   │   │   ├── __init__.py
│   │   │   ├── settings.py
│   │   │   ├── stock_manager.py
│   │   │   └── stocks.json
│   │   ├── data_ingestion
│   │   │   ├── __init__.py
│   │   │   └── fetcher.py
│   │   ├── db
│   │   │   ├── database.py
│   │   │   └── models.py
│   │   ├── notifications
│   │   │   ├── __init__.py
│   │   │   └── email_sender.py
│   │   ├── utils
│   │   │   ├── __init__.py
│   │   │   └── logger.py
│   │   ├── __init__.py
│   │   ├── background_worker.py
│   │   ├── main.py
│   │   └── main_api.py
│   ├── logs
│   ├── tests
│   ├── .python-version
│   ├── athena_eye.db
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend
│   ├── public
│   ├── src
│   │   ├── assets
│   │   │   ├── base.css
│   │   │   └── main.css
│   │   ├── components
│   │   ├── router
│   │   │   └── index.js
│   │   ├── views
│   │   │   ├── ArchiveView.vue
│   │   │   ├── ConfigView.vue
│   │   │   └── DashboardView.vue
│   │   ├── App.vue
│   │   └── main.js
│   ├── .editorconfig
│   ├── .gitattributes
│   ├── .gitignore
│   ├── .prettierrc.json
│   ├── Dockerfile
│   ├── eslint.config.js
│   ├── index.html
│   ├── jsconfig.json
│   ├── nginx.conf
│   ├── package.json
│   ├── README.md
│   └── vite.config.js
├── test
├── .gitignore
├── docker-compose.prod.yml
├── docker-compose.yml
├── GCP_DEPLOY_MANUAL.md
├── init.sql
├── LINUX_OPERATOR_MANUAL.md
├── my.cnf
└── README.md
```

系统采用现代化的全栈容器化架构，通过`Docker Compose`进行编排：

*   **前端 (Frontend)**:
    *   **技术栈**: Vue 3 + Vite
    *   **部署**: 通过多阶段`Dockerfile`构建，最终部署在一个超轻量级的`Nginx`镜像中。
    *   **职责**: 提供用户交互界面，包括系统状态监控、参数在线配置、历史警报查阅。

*   **反向代理 (Reverse Proxy)**:
    *   **技术**: Nginx
    *   **职责**: 作为系统的统一入口，监听80端口，将静态文件请求（如`/`）指向前端应用，并将所有API请求（如`/api/*`）无缝反向代理到后端服务。

*   **后端 (Backend)**:
    *   **技术栈**: Python 3.12, FastAPI, Gunicorn, SQLAlchemy
    *   **部署**: 部署在一个基于`python-slim`的轻量级Docker镜像中，由Gunicorn管理多个Uvicorn worker进程，保证高并发性能。
    *   **职责**: 执行核心业务逻辑，包括定时数据采集、三维分析（量、价、情绪）、AI决策、邮件通知，并通过API与前端和数据库交互。

*   **数据库 (Database)**:
    *   **技术**: MySQL 8.0
    *   **部署**: 运行在官方的Docker镜像中，数据通过Docker Volume进行持久化存储。
    *   **职责**: 持久化存储所有触发的警报记录，为历史回顾和未来数据分析提供支持。

---

## 核心特性

*   **一键式部署**: 在任何安装了Docker的Linux服务器上，通过一条`docker compose`命令即可启动整个全栈应用。
*   **生产级服务**: 后端使用`Gunicorn`进行进程管理，数据库采用低内存优化配置，确保在云端服务器上7x24小时稳定运行。
*   **Web控制台**: 提供功能完善的前端界面，实现对整个系统的**远程可视化管理**，包括启停、参数调整和历史查阅。
*   **数据持久化**: 所有警报记录都存储在专业的MySQL数据库中，安全、可靠且易于查询分析。
*   **三维分析引擎**: 独创性地结合**成交量异动**、**K线价格变化**和**AI新闻市场情绪**，识别复杂的市场博弈。

---

## 云端部署 (Google Cloud Platform)

本项目已在GCP上成功部署并稳定运行。推荐的部署流程和服务器配置如下。

### 1. 服务器推荐配置
*   **实例类型**: **`e2-small` (2 vCPU, 2 GB 内存) 或更高**。
    *   **重要教训**: `e2-micro` (1 GB 内存) **不足以**稳定运行本项目的完整技术栈，会导致MySQL或SSH服务因内存不足而随机崩溃。
*   **操作系统**: **Ubuntu 22.04 LTS** 或 Debian 12。
*   **防火墙**: 务必开放`TCP`协议的`80`, `443`, `22`端口。

### 2. 部署流程
详细的、经过实战检验的部署步骤，请严格参考项目中的权威手册：
**`GCP_DEPLOY_MANUAL.md`**

该手册涵盖了从服务器初始化、Docker安装，到项目克隆、配置、一键启动、日常运维和故障排查的所有环节。

---

## 项目总结：关键经验与教训

1.  **资源规划是基石**: 生产环境的稳定性，始于充足的计算资源。低估内存需求是导致云端部署失败的最主要原因。
2.  **环境隔离是保障**: 本地开发环境与云端生产环境存在巨大差异。Docker是解决“在我电脑上明明是好的”这一经典问题的最有效工具。
3.  **日志是真相的唯一来源**: 无论是应用日志(`docker logs`)还是系统日志(`串行端口`)，都是在遇到问题时定位根源的最终依据。
4.  **细节决定成败**: 从`Dockerfile`中的一个`mkdir`命令，到`my.cnf`中一行业首的注释，再到`screen`会话的权限继承机制，都可能成为影响整个系统成败的关键。
