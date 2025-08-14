# 项目概览: athena_eye_nomysql

本文档由`generate_project_overview.py`自动生成，包含了项目的结构树和所有可读文件的内容。

## 项目结构

```
athena_eye_nomysql/
├── backend
│   ├── .pytest_cache
│   │   ├── v
│   │   │   └── cache
│   │   │       ├── lastfailed
│   │   │       └── nodeids
│   │   ├── .gitignore
│   │   ├── CACHEDIR.TAG
│   │   └── README.md
│   ├── archive
│   │   └── 2025-08-04
│   │       └── 20250804_084829_PERFECTCO_主力入场（强烈看涨）.json
│   ├── athena_eye_project
│   │   ├── analysis
│   │   │   ├── __init__.py
│   │   │   ├── decision_engine.py
│   │   │   ├── sentiment.py
│   │   │   └── volume_price.py
│   │   ├── archiving
│   │   │   └── archiver.py
│   │   ├── config
│   │   │   ├── __init__.py
│   │   │   ├── settings.py
│   │   │   ├── stock_manager.py
│   │   │   └── stocks.json
│   │   ├── data_ingestion
│   │   │   ├── __init__.py
│   │   │   └── fetcher.py
│   │   ├── db
│   │   │   ├── database.py
│   │   │   └── models.py
│   │   ├── notifications
│   │   │   ├── __init__.py
│   │   │   └── email_sender.py
│   │   ├── utils
│   │   │   ├── __init__.py
│   │   │   └── logger.py
│   │   ├── __init__.py
│   │   ├── background_worker.py
│   │   ├── main.py
│   │   └── main_api.py
│   ├── logs
│   ├── test
│   │   └── test_core_logic.py
│   ├── .python-version
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend
│   ├── public
│   ├── src
│   │   ├── assets
│   │   │   ├── base.css
│   │   │   └── main.css
│   │   ├── components
│   │   ├── router
│   │   │   └── index.js
│   │   ├── views
│   │   │   ├── ArchiveView.vue
│   │   │   ├── ConfigView.vue
│   │   │   └── DashboardView.vue
│   │   ├── App.vue
│   │   └── main.js
│   ├── .editorconfig
│   ├── .gitattributes
│   ├── .gitignore
│   ├── .prettierrc.json
│   ├── Dockerfile
│   ├── eslint.config.js
│   ├── index.html
│   ├── jsconfig.json
│   ├── nginx.conf
│   ├── package.json
│   ├── README.md
│   └── vite.config.js
├── test
├── .gitignore
├── DEPLOYMENT_POSTMORTEM.md
├── docker-compose.prod.yml
├── docker-compose.yml
├── DOCKER_LINUX_DEPLOY_MANUAL.md
├── DOCKERNO_LINUX_DEPLOY_MANUAL.md
└── README.md
```

---

# 文件内容

## `.gitignore`

```
# Environments & Secrets
.venv
backend/.venv
.env
backend/.env
.env.*

# Python Caches
*.pyc
__pycache__/
*.egg-info

# IDE / Editor specific
.vscode/
.idea/

# Runtime Generated Files
logs/
archive/
backend/logs/
backend/archive/
backend/data/

# Frontend Build Artifacts
frontend/node_modules/
frontend/dist/
```

## `backend/.pytest_cache/.gitignore`

```
# Created by pytest automatically.
*

```

## `backend/.pytest_cache/CACHEDIR.TAG`

```
Signature: 8a477f597d28d172789f06886806bc55
# This file is a cache directory tag created by pytest.
# For information about cache directory tags, see:
#	https://bford.info/cachedir/spec.html

```

## `backend/.pytest_cache/README.md`

````text
\# pytest cache directory #

This directory contains data from the pytest's cache plugin,
which provides the `--lf` and `--ff` options, as well as the `cache` fixture.

**Do not** commit this to version control.

