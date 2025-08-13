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

# === 新增：数据库配置 ===
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_NAME = os.getenv("MYSQL_DATABASE")

# 构建SQLAlchemy数据库连接URL
# 开发环境使用SQLite，生产环境使用MySQL
if os.getenv("ENVIRONMENT", "development") == "development":
    DATABASE_URL = "sqlite:///./athena_eye.db"
else:
    DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

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
    
    # 生产环境需要MySQL配置
    if os.getenv("ENVIRONMENT", "development") != "development":
        required_vars.update({
            "MYSQL_USER": DB_USER,
            "MYSQL_PASSWORD": DB_PASSWORD,
            "MYSQL_DATABASE": DB_NAME,
        })

    missing_vars = [key for key, value in required_vars.items() if not value]
    if missing_vars:
        raise ValueError(f"错误：缺少必要的配置: {', '.join(missing_vars)}. 请检查 .env 文件。")
    # 注意：不再验证STOCK_WATCHLIST，因为现在使用JSON文件管理股票列表