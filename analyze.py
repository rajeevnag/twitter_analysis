
def get_trending_tweets():
    
    print()
    print("Where would you like to get trending tweets from?")
    print("1) Worldwide")
    print("2) Other")

    location = int(input())
    woeid = int() #id used for identifying location through tweepy

    if location == 1:
        woeid = 1
    elif location == 2:
        location = str(input("Would you like to see some locations? (enter yes or no) "))
        while location != 'yes' and location != 'no':
            print('Error: please enter valid input')
            location = str(input())

        if location == 'yes':

            trend_locations = Twitter.trends_available()

            #get trending locations
            names_of_locations = list()
            for item in trend_locations:
                loc = item['name']
                names_of_locations.append(loc)
                
            #print trending locations
            for spot in names_of_locations:
                print(spot)

            location = input("What location would you like? ")
            
        else:
            location = input("Please enter the specific location: ")
        
        #have woeid of specific location now
        trend_locations = Twitter.trends_available()
        for trend_info in trend_locations:

            if trend_info['name'] == location:
                woeid = int(trend_info['woeid'])
                break

    #now the woeid is obtained for whatever location user is requesting
    trends_for_location = Twitter.trends_place(woeid)
        
    trends_for_location = trends_for_location[0]
    trends_for_location = trends_for_location['trends']

        #get names of trends
    names_of_trends = list()
    for item in trends_for_location:
        if item['tweet_volume'] != None:
            names_of_trends.append(item['name'])        

    #get tweets associated with each trend
    search_results = list()

    for trend in names_of_trends:
        #get search results for trend
        results = Twitter.search(trend,tweet_mode='extended',count = 1000)
        for result in results:
            tweet = result.full_text
            if detect(tweet) == 'en':

                tweet = re.sub(r'([^\s\w]|_)+', '', tweet)    #get just alphanum/spaces from tweets
                if tweet.find('RT',0,4) == 0:
                    
                    tweet = tweet[3:] #remove everything up until first instance of RT in text(always first 2 chars)
                if tweet.find('https') != -1: #remove image tags
                    tweet = tweet[:tweet.find('https')]
                search_results.append(tweet)

    return search_results           

def get_real_username(user_name):
    search_result = list()
    search_result = Twitter.search_users(user_name)
    
    while Twitter.search_users(user_name) == list():
        print('Invalid user, pick again')
        user_name = input()
    
    idx = 1
    for person in search_result:
        
        print(str(idx) +': ' + person.screen_name)
        idx += 1
    breakpoint()
    if idx > 2:# if more than 1 search result
        print('Which person do you want?')
        choice = int(input())
    else:
        choice = 1
    while choice-1 < 0 and choice-1 > len(search_result):
        print('Invalid choice number, pick again')
        choice = input()

    breakpoint()
    user_name = search_result[choice-1].screen_name
    return user_name

def assert_user_has_info(user_name,user_info):
    
    while user_info == list():
        print("User has no tweets, pick another")
        user_name = input()

        #verify username is in use
        user_name = get_real_username(user_name)

        user_info = Twitter.user_timeline(user_name, count = 1000, include_rts=True, tweet_mode='extended')

    return user_info

def get_user_tweets():
    print("Please enter the username of the user you would like to analyze")
    user_name = input()

    
    #verify user exists
    user_name = get_real_username(user_name)
    
    #get user info
    user_info = Twitter.user_timeline(user_name, count = 1000, include_rts=True, tweet_mode='extended')
    breakpoint()
    #assert user has information
    user_info = assert_user_has_info(user_name,user_info)
    
    user_tweets = list()
    #list of tweets from user    

    for entry in user_info:
        tweet = entry.full_text
        if detect(tweet) == 'en':
            tweet = re.sub(r'([^\s\w]|_)+', '', tweet)    #get just alphanum/spaces from tweets
            if tweet.find('RT',0,4) == 0:
                    
                tweet = tweet[3:] #remove everything up until first instance of RT in text(always first 2 chars)

            if tweet.find('https') != -1: #remove image tags
                tweet = tweet[:tweet.find('https')]

            user_tweets.append(tweet)

    return user_tweets



