
def get_trending_tweets():
    trends = Twitter.trends_available()
    print()
    print("Where would you like to get trending tweets from?")
    print("1) Worldwide")
    print("2) Other")

    location = int(input())
    woeid = -1 #id used for identifying location through tweepy

    if location == 1:
        woeid = 1
    elif location == 2:
        location = str(input("Would you like to see some locations? (enter yes or no) "))
        while location != 'yes' and location != 'no':
            location = str(input('Error: please enter valid input'))

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
        results = Twitter.search(trend,tweet_mode='extended')
        for result in results:
            tweet = result.full_text
            tweet = re.sub(r'([^\s\w]|_)+', '', tweet)    #get just alphanum/spaces from tweets
            if tweet != '':
                if(detect(tweet) == 'en'): #if tweet is in english
                    search_results.append(tweet)
                

    for text in search_results:
        print(text)
    print('helloooooooo')
        
       

        
        





def get_user_tweets():
    print('hi')
def get_keyword_tweets():
    print('hi')

import re
import tweepy
from langdetect import detect

consumer_key = 'wailB3ljNEhmyzTu4eOIB69Qn'
consumer_secret = 'rkBX3Il6LxbAneofVPU1vIO9QjLwNgSlNrWJI371qPSqcdrQcV'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

access_token = '1244794411017535489-I6uPkLJNGhhKT5r2es3c7mkIXZDwzo'
access_token_secret = '0y0msMt3RmSlwcc50AJ6CaauJDVB6GR2cGglDj9KrAT0I'

auth.set_access_token(access_token, access_token_secret)

Twitter = tweepy.API(auth)

# public_tweets = api.home_timeline()
# print(type(public_tweets))
# for tweet in public_tweets:
#     print(tweet.text)

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
    elif choice == 2:
        tweets = get_user_tweets()
    elif choice == 3:
        tweets = get_keyword_tweets()
    elif choice == 4:
        break
