from live_connection import fetch_live_tweets, all_tweets
import time

fetch_live_tweets()
time.sleep(6)   # wait once
print(len(all_tweets))
