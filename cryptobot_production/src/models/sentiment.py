import openai
import os
from typing import Dict
from utils.logger import get_logger

logger = get_logger(__name__)

class SentimentAnalyzer:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("SENTIMENT_ANALYSIS_MODEL", "gpt-4")
        
    async def analyze(self, symbols: list = None) -> Dict[str, float]:
        """Returns sentiment scores between -1 (bearish) and 1 (bullish)"""
        if symbols is None:
            symbols = [os.getenv("BASE_PAIR", "BTC/USDT")]
            
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[{
                    "role": "system",
                    "content": "Analyze crypto market sentiment. Respond with only a JSON object containing scores."
                }],
                temperature=0.2
            )
            return self._parse_response(response)
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return {sym: 0 for sym in symbols}  # Neutral on error
            
    def _parse_response(self, response) -> Dict[str, float]:
        """Parse and validate the AI response"""
        try:
            content = response.choices[0].message.content
            return {k: max(-1, min(1, float(v))) for k,v in content.items()}
        except:
            logger.warning("Invalid sentiment response format")
            return {}