See [the docs](https://docs.pytest.org/en/stable/how-to/cache.html) for more information.

````

## `backend/.pytest_cache/v/cache/lastfailed`

```
{}
```

## `backend/.pytest_cache/v/cache/nodeids`

```
[
  "test/test_core_logic.py::test_archive_and_cleanup_logic",
  "test/test_core_logic.py::test_archive_api_endpoints"
]
```

## `backend/.python-version`

```
3.12

```

## `backend/archive/2025-08-04/20250804_084829_PERFECTCO_主力入场（强烈看涨）.json`

```json
{
    "archive_timestamp_utc": "2025-08-04T00:48:29.176710",
    "alert_details": {
        "ticker": "PERFECTCO",
        "alert_type": "主力入场（强烈看涨）",
        "reason": "量价齐升，伴随积极市场情绪。价格在K线周期内上涨 1.0%，情绪评分为 9/10。",
        "price_details": {
            "open": 183.02850599219502,
            "close": 184.85879105211697,
            "change_percent": 1.0
        },
        "volume_details": {
            "latest": 50000,
            "average": 10000,
            "multiplier": 5.0
        },
        "sentiment_details": {
            "overall_sentiment": "Positive",
            "sentiment_score": 9,
            "key_reasons": [
                "Record-breaking profits announced.",
                "Stock upgraded to 'Strong Buy'."
            ],
            "confidence_level": "High"
        }
    },
    "trigger_conditions": {
        "MONITOR_INTERVAL_MINUTES": 15,
        "PRICE_DATA_INTERVAL": "15min",
        "VOLUME_LOOKBACK_PERIOD": 20,
        "VOLUME_SPIKE_MULTIPLIER": 3.5,
        "PRICE_SIGNIFICANT_CHANGE_PERCENT": 0.5,
        "SENTIMENT_SCORE_THRESHOLD": 7,
        "NEWS_FETCH_COUNT": 20
    },
    "raw_news_data": [
        {
            "title": "Record profits!",
            "link": "#"
        }
    ]
}
```

## `backend/athena_eye_project/__init__.py`

[文件为空]

## `backend/athena_eye_project/analysis/__init__.py`

[文件为空]

## `backend/athena_eye_project/analysis/decision_engine.py`

```python
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
            logger.info(f"为 {ticker} 检测到巨量，但价格/情绪组合信号不明确({price_change=}, {sentiment.get('overall_sentiment')})，暂不触发警报。")
            return None

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
```

## `backend/athena_eye_project/analysis/sentiment.py`

```python
# athena_eye_project/analysis/sentiment.py
import json
from openai import OpenAI
from typing import List, Dict, Optional, Any

from athena_eye_project.config import settings
from athena_eye_project.utils.logger import logger

class SentimentAnalyzer:
    """
    使用LLM分析新闻的市场情绪。
    """
    def __init__(self):
        if not settings.API_KEY:
            logger.warning("OpenRouter API密钥未配置，情绪分析功能将不可用。")
            self.client = None
        else:
            self.client = OpenAI(
                api_key=settings.API_KEY,
                base_url=settings.BASE_URL,
            )
            logger.info(f"情绪分析器已初始化，使用模型: {settings.MODEL_NAME}")

    def _build_prompt(self, ticker: str, news_titles: List[str]) -> str:
        """构建发送给LLM的Prompt。"""
        
        # 将新闻标题格式化为带编号的列表
        formatted_titles = "\n".join(f"{i+1}. {title}" for i, title in enumerate(news_titles))

        # 这是Prompt工程的关键部分
        prompt = f"""
        As a top-tier financial analyst specializing in the US stock market, your task is to analyze the sentiment of the following news headlines for the stock ticker "{ticker}". 
        
        News Headlines:
        ---
        {formatted_titles}
        ---

        Based on these headlines, determine the overall market sentiment. Consider factors like product launches, earnings reports, regulatory news, partnerships, and market trends. Ignore generic or irrelevant news.

        Your response MUST be in JSON format with the following structure:
        {{
          "overall_sentiment": "Positive",
          "sentiment_score": 8,
          "key_reasons": [
            "Positive earnings forecast.",
            "Successful new product launch mentioned."
          ],
          "confidence_level": "High"
        }}

        Guidelines for JSON values:
        - "overall_sentiment": Must be one of ["Positive", "Negative", "Neutral"].
        - "sentiment_score": An integer from 1 (most negative) to 10 (most positive). 5 is neutral.
        - "key_reasons": A list of strings, providing brief, key drivers for your sentiment analysis.
        - "confidence_level": Your confidence in this analysis, one of ["High", "Medium", "Low"].
        """
        return prompt

    def analyze_news_sentiment(self, ticker: str, news: List[Dict[str, str]]) -> Optional[Dict[str, Any]]:
        """
        分析一组新闻的整体市场情绪。

        Args:
            ticker (str): 股票代码。
            news (List[Dict[str, str]]): 从fetcher获取的新闻列表。

        Returns:
            Optional[Dict[str, Any]]: 包含情绪分析结果的字典，如果失败则返回None。
        """
        if not self.client:
            logger.warning("由于未配置API密钥，跳过情绪分析。")
            return None
        
        if not news:
            logger.info(f"没有为 {ticker} 提供新闻，无需进行情绪分析。")
            return {"overall_sentiment": "Neutral", "sentiment_score": 5, "key_reasons": ["No news available."], "confidence_level": "High"}


        # 提取新闻标题进行分析
        news_titles = [item['title'] for item in news if item.get('title')]
        if not news_titles:
            logger.info("新闻列表中没有有效的标题，跳过情绪分析。")
            return None

        prompt = self._build_prompt(ticker, news_titles)
        
        try:
            logger.info(f"正在为 {ticker} 的新闻请求情绪分析...")
            chat_completion = self.client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a helpful financial analyst assistant that provides responses in JSON format."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2, # 较低的温度确保结果更具确定性
                response_format={"type": "json_object"} # 确保返回的是JSON
            )
            
            response_content = chat_completion.choices[0].message.content
            logger.info(f"LLM响应接收成功，正在解析JSON...")
            
            analysis_result = json.loads(response_content)
            
            # (可选) 在此可以添加对返回结果的验证，确保它符合我们的格式要求
            
            return analysis_result

        except Exception as e:
            logger.error(f"调用LLM进行情绪分析时出错: {e}")
            return None

# 创建一个单例
sentiment_analyzer = SentimentAnalyzer()
```

## `backend/athena_eye_project/analysis/volume_price.py`

```python
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
```

## `backend/athena_eye_project/archiving/archiver.py`

```python
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
```

## `backend/athena_eye_project/background_worker.py`

```python
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
```

## `backend/athena_eye_project/config/__init__.py`

[文件为空]

## `backend/athena_eye_project/config/settings.py`

```python
# athena_eye_project/config/settings.py (已升级至Polygon)
import os
from dotenv import load_dotenv,find_dotenv
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

# 尝试从多个位置加载.env文件
dotenv_path = find_dotenv()
if not dotenv_path:
    # 如果在当前目录找不到，尝试在上级目录找
    parent_dotenv = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
    if os.path.exists(parent_dotenv):
        dotenv_path = parent_dotenv

load_dotenv(dotenv_path)

# === 核心API与账户配置 ===
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY") # <-- 读取新的API Key
API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
MODEL_NAME = os.getenv("OPENROUTER_MODEL_NAME")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.qq.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

# === 数据库配置 (统一使用SQLite) ===
# 数据库文件将被放置在 /app/data/ 目录下，该目录在生产环境中会被持久化。
DATABASE_URL = "sqlite:///data/athena_eye.db"

# === 用户可调参数 (Tuning) ===
MONITOR_INTERVAL_MINUTES = int(os.getenv("MONITOR_INTERVAL_MINUTES", 15))
PRICE_DATA_INTERVAL = os.getenv("PRICE_DATA_INTERVAL", "15min")
VOLUME_LOOKBACK_PERIOD = int(os.getenv("VOLUME_LOOKBACK_PERIOD", 20))
VOLUME_SPIKE_MULTIPLIER = float(os.getenv("VOLUME_SPIKE_MULTIPLIER", 3.0))
PRICE_SIGNIFICANT_CHANGE_PERCENT = float(os.getenv("PRICE_SIGNIFICANT_CHANGE_PERCENT", 0.5))
SENTIMENT_SCORE_THRESHOLD = int(os.getenv("SENTIMENT_SCORE_THRESHOLD", 7))
NEWS_FETCH_COUNT = int(os.getenv("NEWS_FETCH_COUNT", 20))
# === 配置验证函数 ===
def validate_config():
    required_vars = {
        "POLYGON_API_KEY": POLYGON_API_KEY,
        "SENDER_EMAIL": SENDER_EMAIL,
        "EMAIL_APP_PASSWORD": EMAIL_APP_PASSWORD,
        "RECIPIENT_EMAIL": RECIPIENT_EMAIL,
    }
    
    missing_vars = [key for key, value in required_vars.items() if not value]
    if missing_vars:
        raise ValueError(f"错误：缺少必要的配置: {', '.join(missing_vars)}. 请检查 .env 文件。")
    # 注意：不再验证STOCK_WATCHLIST，因为现在使用JSON文件管理股票列表
```

## `backend/athena_eye_project/config/stock_manager.py`

```python
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
```

## `backend/athena_eye_project/config/stocks.json`

```json
{
  "stocks": [
    {
      "ticker": "NBIS",
      "is_active": true,
      "notes": "生物技术"
    },
    {
      "ticker": "APH",
      "is_active": true,
      "notes": "AI基础设施"
    }
  ]
}
```

## `backend/athena_eye_project/data_ingestion/__init__.py`

[文件为空]

## `backend/athena_eye_project/data_ingestion/fetcher.py`

```python
# athena_eye_project/data_ingestion/fetcher.py (最终健壮版)
import requests
import pandas as pd
from typing import Optional, List, Dict
from datetime import datetime, timedelta
import time
from athena_eye_project.utils.logger import logger
from athena_eye_project.config import settings

class DataFetcher:
    """
    负责从Polygon.io和NewsAPI获取数据。
    """
    def get_stock_data(self, ticker_symbol: str, interval: str) -> Optional[pd.DataFrame]:
        """
        使用Polygon.io获取股票的K线数据 (Aggregates Bars API)。
        """
        logger.info(f"开始为 {ticker_symbol} 获取行情数据 (源: Polygon.io)...")
        if not settings.POLYGON_API_KEY:
            logger.error("Polygon.io API密钥未配置。")
            return None

        try:
            timespan_value = int(interval.replace('min', ''))
            timespan_unit = 'minute'
        except ValueError:
            logger.error(f"不支持的K线周期格式: {interval}。")
            return None
        
        to_date = datetime.now().strftime('%Y-%m-%d')
        from_date = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
        
        url = (
            f"https://api.polygon.io/v2/aggs/ticker/{ticker_symbol}/range/"
            f"{timespan_value}/{timespan_unit}/{from_date}/{to_date}"
        )
        params = { "apiKey": settings.POLYGON_API_KEY, "adjusted": "true", "sort": "asc", "limit": 5000 }
        
        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            # --- 核心修复：使用更健壮的判断逻辑 ---
            if "results" in data and data.get("resultsCount", 0) > 0:
                # 只要有结果，我们就处理
                df = pd.DataFrame(data['results'])
                df['datetime'] = pd.to_datetime(df['t'], unit='ms')
                df.set_index('datetime', inplace=True)
                df.rename(columns={'o': 'Open', 'h': 'High', 'l': 'Low', 'c': 'Close', 'v': 'Volume'}, inplace=True)
                
                logger.info(f"成功从 Polygon.io 获取到 {ticker_symbol} 的 {len(df)} 条行情数据。")
                return df[['Open', 'High', 'Low', 'Close', 'Volume']]
            else:
                # 如果没有结果，才认为是失败
                logger.warning(f"Polygon.io未能返回 {ticker_symbol} 的有效数据。响应: {data}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"请求Polygon.io API时网络出错: {e}")
            return None
        except Exception as e:
            logger.error(f"处理Polygon.io数据时出错: {e}")
            return None

    def get_news(self, ticker_symbol: str) -> Optional[List[Dict[str, str]]]:
        """
        使用 Polygon.io V2 获取与股票相关的新闻。
        """
        logger.info(f"开始为 {ticker_symbol} 获取新闻数据 (源: Polygon.io)...")
        if not settings.POLYGON_API_KEY:
            logger.error("Polygon.io API密钥未配置。")
            return None
        
        # 使用我们验证过的 V2 URL
        url = "https://api.polygon.io/v2/reference/news"
        params = {
            "apiKey": settings.POLYGON_API_KEY,
            "ticker": ticker_symbol,
            "limit": settings.NEWS_FETCH_COUNT,
            "order": "desc",
        }

        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            if "results" in data and len(data.get("results", [])) > 0:
                articles = data.get("results", [])
                formatted_news = [
                    {"title": article.get("title"), "link": article.get("article_url"), "source": article.get("publisher", {}).get("name")} 
                    for article in articles
                ]
                logger.info(f"成功从 Polygon.io 获取到 {len(formatted_news)} 条关于 {ticker_symbol} 的新闻。")
                return formatted_news
            else:
                logger.warning(f"Polygon.io未能返回 {ticker_symbol} 的有效新闻。响应: {data}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"请求Polygon.io新闻API时网络出错: {e}")
            return None
        except Exception as e:
            logger.error(f"处理Polygon.io新闻数据时出错: {e}")
            return None

# 创建单例
data_fetcher = DataFetcher()
```

## `backend/athena_eye_project/db/database.py`

```python
# athena_eye_project/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from athena_eye_project.config import settings
from athena_eye_project.utils.logger import logger

try:
    # 1. 创建数据库引擎 (Engine)
    # 根据数据库类型使用不同的连接参数
    if settings.DATABASE_URL.startswith("sqlite"):
        # SQLite 配置
        engine = create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
            connect_args={"check_same_thread": False}  # SQLite 特有参数
        )
    else:
        # MySQL 配置
        engine = create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 10}
        )

    # 2. 创建一个 SessionLocal 类
    # 这个类本身不是一个数据库会话，而是一个会话的“工厂”。
    # 当我们实例化 SessionLocal() 时，才会创建一个新的会话。
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # 3. 创建一个 Base 类
    # 这是所有ORM模型的基类。我们之后创建的所有数据表模型，
    # 都需要继承自这个Base类，SQLAlchemy才能发现并管理它们。
    Base = declarative_base()

    logger.info("数据库连接引擎和会话工厂已成功初始化。")

except Exception as e:
    logger.critical(f"数据库初始化失败，无法创建引擎: {e}. 请检查.env中的数据库配置和网络连接。")
    # 这是一个致命错误，直接抛出异常以阻止应用启动。
    raise

def get_db():
    """
    FastAPI 依赖注入函数 (Dependency Injection)。

    它的作用是为每个API请求，都生成一个独立的数据库会话，
    并在请求处理完成后，无论成功或失败，都确保会话被关闭。
    这是一种非常健壮和高效的会话管理模式。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    初始化数据库函数。

    它会连接到数据库，并根据所有继承自 Base 的模型，
    创建出所有对应的表。
    关键点：它不会重复创建已经存在的表，所以可以安全地在每次应用启动时调用。
    """
    try:
        logger.info("正在检查并同步数据库表结构...")
        # Base.metadata.create_all() 是SQLAlchemy的魔法所在，
        # 它会遍历所有子类模型，并生成 'CREATE TABLE IF NOT EXISTS ...' 类似的语句。
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表结构同步完成。")
    except Exception as e:
        logger.error(f"创建数据库表时发生严重错误: {e}")
        # 表创建失败也是一个致命错误。
        raise
```

## `backend/athena_eye_project/db/models.py`

```python
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
```

## `backend/athena_eye_project/main.py`

```python
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
```

## `backend/athena_eye_project/main_api.py`

```python
# backend/athena_eye_project/main_api.py (已升级至V5 - 数据库集成)
import threading
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends, Query
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
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
    archive_timestamp_utc: datetime # FastAPI 会自动处理datetime到str的转换
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

    model_config = ConfigDict(from_attributes=True)

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
```

## `backend/athena_eye_project/notifications/__init__.py`

[文件为空]

## `backend/athena_eye_project/notifications/email_sender.py`

```python
# athena_eye_project/notifications/email_sender.py (最终优化版)
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from athena_eye_project.config import settings
from athena_eye_project.utils.logger import logger

class EmailSender:
    def send_email(self, subject: str, body: str) -> bool:
        """
        发送邮件通知 (使用STARTTLS方式，并健壮地处理连接关闭)

        Args:
            subject (str): 邮件主题
            body (str): 邮件正文 (支持HTML)

        Returns:
            bool: 如果发送成功返回True，否则返回False
        """
        if not all([settings.SENDER_EMAIL, settings.EMAIL_APP_PASSWORD, settings.RECIPIENT_EMAIL]):
            logger.error("邮件配置不完整，无法发送邮件。")
            return False

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = settings.SENDER_EMAIL
        message["To"] = settings.RECIPIENT_EMAIL
        message.attach(MIMEText(body, "html"))
        
        server = None
        try:
            context = ssl.create_default_context()
            logger.info(f"正在连接邮件服务器 {settings.SMTP_SERVER}:{settings.SMTP_PORT}...")
            server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT, timeout=10)
            server.starttls(context=context)
            logger.info("TLS加密已启动，正在登录...")
            server.login(settings.SENDER_EMAIL, settings.EMAIL_APP_PASSWORD)
            logger.info("登录成功，正在发送邮件...")
            server.sendmail(settings.SENDER_EMAIL, settings.RECIPIENT_EMAIL, message.as_string())
            
            # 只要sendmail不抛出异常，我们就认为发送成功
            logger.info(f"邮件已成功递交至SMTP服务器，目标邮箱: {settings.RECIPIENT_EMAIL}！")
            return True

        except smtplib.SMTPAuthenticationError:
            logger.error("邮件发送失败：SMTP认证错误。请检查发件箱地址和邮箱授权码。")
            return False
        except Exception as e:
            logger.error(f"发送邮件时发生错误: {e}")
            return False
        finally:
            # 无论成功失败，都尝试关闭连接
            if server:
                try:
                    server.quit()
                    logger.info("SMTP服务器连接已成功关闭。")
                except Exception as e:
                    # 这个错误是可接受的，只记录警告即可
                    logger.warning(f"关闭SMTP连接时发生非关键性问题: {e}")

# 创建一个单例
email_client = EmailSender()
```

## `backend/athena_eye_project/utils/__init__.py`

[文件为空]

## `backend/athena_eye_project/utils/logger.py`

```python
# athena_eye_project/utils/logger.py
import logging
import sys

def setup_logger():
    """配置一个简单的日志记录器"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("logs/athena_eye.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logger()
```

## `backend/Dockerfile`

```dockerfile
# backend/Dockerfile (已修复构建时文件缺失问题)

# --- Stage 1: 使用官方的Python 3.12 slim镜像作为基础 ---
    FROM python:3.12-slim

    # --- 设置环境变量 ---
    ENV PYTHONUNBUFFERED=1
    ENV PATH="/root/.local/bin:${PATH}"
    
    # --- 设置工作目录 ---
    WORKDIR /app
    
    # --- 【核心修复】调整文件复制顺序 ---
    
    # 1. 先复制项目定义文件
    COPY pyproject.toml ./
    
    # 2. 接着，把所有项目代码和相关文件都复制过来
    #    这样，在下一步安装时，构建工具就能找到所有需要的文件了
    COPY . .
    
    # 3. 最后，在文件齐全的情况下，安装所有依赖
    #    这个指令包含了多个步骤，以确保健壮性和镜像体积
    RUN apt-get update && \
        apt-get install -y curl && \
        # 安装uv
        curl -LsSf https://astral.sh/uv/install.sh | sh && \
        # 使用uv安装项目依赖（包括我们自己的包）
        uv pip install . --system && \
        # 清理工作
        apt-get purge -y --auto-remove curl && \
        rm -rf /var/lib/apt/lists/*
    
    RUN mkdir logs
    RUN mkdir /app/data
    # --- 暴露端口 ---
    EXPOSE 8000
    
    # --- 默认启动命令 ---
    CMD ["uvicorn", "athena_eye_project.main_api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

## `backend/pyproject.toml`

```
[project]
name = "athena-eye-backend"
version = "0.1.0"
description = "The backend API and worker for the Athena Eye project."
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "cryptography>=45.0.6",
    "fastapi>=0.116.1",
    "gunicorn>=23.0.0",
    "openai>=1.98.0",
    "pandas>=2.3.1",
    "python-dotenv>=1.1.1",
    "pyyaml>=6.0.2",
    "requests>=2.32.4",
    "schedule>=1.2.2",
    "sqlalchemy>=2.0.42",
    "tenacity>=9.1.2",
    "uvicorn[standard]>=0.35.0",
]


