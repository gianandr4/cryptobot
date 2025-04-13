import openai

def analyze_sentiment(price):
    # Use OpenAI GPT-4 to analyze market sentiment based on the current price
    prompt = f"Analyze the sentiment of the market based on the current price of BTC: {price}"
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=60
    )
    sentiment = response['choices'][0]['text'].strip()
    return sentiment
