import tweepy 
import time
from PIL import Image
import re
from random import randrange
from textblob import TextBlob
import threading
from random_tweets import random_tweets
from environment import oauth_keys

popular_accounts = ['BTW_twt', 'ygofficialblink', 'JYPETWICE']
random_tweet_search_terms = ["#MJ+GOAT", "#DBZ", "SSBU", "Super Smash Bros", "Anime", "Video Games", "BTS"]
default_accounts = ['kanyewest', 'elonmusk', 'barackobama', 'aoc', 'jk_rowling', 'KDTrey5', 'ArianaGrande', 'KimKardashian', 'realmadrid', 'wizkhalifa', 'KevinHart4real', 'akshaykumar', 'BeingSalmanKhan', 'SrBachchan', 'MileyCyrus', 'BTW_twt', 'ygofficialblink', 'JYPETWICE']
keywords = ['Lebron', 'MJ', 'stans', 'Kobe', 'GOAT', 'Pippen', 'Wade', 'Kyrie', "LBJ", "Bron", "Jordan", '"']
reply_phrases_positive = ['facts on facts', 'w', 'EXACTLY!!!!!', 'MJ is the GOAT!!', "couldn't agree more", 'YESSSSS', 'Absolutely', 'No lies here', 'FACTS!!!!', 'Yep', 'KOBE IS THE GOAT!', ' Kobe > Lebron']
reply_phrases_negative = ['L', 'lmao bronstan logic', 'dumb', 'Bronsexuals brah', 'this is the dumbest tweet ever', 'Lol you know nothing', 'Worst take ever', 'lmao this si the stupideest thing i ever read', 'do you even watch basketball??']

def like(api, nfc_account):
    print('liking netorarefanclub tweets -------------')
    for tweet in tweepy.Cursor(api.user_timeline,id=nfc_account.id).items(10):
        print(tweet.text)
        try:
            tweet.favorite()
            time.sleep(20)
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break
        time.sleep(5)

def like_likes(api, nfc_account):
    print('liking netorarefanclub likes -------------')
    for favorite in tweepy.Cursor(api.favorites, id=nfc_account.id).items(20):
        print('liking liked tweet...', favorite.text)
        try:
            favorite.favorite()
            time.sleep(20)
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break
        time.sleep(5)



def reply_to_latest_comments(api, nfc_account):
    print('replying to latest comments -------------')
    user_name = "@netorarefanclub"
    for tweet in tweepy.Cursor(api.user_timeline,id=nfc_account.id).items(5):
        replies = tweepy.Cursor(api.search, q='to:{}'.format(user_name),
                                    since_id=tweet.id, tweet_mode='extended').items()
        screen_names = []
        for reply in replies:
            screen_names.append(reply.user.screen_name)
        
        if api.me().screen_name in screen_names:
            print('HAVE ALREADY REPLIED TO THIS TWEET')
            continue
        iterate_through_replies(replies, tweet, api, True)

def reply_to_commented_tweet(api, nfc_account):
    print('replying to commented tweets -------------')
    for tweet in tweepy.Cursor(api.user_timeline,id=nfc_account.id).items(5):
        random = randrange(2)

        # 33% chance to reply to commented tweet
        if random == 1:
            replies = tweepy.Cursor(api.search, q='to:{}'.format(tweet.in_reply_to_screen_name),
                                    since_id=tweet.in_reply_to_status_id, tweet_mode='extended').items()
            
            screen_names = []
            for reply in replies:
                screen_names.append(reply.user.screen_name)
            
            if api.me().screen_name in screen_names:
                print('HAVE ALREADY REPLIED TO THIS COMMENTED TWEET')
                continue
                
            try: 
                tweet = api.get_status(tweet.in_reply_to_status_id)
                iterate_through_replies(replies, tweet, api, False)
            except tweepy.TweepError as e:
                print(e.reason)
                time.sleep(600)

    

def iterate_through_replies(replies, tweet, api, is_positive=True):
    while True:
        try:
            reply = replies.next()
            if not hasattr(reply, 'in_reply_to_status_id_str'):
                continue
            if reply.in_reply_to_status_id == tweet.id:
                if reply.user.screen_name == api.me().screen_name:
                    print('Already replied to this tweet...')
                    break
                elif is_positive:
                    reply_positive(tweet, api)
                else:
                    reply_negative(tweet, api)

        except tweepy.RateLimitError as e:
            print("Twitter api rate limit reached")
            time.sleep(60)
            continue

        except tweepy.TweepError as e:
            print("Tweepy error occured:{}".format(e))
            break

        except StopIteration:
            break

        except Exception as e:
            print("Failed while fetching replies {}".format(e))
            break