[tool.setuptools]

packages = ["athena_eye_project"]

[project.optional-dependencies]
dev = [
    "httpx>=0.28.1",
    "pytest>=8.4.1",
]

```

## `backend/test/test_core_logic.py`

```python
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

# --- 测试环境设置 ---
TEST_DATABASE_FILE = "test_athena_eye.db"
TEST_DATABASE_URL = f"sqlite:///./{TEST_DATABASE_FILE}"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from athena_eye_project.config import settings
settings.DATABASE_URL = TEST_DATABASE_URL

from athena_eye_project.db.database import Base, get_db
from athena_eye_project.main_api import app
from athena_eye_project.db.models import Alert
from athena_eye_project.archiving.archiver import decision_archiver, ALERT_HISTORY_LIMIT

# --- Pytest Fixture ---
@pytest.fixture(scope="function")
def db_session() -> Session:
    """
    为每个测试函数创建一个独立的、干净的文件数据库。
    并在测试结束后自动清理。
    """
    if os.path.exists(TEST_DATABASE_FILE):
        os.remove(TEST_DATABASE_FILE)
        
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # 【核心修正】在删除文件前，彻底关闭引擎的所有连接
        engine.dispose()
        if os.path.exists(TEST_DATABASE_FILE):
            os.remove(TEST_DATABASE_FILE)

# --- FastAPI 测试客户端设置 ---
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# --- 测试用例 ---

def test_archive_and_cleanup_logic(db_session: Session):
    """
    核心测试：验证存档和自动清理功能。
    """
    print(f"开始测试存档与清理逻辑，记录上限为 {ALERT_HISTORY_LIMIT}...")
    total_to_create = ALERT_HISTORY_LIMIT + 10
    mock_alert_details = {
        "ticker": "TEST", "alert_type": "Test Alert", "reason": "Testing cleanup",
        "price_details": {}, "volume_details": {}, "sentiment_details": {}
    }

    for i in range(total_to_create):
        current_alert_details = mock_alert_details.copy()
        current_alert_details['reason'] = f"Testing cleanup {i+1}"
        decision_archiver.archive_decision_to_db(db_session, current_alert_details, [])

    final_count = db_session.query(Alert).count()
    print(f"存档 {total_to_create} 条记录后，数据库中剩余 {final_count} 条。")
    assert final_count == ALERT_HISTORY_LIMIT

    oldest_remaining_alert = db_session.query(Alert).order_by(Alert.id.asc()).first()
    assert oldest_remaining_alert is not None
    assert "11" in oldest_remaining_alert.reason
    print("验证通过：最旧的10条记录已被正确删除。")


def test_archive_api_endpoints(db_session: Session):
    """
    API集成测试：验证/api/archive端点能否在共享数据库上正常工作。
    """
    print("开始测试API端点...")
    
    alert1 = Alert(ticker="API_T1", alert_type="Type A", reason="Reason A")
    alert2 = Alert(ticker="API_T2", alert_type="Type B", reason="Reason B")
    db_session.add_all([alert1, alert2])
    db_session.commit()
    
    response = client.get("/api/archive")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]['ticker'] == "API_T2"
    print("验证通过：/api/archive 端点工作正常。")
```

## `DEPLOYMENT_POSTMORTEM.md`

````text
\# Athena Eye 项目：云端部署实战复盘报告

**文档目的**: 本文档旨在系统性地记录`Athena Eye`项目从本地开发环境迁移至Google Cloud Platform (GCP)生产环境的全过程中，所遇到的所有关键问题、错误、诊断过程及最终解决方案。其目的是提炼经验与教训，形成知识资产，为未来项目的维护、扩展和新项目的部署提供权威参考。

---

#\# 目录
1.  [**核心经验与教训总结**](#1-核心经验与教训总结)
2.  [**详细问题复盘 (Case Study)**](#2-详细问题复盘-case-study)
    *   [2.1. 环境配置问题：GCP服务器初始化失败](#21-环境配置问题gcp服务器初始化失败)
    *   [2.2. 权限问题：Docker `permission denied`](#22-权限问题docker-permission-denied)
    *   [2.3. 容器启动问题：数据库服务 (`db`) 不健康](#23-容器启动问题数据库服务db不健康)
    *   [2.4. 应用内部错误：后端服务 (`backend`) 崩溃重启](#24-应用内部错误后端服务backend崩溃重启)
    *   [2.5. 网络访问问题：前端无法连接](#25-网络访问问题前端无法连接)
3.  [**最终架构与关键决策**](#3-最终架构与关键决策)

---

#\# 1. 核心经验与教训总结

*   **教训1：永远不要低估生产环境对资源的基础需求。**
    *   **摘要**: 1GB内存的`e2-micro`实例是导致一系列连锁问题的根源。低内存不仅影响应用本身，更会严重拖慢甚至破坏基础的系统服务（如`apt`、`sshd`）。
    *   **经验**: 对于包含数据库的现代化全栈应用，**2GB内存应被视为最低稳定运行的起点**。在项目规划初期，资源评估应优先保证稳定性，而非追求极致的零成本。

*   **教训2：权限问题必须在根源上解决，并理解其生效机制。**
    *   **摘要**: `docker`用户组权限的变更，必须在新登录的Shell会话中才能生效。已存在的`screen`会话会保持其创建时的“旧权限”，导致行为不一致。
    *   **经验**: 解决Linux权限问题，必须遵循“**授权 -> 重新登录 -> 验证**”的三步曲。对于`screen`等会话管理工具，必须杀死旧会话并创建新会话，才能继承新权限。当常规权限配置失效时，`sudo`是最后的、最可靠的保障。

*   **教训3：日志是通往真相的唯一路径。**
    *   **摘要**: 无论是GPG密钥错误、`db`不健康、`backend`崩溃，还是Nginx的`502`错误，最终的答案都清晰地写在对应服务（`apt`, `docker logs`, `串行端口`）的日志中。
    *   **经验**: 必须建立“**日志驱动**”的调试思维。遇到问题时，第一反应永远是“**去看日志**”。熟练使用`docker logs <container>`和`journalctl -u <service>`等命令，是云端运维的核心技能。

*   **教训4：必须为不同环境（开发/生产）提供差异化、隔离的配置。**
    *   **摘要**: 生产环境应移除代码热加载(`volumes`)，使用更健壮的进程管理器(`gunicorn`)，并针对低资源环境进行服务调优（如`my.cnf`）。
    *   **经验**: 使用独立的`docker-compose.prod.yml`文件是管理环境差异的最佳实践。必须清醒地认识到，在`Dockerfile`中，因为`.gitignore`的存在，**开发环境下的文件结构不等于生产镜像中的文件结构**（如此次`logs`目录的缺失）。

---

#\# 2. 详细问题复盘 (Case Study)

##\# 2.1. 环境配置问题：GCP服务器初始化失败

*   **错误表现**:
    1.  执行`apt-get update`或`apt-get install`时，报告GPG错误：`NO_PUBKEY 7EA0A9C3F273FCD8`，`repository ... is not signed`。
    2.  执行`apt`命令时，长时间卡在`Waiting for cache lock...`，或报告`dpkg was interrupted`。

*   **原因分析**:
    1.  **GPG错误**: GCP服务器的网络环境或基础镜像配置，导致无法通过标准流程正确下载并信任Docker官方的GPG公钥。
    2.  **Apt锁死**: 新创建的GCP虚拟机会在后台自动运行`apt upgrade`安全更新，这个进程会长时间占用`apt`锁，与我们手动的`apt`命令发生冲突。强行中断后会导致`dpkg`状态损坏。

*   **解决方法**:
    1.  **GPG问题**: 放弃通过`apt`源安装的方式，改用**Docker官方一键安装脚本** (`curl -fsSL https://get.docker.com | sh`)。该脚本绕过了系统的包管理签名验证，直接下载二进制文件进行安装，成功率最高。
    2.  **Apt锁问题**:
        *   **首选**: 耐心等待5-10分钟，让后台进程自动完成。
        *   **备选**: 打开新SSH窗口，使用`ps aux | grep apt`找到进程PID，用`sudo kill <PID>`终止进程，最后运行`sudo dpkg --configure -a`修复中断状态。

*   **总结**: 云平台初始环境并非100%纯净，其后台的自动化任务可能会与手动操作冲突。遇到顽固的环境配置问题时，应果断切换到更底层的、官方推荐的“通用”安装方案。

##\# 2.2. 权限问题：Docker `permission denied`

*   **错误表现**:
    1.  直接运行`docker ps`或`docker compose`命令，提示`permission denied while trying to connect to the Docker daemon socket`。
    2.  在`screen`会话中运行时出现权限错误，但在主终端中正常。

*   **原因分析**:
    1.  执行`docker`命令的当前用户（`xiaofeng_0209`）不在`docker`用户组中。
    2.  虽然执行了`sudo usermod -aG docker $USER`，但**没有退出并重新登录SSH**，导致权限变更未在当前会话生效。
    3.  `screen`会话**继承了其创建时刻的用户组权限**。如果在权限变更前创建了`screen`会话，那么即使主终端重登后获得了新权限，旧的`screen`会话内部依然是“旧身份”。

*   **解决方法**:
    1.  **标准流程**:
        *   执行`sudo usermod -aG docker $USER`。
        *   **必须 `exit` 退出并重新登录SSH**。
        *   在新会话中运行`groups`命令，确认输出包含`docker`。
    2.  **`screen`会话处理**:
        *   杀死所有旧的、以“旧身份”运行的`screen`会话 (`screen -X -S <会话名> quit`)。
        *   用拥有新权限的SSH会话，创建全新的`screen`会话。
    3.  **最终保障**: 如果以上步骤因某些系统原因依然无效，在所有`docker`和`docker compose`命令前添加`sudo`，以`root`权限执行。

*   **总结**: Linux的用户组权限管理有其特定的生效机制，必须严格遵守“授权后重新登录”的原则。要理解`screen`等工具的会话隔离特性。

##\# 2.3. 容器启动问题：数据库服务 (`db`) 不健康

*   **错误表现**:
    1.  `docker compose up`启动后，`backend`和`frontend`无法启动，最终报错`dependency failed to start: container athena_eye_db is unhealthy`。
    2.  `docker logs athena_eye_db`显示日志在初始化中途无错误地戛然而止。
    3.  `docker logs athena_eye_db`显示`unknown variable 'query_cache_type=0'`或`Found option without preceding group`错误。

*   **原因分析**:
    1.  **无声的死亡**: 服务器内存不足（1GB `e2-micro`），导致MySQL初始化时被系统OOM Killer（Out-of-Memory Killer）强制杀死。
    2.  **配置不兼容**: `my.cnf`中包含了已被MySQL 8.0移除的旧配置项（`query_cache_type`）。
    3.  **配置文件格式错误**: `my.cnf`文件开头存在注释或空行，导致严格的MySQL 8.0解析器无法识别文件格式。

*   **解决方法**:
    1.  **内存问题**:
        *   **治标**: 创建一个为低内存环境优化的`my.cnf`文件，关闭`performance_schema`并大幅降低`innodb_buffer_pool_size`。
        *   **治本**: 将服务器实例**升级到`e2-small`（2GB内存）**。
    2.  **配置兼容性**: 移除`my.cnf`中所有MySQL 8.0不再支持的配置项。
    3.  **格式问题**: 确保`.cnf`配置文件的**第一行必须是有效的组声明**（如`[mysqld]`），不能有任何前导注释或空行。

*   **总结**: 容器服务的健康，不仅取决于应用本身，更严重依赖于宿主机的资源。必须为数据库等内存密集型服务提供充足的资源，并确保配置文件与服务版本严格兼容。

##\# 2.4. 应用内部错误：后端服务 (`backend`) 崩溃重启

*   **错误表现**: 前端访问API时，Nginx日志报告`connect() failed (111: Connection refused)`或`502 Bad Gateway`。`docker logs backend`显示`FileNotFoundError: [Errno 2] No such file or directory: '/app/logs/athena_eye.log'`，并伴有`Worker failed to boot.`的Gunicorn错误。

