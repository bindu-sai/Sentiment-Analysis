import credentials as crd
from textblob import TextBlob
import tweepy
import re
import pandas as pd
import matplotlib.pyplot as plt

consumerKey = crd.consumer_key
consumerKeySecret = crd.consumer_key_secret
accessToken = crd.access_token
accessTokenSecret = crd.access_token_secret

auth=tweepy.OAuthHandler(consumer_key=consumerKey,consumer_secret=consumerKeySecret)
auth.set_access_token(accessToken,accessTokenSecret)
api=tweepy.API(auth)

numOfTweets= int(input('How many tweets to analyze'))
searchWord="#coronavirus"
date_since="2020-03-10"
tweets=tweepy.Cursor(api.search, q=searchWord, lang='en',since=date_since,tweet_mode="extended").items(numOfTweets)
#for tweet in tweets:
#    i=1
#    print(i,")",tweet.full_text,"\n")
#    analysis=TextBlob(tweet.full_text)
#    print(analysis.sentiment)

def cleanText(text):
    text=re.sub('https?://[^\s]+','URL',text)
    text=re.sub('@[^\s]+','',text)
    text=re.sub(r'#','',text)
    text=re.sub(r'RT[\s]','',text)
    text=re.sub('\n',"",text)
    return text

def getPolarity(text):
    return TextBlob(text).sentiment.polarity

def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity
    
def getAnalysis(score):
    if score < 0.0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'

    
df=pd.DataFrame([tweet.full_text for tweet in tweets],columns=['Tweets'])
df['Tweets']=df['Tweets'].apply(cleanText)
df['Polarity']=df['Tweets'].apply(getPolarity)
df['Subjectivity']=df['Tweets'].apply(getSubjectivity)
df['Analysis']=df['Polarity'].apply(getAnalysis)
print(df)

plt.title('Sentiment Analysis')
plt.xlabel('Sentiment')
plt.ylabel('Counts')
df['Analysis'].value_counts().plot(kind='bar')
plt.show()

