import tweepy
from telegram import Bot
import time

# Twitter API credentials (replace with your own)
TWITTER_BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAH6hxgEAAAAAMueN4cwwP3M9uOILfaitKDLqhYs%3DOYcVUTvXjopNGljNGxHfYsgXFralWlZoNJKQoJcE7KszAwXnXK'

# Telegram Bot Token and Chat ID
TELEGRAM_BOT_TOKEN = '7554759873:AAE8xW4IMPZuamLSO6ZSYMQaf7vhvR75fhc'
TELEGRAM_CHAT_ID = 'NovaCallsBot'  # Replace with your Telegram user or group chat ID

# The Twitter username to monitor
TWITTER_USER = 'sullyfromDeets'  # Replace with the username you want to monitor

# Initialize Telegram Bot
telegram_bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Define a StreamClient class for real-time tweet monitoring
class MyStreamClient(tweepy.StreamingClient):
    def __init__(self, bearer_token, telegram_bot, twitter_username, chat_id):
        super().__init__(bearer_token)
        self.telegram_bot = telegram_bot
        self.twitter_username = twitter_username
        self.chat_id = chat_id
        self.user_id = None

        # Get the Twitter user ID of the monitored account
        client = tweepy.Client(bearer_token=bearer_token)
        user = client.get_user(username=self.twitter_username)
        if user and user.data:
            self.user_id = user.data.id
        else:
            raise ValueError(f"Could not find user with username: {self.twitter_username}")

    def on_tweet(self, tweet):
        # Filter tweets from the specific user
        if tweet.author_id == self.user_id:
            tweet_link = f"https://twitter.com/{self.twitter_username}/status/{tweet.id}"
            message = f"New tweet from @{self.twitter_username}:\n\n{tweet.text}\n\n{tweet_link}"
            self.telegram_bot.send_message(chat_id=self.chat_id, text=message)
            print(f"Sent message: {message}")

    def on_error(self, status_code):
        print(f"Error: {status_code}")
        if status_code == 420:  # Rate limit
            return False
        return True

# Initialize the streaming client
try:
    print("Starting Twitter stream...")
    stream_client = MyStreamClient(
        bearer_token=TWITTER_BEARER_TOKEN,
        telegram_bot=telegram_bot,
        twitter_username=TWITTER_USER,
        chat_id=TELEGRAM_CHAT_ID
    )

    # Clear existing rules
    existing_rules = stream_client.get_rules()
    if existing_rules.data:
        rule_ids = [rule.id for rule in existing_rules.data]
        stream_client.delete_rules(rule_ids)

    # Add a rule to monitor the specific user's tweets
    stream_client.add_rules(tweepy.StreamRule(value=f"from:{TWITTER_USER}"))

    # Start the stream
    stream_client.filter()

except Exception as e:
    print(f"Error: {e}")