def get_keyword_tweets():

    print("What keyword would you like to search?")
    query = input()

    search_info = Twitter.search(query,count = 1000,tweet_mode='extended') #get up to first 500 tweets from keyword
    
    tweets = list()

    for entry in search_info:
        tweet = entry.full_text
        
        if detect(tweet) == 'en' and query in tweet: #only look at tweets containing search query
 
            tweet = re.sub(r'([^\s\w]|_)+', '', tweet)    #get just alphanum/spaces from tweets

            if tweet.find('RT',0,4) == 0:
                tweet = tweet[3:] #remove everything up until first instance of RT in text(always first 2 chars)
            if tweet.find('https') != -1: #remove image tags
                tweet = tweet[:tweet.find('https')]

            tweets.append(tweet)
    breakpoint()
    return tweets



def analyze_setiments(tweets):

    from textblob import TextBlob
    print('Would you like your results written to a file? (yes/no)')
    answer = input()
    polarity_counter = 0

    while answer != 'yes' and answer != 'no':
        print('Please retype your answer')
        answer = input()
    if answer == 'yes':
        print('Please enter filename')
        file_name = input()
        with open(file_name +'.txt','w') as file:
            for tweet in tweets:
                blob = TextBlob(tweet)
                
                file.write(tweet)
                file.write('\n')
                file.write('Sentiment: ')

                polarity_counter += blob.sentiment.polarity
                if blob.sentiment.polarity > 0:
                    file.write('Positive')
                elif blob.sentiment.polarity == 0:
                    file.write('Neutral')
                else:
                    file.write('Negative')
                file.write('\n')
                file.write('\n')

            file.write('Average sentiment: ')
            avg_sentiment = float(polarity_counter) / float(len(tweets))
            if avg_sentiment > 0:
                file.write('Positive')
            elif avg_sentiment == 0:
                file.write('Neutral')
            else:
                file.write('Negative')
        

    else:
        for tweet in tweets:
            blob = TextBlob(tweet)
            print(tweet)
                
            polarity_counter += blob.sentiment.polarity

            if blob.sentiment.polarity > 0:
                print('Sentiment: Positive')
            elif blob.sentiment.polarity == 0:
                print('Sentiment: Neutral')
            else:
                print('Sentiment: Negative')

        avg_sentiment = float(polarity_counter) / float(len(tweets))
        print()
        if avg_sentiment > 0:
            print('Average sentiment: Positive')
        elif avg_sentiment == 0:
            print('Average sentiment: Neutral')
        else:
            print('Average sentiment: Negative')

        

    

    
    


        
    


import re
import tweepy
from langdetect import detect

consumer_key = '' #removed for privacy
consumer_secret = '' #removed for privacy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

access_token = '' #removed for privacy
access_token_secret = '' #removed for privacy

auth.set_access_token(access_token, access_token_secret)

Twitter = tweepy.API(auth)


print('Welcome to the Twitter sentiment analyzer')
print('You can analyze the sentiment of trending tweets, user tweets, or tweets falling under a specific keyword')
print("Enter the number of what you'd like to do")


while True:

    print('1) Analyze trending tweets')
    print("2) Analyze user tweets")
    print("3) Analyze tweets under a keyword")
    print("4) Exit program")

    #get choice
    choice = int(input())
    while choice < 1 or choice > 4:
        print("Error: please enter a valid choice")
        choice = int(input())
    
    tweets = list()
    if choice == 1:
        tweets = get_trending_tweets()
        while tweets == list():
            print('Sorry, no tweets from that area.')
            tweets = get_trending_tweets
    elif choice == 2:
        tweets = get_user_tweets()
        while tweets == list():
            print('Sorry, no tweets in English from that person.')
            tweets = get_user_tweets()
    elif choice == 3:
        tweets = get_keyword_tweets()
    elif choice == 4:
        break

    analyze_setiments(tweets)
    
