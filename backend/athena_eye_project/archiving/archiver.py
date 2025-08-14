# athena_eye_project/archiving/archiver.py
from typing import Dict, Any
from sqlalchemy.orm import Session

from athena_eye_project.utils.logger import logger
from athena_eye_project.config import settings
from athena_eye_project.db.models import Alert
# SessionLocal不再需要在archiver中直接使用
# from athena_eye_project.db.database import SessionLocal 

ALERT_HISTORY_LIMIT = 500

class DecisionArchiver:
    """
    负责将触发警报的决策快照存档到数据库。
    """
    def _get_current_params(self) -> Dict[str, Any]:
        """获取当前.env文件中的所有可调参数，用于记录。"""
        # ... (此函数内容不变) ...
        return {
            "MONITOR_INTERVAL_MINUTES": settings.MONITOR_INTERVAL_MINUTES,
            "PRICE_DATA_INTERVAL": settings.PRICE_DATA_INTERVAL,
            "VOLUME_LOOKBACK_PERIOD": settings.VOLUME_LOOKBACK_PERIOD,
            "VOLUME_SPIKE_MULTIPLIER": settings.VOLUME_SPIKE_MULTIPLIER,
            "PRICE_SIGNIFICANT_CHANGE_PERCENT": settings.PRICE_SIGNIFICANT_CHANGE_PERCENT,
            "SENTIMENT_SCORE_THRESHOLD": settings.SENTIMENT_SCORE_THRESHOLD,
            "NEWS_FETCH_COUNT": settings.NEWS_FETCH_COUNT
        }

    def _cleanup_old_alerts(self, db: Session):
        """如果警报数量超过限制，则删除最旧的记录。"""
        # ... (此函数内容不变) ...
        try:
            num_alerts = db.query(Alert).count()
            
            if num_alerts > ALERT_HISTORY_LIMIT:
                num_to_delete = num_alerts - ALERT_HISTORY_LIMIT
                logger.info(f"警报数量 ({num_alerts}) 已超过限制 ({ALERT_HISTORY_LIMIT})，准备删除 {num_to_delete} 条最旧的记录。")
                
                oldest_alerts = db.query(Alert.id).order_by(Alert.id.asc()).limit(num_to_delete).all()
                ids_to_delete = [alert_id for (alert_id,) in oldest_alerts]

                db.query(Alert).filter(Alert.id.in_(ids_to_delete)).delete(synchronize_session=False)
                logger.info(f"已成功删除 {len(ids_to_delete)} 条旧记录。")
        except Exception as e:
            logger.error(f"清理旧警报记录时出错: {e}")

    def archive_decision_to_db(
        self,
        db: Session,  # <-- 【核心变更】数据库会话作为参数传入
        alert_details: Dict[str, Any],
        raw_news_data: list
        ):
        """
        将一次完整的决策快照保存到数据库中，并执行清理。
        """
        try:
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

            db.add(new_alert_record)
            db.commit()
            db.refresh(new_alert_record)
            
            logger.info(f"决策快照已成功存档至数据库，记录ID: {new_alert_record.id}")

            self._cleanup_old_alerts(db)
            db.commit()
            
        except Exception as e:
            logger.error(f"决策快照数据库存档失败: {e}")
            db.rollback()
        # finally块不再需要，因为会话的关闭由调用者负责

# 创建一个单例
decision_archiver = DecisionArchiver()