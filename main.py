import tweepy 
import time
from PIL import Image
import re
from random import randrange
from textblob import TextBlob
import threading
from random_tweets import random_tweets
from environment import oauth_keys
from datetime import datetime
from colorama import Fore, Back, Style

blacklisted_terms = ['nigger', 'retard', 'faggot', 'chink', 'gook', 'kike', 'jew']
popular_accounts = ['BTS_twt', 'ygofficialblink', 'JYPETWICE']
random_tweet_search_terms = ["#MJ+GOAT", "#DBZ", "SSBU", "Super Smash Bros", "Anime", "Video Games", "BTS", "#Twice", "#blackpink", "#Lakers", "#naruto", '#tsundere', "#realmadrid", "#kobe"]
default_accounts = ['kanyewest', 'elonmusk', 'barackobama', 'aoc', 'jk_rowling', 'KDTrey5', 'ArianaGrande', 'KimKardashian', 'realmadrid', 'wizkhalifa', 'KevinHart4real', 'akshaykumar', 'BeingSalmanKhan', 'SrBachchan', 'MileyCyrus', 'BTW_twt', 'ygofficialblink', 'JYPETWICE']
keywords = ['Lebron', 'MJ', 'stans', 'Kobe', 'GOAT', 'Pippen', 'Wade', 'Kyrie', "LBJ", "Bron", "Jordan", 'Wilt', 'L']
reply_phrases_positive = ['facts on facts', 'w', 'EXACTLY!!!!!', 'MJ is the GOAT!!', "couldn't agree more", 'YESSSSS', 'Absolutely', 'No lies here', 'FACTS!!!!', 'Yep', 'KOBE IS THE GOAT!', ' Kobe > Lebron']
reply_phrases_negative = ['L', 'lmao bronstan logic', 'dumb', 'Bronsexuals brah', 'this is the dumbest tweet ever', 'Lol you know nothing', 'Worst take ever', 'lmao this si the stupideest thing i ever read', 'do you even watch basketball??', 'You legit got no braincells smh']
general_questions = ['wyd', 'what it do babyyyyyyyy?', 'Where can I find the strongest pokemon?', 'Will you be my girlfriend?', 'Why?', 'Are you the one?', 'sup']
general_responses = ['ok', 'lol', 'hmmmmm', 'i think i love you', 'i want hamburgers', "that ain't right", 'definitely sus haha', 'lmao wut']
image_dict = {
    0: 'clown.jpg',
    1: 'drooling_wojak_friends.png',
    2: 'drooling_wojak.png',
    3: 'bronsexuals.jpg'
}


def like(api, nfc_account):
    print(Fore.GREEN, 'liking tweets from----------', nfc_account.name, get_current_time())
    for tweet in tweepy.Cursor(api.user_timeline,id=nfc_account.id).items(10):
        print(Fore.GREEN, tweet.text)
        try:
            tweet.favorite()
            time.sleep(20)
        except tweepy.TweepError as e:
            print(Fore.RED, e.reason)
        except StopIteration:
            break
        time.sleep(5)

def like_likes(api, nfc_account):
    print(Fore.GREEN, 'liking netorarefanclub likes -------------', get_current_time())
    for favorite in tweepy.Cursor(api.favorites, id=nfc_account.id).items(20):
        print(Fore.GREEN, 'liking liked tweet...', favorite.text)
        try:
            favorite.favorite()
            time.sleep(20)
        except tweepy.TweepError as e:
            print(Fore.RED, e.reason)
        except StopIteration:
            break
        time.sleep(5)



def reply_to_latest_comments(api, nfc_account):
    print(Fore.GREEN, 'replying to latest comments -------------', get_current_time())
    user_name = "@netorarefanclub"
    for tweet in tweepy.Cursor(api.user_timeline,id=nfc_account.id).items(5):
        has_keywords = re.findall(r"(?=("+'|'.join(keywords)+r"))",tweet.text)

        if not has_keywords:
            print(Fore.GREEN, 'tweet has no keywords, continuing...')
            continue
        replies_iterator = tweepy.Cursor(api.search, q='to:{}'.format(user_name),
                                    since_id=tweet.id, tweet_mode='extended').items(100)
        screen_names = []
        replies = []
        for reply in replies_iterator:
            screen_names.append(reply.user.screen_name)
            replies.append(reply)
        
        if api.me().screen_name in screen_names:
            print(Fore.RED, 'HAVE ALREADY REPLIED TO THIS TWEET')
            continue
        reply_positive(tweet, api)

