
import openai

class MarketSentiment:
    def __init__(self):
        openai.api_key = 'your_openai_api_key'
    
    def analyze_sentiment(self):
        response = openai.Completion.create(
            engine="gpt-4",
            prompt="Analyze market sentiment for Bitcoin trading:",
            max_tokens=60
        )
        sentiment = response.choices[0].text.strip()
        return sentiment
    
    def adjust_grid(self, sentiment):
        # Adjust grid size based on sentiment (simplified example)
        if sentiment.lower() == "bullish":
            return 100
        elif sentiment.lower() == "bearish":
            return 50
        else:
            return 75
