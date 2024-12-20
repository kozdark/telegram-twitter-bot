import tweepy
from telegram import Bot

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

# Define a StreamListener class for real-time tweet monitoring
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        # Check if the tweet is from the user we're interested in
        if status.user.screen_name.lower() == TWITTER_USER.lower():
            tweet_text = status.text
            tweet_id = status.id
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

# Set up the Twitter stream
listener = MyStreamListener()
stream = tweepy.Stream(auth=twitter_api.auth, listener=listener)

# Start streaming the user's tweets in real-time
try:
    print(f"Listening for new tweets from @{TWITTER_USER}...")
    stream.filter(follow=[str(twitter_api.get_user(screen_name=TWITTER_USER).id)])
except Exception as e:
    print(f"Error starting the stream: {e}")