def reply_to_commented_tweet(api, nfc_account):
    print(Fore.GREEN, 'replying to commented tweets -------------', get_current_time())
    for tweet in tweepy.Cursor(api.user_timeline,id=nfc_account.id).items(5):
        print(Fore.GREEN, 'Here is our tweet', tweet.text)
        has_keywords = re.findall(r"(?=("+'|'.join(keywords)+r"))",tweet.text)
        if not has_keywords:
            print(Fore.GREEN, 'tweet has no keywords, continuing...')
            continue
        replies_iterator = tweepy.Cursor(api.search, q='to:{}'.format(tweet.in_reply_to_screen_name),
                                since_id=tweet.in_reply_to_status_id, tweet_mode='extended').items(100)
        
        if not tweet.in_reply_to_status_id:
            print(Fore.GREEN, 'no in_reply_to_status_id in tweet, continuing')
            continue

        else:
            screen_names = []
            for reply in replies_iterator:
                screen_names.append(reply.user.screen_name)
            
            if api.me().screen_name in screen_names:
                print(Fore.GREEN, 'HAVE ALREADY REPLIED TO THIS COMMENTED TWEET')
                continue
                
            try: 
                print(Fore.GREEN, 'trying to find original tweet...')
                original_tweet = api.get_status(tweet.in_reply_to_status_id)
                reply_negative(original_tweet, tweet, api)
            except tweepy.TweepError as e:
                print(Fore.RED, e.reason)
                continue
        
    print('Finished reply_to_commented_tweet --------------')

