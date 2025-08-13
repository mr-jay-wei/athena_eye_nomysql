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