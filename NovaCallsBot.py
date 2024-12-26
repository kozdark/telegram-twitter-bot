import tweepy
from telegram import Bot
from time import sleep

# Twitter API keys
TWITTER_API_KEY = 'ZqSbHnlqxRsEj2po0jd7EAxlr'
TWITTER_API_SECRET = 'Yd6rP5oIvipEU2rz9CgMKMabWL6elb02ttNQ6FY1ylROdFOcI3'
TWITTER_BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAH6hxgEAAAAAMueN4cwwP3M9uOILfaitKDLqhYs%3DOYcVUTvXjopNGljNGxHfYsgXFralWlZoNJKQoJcE7KszAwXnXK'

# Telegram Bot Token and Chat ID
TELEGRAM_BOT_TOKEN = '7554759873:AAE8xW4IMPZuamLSO6ZSYMQaf7vhvR75fhc'
TELEGRAM_CHAT_ID = 'NovaCallsBot'  # Replace with your Telegram user or group chat ID

# Twitter username to monitor
TWITTER_USER = 'sullyfromDeets'  # Replace with the username you want to monitor

# Initialize Twitter Client with Bearer Token
client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

# Initialize Telegram Bot
telegram_bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Keep track of the last tweet ID
last_tweet_id = None

def fetch_latest_tweet():
    global last_tweet_id
    try:
        # Search recent tweets from the user
        query = f"from:{TWITTER_USER} -is:retweet"
        tweets = client.search_recent_tweets(query=query, max_results=1, tweet_fields=['id', 'text', 'created_at'])
        
        if tweets.data:
            latest_tweet = tweets.data[0]
            if last_tweet_id != latest_tweet.id:
                last_tweet_id = latest_tweet.id
                tweet_text = latest_tweet.text
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
        fetch_latest_tweet()
        sleep(60)  # Check for new tweets every 60 seconds
except KeyboardInterrupt:
    print("Stopped monitoring.")
except Exception as e:
    print(f"Unexpected error: {e}")
