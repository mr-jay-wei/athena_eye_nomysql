# athena_eye_project/analysis/volume_price.py
import pandas as pd
from typing import Optional, Dict, Any

from athena_eye_project.utils.logger import logger
from athena_eye_project.config import settings

class VolumePriceAnalyzer:
    """
    负责分析量价关系，识别市场异动。
    """
    
    def analyze_latest_candle(self, df: pd.DataFrame) -> Optional[Dict[str, Any]]:
        """
        分析最新的K线，检测成交量异动和价格变化。
        所有参数均从config.settings加载。
        
        Args:
            df (pd.DataFrame): 包含'Volume', 'Close', 'Open'列的行情数据。
        
        Returns:
            Optional[Dict[str, Any]]: 如果检测到巨量，返回分析结果，否则返回None。
        """
        # 从 settings 加载配置参数
        lookback_period = settings.VOLUME_LOOKBACK_PERIOD
        volume_threshold_multiplier = settings.VOLUME_SPIKE_MULTIPLIER

        if df is None or len(df) < lookback_period + 1:
            logger.warning(f"数据点({len(df) if df is not None else 0})不足以进行回看期为{lookback_period}的量价分析。")
            return None

        historical_df = df.iloc[-(lookback_period + 1):-1]
        latest_candle = df.iloc[-1]
        
        average_volume = historical_df['Volume'].mean()
        latest_volume = latest_candle['Volume']
        
        # 避免除以零的错误
        if average_volume == 0:
            logger.warning("历史平均成交量为0，无法计算放大倍数。")
            return None

        # 核心判断：是否为巨量
        if latest_volume > average_volume * volume_threshold_multiplier:
            actual_multiplier = round(latest_volume / average_volume, 2)
            
            # 计算当前K线的价格变化百分比
            price_change_percent = 0
            if latest_candle['Open'] > 0:
                price_change_percent = round(
                    ((latest_candle['Close'] - latest_candle['Open']) / latest_candle['Open']) * 100, 
                    2
                )
            
            result = {
                "event": "Volume Spike Detected",
                "latest_open": latest_candle['Open'],
                "latest_close": latest_candle['Close'],
                "latest_volume": int(latest_volume),
                "average_volume": int(average_volume),
                "volume_multiplier": actual_multiplier,
                "price_change_percent": price_change_percent
            }
            logger.info(
                f"检测到巨量: 成交量放大 {actual_multiplier} 倍 (阈值 {volume_threshold_multiplier}x), "
                f"价格变化 {price_change_percent}%."
            )
            return result
            
        return None

# 创建单例
volume_price_analyzer = VolumePriceAnalyzer()