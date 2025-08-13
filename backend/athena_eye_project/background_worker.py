# backend/athena_eye_project/background_worker.py

import schedule
import time
import threading

# 路径修复 (同样需要)
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from athena_eye_project.main import run_monitor_cycle # 从我们旧的main脚本导入核心工作流
from athena_eye_project.utils.logger import logger
from athena_eye_project.config import settings

class SystemState:
    """一个简单的单例类，用于管理整个应用的共享状态。"""
    def __init__(self):
        self.is_running: bool = False
        self.stop_event = threading.Event()

# 创建一个全局的状态实例
system_state = SystemState()

def monitoring_task():
    """这是将在后台线程中运行的主任务。"""
    logger.info("后台监控线程已启动。")
    system_state.is_running = True
    
    # 立即执行一次
    try:
        run_monitor_cycle()
    except Exception as e:
        logger.error(f"首次运行监控周期时出错: {e}")

    # 设置定时任务
    schedule.every(settings.MONITOR_INTERVAL_MINUTES).minutes.do(run_monitor_cycle)
    
    # 这是新的、可被控制的循环
    while not system_state.stop_event.is_set():
        schedule.run_pending()
        time.sleep(1)
        
    # 循环结束后，清理状态
    system_state.is_running = False
    schedule.clear()
    logger.info("后台监控线程已优雅地停止。")