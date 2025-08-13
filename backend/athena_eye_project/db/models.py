# athena_eye_project/db/models.py
from sqlalchemy import (Column, Integer, String, Float, DateTime,
                        Text, JSON, func, Boolean)
# 从我们刚刚创建的database.py中导入Base基类
from .database import Base

class Alert(Base):
    """
    定义 'alerts' 数据表的ORM (Object-Relational Mapping) 模型。
    这个Python类会被SQLAlchemy映射为MySQL中的一张表。
    """
    # __tablename__ 告诉SQLAlchemy这张表在数据库中的名字
    __tablename__ = "alerts"

    # --- 核心字段 ---
    # id: 主键，自增，带索引以加速查询
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # archive_timestamp_utc: 存档时间戳，数据库会自动填入当前时间
    archive_timestamp_utc = Column(DateTime, server_default=func.now())
    # ticker: 股票代码，非空，带索引
    ticker = Column(String(20), nullable=False, index=True)
    # alert_type: 警报类型，非空
    alert_type = Column(String(100), nullable=False)
    # reason: 警报原因，长文本
    reason = Column(Text, nullable=False)

    # --- 价格详情 (允许为空，以防数据缺失) ---
    price_open = Column(Float, nullable=True)
    price_close = Column(Float, nullable=True)
    price_change_percent = Column(Float, nullable=True)

    # --- 成交量详情 (允许为空) ---
    volume_latest = Column(Integer, nullable=True)
    volume_average = Column(Integer, nullable=True)
    volume_multiplier = Column(Float, nullable=True)

    # --- 情绪详情 (允许为空) ---
    sentiment_overall = Column(String(50), nullable=True)
    sentiment_score = Column(Integer, nullable=True)
    # sentiment_key_reasons: 使用JSON类型存储字符串列表，非常灵活
    sentiment_key_reasons = Column(JSON, nullable=True)
    sentiment_confidence = Column(String(50), nullable=True)

    # --- 系统与原始数据快照 ---
    # trigger_conditions: 使用JSON类型存储触发时的参数字典
    trigger_conditions = Column(JSON, nullable=True)
    # raw_news_data: 使用JSON类型存储原始新闻数据列表
    raw_news_data = Column(JSON, nullable=True)

    def __repr__(self):
        """定义一个方便调试的字符串表示形式"""
        return f"<Alert(id={self.id}, ticker='{self.ticker}', type='{self.alert_type}')>"


class StockConfig(Base):
    """
    定义 'stock_configs' 数据表的ORM模型。
    用于存储每只股票的监控配置和策略参数。
    """
    __tablename__ = "stock_configs"

    # --- 核心字段 ---
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ticker = Column(String(20), nullable=False, unique=True, index=True)  # 股票代码，唯一
    is_active = Column(Boolean, default=True, nullable=False)  # 是否启用监控
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # --- 策略参数 (可选，为空时使用全局默认值) ---
    volume_spike_multiplier = Column(Float, nullable=True)  # 成交量放大倍数阈值
    price_significant_change_percent = Column(Float, nullable=True)  # 显著价格变化百分比
    sentiment_score_threshold = Column(Integer, nullable=True)  # 情绪评分阈值
    
    # --- 备注信息 ---
    notes = Column(Text, nullable=True)  # 用户备注

    def __repr__(self):
        return f"<StockConfig(ticker='{self.ticker}', active={self.is_active})>"