*   **原因分析**:
    *   `backend/logs`目录被写入了`.gitignore`，因此没有被Git提交和克隆到服务器上。
    *   `Dockerfile`中的`COPY . .`指令，在构建镜像时，因为源目录（服务器上的`backend`目录）不存在`logs`文件夹，所以最终构建的生产镜像里也没有`/app/logs`这个目录。
    *   后端应用启动时，`logger.py`尝试在不存在的目录中创建日志文件，导致`FileNotFoundError`，使Gunicorn的worker进程启动失败并崩溃。

*   **解决方法**:
    *   在`backend/Dockerfile`中，`COPY . .`指令之后，明确添加一行`RUN mkdir logs`。这保证了无论源目录结构如何，最终的生产镜像中都必定存在一个空的`/app/logs`目录。

*   **总结**: 必须清醒地意识到开发环境和生产镜像之间的文件系统差异，特别是那些被`.gitignore`忽略的、但应用运行时又必需的空目录结构，必须在`Dockerfile`中显式创建。

##\# 2.5. 网络访问问题：前端无法连接

*   **错误表现**:
    1.  浏览器访问`http://<IP地址>`，提示`ERR_CONNECTION_TIMED_OUT`。
    2.  浏览器访问`http://<IP地址>`，提示`ERR_CONNECTION_CLOSED`，Nginx日志显示`"\x16\x03\x01\x01" 400`错误。

*   **原因分析**:
    1.  **超时**: GCP的VPC防火墙默认阻止了所有外部流量，没有创建允许`80`和`443`端口入站的规则。
    2.  **连接关闭**: 浏览器自动尝试使用`HTTPS`协议访问，而Nginx当时只配置了监听`80 (HTTP)`端口，无法处理`HTTPS`的加密握手请求，因此直接关闭了连接。

*   **解决方法**:
    1.  **防火墙**:
        *   **最佳实践**: 在创建GCP实例时，直接勾选“允许HTTP流量”和“允许HTTPS流量”。
        *   **手动配置**: 在VPC网络 -> 防火墙中，创建一条允许来自`0.0.0.0/0`对`tcp:80,443`端口入站流量的规则。
    2.  **协议问题**: 在浏览器地址栏中，**明确、完整地输入`http://`**，强制浏览器使用HTTP协议进行访问。

*   **总结**: 云端部署必须考虑“网络入口”问题。应用内部的端口监听（`ports`指令）和云平台外部的防火墙规则，必须协同工作，才能打通访问链路。

---

#\# 3. 最终架构与关键决策

经过这场部署实战，我们最终确定了`Athena Eye`项目的最佳实践架构：
*   **云主机**: GCP `e2-small` (2GB RAM) Ubuntu 22.04 LTS。
*   **部署技术**: Docker + Docker Compose。
*   **部署单元**: 使用`docker-compose.prod.yml`编排`db (MySQL)`, `backend (Gunicorn)`, `frontend (Nginx)`三个核心服务。
*   **运维模式**: 通过`screen`执行长时间部署，日常管理通过前端Web界面和`docker compose`命令进行。
*   **配置管理**: 通过`.env`和`my.cnf`等外部配置文件，实现了应用与配置的完全分离。

这份文档将作为项目的核心资产，指导我们未来的每一步。
````

## `docker-compose.prod.yml`

```yaml
# athena_eye/docker-compose.prod.yml
# 专为生产环境设计，移除了本地开发特性（如热加载），增加了前端服务。

services:
  # --- 数据库服务 (与本地开发基本一致) ---
  # db:
  #   image: mysql:8.0
  #   container_name: athena_eye_db
  #   restart: unless-stopped
  #   #env_file: ./.env
  #   environment:
  #     MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
  #     MYSQL_DATABASE: ${MYSQL_DATABASE}
  #     MYSQL_USER: ${MYSQL_USER}
  #     MYSQL_PASSWORD: ${MYSQL_PASSWORD}
  #   volumes:
  #     - db_data:/var/lib/mysql
  #     # 在生产环境中，我们依然使用init.sql来初始化用户
  #     - ./init.sql:/docker-entrypoint-initdb.d/init.sql
  #     - ./my.cnf:/etc/mysql/conf.d/low-memory.cnf
  #   healthcheck:
  #     test:
  #       [
  #         "CMD",
  #         "mysqladmin",
  #         "ping",
  #         "-h",
  #         "localhost",
  #         "-u",
  #         "root",
  #         "-p${MYSQL_ROOT_PASSWORD}",
  #       ]
  #     interval: 10s
  #     timeout: 5s
  #     retries: 5
    # 生产环境不应暴露端口到公网，服务间通过内部网络通信
    # ports:
    #  - "33060:3306"

  # --- 后端应用服务 (生产环境优化) ---
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: athena_eye_backend
    restart: unless-stopped
    env_file: ./.env
    volumes:
      # 将主机根目录的 .env 文件，挂载到容器内 /app/.env
      # 这样 find_dotenv() 就能在容器里找到它了
      - ./.env:/app/.env
      - db_data:/app/data
      - ./backend/athena_eye_project/config:/app/athena_eye_project/config
    # depends_on:
    #   db:
    #     condition: service_healthy # 依然依赖数据库健康
    # 【生产环境核心区别】
    # 1. 移除 'volumes'：不再将本地代码挂载到容器中。镜像是自包含的、不可变的。
    # 2. 移除 'ports'：不再直接将8000端口暴露给外界，所有流量都应通过Nginx反向代理。
    # 3. 修改 'command'：使用更稳定的gunicorn作为WSGI服务器来运行FastAPI应用。
    command: ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "1", "-b", "0.0.0.0:8000", "--timeout", "120", "athena_eye_project.main_api:app"]

  # --- 【新增】前端与反向代理服务 (Nginx) ---
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: athena_eye_frontend
    restart: unless-stopped
    ports:
      # 将此容器的80端口，映射到云服务器的80端口（HTTP）
      - "80:80"
      # 如果未来配置SSL(HTTPS)，则需要映射443端口
      # - "443:443"
    depends_on:
      # 依赖后端，确保后端启动后前端代理才生效
      - backend

volumes:
  db_data:
```

## `docker-compose.yml`

```yaml
# athena_eye/docker-compose.yml (最终本地开发版 - 安全且可靠)
services:
  # db:
  #   image: mysql:8.0
  #   container_name: athena_eye_db
  #   restart: unless-stopped
  #   # 【核心修改】我们让db服务也从.env读取变量
  #   # env_file:
  #   #   - ./.env
  #   # 【安全加固】同时在environment中明确引用，这是最稳妥的方式
  #   environment:
  #     MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
  #     MYSQL_DATABASE: ${MYSQL_DATABASE}
  #   ports:
  #     - "33060:3306"
  #   volumes:
  #     - db_data:/var/lib/mysql
  #     - ./init.sql:/docker-entrypoint-initdb.d/init.sql
  #   healthcheck:
  #     test:
  #       [
  #         "CMD",
  #         "mysqladmin",
  #         "ping",
  #         "-h",
  #         "localhost",
  #         "-u",
  #         "root",
  #         "-p${MYSQL_ROOT_PASSWORD}",
  #       ]
  #     interval: 10s
  #     timeout: 5s
  #     retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: athena_eye_backend
    restart: unless-stopped
    # 后端继续使用.env文件
    env_file:
      - ./.env
    # command: >
    #   sh -c "echo 'Waiting 5s for MySQL to be fully ready...' && sleep 5 && uvicorn athena_eye_project.main_api:app --host 0.0.0.0 --port 8000 --reload"
    ports:
      - "9000:8000"
    volumes:
      - ./backend:/app
      - ./.env:/app/.env
    # depends_on:
    #   db:
    #     condition: service_healthy
# volumes:
#   db_data:

```

## `DOCKER_LINUX_DEPLOY_MANUAL.md`

````text
\# Athena Eye - GCP服务器Docker化部署权威手册 (SOP V2.2 - SQLite版)

本文档是 `Athena Eye` 项目在全新的Google Cloud Platform (GCP) Linux服务器上，使用Docker进行**生产环境**容器化部署的**最终标准操作规程**。它凝聚了项目部署过程中的所有实战经验，旨在提供一个从零开始、一站式、高可靠性的部署指南。

---

