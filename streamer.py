__author__ = 'arikarchmer'

import tweepy
import json
import time
from sentimentAnalyzer import SentimentAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
import sys
import math
from datetime import datetime
import calendar

# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(tweepy.StreamListener):
    
    my_data = []
    keyword = None
    stop = True

    def setKeyword(self, k):
        self.keyword = k
        
    
    def getKeyword(self):
        return self.keyword
        
    
    def printRes(self, res):
        print "\n\n"
        print "**********"
        for k, v in res.iteritems():
            print str(k) + ': '
            print v
    

    def on_data(self, data):
        a = SentimentAnalyzer()
        obj = json.loads(data)

        result = {}
        if 'author' in obj:
            author = obj['author']
            if 'name' in author:
                result['author'] = author['name']
        if 'text' in obj:
            result['tweet'] = obj['text'].encode('utf-8').strip()
        if 'id' in obj:
            result['id'] = obj['id']
            
        k = self.getKeyword()
        print k
        if k is not None:
            if k in result['tweet']:
            
                result['sentiment'] = a.analyze(result['tweet'])
        
                self.printRes(result)
    
                self.my_data.append((result['sentiment']['positive'], calendar.timegm(time.gmtime()) / 1000.0))
                time.sleep(1)

                return True
        else:
            if 'tweet' in result:
                result['sentiment'] = a.analyze(result['tweet'])
            
                self.printRes(result)
                
                self.my_data.append((result['sentiment']['positive'], calendar.timegm(time.gmtime()) / 1000.0))
                time.sleep(1)

            return True

    def on_error(self, status):
        return False

    
    #geo is object with keys: lat, lng, radius
    def stream(self, consumer_key, consumer_secret, access_token, access_token_secret, t=None, geo=None):
        
        self.setKeyword(t)
        
        try:
            # This handles Twitter authetification and the connection to Twitter Streaming API
            l = StdOutListener()
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            stream = tweepy.Stream(auth, l)
    
            if geo is not None and t is not None:
                box = str(float(geo['lat']) - float(geo['radius'])*math.cos(45)) + ',' + str(float(geo['lng'] - float(geo['radius'])*math.sin(45))) + ',' + str(float(geo['lat']) + float(geo['radius'])*math.cos(45)) + ',' + str(float(geo['lng'] + float(geo['radius'])*math.sin(45)))
                self.setKeyword(t)                
                stream.filter(geocode=box, languages=["en"])
            elif geo is None and t is not None:
                stream.filter(track=t, languages=["en"])
            elif geo is not None and t is None:
                box = str(float(geo['lat']) - float(geo['radius'])*math.cos(45)) + ',' + str(float(geo['lng'] - float(geo['radius'])*math.sin(45))) + ',' + str(float(geo['lat']) + float(geo['radius'])*math.cos(45)) + ',' + str(float(geo['lng'] + float(geo['radius'])*math.sin(45)))         
                stream.filter(geocode=box, languages=["en"])
        
        except KeyboardInterrupt:
            
            print '\nSTOPPING STREAM\n'
            print self.my_data
            df = pd.DataFrame(data=self.my_data, columns=['sentiment', 'time'])
            df = df.set_index('time')
            print df
#            results = df.scatter()

            results = plt.plot(df['time'], df['sentiment'], color='green', alpha=0.66)
            plt.savefig('results')

            sys.exit(0)

