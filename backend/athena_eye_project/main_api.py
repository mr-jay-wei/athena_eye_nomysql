# backend/athena_eye_project/main_api.py (已升级至V5 - 数据库集成)
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, Query
from typing import List, Optional
from pydantic import BaseModel, Field
from dotenv import find_dotenv, set_key
from sqlalchemy.orm import Session
import json

# 路径修复
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# --- 核心数据库导入 ---
from athena_eye_project.db.database import init_db, get_db
from athena_eye_project.db import models as db_models

from athena_eye_project.config import settings
from athena_eye_project.utils.logger import logger
from athena_eye_project.background_worker import system_state, monitoring_task

# --- FastAPI 生命周期管理 ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时执行
    logger.info("FastAPI 应用启动...")
    try:
        settings.validate_config()
        logger.info("配置验证通过。")
        init_db() # <-- 在此自动创建数据库表！
    except Exception as e:
        logger.critical(f"应用启动失败，关键配置或数据库初始化错误: {e}")
        # 在关键错误时阻止应用启动是合理的
        raise
    yield
    # 应用关闭时执行
    logger.info("FastAPI 应用关闭...")

# FastAPI应用实例
app = FastAPI(
    title="Athena Eye API",
    description="用于控制和监控Athena Eye系统的API。",
    version="5.0.0",
    lifespan=lifespan # <-- 注册生命周期函数
)

# --- Pydantic 模型 ---
class TunableConfig(BaseModel):
    # ... (这部分模型不变) ...
    MONITOR_INTERVAL_MINUTES: int = Field(..., gt=0, description="监控频率（分钟）")
    PRICE_DATA_INTERVAL: str = Field(..., description="K线周期 (e.g., '15min')")
    VOLUME_LOOKBACK_PERIOD: int = Field(..., gt=0, description="成交量回看期")
    VOLUME_SPIKE_MULTIPLIER: float = Field(..., gt=0, description="成交量放大倍数阈值")
    PRICE_SIGNIFICANT_CHANGE_PERCENT: float = Field(..., ge=0, description="显著价格变化百分比")
    SENTIMENT_SCORE_THRESHOLD: int = Field(..., ge=1, le=9, description="情绪评分阈值")
    NEWS_FETCH_COUNT: int = Field(..., gt=0, le=100, description="新闻获取数量")

# --- 新增：用于API响应的Pydantic模型 ---
class AlertResponse(BaseModel):
    id: int
    archive_timestamp_utc: str # FastAPI 会自动处理datetime到str的转换
    ticker: str
    alert_type: str
    reason: str
    price_open: Optional[float]
    price_close: Optional[float]
    price_change_percent: Optional[float]
    volume_latest: Optional[int]
    volume_average: Optional[int]
    volume_multiplier: Optional[float]
    sentiment_overall: Optional[str]
    sentiment_score: Optional[int]
    sentiment_key_reasons: Optional[list]
    sentiment_confidence: Optional[str]
    trigger_conditions: Optional[dict]
    raw_news_data: Optional[list]

    class Config:
        # Pydantic V2 使用 from_attributes = True
        from_attributes = True

# --- 股票配置相关的Pydantic模型 ---
class StockItem(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=20, description="股票代码")
    is_active: bool = Field(True, description="是否启用监控")
    notes: Optional[str] = Field(None, description="用户备注")

class StockListResponse(BaseModel):
    stocks: List[StockItem]

# --- 导入股票管理模块 ---
from athena_eye_project.config.stock_manager import (
    load_stocks_config, 
    save_stocks_config, 
    get_active_watchlist
)

# --- API Endpoints ---
background_thread = None
@app.get("/")
def read_root(): return {"message": "Welcome to the Athena Eye API v5!"}

# --- 控制API (不变) ---
# ... /api/control/* 的代码完全不变 ...
@app.get("/api/control/status", tags=["Control"])
def get_status() -> dict:
    """获取后台监控任务的当前状态。"""
    return {
        "is_running": system_state.is_running,
        "monitoring_watchlist": get_active_watchlist()
    }

