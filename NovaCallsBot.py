import tweepy
from telegram import Bot

# Twitter API keys
TWITTER_API_KEY = 'ZqSbHnlqxRsEj2po0jd7EAxlr'
TWITTER_API_SECRET = 'Yd6rP5oIvipEU2rz9CgMKMabWL6elb02ttNQ6FY1ylROdFOcI3'
TWITTER_ACCESS_TOKEN = '1516153749244362760-EJaUXObu6Ci2uxDGnQu5rpI1aHTxCu'
TWITTER_ACCESS_SECRET = 'Wzvzf2JnYIPV2Ls8RePIjyCLOShr7Qpal2UR3ay2J3Gww'
TWITTER_BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAH6hxgEAAAAA%2BG3HcH6cXYW8%2FhuRAckyGNgURNA%3DMycOROeCJqt2dIpuh4AvROlVVti0LWtMveyef6zjKtP8CzwjEE'

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = '7554759873:AAE8xW4IMPZuamLSO6ZSYMQaf7vhvR75fhc'
TELEGRAM_CHAT_ID = 'NovaCallsBot'  # Replace with your Telegram user or group chat ID

# Initialize Twitter API
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
twitter_api = tweepy.API(auth)

# Initialize Telegram Bot
telegram_bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Account to monitor
TWITTER_USER = 'sullyfromDeets'  # Replace with the Twitter username

# Define a StreamClient class for real-time tweet monitoring (for Tweepy v4.x+)
class MyStreamClient(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        # Check if the tweet is from the user we're interested in
        if tweet.author_id == twitter_api.get_user(screen_name=TWITTER_USER).id:
            tweet_text = tweet.text
            tweet_id = tweet.id
            tweet_link = f"https://twitter.com/{TWITTER_USER}/status/{tweet_id}"
            
            # Construct the message
            message = f"New tweet from @{TWITTER_USER}:\n\n{tweet_text}\n\nLink: {tweet_link}"
            
            # Send the message to the Telegram chat
            telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    
    def on_error(self, status_code):
        if status_code == 420:
            # Return False to disconnect the stream in case of rate limiting
            print("Rate limit reached, disconnecting stream.")
            return False
        print(f"Error: {status_code}")
        return True

# Set up the Twitter stream using v4.x StreamingClient
client = MyStreamClient(bearer_token=TWITTER_BEARER_TOKEN)

# Start streaming the user's tweets in real-time
try:
    print(f"Listening for new tweets from @{TWITTER_USER}...")
    # Filter the stream to track the user's tweets by author_id
    client.add_rules(tweepy.StreamRule(f"from:{TWITTER_USER}"))
    client.filter()
except Exception as e:
    print(f"Error starting the stream: {e}")