def reply_positive(tweet, api):
    print(Fore.GREEN, 'replying positive----------------', get_current_time())
    print(Fore.GREEN, 'tweet: ', tweet.text)
    random_idx = randrange(len(reply_phrases_positive))
    random_positive_response = reply_phrases_positive[random_idx]
    random = randrange(10)
    if random == 10 or random == 9:
        try:
            api.update_with_media('dropped_this_king.jpg', in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
            print(Fore.GREEN, 'replying positively with image: ', 'dropped_this_king.jpg')
            time.sleep(600)
        except tweepy.TweepError as e:
            print(Fore.GREEN, e.reason)
            time.sleep(600)
    else:
        api.update_status(random_positive_response, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
        print(Fore.GREEN, 'replying positively with text: ', random_positive_response)
        time.sleep(600)

def reply_negative(original_tweet, tweet, api):
    print(Fore.GREEN, 'replying negative----------------', get_current_time())
    print(Fore.GREEN, 'original_tweet: ', original_tweet.text)
    print(Fore.GREEN, 'my_tweet: ', tweet.text)

    random_idx = randrange(len(reply_phrases_negative))
    random_negative_response = reply_phrases_negative[random_idx]
    random = randrange(5)
    # 2/5 chance to post image
    if random == 5 or random == 2:
        try: 
            rd_img = randrange(3)
            img = image_dict[rd_img]
            api.update_with_media(img, in_reply_to_status_id=original_tweet.id, auto_populate_reply_metadata=True, status=random_negative_response)
            print(Fore.GREEN, 'replying negatively with image: ', img)
            time.sleep(600)
        except tweepy.TweepError as e:
            print(Fore.RED, e.reason)
            time.sleep(600)
    else:
        try:
            api.update_status(random_negative_response, in_reply_to_status_id=original_tweet.id, auto_populate_reply_metadata=True)
            print(Fore.GREEN, 'replying negatively with text: ', random_negative_response)
            time.sleep(600)
        except tweepy.TweepError as e:
            print(Fore.RED, e.reason)
            time.sleep(600)

def tweet_random_tweet(api):
    print(Fore.CYAN, 'running tweet_random_tweet -------------', get_current_time())
    random_search_idx = randrange(len(random_tweet_search_terms))
    search_term = random_tweet_search_terms[random_search_idx]
    tweets = []
    for tweet in tweepy.Cursor(api.search, q=search_term, lang="en").items(50):
        tweets.append(tweet)

    random_tweet_idx = randrange(len(tweets))
    random_tweet = tweets[random_tweet_idx]
    random_tweet_has_blacklisted_terms = re.findall(r"(?=("+'|'.join(blacklisted_terms)+r"))",random_tweet.text)
    if not random_tweet_has_blacklisted_terms:
        print(Fore.CYAN, 'tweeting random tweet:', random_tweet.text)
        try:
            api.update_status(random_tweet.text)
            time.sleep(20)
        except tweepy.TweepError as e:
            print(Fore.RED, e.reason)
            time.sleep(20)



def retweet_random_tweet(api):
    print(Fore.CYAN, 'running retweet_random_tweet -------------', get_current_time())
    random_search_idx = randrange(len(random_tweet_search_terms))
    search_term = random_tweet_search_terms[random_search_idx]
    tweets = []
    for tweet in tweepy.Cursor(api.search, q=search_term, lang="en").items(50):
        tweets.append(tweet)

    random_tweet_idx = randrange(len(tweets))
    random_tweet = tweets[random_tweet_idx]
    print(Fore.CYAN, 'retweeting this tweet:', random_tweet.text)
    try:
        api.retweet(tweet.id)
        time.sleep(20)
    except tweepy.TweepError as e:
        print(Fore.RED, e.reason)
        time.sleep(20)
    print(Fore.CYAN, "Following person who I retweeted", random_tweet.user) 
    try: 
        api.create_friendship(random_tweet.user.id)
        time.sleep(20)
    except tweepy.TweepError as e:
        print(Fore.RED, e.reason)
        time.sleep(20)
    
def retweet_popular_accounts(api):
    print(Fore.CYAN, 'running retweet_popular_accounts -------------', get_current_time())
    for name in popular_accounts:
        user = api.get_user(screen_name = name)
        for tweet in tweepy.Cursor(api.user_timeline,id=user.id).items(1):
            print(Fore.CYAN, 'retweeting popular account tweet', name, tweet.text)
            try:
                api.retweet(tweet.id)
                time.sleep(20)
                tweet.favorite()
            except tweepy.TweepError as e:
                print(Fore.RED, e.reason)
            except StopIteration:
                break
            time.sleep(20)
        
def delete_all_tweets(api, nfc_account):
    for tweet in tweepy.Cursor(api.user_timeline,id=api.me().id).items(10):
        print(tweet)
        try:
            api.destroy_status(tweet.id)
            time.sleep(20)
        except tweepy.TweepError as e:
            print(Fore.RED, e.reason)
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
    print(Fore.GREEN, 'running main....')
    while True:
        for consumer_key, consumer_secret, access_key, access_secret in oauth_keys:
            consumer_key = consumer_key
            consumer_secret = consumer_secret
            access_token = access_key
            access_token_secret = access_secret
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
            auth.set_access_token(access_token, access_token_secret)

            api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
            print(Fore.GREEN, api.me())

            nfc_account = api.get_user(screen_name = 'netorarefanclub')
            nowicantlose_account = api.get_user(screen_name = 'nowicantlose')

            like(api, nfc_account)
            like(api, nowicantlose_account)
            like_likes(api, nfc_account)
            reply_to_latest_comments(api, nfc_account)
            reply_to_commented_tweet(api, nfc_account)

            # delete_all_tweets(api, nfc_account)
            print(Fore.GREEN, 'FINISHED ALL ACTIONS FOR CURRENT ACCOUNT ---------------------------------------------------')
        time.sleep(3600)

def run_tweet_from_accounts():
    print(Fore.CYAN, 'running random_tweets_for_accounts....')
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

        time.sleep(1800)


def get_current_time():
    now = datetime.now()
 
    print("now =", now)

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string


try:
    t = threading.Thread(target=run_tweet_from_accounts)
    t.start()
    f = threading.Thread(target=main)
    f.start()
except:
   print("Error: unable to start thread")