def reply_positive(tweet, api):
    has_keywords = re.findall(r"(?=("+'|'.join(keywords)+r"))",tweet.text)

    # If there is a match in related content we reply
    if len(has_keywords) > 0:
        print('comment', tweet.text)
        print('replying with ', api.me().id)
        random_idx = randrange(len(reply_phrases_positive))
        random_positive_response = reply_phrases_positive[random_idx]
        random = randrange(10)
        if random == 10 or random == 9:
            try:
                api.update_with_media('dropped_this_king.jpg', in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
                print('replying with image: ', 'dropped_this_king.jpg')
                time.sleep(600)
            except tweepy.TweepError as e:
                print(e.reason)
                time.sleep(600)
        else:
            api.update_status(random_positive_response, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
            print('replying with text: ', random_positive_response)
            time.sleep(600)

def reply_negative(tweet, api):
    has_keywords = re.findall(r"(?=("+'|'.join(keywords)+r"))",tweet.text)

    # If there is a match in related content we reply
    if len(has_keywords) > 0:
        print('comment', tweet.text)
        print('replying with ', api.me().id)
        random_idx = randrange(len(reply_phrases_negative))
        random_negative_response = reply_phrases_negative[random_idx]
        random = randrange(5)
        # 2/5 chance to post image
        if random == 5 or random == 2:
            try: 
                rd_img = randrange(1)
                img = 'drooling_wojak.png' if rd_img == 1 else 'drooling_wojak_friends.png'
                api.update_with_media(img, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True, status=random_negative_response)
                print('replying with image: ', img)
                time.sleep(600)
            except tweepy.TweepError as e:
                print(e.reason)
                time.sleep(600)
        else:
            try:
                api.update_status(random_negative_response, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
                print('replying with text: ', random_negative_response)
                time.sleep(600)
            except tweepy.TweepError as e:
                print(e.reason)
                time.sleep(600)

def tweet_random_tweet(api):
    print('running tweet_random_tweet -------------')
    random_search_idx = randrange(len(random_tweet_search_terms))
    search_term = random_tweet_search_terms[random_search_idx]
    tweets = []
    for tweet in tweepy.Cursor(api.search, q=search_term, lang="en").items(50):
        tweets.append(tweet)

    random_tweet_idx = randrange(len(tweets))
    random_tweet = tweets[random_tweet_idx]
    sentiment_object = TextBlob(random_tweet.text)
    print(sentiment_object.polarity, sentiment_object)
    print('tweeting random tweet:', random_tweet.text)
    try:
        api.update_status(random_tweet.text)
        time.sleep(20)
    except tweepy.TweepError as e:
        print(e.reason)
        time.sleep(20)



def retweet_random_tweet(api):
    print('running retweet_random_tweet -------------')
    random_search_idx = randrange(len(random_tweet_search_terms))
    search_term = random_tweet_search_terms[random_search_idx]
    tweets = []
    for tweet in tweepy.Cursor(api.search, q=search_term, lang="en").items(50):
        tweets.append(tweet)

    random_tweet_idx = randrange(len(tweets))
    random_tweet = tweets[random_tweet_idx]
    sentiment_object = TextBlob(random_tweet.text)
    print(sentiment_object.polarity, sentiment_object)
    print('retweeting this tweet:', random_tweet.text)
    try:
        api.retweet(tweet.id)
        time.sleep(20)
    except tweepy.TweepError as e:
        print(e.reason)
        time.sleep(20)
    
    print("Following person who I retweeted", random_tweet.user)
    try: 
        api.create_friendship(random_tweet.user.id)
        time.sleep(20)
    except tweepy.TweepError as e:
        print(e.reason)
        time.sleep(20)
    
def retweet_popular_accounts(api):
    print('running retweet_popular_accounts -------------')
    for name in popular_accounts:
        user = api.get_user(screen_name = name)
        for tweet in tweepy.Cursor(api.user_timeline,id=user.id).items(1):
            print('retweeting popular account tweet', name, tweet.text)
            try:
                api.retweet(tweet.id)
                time.sleep(20)
                tweet.favorite()
            except tweepy.TweepError as e:
                print(e.reason)
            except StopIteration:
                break
            time.sleep(20)



def remove_url(txt):
    """Replace URLs found in a text string with nothing 
    (i.e. it will remove the URL from the string).

    Parameters
    ----------
    txt : string
        A text string that you want to parse and remove urls.

    Returns
    -------
    The same txt string with url's removed.
    """

    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())
        
def delete_all_tweets(api, nfc_account):
    for tweet in tweepy.Cursor(api.user_timeline,id=api.me().id).items(10):
        print(tweet)
        try:
            api.destroy_status(tweet.id)
            time.sleep(20)
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break

def follow(api, nfc_account):
    print('following users netorarefanclub')
    api.create_friendship(nfc_account.id)
    time.sleep(10)


def follow_default_users(api):
    print('following default users...')
    for name in default_accounts:
        print('following: ', name)
        user = api.get_user(screen_name = name)
        print('user...', user)
        try:
            api.create_friendship(user.id)
        except tweepy.TweepError as e:
            print(e.reason)
            
        time.sleep(10)

def main():
    print('running main....')
    while True:
        for consumer_key, consumer_secret, access_key, access_secret in oauth_keys:
            consumer_key = consumer_key
            consumer_secret = consumer_secret
            access_token = access_key
            access_token_secret = access_secret
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
            auth.set_access_token(access_token, access_token_secret)

            api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
            print(api.me())

            nfc_account = api.get_user(screen_name = 'netorarefanclub')
            # print(nfc_account)

            # follow(api, nfc_account)
            # follow_default_users(api)

            like(api, nfc_account)
            like_likes(api, nfc_account)
            reply_to_latest_comments(api, nfc_account)
            reply_to_commented_tweet(api, nfc_account)

            # delete_all_tweets(api, nfc_account)

        time.sleep(3600)

def run_tweet_from_accounts():
    print('running random_tweets_for_accounts....')
    while True:
        for consumer_key, consumer_secret, access_key, access_secret in oauth_keys:
            consumer_key = consumer_key
            consumer_secret = consumer_secret
            access_token = access_key
            access_token_secret = access_secret
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
            auth.set_access_token(access_token, access_token_secret)

            api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

            tweet_random_tweet(api)
            retweet_random_tweet(api)
            retweet_popular_accounts(api)

        time.sleep(7200)


try:
    t = threading.Thread(target=run_tweet_from_accounts)
    t.start()
    f = threading.Thread(target=main)
    f.start()
except:
   print("Error: unable to start thread")

