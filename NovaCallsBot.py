import tweepy
from telegram import Bot

# Twitter API keys (OAuth 1.0a)
TWITTER_API_KEY = 'ZqSbHnlqxRsEj2po0jd7EAxlr'
TWITTER_API_SECRET = 'Yd6rP5oIvipEU2rz9CgMKMabWL6elb02ttNQ6FY1ylROdFOcI3'
TWITTER_ACCESS_TOKEN = '1516153749244362760-EJaUXObu6Ci2uxDGnQu5rpI1aHTxCu'
TWITTER_ACCESS_SECRET = 'Wzvzf2JnYIPV2Ls8RePIjyCLOShr7Qpal2UR3ay2J3Gww'

# Telegram Bot Token and Chat ID
TELEGRAM_BOT_TOKEN = '7554759873:AAE8xW4IMPZuamLSO6ZSYMQaf7vhvR75fhc'
TELEGRAM_CHAT_ID = 'NovaCallsBot'  # Replace with your Telegram user or group chat ID

# The Twitter username to monitor
TWITTER_USER = 'sullyfromDeets'  # Replace with the username you want to monitor

# Initialize Twitter API
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
twitter_api = tweepy.API(auth)

# Initialize Telegram Bot
telegram_bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Get the User ID of the monitored Twitter account
try:
    user = twitter_api.get_user(screen_name=TWITTER_USER)
    TWITTER_USER_ID = user.id_str
    print(f"Monitoring tweets from @{TWITTER_USER} (User ID: {TWITTER_USER_ID})")
except Exception as e:
    print(f"Error fetching user details: {e}")
    exit()

# Define a StreamListener for real-time monitoring
class MyStreamListener(tweepy.Stream):
    def on_status(self, status):
        if str(status.user.id) == TWITTER_USER_ID:
            tweet_text = status.text
            tweet_id = status.id
            tweet_link = f"https://twitter.com/{TWITTER_USER}/status/{tweet_id}"
            
            # Construct the message
            message = f"New tweet from @{TWITTER_USER}:\n\n{tweet_text}\n\nLink: {tweet_link}"
            
            # Send the message to the Telegram chat
            telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
            print(f"Sent message: {message}")

    def on_error(self, status_code):
        print(f"Error: {status_code}")
        if status_code == 420:  # Rate limiting
            return False

# Start the stream
try:
    print("Starting Twitter stream...")
    stream_listener = MyStreamListener(
        consumer_key=TWITTER_API_KEY,
        consumer_secret=TWITTER_API_SECRET,
        access_token=TWITTER_ACCESS_TOKEN,
        access_token_secret=TWITTER_ACCESS_SECRET,
    )
    stream_listener.filter(follow=[TWITTER_USER_ID], is_async=False)
except Exception as e:
    print(f"Error starting the stream: {e}")
