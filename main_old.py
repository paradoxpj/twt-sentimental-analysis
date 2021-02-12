from tweepy import OAuthHandler, API, Cursor
from textblob import TextBlob

from datetime import datetime, date, time, timedelta
from collections import Counter

from dotenv import load_dotenv
import os


load_dotenv()
consumer_key = os.environ.get("TWTAPI_CK")
consumer_secret = os.environ.get("TWTAPI_CS")
access_token = os.environ.get("TWTAPI_AT")
access_token_secret = os.environ.get("TWTAPI_ATS")

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)

input1 = input("Enter username: ")
account_list = [input1]

for target in account_list:
    print("Data for "+target)
    item = auth_api.get_user(target)
    print(item.name)
    print(item.screen_name)
    print(item.description)
    print(item.statuses_count)
    print(item.friends_count)
    print(item.followers_count)

print("-"*15)

count=0
total_polarity = 0
tweet_count = 25
for status in Cursor(auth_api.user_timeline, id=account_list[0], tweet_mode="extended").items():
    if(count==0):
        print(dir(status))
    if(status.retweeted==True):
        continue
    print("-"*15)
    print(count+1)
    print("text: ", status.full_text)
    blob = TextBlob(status.full_text)
    print("polarity: ", blob.sentiment.polarity)
    total_polarity += blob.sentiment.polarity
    print("user: ", status.user.name)
    #break
    count+=1
    if(count==tweet_count):
        break
print("-"*15)
print("Average Polarity: ", total_polarity/tweet_count)
