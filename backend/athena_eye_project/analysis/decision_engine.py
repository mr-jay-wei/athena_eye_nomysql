# athena_eye_project/analysis/decision_engine.py
from typing import Optional, Dict, Any

from athena_eye_project.utils.logger import logger
from athena_eye_project.config import settings

class DecisionEngineV2:
    """
    V2决策引擎：融合量、价、情绪三维信息，识别市场博弈。
    所有参数均从config.settings加载。
    """
    
    def decide(
        self, 
        ticker: str,
        volume_analysis: Optional[Dict[str, Any]], 
        sentiment_analysis: Optional[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        基于三维信息做出决策。

        Args:
            ticker (str): 股票代码。
            volume_analysis (Optional[Dict]): 来自V2量价分析器的结果。
            sentiment_analysis (Optional[Dict]): 情绪分析结果。

        Returns:
            Optional[Dict[str, Any]]: 警报字典或None。
        """
        if not volume_analysis:
            # 前提条件：没有成交量异动，就没有故事。
            return None

        sentiment = sentiment_analysis or {"overall_sentiment": "Neutral", "sentiment_score": 5, "key_reasons": ["N/A"]}
        
        # 从分析结果和配置中提取关键变量
        price_change = volume_analysis.get("price_change_percent", 0)
        
        is_positive_sentiment = (
            sentiment.get("overall_sentiment") == "Positive" and 
            sentiment.get("sentiment_score", 5) >= settings.SENTIMENT_SCORE_THRESHOLD
        )
        is_negative_sentiment = (
            sentiment.get("overall_sentiment") == "Negative" and 
            sentiment.get("sentiment_score", 5) < (10 - settings.SENTIMENT_SCORE_THRESHOLD)
        )
        is_price_up = price_change > settings.PRICE_SIGNIFICANT_CHANGE_PERCENT
        is_price_down = price_change < -settings.PRICE_SIGNIFICANT_CHANGE_PERCENT

        alert_type = None
        alert_reason = ""

        # --- V2 决策矩阵 (Decision Matrix) ---
        
        if is_price_up and is_positive_sentiment:
            alert_type = "主力入场（强烈看涨）"
            alert_reason = f"量价齐升，伴随积极市场情绪。价格在K线周期内上涨 {price_change}%，情绪评分为 {sentiment.get('sentiment_score')}/10。"
        
        elif is_price_down and is_negative_sentiment:
            alert_type = "主力出货（强烈看跌）"
            alert_reason = f"放量下跌，伴随悲观市场情绪。价格在K线周期内下跌 {price_change}%，情绪评分为 {sentiment.get('sentiment_score')}/10。"
            
        elif is_price_up and is_negative_sentiment:
            alert_type = "多头陷阱警报（高风险）"
            alert_reason = f"价格上涨但市场情绪悲观 ({sentiment.get('sentiment_score')}/10)。可能是主力利用拉高诱多，掩护其真实卖出意图。"
            
        elif is_price_down and is_positive_sentiment:
            alert_type = "空头陷阱警报（潜在机会）"
            alert_reason = f"价格下跌但市场情绪积极 ({sentiment.get('sentiment_score')}/10)。可能是主力利用恐慌打压价格，以吸取廉价筹码。"

        else:
            # 只要走到了这里，就说明有量价异动，但组合不明确
            # 我们不再返回None，而是创建一个通用的警报
            logger.info(f"为 {ticker} 检测到巨量，但价格/情绪组合信号不明确，生成中性观察警报。")
            alert_type = "量价异动（中性观察）"
            alert_reason = (
                f"检测到成交量显著放大，但价格变动 ({price_change}%) 或 "
                f"市场情绪 ({sentiment.get('overall_sentiment')}, {sentiment.get('sentiment_score')}/10) "
                f"未形成明确的多空信号。建议密切关注。"
            )

        # 组装警报
        alert_details = {
            "ticker": ticker,
            "alert_type": alert_type,
            "reason": alert_reason,
            "price_details": {
                "open": volume_analysis.get('latest_open'),
                "close": volume_analysis.get('latest_close'),
                "change_percent": price_change
            },
            "volume_details": {
                "latest": volume_analysis.get('latest_volume'),
                "average": volume_analysis.get('average_volume'),
                "multiplier": volume_analysis.get('volume_multiplier')
            },
            "sentiment_details": sentiment
        }
        
        logger.info(f"V2决策引擎为 {ticker} 生成警报: {alert_type}")
        return alert_details

# 创建一个V2引擎的单例
decision_engine = DecisionEngineV2()