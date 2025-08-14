# athena_eye_project/main.py (最终工业版 - 带速率控制)
import schedule
import time
from typing import Dict, Any

from athena_eye_project.config import settings
from athena_eye_project.config.stock_manager import get_active_watchlist
from athena_eye_project.utils.logger import logger
from athena_eye_project.data_ingestion.fetcher import data_fetcher
from athena_eye_project.analysis.volume_price import volume_price_analyzer
from athena_eye_project.analysis.sentiment import sentiment_analyzer
from athena_eye_project.analysis.decision_engine import decision_engine
from athena_eye_project.notifications.email_sender import email_client

from athena_eye_project.archiving.archiver import decision_archiver
from athena_eye_project.db.database import SessionLocal
# --- 新增：速率控制参数 ---
# Polygon.io 免费版 5次/分钟 -> 每次调用间隔至少12秒。我们设为15秒以策安全。
API_CALL_INTERVAL_SECONDS = 30

def format_alert_email_v2(alert_details: Dict[str, Any]) -> str:
    # ... (此函数内容完全不变)
    ticker = alert_details['ticker']
    alert_type = alert_details['alert_type']
    color = "#D23F31"
    if "看涨" in alert_type or "机会" in alert_type:
        color = "#28a745"
    sentiment_details = alert_details.get('sentiment_details', {})
    price_details = alert_details.get('price_details', {})
    volume_details = alert_details.get('volume_details', {})
    html = f"""
    <html><head><style>
        body {{ font-family: 'Segoe UI', sans-serif; margin: 20px; color: #333; background-color: #f4f7f6; }}
        .container {{ border: 1px solid #ddd; border-top: 5px solid {color}; padding: 25px; border-radius: 10px; max-width: 680px; margin: auto; background-color: #fff; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
        .header {{ color: {color}; padding-bottom: 10px; }}
        h1 {{ margin: 0; font-size: 24px; }}
        h2 {{ font-size: 20px; border-bottom: 2px solid #eee; padding-bottom: 8px; margin-top: 0; }}
        h3 {{ font-size: 16px; color: #444; margin-top: 25px; border-bottom: 1px solid #eee; padding-bottom: 5px;}}
        .section {{ margin-top: 20px; }}
        strong {{ color: #000; }}
        ul {{ list-style-type: none; padding-left: 0; }}
        li {{ background-color: #f9f9f9; margin-bottom: 8px; padding: 12px; border-radius: 5px; border-left: 5px solid {color}; display: flex; justify-content: space-between; align-items: center; }}
        .label {{ font-weight: bold; color: #555; }}
        .value {{ font-size: 1.1em; font-weight: bold; }}
        .reason-list li {{ background-color: #eef; border-left-color: #778beb; }}
    </style></head><body>
        <div class="container">
            <div class="header"><h1>Athena Eye - V2 智能博弈警报</h1></div>
            <div class="section">
                <h2>{ticker} — {alert_type}</h2>
                <p><strong>核心判断:</strong> {alert_details.get('reason', 'N/A')}</p>
            </div>
            <div class="section">
                <h3>三维分析详情:</h3>
                <ul>
                    <li><span class="label">价格动态 (K线周期: {settings.PRICE_DATA_INTERVAL})</span> <span class="value">{price_details.get('change_percent', 0)}%</span></li>
                    <li><span class="label">成交量放大倍数</span> <span class="value">{volume_details.get('multiplier', 0)}x</span></li>
                    <li><span class="label">市场情绪评分</span> <span class="value">{sentiment_details.get('sentiment_score', 5)}/10</span></li>
                </ul>
            </div>
            <div class="section reason-list">
                <h3>LLM分析的关键新闻点:</h3>
                <ul>
                    {''.join(f'<li>- {reason}</li>' for reason in sentiment_details.get('key_reasons', ['N/A']))}
                </ul>
            </div>
        </div>
    </body></html>
    """
    return html

def run_monitor_cycle():
    """执行一个完整的、事件驱动的监控周期"""
    logger.info(f"====== 开始新一轮监控周期 (间隔: {settings.MONITOR_INTERVAL_MINUTES}分钟) ======")
    watchlist = get_active_watchlist()
    if not watchlist:
        logger.warning("监控列表为空，跳过本轮周期。")
        return

    for i, ticker in enumerate(watchlist):
        logger.info(f"--- 正在处理股票: {ticker} ({i+1}/{len(watchlist)}) ---")
        
        # --- 第一步：获取并分析量价数据 ---
        stock_data = data_fetcher.get_stock_data(ticker, interval=settings.PRICE_DATA_INTERVAL)
        if stock_data is None:
            logger.error(f"未能获取到 {ticker} 的行情数据，跳过分析。")
            if i < len(watchlist) - 1:
                time.sleep(API_CALL_INTERVAL_SECONDS)
            continue
            
        volume_result = volume_price_analyzer.analyze_latest_candle(stock_data)
        
        # --- 第二步：事件驱动判断 ---
        if volume_result:
            logger.info(f"为 {ticker} 检测到量价异动，启动深度分析...")
            
            # 只有在异动发生时，才进行新闻获取和情绪分析
            news_data = data_fetcher.get_news(ticker)
            sentiment_result = sentiment_analyzer.analyze_news_sentiment(ticker, news_data)
            
            # 将所有信息送入决策引擎
            alert = decision_engine.decide(ticker, volume_result, sentiment_result)
            
            if alert:
                logger.info(f"为 {ticker} 触发警报，执行通知和存档...")
                
                db = SessionLocal()
                try:
                    decision_archiver.archive_decision_to_db(db, alert, news_data or [])
                finally:
                    db.close()
                
                subject = f"【Athena Eye V2 警报】{ticker}: {alert['alert_type']}"
                body = format_alert_email_v2(alert) # format_alert_email_v2需要完整定义
                email_client.send_email(subject, body)
            else:
                logger.info(f"对 {ticker} 的深度分析未触发警-报。")

        else:
            logger.info(f"对 {ticker} 的量价分析未发现异动，跳过深度分析。")

        # 速率控制
        if i < len(watchlist) - 1:
            logger.info(f"速率控制：暂停 {API_CALL_INTERVAL_SECONDS} 秒...")
            time.sleep(API_CALL_INTERVAL_SECONDS)

    logger.info("====== 本轮监控周期结束 ======")

def main():
    """程序主入口"""
    try:
        settings.validate_config()
        logger.info("配置验证通过，Athena Eye V2 系统启动...")
        current_watchlist = get_active_watchlist()
        logger.info(f"当前监控列表: {current_watchlist}")
        logger.info(f"监控频率: {settings.MONITOR_INTERVAL_MINUTES} 分钟")
    except ValueError as e:
        logger.error(f"系统启动失败: {e}")
        return

    logger.info("立即执行一次 V2 启动运行...")
    run_monitor_cycle()
    
    logger.info(f"设置定时任务：每 {settings.MONITOR_INTERVAL_MINUTES} 分钟运行一次 V2 监控。")
    schedule.every(settings.MONITOR_INTERVAL_MINUTES).minutes.do(run_monitor_cycle)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()