@app.post("/api/control/start", status_code=202, tags=["Control"])
def start_monitoring() -> dict:
    """启动后台监控任务。"""
    global background_thread
    if system_state.is_running:
        raise HTTPException(status_code=400, detail="监控任务已经在运行中。")
    system_state.stop_event.clear()
    background_thread = threading.Thread(target=monitoring_task, daemon=True)
    background_thread.start()
    return {"message": "监控任务已启动。"}

@app.post("/api/control/stop", status_code=202, tags=["Control"])
def stop_monitoring() -> dict:
    """停止后台监控任务。"""
    if not system_state.is_running:
        raise HTTPException(status_code=400, detail="监控任务当前未运行。")
    system_state.stop_event.set()
    return {"message": "监控任务正在停止..."}


# --- 配置API (不变) ---
# ... /api/config 的代码完全不变 ...
@app.get("/api/config", response_model=TunableConfig, tags=["Configuration"])
def get_config() -> TunableConfig:
    """获取当前所有可调参数的配置。"""
    return TunableConfig(
        MONITOR_INTERVAL_MINUTES=settings.MONITOR_INTERVAL_MINUTES,
        PRICE_DATA_INTERVAL=settings.PRICE_DATA_INTERVAL,
        VOLUME_LOOKBACK_PERIOD=settings.VOLUME_LOOKBACK_PERIOD,
        VOLUME_SPIKE_MULTIPLIER=settings.VOLUME_SPIKE_MULTIPLIER,
        PRICE_SIGNIFICANT_CHANGE_PERCENT=settings.PRICE_SIGNIFICANT_CHANGE_PERCENT,
        SENTIMENT_SCORE_THRESHOLD=settings.SENTIMENT_SCORE_THRESHOLD,
        NEWS_FETCH_COUNT=settings.NEWS_FETCH_COUNT
    )

@app.post("/api/config", response_model=TunableConfig, tags=["Configuration"])
def update_config(config: TunableConfig) -> TunableConfig:
    """更新.env文件中的可调参数。"""
    logger.info(f"更新系统配置请求: {config.model_dump_json()}")
    try:
        dotenv_path = find_dotenv()
        if not dotenv_path:
            raise HTTPException(status_code=500, detail=".env file not found.")
        for key, value in config.model_dump().items():
            set_key(dotenv_path, key, str(value))
        logger.info(".env文件更新成功。")
        return config
    except Exception as e:
        logger.error(f"更新.env文件时出错: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update config file: {e}")


# --- 存档API (已重构为数据库) ---
@app.get("/api/archive", response_model=List[AlertResponse], tags=["Archive"])
def list_archived_alerts(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="跳过前N条记录"),
    limit: int = Query(100, ge=1, le=500, description="每页最多返回的记录数")
    ) -> List[AlertResponse]:
    """
    获取所有已存档警报的列表，按时间倒序排列，支持分页。
    - /api/archive -> 获取最新的100条
    - /api/archive?skip=100&limit=50 -> 获取第101到150条
    """
    logger.info(f"获取存档列表请求: skip={skip}, limit={limit}")
    try:
        alerts = db.query(db_models.Alert).order_by(db_models.Alert.id.desc()).offset(skip).limit(limit).all()
        # 这里不需要自己解析URL，FastAPI已经帮我们做好了！
        # SQLAlchemy的 .offset(skip) 和 .limit(limit) 正是用于SQL分页查询的。
        return alerts
    except Exception as e:
        logger.error(f"查询存档列表时出错: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve archive list from database.")

@app.get("/api/archive/{alert_id}", response_model=AlertResponse, tags=["Archive"])
def get_archived_alert_detail(alert_id: int, db: Session = Depends(get_db)) -> AlertResponse:
    """根据ID获取指定警报存档的详细内容。"""
    logger.info(f"获取存档详情请求, ID: {alert_id}")
    try:
        alert = db.query(db_models.Alert).filter(db_models.Alert.id == alert_id).first()
        if alert is None:
            raise HTTPException(status_code=404, detail="Alert not found in database.")
        return alert
    except HTTPException:
        raise # 重新抛出已知的HTTP异常
    except Exception as e:
        logger.error(f"查询存档详情(ID: {alert_id})时出错: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve archive detail from database.")