#\# 目录
1.  [**服务器首次配置 (One-Time Setup)**](#1-服务器首次配置-one-time-setup)
    *   [1.1. 前提条件与实例创建建议](#11-前提条件与实例创建建议)
    *   [1.2. 【核心】安装核心工具 (Docker, Git, Screen)](#12-核心安装核心工具-docker-git-screen)
    *   [1.3. 优化SSH连接 (可选但强烈推荐)](#13-优化ssh连接-可选但强烈推荐)
2.  [**项目部署 (Initial Deployment)**](#2-项目部署-initial-deployment)
    *   [2.1. 克隆项目代码](#21-克隆项目代码)
    *   [2.2. 创建生产环境变量 (`.env`)](#22-创建生产环境变量-env)
    *   [2.3. 【关键】后台构建并启动系统](#23-关键后台构建并启动系统)
3.  [**日常运维 (Daily Operations)**](#3-日常运维-daily-operations)
    *   [3.1. 验证系统状态](#31-验证系统状态)
    *   [3.2. 查看服务日志](#32-查看服务日志)
    *   [3.3. 停止/重启系统](#33-停止重启系统)
4.  [**更新与维护 (Updates & Maintenance)**](#4-更新与维护-updates--maintenance)
5.  [**故障排查手册 (Troubleshooting FAQ)**](#5-故障排查手册-troubleshooting-faq)

---

#\# 1. 服务器首次配置 (One-Time Setup)

在全新的GCP服务器上，严格按照以下步骤操作一遍。

##\# 1.1. 前提条件与实例创建建议
*   **创建实例**: 在GCP控制台 **Compute Engine -> 虚拟机实例 -> 创建实例**。
*   **机器类型 (重要)**: 推荐 **`e2-small` (2 vCPU, 2 GB 内存)** 或更高配置。`e2-micro` (1 GB 内存) 现在有了运行的可能性，但仍建议从`e2-small`开始以保证稳定。
*   **启动磁盘**: 推荐使用 **`Ubuntu 22.04 LTS` (x86/64架构)** 镜像。
*   **防火墙**: 在创建实例时，务必**勾选“允许HTTP流量”和“允许HTTPS流量”**。

##\# 1.2. 【核心】安装核心工具 (Docker, Git, Screen)

**在新创建的服务器终端中，执行以下操作：**

1.  **等待系统更新完成**: 新服务器后台会自动运行安全更新。运行 `sudo apt install -y screen`，如果提示 `Waiting for cache lock...`，请耐心等待5-10分钟。
2.  **安装工具**:
    \`\`\`bash
    \# 更新系统包列表
    sudo apt update
    \# 安装 Git 和 Screen
    sudo apt install -y git screen
    \# 使用Docker官方一键安装脚本
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    \# 将当前用户添加到docker组以实现免sudo操作
    sudo usermod -aG docker $USER
    \# 完成提示
    echo "✅ 核心工具已全部安装！请执行 'exit' 退出并重新登录SSH，使Docker权限生效。"
    \`\`\`
3.  **重新登录**: `exit` 退出并重新登录SSH。验证`docker ps`不报错。

##\# 1.3. 优化SSH连接 (可选但强烈推荐)
为防止SSH因空闲而自动断开，请在**您的本地电脑**上配置SSH KeepAlive。编辑 `~/.ssh/config` 文件并添加：
\`\`\`
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
\`\`\`

---

#\# 2. 项目部署 (Initial Deployment)

(确保您已经重新登录SSH，并获得了Docker权限)

##\# 2.1. 克隆项目代码
\`\`\`bash
git clone https://your-git-repository-url/athena_eye.git
cd athena_eye_nomysql
\`\`\`

##\# 2.2. 创建生产环境变量 (`.env`)
\`\`\`bash
nano .env
\`\`\`
将您本地电脑上`.env`文件的**全部内容**复制并粘贴进来。按 `Ctrl+X` -> `Y` -> `Enter` 保存。

##\# 2.3. 【关键】后台构建并启动系统
使用`screen`来防止SSH断开导致构建中断。

1.  **创建新的`screen`会话**: `screen -S athena`
2.  **在`screen`会话中，执行构建和启动命令**:
    \`\`\`bash
    \# --build: 首次部署时必须使用，以构建镜像
    \# -d: 后台运行
    sudo docker compose -f docker-compose.prod.yml up --build -d
    \`\`\`
    > **注意**: 如果免sudo配置成功，`sudo`不是必需的，但加上更保险。
3.  **脱离会话**: 按下组合键 **`Ctrl+A`**，然后松开，再按 **`d`**。构建需要一些时间，脱离后可安全断开SSH。

---

#\# 3. 日常运维 (Daily Operations)

##\# 3.1. 验证系统状态\`\`\`bash
sudo docker compose -f docker-compose.prod.yml ps
\`\`\`
##\# 3.2. 查看服务日志
\`\`\`bash
\# 查看后端实时日志
sudo docker compose -f docker-compose.prod.yml logs -f backend

\# 查看前端Nginx实时日志
sudo docker compose -f docker-compose.prod.yml logs -f frontend
\`\`\`
##\# 3.3. 停止/重启系统
\`\`\`bash
\# 停止
sudo docker compose -f docker-compose.prod.yml down

\# 启动
sudo docker compose -f docker-compose.prod.yml up -d
\`\`\`
---

#\# 4. 更新与维护 (Updates & Maintenance)
1.  `cd ~/athena_eye`
2.  `git pull`
3.  `sudo docker compose -f docker-compose.prod.yml up --build -d`
4.  (可选) `sudo docker image prune -f`

---

#\# 5. 故障排查手册 (Troubleshooting FAQ)

*   **问题**: `apt`命令提示`Waiting for cache lock...`
    *   **解决**: 耐心等待5-10分钟，让后台自动更新完成。

*   **问题**: 运行`docker`命令提示`permission denied`。
    *   **解决**: 确保已执行`sudo usermod -aG docker $USER`，并且**必须 `exit` 退出并重新登录SSH**。

*   **问题**: `backend`容器无法启动或不断重启。
    *   **原因**: 通常是`.env`文件配置错误或缺失。
    *   **解决**: 仔细检查`.env`文件是否存在且内容正确。使用`sudo docker compose -f docker-compose.prod.yml logs backend`查看详细的错误日志。

*   **问题**: `screen -r`提示会话`(Attached)`。
    *   **解决**: 先运行`screen -d <会话名>`强制脱离，再运行`screen -r <会ta名>`重新连接。
````

## `DOCKERNO_LINUX_DEPLOY_MANUAL.md`

````text
\# Athena Eye - Linux 服务器操作手册 (SOP)

本文档是`Athena Eye`项目在Linux服务器（Debian/Ubuntu on Google Cloud）上的标准操作规程（Standard Operating Procedure）。它涵盖了从首次部署到日常维护的所有关键命令和流程。

---

#\# 目录
1.  [首次部署](#1-首次部署)
2.  [日常管理](#2-日常管理)
3.  [更新与维护 (标准流程)](#3-更新与维护-标准流程)
4.  [故障排查](#4-故障排查)
5.  [`screen` 快捷键备忘录](#5-screen-快捷键备忘录)

---

#\# 1. 首次部署

当你在一个全新的、干净的Linux服务器上部署本项目时，请严格按照以下步骤操作。

##\# 1.1 登录服务器
通过SSH客户端或云服务商提供的Web Shell，登录到你的服务器。

##\# 1.2 更新系统并安装核心工具
\`\`\`bash
\# 更新软件包列表和已安装的软件
sudo apt update && sudo apt upgrade -y

\# 安装Git, Python虚拟环境工具, 和Screen
sudo apt install -y git python3-venv screen
\`\`\`

##\# 1.3 安装 `uv` 包管理器
\`\`\`bash
\# 下载并执行安装脚本
curl -LsSf https://astral.sh/uv/install.sh | sh
#curl -LsSf https://astral.sh/uv/install.sh -o install.sh
#sh install.sh
\# 重新加载Shell配置以使uv命令生效
source ~/.profile

\# 验证安装
uv --version
\`\`\`

##\# 1.4 克隆项目代码
从你的Git仓库克隆项目。建议使用私有仓库。
\`\`\`bash
git clone https://your-git-repository-url/athena_eye.git

\# 进入项目目录
cd athena_eye/backend
\`\`\`

##\# 1.5 创建并配置 `.env` 文件
`.env`文件包含了所有密钥和配置，**绝不能**上传到Git仓库。你需要在服务器上手动创建它。
\`\`\`bash
\# 使用nano文本编辑器创建文件
nano .env
\`\`\`
将你本地的`.env`文件内容**完整地复制并粘贴**到编辑器中。按 `Ctrl+X` -> `Y` -> `Enter` 保存并退出。

##\# 1.6 创建并激活Python虚拟环境
这是一个至关重要的步骤，它为项目提供了一个隔离、干净的运行环境。
\`\`\`bash
\# 在项目根目录(~/athena_eye/backend)下，创建一个名为.venv的虚拟环境
uv venv

\# 激活该虚拟环境
source .venv/bin/activate
\`\`\`
激活后，你的命令行提示符前会出现`(.venv)`字样。

##\# 1.7 安装项目依赖
在激活的虚拟环境中，安装`pyproject.toml`中定义的所有依赖。
\`\`\`bash
\# -e . 表示以可编辑模式安装当前目录下的项目
uv pip install -e .
\`\`\`
至此，首次部署全部完成！

---

#\# 2. 日常管理

##\# 2.1 启动 Athena Eye (后台运行)
\`\`\`bash
\# 1. 确保你处于激活的虚拟环境中
\# (如果提示符前没有(.venv)，请先运行: source .venv/bin/activate)

\# 2. 创建一个名为 athena 的 screen 后台会话
screen -S athena

\# 3. 在新会话中，启动主程序
uv run -m athena_eye_project.main

\# 4. 脱离会话，让它在后台运行
\# 按下组合键: Ctrl+A, 然后松开, 再按 d
\`\`\`

##\# 2.2 检查运行状态

###\# 方法A：查看后台会话列表
\`\`\`bash
screen -ls
\`\`\`
-   如果看到 `(Detached)`，说明程序正在后台正常运行。
-   如果看到 `(Attached)`，说明你当前的终端正连接着该会话。
-   如果看到 `No Sockets found...`，说明没有任何程序在后台运行。

###\# 方法B：连接到会话，查看实时日志
\`\`\`bash
screen -r athena
\`\`\`
执行后，你会“进入”程序的运行界面，看到实时的日志输出。看完后，按`Ctrl+A`, `d`再次脱离。

##\# 2.3 安全停止 Athena Eye
\`\`\`bash
\# 1. 连接回正在运行的会话
screen -r athena

\# 2. 在程序日志滚动的界面，按下 Ctrl+C 来中断Python程序
\# 你会看到命令行提示符重新出现

\# 3. 输入 exit 并按回车，彻底关闭这个screen会话
exit
\`\`\`

---

#\# 3. 更新与维护 (标准流程)

当你需要**修改配置**或**更新代码**时，请严格遵循以下SOP：

1.  **回去**: `screen -r athena`
2.  **停止**: `Ctrl+C`
3.  **关闭**: `exit`
4.  **进目录**: `cd ~/athena_eye/backend`
5.  **激活环境**: `source .venv/bin/activate`
6.  **修改**: `nano .env` (修改配置) 或 `git pull` (更新代码)
7.  **新建**: `screen -S athena`
8.  **启动**: `uv run -m athena_eye_project.main`
9.  **离开**: `Ctrl+A`, `d`

---

#\# 4. 故障排查

##\# 4.1 问题：`screen -ls` 显示有多个同名会话
**原因**: 重复执行了`screen -S athena`而没有关闭旧会话。
**解决方案**:
\`\`\`bash
\# 1. 查看所有会话及其ID
screen -ls

\# 2. 假设你想杀死ID为 83675.athena 的旧会话
screen -X -S 83675.athena quit
\`\`\`

##\# 4.2 问题：`screen -ls` 显示 `(Attached)`，但无法 `Ctrl+A, d` 脱离
**原因**: 当前SSH连接“卡”在了会话里，无法通过常规快捷键脱离。
**解决方案**:
1.  **保持当前SSH窗口不动。**
2.  **打开一个全新的SSH窗口**，登录到同一台服务器。
3.  在新窗口中，执行强制脱离命令：
    \`\`\`bash
    screen -d athena
    \`\`\`
4.  回到原来的窗口，你会发现它已经被踢回了主终端。

---

#\# 5. `screen` 快捷键备忘录

所有命令都以“唤醒词” **`Ctrl+A`** 作为前缀。

-   **`Ctrl+A` `d`**: **D**etach，脱离当前会话（最常用）。
-   **`Ctrl+A` `c`**: **C**reate，在当前会话中创建新窗口（标签页）。
-   **`Ctrl+A` `n`**: **N**ext，切换到下一个窗口。
-   **`Ctrl+A` `p`**: **P**revious，切换到上一个窗口。
-   **`Ctrl+A` `k`**: **K**ill，杀死当前窗口。
-   **`Ctrl+A` `[`**: 进入滚动/复制模式，可以用方向键上翻查看历史日志，按`Esc`退出。
-   **`Ctrl+A` `?`**: 显示帮助信息。
````

## `frontend/.editorconfig`

```
[*.{js,jsx,mjs,cjs,ts,tsx,mts,cts,vue,css,scss,sass,less,styl}]
charset = utf-8
indent_size = 2
indent_style = space
insert_final_newline = true
trim_trailing_whitespace = true
end_of_line = lf
max_line_length = 100

```

## `frontend/.gitattributes`

```
* text=auto eol=lf

```

## `frontend/.gitignore`

```
# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

node_modules
.DS_Store
dist
dist-ssr
coverage
*.local

/cypress/videos/
/cypress/screenshots/

# Editor directories and files
.vscode/*
!.vscode/extensions.json
.idea
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?

*.tsbuildinfo

```

## `frontend/.prettierrc.json`

```json
{
  "$schema": "https://json.schemastore.org/prettierrc",
  "semi": false,
  "singleQuote": true,
  "printWidth": 100
}

```

## `frontend/Dockerfile`

```dockerfile
# frontend/Dockerfile
# 使用多阶段构建（Multi-stage build），保持最终镜像的轻量

# --- 第一阶段: 构建阶段 (Build Stage) ---
# 使用一个包含完整Node.js环境的镜像来构建我们的Vue项目
FROM node:20-alpine AS build-stage

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 package-lock.json (或 yarn.lock / pnpm-lock.yaml)
COPY package*.json ./

# 安装项目依赖
RUN npm install

# 复制所有前端源代码
COPY . .

# 执行构建命令，生成静态文件到 /app/dist 目录
RUN npm run build


# --- 第二阶段: 生产阶段 (Production Stage) ---
# 使用一个超轻量级的Nginx官方镜像作为我们的生产环境基础
FROM nginx:stable-alpine

# 将构建阶段生成的静态文件，复制到Nginx的默认网站根目录
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 【核心】复制我们自定义的Nginx配置文件
# 这个文件将告诉Nginx如何处理请求和反向代理
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露80端口
EXPOSE 80

# Nginx镜像的默认CMD就是启动Nginx服务，我们无需重写
```

## `frontend/eslint.config.js`

```javascript
import { defineConfig, globalIgnores } from 'eslint/config'
import globals from 'globals'
import js from '@eslint/js'
import pluginVue from 'eslint-plugin-vue'
import skipFormatting from '@vue/eslint-config-prettier/skip-formatting'

export default defineConfig([
  {
    name: 'app/files-to-lint',
    files: ['**/*.{js,mjs,jsx,vue}'],
  },

  globalIgnores(['**/dist/**', '**/dist-ssr/**', '**/coverage/**']),

  {
    languageOptions: {
      globals: {
        ...globals.browser,
      },
    },
  },

  js.configs.recommended,
  ...pluginVue.configs['flat/essential'],
  skipFormatting,
])

```

## `frontend/index.html`

```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8">
    <link rel="icon" href="/favicon.ico">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Athena Eye</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>

```

## `frontend/jsconfig.json`

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "exclude": ["node_modules", "dist"]
}

```

## `frontend/nginx.conf`

```
# frontend/nginx.conf
# Nginx 配置文件

server {
    # 监听80端口
    listen 80;
    # 默认的网站根目录，我们的Vue静态文件就在这里
    root /usr/share/nginx/html;
    # 默认首页文件
    index index.html;

    # --- API反向代理配置 ---
    # 所有以 /api/ 开头的请求，都转发给后端服务
    location /api/ {
        # proxy_pass 指令是反向代理的核心
        # http://backend:8000 中的 'backend' 是我们在docker-compose.prod.yml中定义的服务名
        # Docker的内部DNS会自动将其解析为后端容器的IP地址
        proxy_pass http://backend:8000;
        
        # --- 以下是反向代理的标准头部设置 ---
        # 将原始请求的Host头部传递给后端
        proxy_set_header Host $host;
        # 将客户端的真实IP地址传递给后端
        proxy_set_header X-Real-IP $remote_addr;
        # 传递代理服务器的IP地址列表
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        # 告诉后端是通过https还是http连接的
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # --- Vue Router history 模式配置 ---
    # 这是一个关键配置，用于解决Vue单页应用刷新页面时出现404的问题
    # 它匹配所有不以/api/开头，且不是一个真实存在的文件的请求
    location / {
        # 尝试按顺序查找文件：$uri (请求的URI) -> $uri/ (请求的目录) -> /index.html
        # 如果前两者都找不到，就回退到/index.html，让Vue Router来接管路由
        try_files $uri $uri/ /index.html;
    }
}
```

## `frontend/package.json`

```json
{
  "name": "vue-project",
  "version": "0.0.0",
  "private": true,
  "type": "module",
  "engines": {
    "node": "^20.19.0 || >=22.12.0"
  },
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --fix",
    "format": "prettier --write src/"
  },
  "dependencies": {
    "vue": "^3.5.18",
    "vue-router": "^4.5.1"
  },
  "devDependencies": {
    "@eslint/js": "^9.31.0",
    "@vitejs/plugin-vue": "^6.0.1",
    "@vue/eslint-config-prettier": "^10.2.0",
    "eslint": "^9.31.0",
    "eslint-plugin-vue": "~10.3.0",
    "globals": "^16.3.0",
    "prettier": "3.6.2",
    "vite": "^7.0.6",
    "vite-plugin-vue-devtools": "^8.0.0"
  }
}

```

## `frontend/README.md`

````text
\# vue-project

This template should help get you started developing with Vue 3 in Vite.

#\# Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

#\# Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

#\# Project Setup

\`\`\`sh
npm install
\`\`\`

##\# Compile and Hot-Reload for Development

\`\`\`sh
npm run dev
\`\`\`

##\# Compile and Minify for Production

\`\`\`sh
npm run build
\`\`\`

##\# Lint with [ESLint](https://eslint.org/)

\`\`\`sh
npm run lint
\`\`\`

````

## `frontend/src/App.vue`

```
<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <header>
    <div class="wrapper">
      <h1>Athena Eye - 智能监控面板</h1>
      <nav>
        <RouterLink to="/">控制面板</RouterLink>
        <RouterLink to="/config">系统配置</RouterLink>
        <RouterLink to="/archive">历史警报</RouterLink>
      </nav>
    </div>
  </header>

  <!-- RouterView是所有页面的“出口”，我们的页面组件将在这里被渲染 -->
  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
  border-bottom: 1px solid #ddd;
  margin-bottom: 2rem;
}

h1 {
  font-weight: bold;
  color: #2c3e50;
}

.wrapper {
  padding: 1rem 2rem;
}

nav {
  width: 100%;
  font-size: 1rem;
  text-align: left;
  margin-top: 1rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
  border-bottom: 2px solid hsla(160, 100%, 37%, 1);
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
  padding-left: 0;
}
</style>
```

## `frontend/src/assets/base.css`

```css
/* color palette from <https://github.com/vuejs/theme> */
:root {
  --vt-c-white: #ffffff;
  --vt-c-white-soft: #f8f8f8;
  --vt-c-white-mute: #f2f2f2;

  --vt-c-black: #181818;
  --vt-c-black-soft: #222222;
  --vt-c-black-mute: #282828;

  --vt-c-indigo: #2c3e50;

  --vt-c-divider-light-1: rgba(60, 60, 60, 0.29);
  --vt-c-divider-light-2: rgba(60, 60, 60, 0.12);
  --vt-c-divider-dark-1: rgba(84, 84, 84, 0.65);
  --vt-c-divider-dark-2: rgba(84, 84, 84, 0.48);

  --vt-c-text-light-1: var(--vt-c-indigo);
  --vt-c-text-light-2: rgba(60, 60, 60, 0.66);
  --vt-c-text-dark-1: var(--vt-c-white);
  --vt-c-text-dark-2: rgba(235, 235, 235, 0.64);
}

/* semantic color variables for this project */
:root {
  --color-background: var(--vt-c-white);
  --color-background-soft: var(--vt-c-white-soft);
  --color-background-mute: var(--vt-c-white-mute);

  --color-border: var(--vt-c-divider-light-2);
  --color-border-hover: var(--vt-c-divider-light-1);

  --color-heading: var(--vt-c-text-light-1);
  --color-text: var(--vt-c-text-light-1);

  --section-gap: 160px;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-background: var(--vt-c-black);
    --color-background-soft: var(--vt-c-black-soft);
    --color-background-mute: var(--vt-c-black-mute);

    --color-border: var(--vt-c-divider-dark-2);
    --color-border-hover: var(--vt-c-divider-dark-1);

    --color-heading: var(--vt-c-text-dark-1);
    --color-text: var(--vt-c-text-dark-2);
  }
}

*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  font-weight: normal;
}

body {
  min-height: 100vh;
  color: var(--color-text);
  background: var(--color-background);
  transition:
    color 0.5s,
    background-color 0.5s;
  line-height: 1.6;
  font-family:
    Inter,
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    Roboto,
    Oxygen,
    Ubuntu,
    Cantarell,
    'Fira Sans',
    'Droid Sans',
    'Helvetica Neue',
    sans-serif;
  font-size: 15px;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

```

## `frontend/src/assets/main.css`

```css
@import './base.css';

#app {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
  font-weight: normal;
}

a,
.green {
  text-decoration: none;
  color: hsla(160, 100%, 37%, 1);
  transition: 0.4s;
  padding: 3px;
}

@media (hover: hover) {
  a:hover {
    background-color: hsla(160, 100%, 37%, 0.2);
  }
}

@media (min-width: 1024px) {
  body {
    display: flex;
    place-items: center;
  }

  #app {
    display: grid;
    grid-template-columns: 1fr 1fr;
    padding: 0 2rem;
  }
}

```

## `frontend/src/main.js`

```javascript
import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(router)

app.mount('#app')

```

## `frontend/src/router/index.js`

```javascript
import { createRouter, createWebHistory } from 'vue-router'
// 我们将把默认的 HomeView 重命名为更有意义的 DashboardView
import DashboardView from '../views/DashboardView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView
    },
    // 我们为未来的页面先占好位置
    {
      path: '/config',
      name: 'config',
      // 路由懒加载：只有当用户访问这个页面时，才会加载对应的组件代码
      component: () => import('../views/ConfigView.vue')
    },
    {
        path: '/archive',
        name: 'archive',
        component: () => import('../views/ArchiveView.vue')
    }
  ]
})

export default router
```

## `frontend/src/views/ArchiveView.vue`

```
<script setup>
import { ref, onMounted, computed } from 'vue';

// --- 响应式变量 ---
const alerts = ref([]);            // 存储从API获取的所有警报记录
const selectedAlert = ref(null);   // 存储当前在弹窗中查看的警报详情
const isLoading = ref(true);
const error = ref(null);

// --- API 调用 ---
const fetchAlerts = async () => {
  isLoading.value = true;
  error.value = null;
  try {
    // 新的API端点，一次性获取所有警报数据
    const response = await fetch('/api/archive?limit=200'); // 获取最近200条
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || '无法加载历史警报');
    }
    const data = await response.json();
    // 后端返回的是倒序，我们前端可以根据需要再次排序或直接使用
    alerts.value = data;
  } catch (err) {
    error.value = err.message;
  } finally {
    isLoading.value = false;
  }
};

// --- 生命周期钩子 ---
onMounted(fetchAlerts);

// --- UI交互函数 ---
const viewDetails = (alert) => {
  // 点击“查看详情”按钮时，设置选中的警报，并显示弹窗
  selectedAlert.value = alert;
};

const closeDetailsModal = () => {
  // 关闭弹窗
  selectedAlert.value = null;
};

// --- 计算属性 ---
// 一个简单的计算属性，用于动态决定警报类型的颜色
const getAlertTypeClass = (alertType) => {
  if (alertType.includes('看涨') || alertType.includes('机会')) {
    return 'positive';
  }
  if (alertType.includes('看跌') || alertType.includes('风险')) {
    return 'negative';
  }
  return 'neutral';
};

</script>

<template>
  <main class="archive-view">
    <h2>历史警报记录</h2>

    <div v-if="isLoading" class="loading-state">正在从数据库加载记录...</div>
    <div v-if="error" class="error-msg">{{ error }}</div>

    <div v-if="!isLoading && alerts.length > 0" class="card">
      <table class="alerts-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>时间 (UTC)</th>
            <th>股票代码</th>
            <th>警报类型</th>
            <th class="reason-col">核心判断</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="alert in alerts" :key="alert.id">
            <td>{{ alert.id }}</td>
            <td>{{ new Date(alert.archive_timestamp_utc).toLocaleString('sv-SE') }}</td>
            <td><strong>{{ alert.ticker }}</strong></td>
            <td>
              <span :class="['alert-type-badge', getAlertTypeClass(alert.alert_type)]">
                {{ alert.alert_type }}
              </span>
            </td>
            <td class="reason-col">{{ alert.reason }}</td>
            <td>
              <button @click="viewDetails(alert)" class="details-btn">查看详情</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="!isLoading && alerts.length === 0 && !error" class="placeholder">
      数据库中还没有任何警报记录。
    </div>

    <!-- 详情弹窗 (Modal) -->
    <div v-if="selectedAlert" class="modal-overlay" @click.self="closeDetailsModal">
      <div class="modal-content card">
        <button class="close-btn" @click="closeDetailsModal">&times;</button>
        <h3>警报详情 (ID: {{ selectedAlert.id }})</h3>
        <div class="details-grid">
          <p><strong>股票:</strong> {{ selectedAlert.ticker }}</p>
          <p><strong>类型:</strong> {{ selectedAlert.alert_type }}</p>
          <p><strong>时间:</strong> {{ new Date(selectedAlert.archive_timestamp_utc).toLocaleString() }}</p>
          <p class="full-width"><strong>核心判断:</strong> {{ selectedAlert.reason }}</p>
        </div>

        <details open>
          <summary>三维分析快照</summary>
          <div class="snapshot-grid">
            <span><strong>价格变化:</strong> {{ selectedAlert.price_change_percent }}%</span>
            <span><strong>成交量倍数:</strong> {{ selectedAlert.volume_multiplier }}x</span>
            <span><strong>情绪评分:</strong> {{ selectedAlert.sentiment_score }}/10</span>
          </div>
        </details>

        <details>
          <summary>触发时系统参数</summary>
          <pre>{{ JSON.stringify(selectedAlert.trigger_conditions, null, 2) }}</pre>
        </details>

        <details v-if="selectedAlert.raw_news_data && selectedAlert.raw_news_data.length > 0">
          <summary>原始新闻数据</summary>
          <ul>
            <li v-for="(news, index) in selectedAlert.raw_news_data" :key="index" class="news-item">
              <a :href="news.link" target="_blank" rel="noopener noreferrer">{{ news.title }}</a>
              <span v-if="news.source" class="news-source"> ({{ news.source }})</span>
            </li>
          </ul>
        </details>
      </div>
    </div>

  </main>
</template>

<style scoped>
/* --- 主布局与卡片 --- */
.archive-view {
  padding: 0 1rem;
  width: 100%;
}
.card {
  background-color: #ffffff;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  overflow-x: auto; /* 让表格可以横向滚动 */
}

/* --- 表格样式 --- */
.alerts-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}
.alerts-table th, .alerts-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #e0e0e0;
  vertical-align: middle;
}
.alerts-table th {
  background-color: #f8f9fa;
  font-weight: bold;
  color: #343a40;
}
.alerts-table tbody tr:hover {
  background-color: #f1f3f5;
}
.reason-col {
  max-width: 400px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.details-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}
