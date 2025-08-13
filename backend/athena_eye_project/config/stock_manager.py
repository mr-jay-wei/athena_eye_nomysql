# athena_eye_project/config/stock_manager.py
import json
import os
from typing import List, Dict, Any
from athena_eye_project.utils.logger import logger

def get_stocks_config_path():
    """获取股票配置文件路径"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "stocks.json")

def load_stocks_config() -> Dict[str, Any]:
    """从JSON文件加载股票配置"""
    config_path = get_stocks_config_path()
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"股票配置文件不存在: {config_path}，返回空列表")
        return {"stocks": []}
    except json.JSONDecodeError as e:
        logger.error(f"股票配置文件格式错误: {e}")
        return {"stocks": []}

def get_active_watchlist() -> List[str]:
    """获取当前启用的股票列表"""
    config = load_stocks_config()
    active_stocks = [
        stock["ticker"] 
        for stock in config.get("stocks", []) 
        if stock.get("is_active", True)
    ]
    logger.info(f"从配置文件加载到 {len(active_stocks)} 只活跃股票: {active_stocks}")
    return active_stocks

def save_stocks_config(config_data: Dict[str, Any]):
    """保存股票配置到JSON文件"""
    config_path = get_stocks_config_path()
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        logger.info(f"股票配置已保存到: {config_path}")
    except Exception as e:
        logger.error(f"保存股票配置文件时出错: {e}")
        raise