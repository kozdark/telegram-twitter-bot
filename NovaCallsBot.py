import tweepy
from telegram import Bot

# Twitter API keys
TWITTER_API_KEY = 'ZqSbHnlqxRsEj2po0jd7EAxlr'
TWITTER_API_SECRET = 'Yd6rP5oIvipEU2rz9CgMKMabWL6elb02ttNQ6FY1ylROdFOcI3'
TWITTER_BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAH6hxgEAAAAA%2BG3HcH6cXYW8%2FhuRAckyGNgURNA%3DMycOROeCJqt2dIpuh4AvROlVVti0LWtMveyef6zjKtP8CzwjEE'

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = '7554759873:AAE8xW4IMPZuamLSO6ZSYMQaf7vhvR75fhc'
TELEGRAM_CHAT_ID = 'NovaCallsBot'  # Replace with your Telegram user or group chat ID

# Initialize Telegram Bot
telegram_bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Account to monitor
TWITTER_USER = 'sullyfromDeets'  # Replace with the Twitter username

# Define a StreamClient class for real-time tweet monitoring (for Tweepy v4.x+)
class MyStreamClient(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        print(f"Tweet detected: {tweet.text}")
        message = f"New tweet from @{TWITTER_USER}:\n\n{tweet.text}\n\nLink: https://twitter.com/{TWITTER_USER}/status/{tweet.id}"
        telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

    def on_error(self, status_code):
        print(f"Error: {status_code}")
        return True

# Set up the Twitter stream
client = MyStreamClient(bearer_token=TWITTER_BEARER_TOKEN)

try:
    # Clear existing rules
    existing_rules = client.get_rules()
    if existing_rules.data:
        rule_ids = [rule.id for rule in existing_rules.data]
        client.delete_rules(rule_ids)

    # Add a new rule to filter by the user's tweets
    client.add_rules(tweepy.StreamRule(f"from:{TWITTER_USER}"))

    print(f"Listening for new tweets from @{TWITTER_USER}...")
    client.filter()
except Exception as e:
    print(f"Error starting the stream: {e}")
