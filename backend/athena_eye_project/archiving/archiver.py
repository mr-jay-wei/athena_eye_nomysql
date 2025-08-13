# athena_eye_project/archiving/archiver.py (已升级至数据库)
from typing import Dict, Any
from sqlalchemy.orm import Session

from athena_eye_project.utils.logger import logger
from athena_eye_project.config import settings
# --- 核心导入 ---
from athena_eye_project.db.models import Alert # 导入我们的数据库模型
from athena_eye_project.db.database import SessionLocal # 导入数据库会话工厂

class DecisionArchiver:
    """
    负责将触发警报的决策快照存档到数据库。
    """
    def _get_current_params(self) -> Dict[str, Any]:
        """获取当前.env文件中的所有可调参数，用于记录。"""
        return {
            "MONITOR_INTERVAL_MINUTES": settings.MONITOR_INTERVAL_MINUTES,
            "PRICE_DATA_INTERVAL": settings.PRICE_DATA_INTERVAL,
            "VOLUME_LOOKBACK_PERIOD": settings.VOLUME_LOOKBACK_PERIOD,
            "VOLUME_SPIKE_MULTIPLIER": settings.VOLUME_SPIKE_MULTIPLIER,
            "PRICE_SIGNIFICANT_CHANGE_PERCENT": settings.PRICE_SIGNIFICANT_CHANGE_PERCENT,
            "SENTIMENT_SCORE_THRESHOLD": settings.SENTIMENT_SCORE_THRESHOLD,
            "NEWS_FETCH_COUNT": settings.NEWS_FETCH_COUNT
        }

    def archive_decision_to_db(
        self,
        alert_details: Dict[str, Any],
        raw_news_data: list
    ):
        """
        将一次完整的决策快照保存到数据库中。

        Args:
            alert_details (Dict[str, Any]): 从决策引擎生成的警报详情。
            raw_news_data (list): 原始的新闻数据列表。
        """
        db: Session = SessionLocal() # 创建一个新的数据库会话
        try:
            # --- 数据扁平化映射 ---
            # 将嵌套的字典数据，映射到我们定义的扁平化的Alert模型字段上
            price_details = alert_details.get('price_details', {})
            volume_details = alert_details.get('volume_details', {})
            sentiment_details = alert_details.get('sentiment_details', {})

            new_alert_record = Alert(
                ticker=alert_details.get('ticker'),
                alert_type=alert_details.get('alert_type'),
                reason=alert_details.get('reason'),

                price_open=price_details.get('open'),
                price_close=price_details.get('close'),
                price_change_percent=price_details.get('change_percent'),

                volume_latest=volume_details.get('latest'),
                volume_average=volume_details.get('average'),
                volume_multiplier=volume_details.get('multiplier'),

                sentiment_overall=sentiment_details.get('overall_sentiment'),
                sentiment_score=sentiment_details.get('sentiment_score'),
                sentiment_key_reasons=sentiment_details.get('key_reasons'),
                sentiment_confidence=sentiment_details.get('confidence_level'),

                trigger_conditions=self._get_current_params(),
                raw_news_data=raw_news_data
            )

            # --- 数据库操作 ---
            db.add(new_alert_record) # 将新记录添加到会话中
            db.commit()              # 提交事务，将数据写入数据库
            db.refresh(new_alert_record) # 刷新记录，以获取数据库生成的数据（如ID和时间戳）

            logger.info(f"决策快照已成功存档至数据库，记录ID: {new_alert_record.id}")

        except Exception as e:
            logger.error(f"决策快照数据库存档失败: {e}")
            db.rollback() # 如果发生错误，回滚事务，保证数据一致性
        finally:
            db.close() # 无论成功与否，都要关闭会话，释放连接

# 创建一个单例，方便在项目其他地方调用
decision_archiver = DecisionArchiver()