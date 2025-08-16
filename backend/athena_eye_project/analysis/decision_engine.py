# athena_eye_project/analysis/decision_engine.py
from typing import Optional, Dict, Any

from athena_eye_project.utils.logger import logger
from athena_eye_project.config import settings

class DecisionEngineV3:
    """
    V3决策引擎：基于股价变动触发，融合价格、情绪信息，识别市场机会。
    所有参数均从config.settings加载。
    """
    
    def decide(
        self, 
        ticker: str,
        price_analysis: Optional[Dict[str, Any]], 
        sentiment_analysis: Optional[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        基于股价变动和情绪信息做出决策。

        Args:
            ticker (str): 股票代码。
            price_analysis (Optional[Dict]): 来自量价分析器的结果（现在主要关注价格变动）。
            sentiment_analysis (Optional[Dict]): 情绪分析结果。

        Returns:
            Optional[Dict[str, Any]]: 警报字典或None。
        """
        if not price_analysis:
            # 前提条件：没有显著股价变动，就没有警报。
            return None

        sentiment = sentiment_analysis or {"overall_sentiment": "Neutral", "sentiment_score": 5, "key_reasons": ["N/A"]}
        
        # 从分析结果和配置中提取关键变量
        price_change = price_analysis.get("price_change_percent", 0)
        
        is_positive_sentiment = (
            sentiment.get("overall_sentiment") == "Positive" and 
            sentiment.get("sentiment_score", 5) >= settings.SENTIMENT_SCORE_THRESHOLD
        )
        is_negative_sentiment = (
            sentiment.get("overall_sentiment") == "Negative" and 
            sentiment.get("sentiment_score", 5) < (10 - settings.SENTIMENT_SCORE_THRESHOLD)
        )
        is_price_up = price_change > 0
        is_price_down = price_change < 0

        alert_type = None
        alert_reason = ""

        # --- V3 决策矩阵 (基于股价变动触发) ---
        
        if is_price_up and is_positive_sentiment:
            alert_type = "股价上涨+积极情绪（强烈看涨）"
            alert_reason = f"股价显著上涨，伴随积极市场情绪。价格在K线周期内上涨 {price_change}%，情绪评分为 {sentiment.get('sentiment_score')}/10。"
        
        elif is_price_down and is_negative_sentiment:
            alert_type = "股价下跌+悲观情绪（强烈看跌）"
            alert_reason = f"股价显著下跌，伴随悲观市场情绪。价格在K线周期内下跌 {price_change}%，情绪评分为 {sentiment.get('sentiment_score')}/10。"
            
        elif is_price_up and is_negative_sentiment:
            alert_type = "股价上涨+悲观情绪（多头陷阱风险）"
            alert_reason = f"股价上涨但市场情绪悲观 ({sentiment.get('sentiment_score')}/10)。可能存在多头陷阱风险，建议谨慎。"
            
        elif is_price_down and is_positive_sentiment:
            alert_type = "股价下跌+积极情绪（潜在抄底机会）"
            alert_reason = f"股价下跌但市场情绪积极 ({sentiment.get('sentiment_score')}/10)。可能是短期调整，存在潜在抄底机会。"
            
        elif is_price_up:
            alert_type = "股价显著上涨"
            alert_reason = f"股价在K线周期内显著上涨 {price_change}%，市场情绪中性。"
            
        elif is_price_down:
            alert_type = "股价显著下跌"
            alert_reason = f"股价在K线周期内显著下跌 {price_change}%，市场情绪中性。"

        else:
            logger.info(f"为 {ticker} 检测到股价变动，但信号不明确({price_change=}, {sentiment.get('overall_sentiment')})，暂不触发警报。")
            return None

        # 组装警报
        alert_details = {
            "ticker": ticker,
            "alert_type": alert_type,
            "reason": alert_reason,
            "price_details": {
                "open": price_analysis.get('latest_open'),
                "close": price_analysis.get('latest_close'),
                "change_percent": price_change
            },
            "volume_details": {
                "latest": price_analysis.get('latest_volume'),
                "average": price_analysis.get('average_volume'),
                "multiplier": price_analysis.get('volume_multiplier')
            },
            "sentiment_details": sentiment
        }
        
        logger.info(f"V3决策引擎为 {ticker} 生成警报: {alert_type}")
        return alert_details

# 创建一个V3引擎的单例
decision_engine = DecisionEngineV3()