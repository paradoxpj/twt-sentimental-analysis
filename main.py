import os

from tweepy import OAuthHandler, API, Cursor
from dotenv import load_dotenv
from nltk.sentiment import SentimentIntensityAnalyzer

from constants import users_list


def fetch_user_details(auth_api, user):
    '''A function to fetch a given user's details from Twitter API'''
    user_item = auth_api.get_user(user)
    # Adding user details into a list.
    user_details = [
        user_item.name,
        user_item.screen_name,
        user_item.description,
        user_item.statuses_count,
        user_item.friends_count,
        user_item.followers_count,
    ]
    return user_details

def fetch_user_tweets(auth_api, user, max_count):
    '''A function to fetch the given user's tweets'''
    # A list to store all the tweets by the user
    user_tweets = []
    # Fetching tweets of the given user from Twitter API and travesing through them.
    for status in Cursor(auth_api.user_timeline, id=user, tweet_mode="extended").items(max_count):
        if(status.retweeted==True):
            # Condition to check if the tweet is not original
            continue
        # Appending all the necessary details related to the tweet into the user tweets list.
        user_tweets.append(status.full_text)
    return user_tweets

def process_users(auth_api):
    '''A function to process all the users in the users list and perform necessary operations'''
    # Traversing through all the users in the users list.
    for user in users_list:
        # Calling functions to fetch the user's details and tweets.
        user_details = fetch_user_details(auth_api, user)
        user_tweets = fetch_user_tweets(auth_api, user, 200)
        polarity_list = []
        for tweet in user_tweets:
            polarity_list.append(polarity_calculator(tweet))
        print("User:", user_details)
        print("Result:")
        for i in polarity_list:
            print(i)

def polarity_calculator(text):
    '''A function that returns polarity of a text using nltk's pre trained sentiment analyzer'''
    # Making a SentimentIntensityAnalyzer object
    analyzer = SentimentIntensityAnalyzer()
    # returning the polarity_scores of the given text
    return analyzer.polarity_scores(text)

if __name__ == "__main__":
    '''main function'''
    # Loading environment variables from .env file
    load_dotenv()
    # Assigning values of authorization keys from environment variables
    consumer_key = os.environ.get("TWTAPI_CK")
    consumer_secret = os.environ.get("TWTAPI_CS")
    access_token = os.environ.get("TWTAPI_AT")
    access_token_secret = os.environ.get("TWTAPI_ATS")
    # Authorizing Twitter API
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    auth_api = API(auth)
    # Calling a function to process users in the users list.
    # for i in range(10):
    #     text = input("Enter text: ")
    #     print(polarity_calculator(text))
    process_users(auth_api)
