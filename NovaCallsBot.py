import tweepy
from telegram import Bot
from time import sleep

# Twitter API keys
TWITTER_API_KEY = 'ZqSbHnlqxRsEj2po0jd7EAxlr'
TWITTER_API_SECRET = 'Yd6rP5oIvipEU2rz9CgMKMabWL6elb02ttNQ6FY1ylROdFOcI3'
TWITTER_ACCESS_TOKEN = '1516153749244362760-EJaUXObu6Ci2uxDGnQu5rpI1aHTxCu'
TWITTER_ACCESS_SECRET = 'Wzvzf2JnYIPV2Ls8RePIjyCLOShr7Qpal2UR3ay2J3Gww'

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

last_tweet_id = None

def check_for_new_tweets():
    global last_tweet_id
    tweets = twitter_api.user_timeline(screen_name=TWITTER_USER, count=1, tweet_mode="extended")
    if tweets:
        latest_tweet = tweets[0]
        if last_tweet_id != latest_tweet.id:
            last_tweet_id = latest_tweet.id
            message = f"New tweet from @{TWITTER_USER}:\n\n{latest_tweet.full_text}\n\nLink: https://twitter.com/{TWITTER_USER}/status/{latest_tweet.id}"
            telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

# Continuous Monitoring
while True:
    try:
        check_for_new_tweets()
    except Exception as e:
        print(f"Error: {e}")
    sleep(60)  # Check every 60 seconds