# --- 股票列表管理API ---
@app.get("/api/stocks", response_model=StockListResponse, tags=["Stocks"])
def get_stocks() -> StockListResponse:
    """获取股票监控列表"""
    logger.info("获取股票列表请求")
    config = load_stocks_config()
    return StockListResponse(stocks=config.get("stocks", []))

@app.post("/api/stocks", response_model=StockListResponse, tags=["Stocks"])
def update_stocks(stock_list: StockListResponse) -> StockListResponse:
    """更新股票监控列表"""
    logger.info(f"更新股票列表请求: {len(stock_list.stocks)} 只股票")
    
    # 验证股票代码格式
    for stock in stock_list.stocks:
        if not stock.ticker.strip():
            raise HTTPException(status_code=400, detail="股票代码不能为空")
        stock.ticker = stock.ticker.upper().strip()  # 统一转为大写并去除空格
    
    # 检查重复的股票代码
    tickers = [stock.ticker for stock in stock_list.stocks]
    if len(tickers) != len(set(tickers)):
        raise HTTPException(status_code=400, detail="股票列表中存在重复的代码")
    
    # 保存配置
    config_data = {"stocks": [stock.dict() for stock in stock_list.stocks]}
    save_stocks_config(config_data)
    
    return stock_list

@app.post("/api/stocks/add", response_model=StockListResponse, tags=["Stocks"])
def add_stock(stock: StockItem) -> StockListResponse:
    """添加单只股票到监控列表"""
    logger.info(f"添加股票请求: {stock.ticker}")
    
    stock.ticker = stock.ticker.upper().strip()
    if not stock.ticker:
        raise HTTPException(status_code=400, detail="股票代码不能为空")
    
    config = load_stocks_config()
    stocks = config.get("stocks", [])
    
    # 检查是否已存在
    for existing_stock in stocks:
        if existing_stock["ticker"] == stock.ticker:
            raise HTTPException(status_code=400, detail=f"股票 {stock.ticker} 已存在于监控列表中")
    
    # 添加新股票
    stocks.append(stock.dict())
    config_data = {"stocks": stocks}
    save_stocks_config(config_data)
    
    return StockListResponse(stocks=stocks)

@app.delete("/api/stocks/{ticker}", response_model=StockListResponse, tags=["Stocks"])
def remove_stock(ticker: str) -> StockListResponse:
    """从监控列表中移除指定股票"""
    logger.info(f"移除股票请求: {ticker}")
    
    ticker = ticker.upper().strip()
    config = load_stocks_config()
    stocks = config.get("stocks", [])
    
    # 查找并移除股票
    original_count = len(stocks)
    stocks = [stock for stock in stocks if stock["ticker"] != ticker]
    
    if len(stocks) == original_count:
        raise HTTPException(status_code=404, detail=f"股票 {ticker} 不存在于监控列表中")
    
    config_data = {"stocks": stocks}
    save_stocks_config(config_data)
    
    return StockListResponse(stocks=stocks)

@app.put("/api/stocks/{ticker}", response_model=StockItem, tags=["Stocks"])
def update_stock(ticker: str, stock_update: StockItem) -> StockItem:
    """更新指定股票的配置"""
    logger.info(f"更新股票配置请求: {ticker}")
    
    ticker = ticker.upper().strip()
    stock_update.ticker = stock_update.ticker.upper().strip()
    
    config = load_stocks_config()
    stocks = config.get("stocks", [])
    
    # 查找并更新股票
    stock_found = False
    for i, stock in enumerate(stocks):
        if stock["ticker"] == ticker:
            stocks[i] = stock_update.dict()
            stock_found = True
            break
    
    if not stock_found:
        raise HTTPException(status_code=404, detail=f"股票 {ticker} 不存在于监控列表中")
    
    config_data = {"stocks": stocks}
    save_stocks_config(config_data)
    
    return stock_update

# --- 主程序入口 (不变) ---
if __name__ == "__main__":
    import uvicorn
    # uvicorn 会自动识别并运行 lifespan 函数
    uvicorn.run("main_api:app", host="0.0.0.0", port=8000, reload=True)