.details-btn:hover {
  background-color: #0056b3;
}

/* --- 警报类型徽章 --- */
.alert-type-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8em;
  font-weight: bold;
  color: #fff;
}
.alert-type-badge.positive { background-color: #28a745; }
.alert-type-badge.negative { background-color: #dc3545; }
.alert-type-badge.neutral { background-color: #6c757d; }

/* --- 状态提示 --- */
.loading-state, .placeholder {
  text-align: center;
  padding: 3rem;
  color: #6c757d;
  font-size: 1.2rem;
}
.error-msg {
  color: #dc3545;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  padding: 1rem;
  border-radius: 5px;
  text-align: center;
}

/* --- 详情弹窗 (Modal) --- */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.modal-content {
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
}
.close-btn {
  position: absolute;
  top: 15px;
  right: 15px;
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #6c757d;
}
.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}
.full-width { grid-column: 1 / -1; }
details {
  margin-top: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 0.8rem;
}
summary { font-weight: bold; cursor: pointer; }
pre { background-color: #f5f5f5; padding: 1rem; border-radius: 5px; white-space: pre-wrap; word-break: break-all; margin-top: 0.5rem; }
.snapshot-grid { display: flex; gap: 2rem; margin-top: 0.5rem; }
.news-item { font-size: 0.9em; margin-top: 0.5rem; }
.news-item a { color: #007bff; text-decoration: none; }
.news-item a:hover { text-decoration: underline; }
.news-source { color: #6c757d; font-style: italic; }
strong { font-weight: bold; }
</style>
```

## `frontend/src/views/ConfigView.vue`

```
<script setup>
import { ref, onMounted } from 'vue'

const config = ref({}); // 用于存储配置项
const isLoading = ref(true); // 控制加载状态
const message = ref(''); // 用于显示反馈信息
const messageType = ref(''); // success 或 error

// 获取当前配置
const fetchConfig = async () => {
  isLoading.value = true;
  message.value = '';
  try {
    const response = await fetch('/api/config');
    if (!response.ok) throw new Error('无法加载配置');
    config.value = await response.json();
  } catch (error) {
    message.value = `错误: ${error.message}`;
    messageType.value = 'error';
  } finally {
    isLoading.value = false;
  }
};

// 保存配置
const saveConfig = async () => {
  isLoading.value = true;
  message.value = '正在保存...';
  messageType.value = 'info';
  try {
    const response = await fetch('/api/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config.value)
    });
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || '保存失败');
    }
    await response.json();
    message.value = '配置已成功保存！请注意，部分更改可能需要重启后台监控任务才能生效。';
    messageType.value = 'success';
  } catch (error) {
    message.value = `错误: ${error.message}`;
    messageType.value = 'error';
  } finally {
    isLoading.value = false;
  }
};

onMounted(fetchConfig);
</script>

<template>
  <main class="config-view">
    <h2>系统配置</h2>
    <div class="card">
      <div v-if="isLoading && !Object.keys(config).length">正在加载配置...</div>
      <form v-else @submit.prevent="saveConfig">
        <div v-for="(value, key) in config" :key="key" class="form-group">
          <label :for="key">{{ key.replaceAll('_', ' ') }}</label>
          <input 
            :id="key"
            :type="typeof value === 'number' ? 'number' : 'text'"
            v-model="config[key]"
            :step="typeof value === 'number' && !Number.isInteger(value) ? '0.1' : '1'"
          />
        </div>
        <button type="submit" class="save-btn" :disabled="isLoading">
          {{ isLoading ? '保存中...' : '保存更改' }}
        </button>
      </form>
      <div v-if="message" :class="['message', messageType]">
        {{ message }}
      </div>
    </div>
  </main>
</template>

<style scoped>
.config-view { padding: 0 2rem; }
.card { background-color: #fff; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.form-group { margin-bottom: 1.5rem; }
label { display: block; margin-bottom: 0.5rem; font-weight: bold; text-transform: capitalize; color: #555; }
input { width: 100%; padding: 0.8rem; border: 1px solid #ccc; border-radius: 4px; font-size: 1rem; }
.save-btn { background-color: #007bff; color: white; padding: 0.8rem 1.5rem; border: none; border-radius: 5px; cursor: pointer; font-size: 1rem; transition: background-color 0.3s; }
.save-btn:hover:not(:disabled) { background-color: #0056b3; }
.save-btn:disabled { background-color: #aaa; cursor: not-allowed; }
.message { margin-top: 1rem; padding: 1rem; border-radius: 5px; }
.message.success { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
.message.error { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
.message.info { background-color: #cce5ff; color: #004085; border: 1px solid #b8daff; }
</style>
```

## `frontend/src/views/DashboardView.vue`

```
<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// --- 响应式变量 ---
const statusText = ref('正在加载...');
const isRunning = ref(false);
const watchlist = ref([]);
const isLoading = ref(false); // 用于控制按钮的禁用状态
let statusInterval = null; // 用于存放我们的定时器

// --- 股票管理相关变量 ---
const stockList = ref([]);
const newStockTicker = ref('');
const newStockNotes = ref('');
const isStockLoading = ref(false);
const showAddStock = ref(false);

// --- API 调用函数 ---

// 获取股票列表
const fetchStocks = async () => {
  try {
    const response = await fetch('/api/stocks');
    if (!response.ok) throw new Error('获取股票列表失败');
    const data = await response.json();
    stockList.value = data.stocks;
  } catch (error) {
    console.error('获取股票列表失败:', error);
  }
};

// 添加股票
const addStock = async () => {
  if (!newStockTicker.value.trim()) return;
  
  isStockLoading.value = true;
  try {
    const response = await fetch('/api/stocks/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ticker: newStockTicker.value.toUpperCase().trim(),
        is_active: true,
        notes: newStockNotes.value.trim() || null
      })
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || '添加股票失败');
    }
    
    // 重新获取股票列表和状态
    await fetchStocks();
    await fetchStatus();
    
    // 清空输入框
    newStockTicker.value = '';
    newStockNotes.value = '';
    showAddStock.value = false;
  } catch (error) {
    console.error('添加股票失败:', error);
    alert('添加股票失败: ' + error.message);
  } finally {
    isStockLoading.value = false;
  }
};

// 删除股票
const removeStock = async (ticker) => {
  if (!confirm(`确定要删除股票 ${ticker} 吗？`)) return;
  
  isStockLoading.value = true;
  try {
    const response = await fetch(`/api/stocks/${ticker}`, {
      method: 'DELETE'
    });
    
    if (!response.ok) throw new Error('删除股票失败');
    
    // 重新获取股票列表和状态
    await fetchStocks();
    await fetchStatus();
  } catch (error) {
    console.error('删除股票失败:', error);
    alert('删除股票失败: ' + error.message);
  } finally {
    isStockLoading.value = false;
  }
};

// 切换股票启用状态
const toggleStock = async (stock) => {
  isStockLoading.value = true;
  try {
    const response = await fetch(`/api/stocks/${stock.ticker}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...stock,
        is_active: !stock.is_active
      })
    });
    
    if (!response.ok) throw new Error('更新股票状态失败');
    
    // 重新获取股票列表和状态
    await fetchStocks();
    await fetchStatus();
  } catch (error) {
    console.error('更新股票状态失败:', error);
    alert('更新股票状态失败: ' + error.message);
  } finally {
    isStockLoading.value = false;
  }
};

// 获取系统状态
const fetchStatus = async () => {
  try {
    const response = await fetch('/api/control/status');
    if (!response.ok) throw new Error('网络响应错误');
    const data = await response.json();
    isRunning.value = data.is_running;
    statusText.value = data.is_running ? '运行中' : '已停止';
    watchlist.value = data.monitoring_watchlist;
  } catch (error) {
    console.error('获取状态失败:', error);
    statusText.value = '获取状态失败 (请确保后端服务已运行)';
  }
};

// 启动监控
const startMonitor = async () => {
  if (isRunning.value) return; // 如果已在运行，则不执行
  isLoading.value = true;
  statusText.value = '正在启动...';
  try {
    const response = await fetch('/api/control/start', { method: 'POST' });
    if (!response.ok) throw new Error('启动请求失败');
    // 请求成功后，我们立即刷新一次状态，而不是等待轮询
    await fetchStatus(); 
  } catch (error) {
    console.error('启动监控失败:', error);
    statusText.value = '启动失败';
  } finally {
    isLoading.value = false;
  }
};

// 停止监控
const stopMonitor = async () => {
  if (!isRunning.value) return; // 如果已停止，则不执行
  isLoading.value = true;
  statusText.value = '正在停止...';
  try {
    const response = await fetch('/api/control/stop', { method: 'POST' });
    if (!response.ok) throw new Error('停止请求失败');
    await fetchStatus();
  } catch (error) {
    console.error('停止监控失败:', error);
    statusText.value = '停止失败';
  } finally {
    isLoading.value = false;
  }
};


// --- 生命周期钩子 ---

// onMounted: 组件加载后执行
onMounted(() => {
  fetchStatus(); // 立即获取一次状态
  fetchStocks(); // 获取股票列表
  // 设置一个定时器，每5秒自动刷新一次状态
  statusInterval = setInterval(fetchStatus, 5000); 
});

// onUnmounted: 组件被销毁前执行 (例如切换到其他页面)
onUnmounted(() => {
  // 清除定时器，防止内存泄漏
  clearInterval(statusInterval); 
});

</script>

<template>
  <main class="dashboard">
    <h2>系统状态</h2>

    <div class="status-card">
      <div class="status-indicator" :class="{ 'running': isRunning, 'stopped': !isRunning }"></div>
      <span class="status-text">{{ statusText }}</span>
    </div>

    <div v-if="watchlist.length > 0" class="watchlist-card">
      <h3>当前监控列表:</h3>
      <ul>
        <li v-for="ticker in watchlist" :key="ticker">{{ ticker }}</li>
      </ul>
    </div>

    <!-- 股票管理卡片 -->
    <div class="stock-management-card">
      <div class="card-header">
        <h3>股票管理</h3>
        <button 
          @click="showAddStock = !showAddStock" 
          class="add-btn"
          :disabled="isStockLoading">
          {{ showAddStock ? '取消' : '添加股票' }}
        </button>
      </div>

      <!-- 添加股票表单 -->
      <div v-if="showAddStock" class="add-stock-form">
        <div class="form-row">
          <input 
            v-model="newStockTicker" 
            placeholder="股票代码 (如: AAPL)" 
            class="stock-input"
            @keyup.enter="addStock"
            :disabled="isStockLoading">
          <input 
            v-model="newStockNotes" 
            placeholder="备注 (可选)" 
            class="notes-input"
            @keyup.enter="addStock"
            :disabled="isStockLoading">
          <button 
            @click="addStock" 
            class="control-btn start-btn"
            :disabled="!newStockTicker.trim() || isStockLoading">
            {{ isStockLoading ? '添加中...' : '确认添加' }}
          </button>
        </div>
      </div>

      <!-- 股票列表 -->
      <div class="stock-list">
        <div v-if="stockList.length === 0" class="empty-state">
          暂无监控股票，点击"添加股票"开始配置
        </div>
        <div v-else>
          <div 
            v-for="stock in stockList" 
            :key="stock.ticker" 
            class="stock-item"
            :class="{ 'inactive': !stock.is_active }">
            <div class="stock-info">
              <span class="stock-ticker">{{ stock.ticker }}</span>
              <span v-if="stock.notes" class="stock-notes">{{ stock.notes }}</span>
            </div>
            <div class="stock-actions">
              <button 
                @click="toggleStock(stock)" 
                class="toggle-btn"
                :class="{ 'active': stock.is_active }"
                :disabled="isStockLoading">
                {{ stock.is_active ? '启用' : '禁用' }}
              </button>
              <button 
                @click="removeStock(stock.ticker)" 
                class="remove-btn"
                :disabled="isStockLoading">
                删除
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="controls-card">
        <h3>系统控制</h3>
        <!-- 核心升级：为按钮绑定点击事件和禁用状态 -->
        <button 
          @click="startMonitor" 
          :disabled="isRunning || isLoading" 
          class="control-btn start-btn">
          {{ isLoading && !isRunning ? '启动中...' : '启动监控' }}
        </button>
        <button 
          @click="stopMonitor" 
          :disabled="!isRunning || isLoading" 
          class="control-btn stop-btn">
          {{ isLoading && isRunning ? '停止中...' : '停止监控' }}
        </button>
    </div>
  </main>
</template>

<style scoped>
/* ... (样式部分完全不变) ... */
.dashboard {
  padding: 0 2rem;
}
.status-card {
  display: flex;
  align-items: center;
  background-color: #f5f7fa;
  padding: 1rem;
  border-radius: 8px;
  font-size: 1.2rem;
  margin-bottom: 2rem;
}
.status-indicator {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  margin-right: 1rem;
  animation: pulse 2s infinite;
}
.status-indicator.running {
  background-color: #28a745;
}
.status-indicator.stopped {
  background-color: #dc3545;
  animation: none;
}
.watchlist-card, .controls-card {
    background-color: #fff;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
}
.watchlist-card ul {
    list-style: none;
    padding: 0;
    display: flex;
    flex-wrap: wrap;
}
.watchlist-card li {
    background-color: #eef;
    padding: 0.5rem 1rem;
    margin: 0.5rem;
    border-radius: 20px;
    font-weight: bold;
}
.control-btn {
    padding: 0.8rem 1.5rem;
    border: none;
    border-radius: 5px;
    color: white;
    font-size: 1rem;
    cursor: pointer;
    margin-right: 1rem;
    transition: all 0.3s ease;
}
.control-btn:disabled {
    cursor: not-allowed;
    opacity: 0.5;
}
.start-btn {
    background-color: #28a745;
}
.start-btn:hover:not(:disabled) {
    background-color: #218838;
}
.stop-btn {
    background-color: #dc3545;
}
.stop-btn:hover:not(:disabled) {
    background-color: #c82333;
}
/* 股票管理样式 */
.stock-management-card {
    background-color: #fff;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.add-btn {
    padding: 0.5rem 1rem;
    border: 2px solid #007bff;
    border-radius: 5px;
    background-color: transparent;
    color: #007bff;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.3s ease;
}

.add-btn:hover:not(:disabled) {
    background-color: #007bff;
    color: white;
}

.add-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.add-stock-form {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 5px;
    margin-bottom: 1rem;
}

.form-row {
    display: flex;
    gap: 1rem;
    align-items: center;
}

.stock-input, .notes-input {
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
}

.stock-input {
    flex: 0 0 150px;
    text-transform: uppercase;
}

.notes-input {
    flex: 1;
}

.stock-input:disabled, .notes-input:disabled {
    background-color: #f5f5f5;
    cursor: not-allowed;
}

.empty-state {
    text-align: center;
    color: #666;
    padding: 2rem;
    font-style: italic;
}

.stock-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border: 1px solid #eee;
    border-radius: 5px;
    margin-bottom: 0.5rem;
    transition: all 0.3s ease;
}

.stock-item:hover {
    background-color: #f8f9fa;
}

.stock-item.inactive {
    opacity: 0.6;
    background-color: #f5f5f5;
}

.stock-info {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.stock-ticker {
    font-weight: bold;
    font-size: 1.1rem;
    color: #333;
}

.stock-notes {
    font-size: 0.9rem;
    color: #666;
    font-style: italic;
}

.stock-actions {
    display: flex;
    gap: 0.5rem;
}

.toggle-btn {
    padding: 0.4rem 0.8rem;
    border: 1px solid #28a745;
    border-radius: 4px;
    background-color: transparent;
    color: #28a745;
    font-size: 0.8rem;
    cursor: pointer;
    transition: all 0.3s ease;
}

.toggle-btn.active {
    background-color: #28a745;
    color: white;
}

.toggle-btn:not(.active) {
    border-color: #6c757d;
    color: #6c757d;
}

.toggle-btn:hover:not(:disabled) {
    background-color: #28a745;
    color: white;
}

.remove-btn {
    padding: 0.4rem 0.8rem;
    border: 1px solid #dc3545;
    border-radius: 4px;
    background-color: transparent;
    color: #dc3545;
    font-size: 0.8rem;
    cursor: pointer;
    transition: all 0.3s ease;
}

.remove-btn:hover:not(:disabled) {
    background-color: #dc3545;
    color: white;
}

.toggle-btn:disabled, .remove-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

@keyframes pulse {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(40, 167, 69, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(40, 167, 69, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(40, 167, 69, 0); }
}
</style>
```

## `frontend/vite.config.js`

```javascript
import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  // --- 新增的代理配置 ---
  server: {
    host: 'localhost', // 只允许本地访问
    port: 5173, // 使用 Vite 默认端口
    proxy: {
      // 字符串简写写法
      // '/api': 'http://localhost:8000',

      // 选项写法，更灵活
      '/api': {
        target: 'http://localhost:9000', // 目标后端服务地址
        changeOrigin: true, // 需要虚拟主机站点
        // 如果你的后端API路径没有 /api 前缀，可以用这个重写
        // rewrite: (path) => path.replace(/^\/api/, '')
      },
    },
  },
})

```

## `README.md`

````text
\# Athena Eye V3 - 智能美股异动监控系统 (全栈容器化版)

**Athena Eye** 是一个基于Docker容器化部署的全栈、高度可配置的智能监控系统。它旨在实时分析美股市场的**量、价、情绪**三维信息，捕捉潜在的机构投资者活动，并通过邮件向用户发送即时警报。

该项目已完成从本地开发到云端生产环境的完整部署，融合了专业的软件工程实践、量化交易策略和大型语言模型（LLM）的认知能力，形成了一套稳定、可靠、可扩展的自动化交易信号解决方案。

---

#\# 核心架构
\`\`\`
athena_eye/
├── backend
│   ├── archive
│   │   └── 2025-08-04
│   │       └── 20250804_084829_PERFECTCO_主力入场（强烈看涨）.json
│   ├── athena_eye_project
│   │   ├── analysis
│   │   │   ├── __init__.py
│   │   │   ├── decision_engine.py
│   │   │   ├── sentiment.py
│   │   │   └── volume_price.py
│   │   ├── archiving
│   │   │   └── archiver.py
│   │   ├── config
│   │   │   ├── __init__.py
│   │   │   ├── settings.py
│   │   │   ├── stock_manager.py
│   │   │   └── stocks.json
│   │   ├── data_ingestion
│   │   │   ├── __init__.py
│   │   │   └── fetcher.py
│   │   ├── db
│   │   │   ├── database.py
│   │   │   └── models.py
│   │   ├── notifications
│   │   │   ├── __init__.py
│   │   │   └── email_sender.py
│   │   ├── utils
│   │   │   ├── __init__.py
│   │   │   └── logger.py
│   │   ├── __init__.py
│   │   ├── background_worker.py
│   │   ├── main.py
│   │   └── main_api.py
│   ├── logs
│   ├── tests
│   ├── .python-version
│   ├── athena_eye.db
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend
│   ├── public
│   ├── src
│   │   ├── assets
│   │   │   ├── base.css
│   │   │   └── main.css
│   │   ├── components
│   │   ├── router
│   │   │   └── index.js
│   │   ├── views
│   │   │   ├── ArchiveView.vue
│   │   │   ├── ConfigView.vue
│   │   │   └── DashboardView.vue
│   │   ├── App.vue
│   │   └── main.js
│   ├── .editorconfig
│   ├── .gitattributes
│   ├── .gitignore
│   ├── .prettierrc.json
│   ├── Dockerfile
│   ├── eslint.config.js
│   ├── index.html
│   ├── jsconfig.json
│   ├── nginx.conf
│   ├── package.json
│   ├── README.md
│   └── vite.config.js
├── test
├── .gitignore
├── docker-compose.prod.yml
├── docker-compose.yml
├── GCP_DEPLOY_MANUAL.md
├── LINUX_OPERATOR_MANUAL.md
└── README.md
\`\`\`

---

#\# 核心架构

系统采用现代化的全栈容器化架构，通过`Docker Compose`进行编排：

*   **前端 (Frontend)**:
    *   **技术栈**: Vue 3 + Vite
    *   **部署**: 通过多阶段`Dockerfile`构建，最终部署在一个超轻量级的`Nginx`镜像中。
    *   **职责**: 提供用户交互界面，包括系统状态监控、参数在线配置、历史警报查阅。

*   **反向代理 (Reverse Proxy)**:
    *   **技术**: Nginx
    *   **职责**: 作为系统的统一入口，监听80端口，将静态文件请求（如`/`）指向前端应用，并将所有API请求（如`/api/*`）无缝反向代理到后端服务。

*   **后端 (Backend)**:
    *   **技术栈**: Python 3.12, FastAPI, Gunicorn, SQLAlchemy
    *   **部署**: 部署在一个基于`python-slim`的轻量级Docker镜像中，由Gunicorn管理多个Uvicorn worker进程，保证高并发性能。
    *   **职责**: 执行核心业务逻辑，包括数据采集、分析、决策、通知，并通过API与前端和数据库交互。

*   **数据库 (Database)**:
    *   **技术**: **SQLite** (嵌入式数据库)
    *   **部署**: 作为后端服务的一部分运行，数据库文件通过Docker Volume进行持久化，实现零服务、零内存占用的数据存储。
    *   **职责**: 持久化存储最新的500条警报记录，为历史回顾和数据分析提供支持。

---

#\# 核心特性

*   **一键式部署**: 在任何安装了Docker的Linux服务器上，通过一条`docker compose`命令即可启动整个全栈应用。
*   **生产级服务**: 后端使用`Gunicorn`进行进程管理，数据库采用零配置的`SQLite`，确保在云端服务器上7x24小时稳定运行。
*   **Web控制台**: 提供功能完善的前端界面，实现对整个系统的**远程可视化管理**，包括启停、参数调整和历史查阅。
*   **数据持久化**: 所有警报记录都存储在健壮的SQLite数据库文件中，并通过数据卷保证数据安全。
*   **三维分析引擎**: 独创性地结合**成交量异动**、**K线价格变化**和**AI新闻市场情绪**，识别复杂的市场博弈。
*   **自动维护**: 系统会自动清理旧的警报记录，仅保留最新的500条，防止数据库文件无限膨胀。

---

#\# 云端部署 (Google Cloud Platform)

本项目已在GCP上成功部署并稳定运行。推荐的部署流程和服务器配置如下。

##\# 1. 服务器推荐配置
*   **实例类型**: **`e2-small` (2 vCPU, 2 GB 内存) 或更高**。
    *   **重要教训**: `e2-micro` (1 GB 内存) **不足以**稳定运行本项目的完整技术栈，会导致MySQL或SSH服务因内存不足而随机崩溃。
*   **操作系统**: **Ubuntu 22.04 LTS** 或 Debian 12。
*   **防火墙**: 务必开放`TCP`协议的`80`, `443`, `22`端口。

##\# 2. 部署流程
详细的、经过实战检验的部署步骤，请严格参考项目中的权威手册：
**`DOCKER_LINUX_DEPLOY_MANUAL.md`**

该手册涵盖了从服务器初始化、Docker安装，到项目克隆、配置、一键启动、日常运维和故障排查的所有环节。

---

#\# 项目总结：关键经验与教训

1.  **资源规划是基石**: 生产环境的稳定性，始于充足的计算资源。低估内存需求是导致云端部署失败的最主要原因。
2.  **环境隔离是保障**: 本地开发环境与云端生产环境存在巨大差异。Docker是解决“在我电脑上明明是好的”这一经典问题的最有效工具。
3.  **日志是真相的唯一来源**: 无论是应用日志(`docker logs`)还是系统日志(`串行端口`)，都是在遇到问题时定位根源的最终依据。
4.  **细节决定成败**: 从`Dockerfile`中的一个`mkdir`命令，到`my.cnf`中一行业首的注释，再到`screen`会话的权限继承机制，都可能成为影响整个系统成败的关键。\`\`\``

###\# `DOCKER_LINUX_DEPLOY_MANUAL.md`
*(变更：移除了关于创建`my.cnf`的步骤，并更新了故障排查部分)*
````

