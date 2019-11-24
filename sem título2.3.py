# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 12:46:03 2018
@author: Bruno Martins
"""
import twitter_credentials as tc
import tweepy
#import csv
import pandas as pd 
import numpy as np
import re
from textblob import TextBlob

# # # # # # # # # # # # # # # # # 
# Tratamento do tweet - código base usado: https://www.youtube.com/watch?v=1gQ6uG5Ujiw
# # # # # # # # # # # # # # # # # 

def clean_tweet(tweet):   ###(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+) - MOD ([^0-9A-Za-z\u0000-\uffff \t])|(\w+:\/\/\S+) 
        return ' '.join(re.sub("([^0-9A-Za-z\u0000-\uffff \t])|(\w+:\/\/\S+)", " ", tweet).split())

# # # # # # # # # # # # # # # # # 
# Módulos de autenticação do Twitter - código base usado: https://www.youtube.com/watch?v=1gQ6uG5Ujiw
# # # # # # # # # # # # # # # # # 

auth = tweepy.OAuthHandler(tc.CONSUMER_KEY, tc.CONSUMER_SECRET)
auth.set_access_token(tc.ACCESS_TOKEN, tc.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth,wait_on_rate_limit=True)


# # # # # # # # # # # # # # # # # 
# Extrator de Tweets  - código base usado: https://www.youtube.com/watch?v=1gQ6uG5Ujiw
# # # # # # # # # # # # # # # # # 

search_date = '2019-11-20'
tweets=[]
for tweet in tweepy.Cursor(api.search,q="$AAPL",count=100, lang="en", since=str(search_date)).items():
    print(tweet.text,'/n', '---------------CRIADO EM----------------/n/n ', tweet.created_at)
    tweets.append(tweet)

# # # # # # # # # # # # # # # # # 
# Criação do dataframe para análise de sentimento  - código base usado: https://www.youtube.com/watch?v=1gQ6uG5Ujiw
# # # # # # # # # # # # # # # # # 

df = pd.DataFrame(data=[clean_tweet(tweet.text) for tweet in tweets], columns=['Tweets']) #limpeza removida - clean_tweet(tweet.text)
df['date'] = np.array([tweet.created_at for tweet in tweets])
df['source'] = np.array([tweet.source for tweet in tweets])
df['id'] = np.array([tweet.id for tweet in tweets])
df['len'] = np.array([len(tweet.text) for tweet in tweets])
df['date'] = np.array([tweet.created_at for tweet in tweets])
df['source'] = np.array([tweet.source for tweet in tweets])
df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

# # # # # # # # # # # # # # # # # 
# Análise de sentimento dos dados extraídos - código base usado: https://www.youtube.com/watch?v=1gQ6uG5Ujiw
# # # # # # # # # # # # # # # # # 

def analyze_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))

    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1
    


df['sentiment'] = np.array([analyze_sentiment(tweet) for tweet in df['Tweets']])
df['polarity'] = np.array([(TextBlob(clean_tweet(tweet)).polarity) for tweet in df['Tweets']])

# # # # # # # # # # # # # # # # # 
# Salvando o arquivo  - código base usado: https://www.youtube.com/watch?v=1gQ6uG5Ujiw
# # # # # # # # # # # # # # # # # 
df.to_csv('base_aapl20-11.csv',index=True)#, encoding='utf-8')
#df.to_excel("output_sem_tratamento.xlsx", index=True, encoding=str)
