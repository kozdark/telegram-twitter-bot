import tweepy
from telegram import Bot
from time import sleep

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

# Keep track of the last tweet ID
last_tweet_id = None

def fetch_latest_tweets():
    global last_tweet_id
    try:
        # Fetch the most recent tweet
        tweets = twitter_api.user_timeline(screen_name=TWITTER_USER, count=1, tweet_mode="extended")
        if tweets:
            latest_tweet = tweets[0]
            if last_tweet_id != latest_tweet.id:
                last_tweet_id = latest_tweet.id
                tweet_text = latest_tweet.full_text
                tweet_link = f"https://twitter.com/{TWITTER_USER}/status/{latest_tweet.id}"
                
                # Construct the message
                message = f"New tweet from @{TWITTER_USER}:\n\n{tweet_text}\n\nLink: {tweet_link}"
                
                # Send the message to the Telegram chat
                telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
                print(f"Sent message: {message}")
    except Exception as e:
        print(f"Error fetching tweets: {e}")

# Polling loop
try:
    print(f"Monitoring tweets from @{TWITTER_USER}...")
    while True:
        fetch_latest_tweets()
        sleep(15)  # Check for new tweets every 15 seconds
except KeyboardInterrupt:
    print("Stopped monitoring.")
except Exception as e:
    print(f"Unexpected error: {e}")
