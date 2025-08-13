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