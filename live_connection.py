
import requests
import time
from datetime import datetime
from preprocess import clean_text, get_sentiment
from predict_sentiment import predict_sentiment, clean_text
import pandas as pd 
import mysql.connector

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database ="social_dashboard"
)
cursor = conn.cursor()

USE_REAL_API = False  

API_KEY = "new1_ead1ad3d7348407e9ee4407009ee883d"

url = "https://api.twitterapi.io/twitter/tweet/search"

headers = {
    "X-API-Key": API_KEY
}

params = {
    "query": "Myntra",
    "limit": 20
}
# global varibale 
all_tweets = []
seen_ids = set()
last_call_time = 0  

# function to fetch tweets 
def fetch_live_tweets():
    """
    Fetch live tweets from API or simulate if USE_REAL_API=False
    Updates the global all_tweets list.
    """
    global all_tweets,seen_ids,last_call_time

     # SIMULATED LIVE DATA MODE
    
    if not USE_REAL_API:
        time.sleep(2)

        sample_texts = [
            "Myntra sale is amazing, great discounts!",
            "Myntra delivery is very slow, disappointed",
            "Love Myntra fashion collection ❤️",
            "Worst return policy, very unhappy",
            "Myntra customer support is helpful"
        ]

        for text in sample_texts:
            cleaned = clean_text(text)
            sentiment = predict_sentiment(text)


            all_tweets.append({
                "time": datetime.now(),
                "tweet": text,
                "sentiment": sentiment
            })
 
        # Save tweet to MySQL
            cursor.execute(
                "INSERT INTO tweets (tweet, sentiment, created_at) VALUES (%s, %s, %s)",
                (text, sentiment, datetime.now())
            )
        conn.commit()
        return 

#real api mode 

    if time.time() - last_call_time < 5:
        print("Skipping API call (rate limit)")
        return

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    last_call_time = time.time()

    print(" FULL API RESPONSE:", data)  

    tweets = data.get("data", [])
    print(f" Tweets found: {len(tweets)}")
    for t in tweets:
        tweet_id = t.get("id")
        if tweet_id in seen_ids:
            continue
        seen_ids.add(tweet_id)
        text = t.get("text", "")
        ...
        all_tweets.append({...})


def get_tweets_df():
    """
    Returns a pandas DataFrame of all tweets.
    """
    if len(all_tweets) == 0:
        return pd.DataFrame(columns=["time", "tweet", "sentiment"])
    else:
        df = pd.DataFrame(all_tweets)
        df['time'] = pd.to_datetime(df['time'])
        return df

