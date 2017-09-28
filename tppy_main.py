# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 11:46:49 2017

@author: akarchmer
"""

from searcher import Searcher
from streamer import StdOutListener
from keys import keys as k
import sys

class Sentiment():
    
    def print_result(self, results):
        for r in range(len(results)):
            print "\n\n"
            print "*****"
            print "* " + str(r) + " *"
            print "*****"
            t = results[r]
            for key, val in t.iteritems():
                print str(key) + ': '
                print val
                
    
    def getMode(self, args):

        arg1 = args[1]
        
        if arg1[0] == '-':
            if arg1 == '-kcs':
                return 'keywordcitystate'
            if arg1 == '-cs':
                return 'citystate'
            if arg1 == '-kl':
                return 'keywordlatlngr'
            if arg1 == '-l':
                return 'latlngr'
            if arg1 == '-k':
                return 'keyword'
            if arg1 == '-st':
                return 'stream'
                

if __name__ == '__main__':
    
    keyword, city, state, lat, lng, r, num_tweets = None, None, None, None, None, None, None
    
    sent = Sentiment()
    
    mode = sent.getMode(sys.argv)
    print mode
    
    s = Searcher()
    
    if mode == 'keywordcitystate':
        keyword, city, state, num_tweets = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
        results = s.search(keyword=keyword, city=city, state=state, num=num_tweets)
    if mode == 'citystate':
        city, state, num_tweets = sys.argv[2], sys.argv[3], sys.argv[4]
        results = s.search(city=city, state=state, num=num_tweets)
    if mode == 'keywordlatlngr':
        keyword, lat, lng, r, num_tweets = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]
        results = s.search(keyword=keyword, coordinates={'lat': lat, 'lng': lng}, radius=r, num=num_tweets)
    if mode == 'latlngr':
        lat, lng, r, num_tweets = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
        results = s.search(coordinates={'lat': lat, 'lng': lng}, radius=r, num=num_tweets)
    if mode == 'keyword':
        keyword, num_tweets = sys.argv[2], sys.argv[3]
        results = s.search(keyword=keyword, num=num_tweets)
        
    if mode == 'stream':
        keyword = sys.argv[2]
        print 'Streaming tweets about ' + keyword + ':\n'
        
        streamer = StdOutListener()
        streamer.stream(k.consumer_key, k.consumer_secret, k.access_token, k.access_token_secret, t=keyword)

    else:
        
        if keyword:
            print 'keyword: ' + keyword
        if city:
            print 'city: ' + city
        if state:
            print 'state: ' + state
        if lat:
            print 'lat: ' + lat
        if lng:
            print 'lng: ' + lng
        if r:
            print 'radius: ' + r
        print '****************************\n\n'
        
        sent.print_result(results)
    
        overall_sentiment = [0, 0, 0]
        for r in results:
            for key, val in r.iteritems():
                if key == 'sentiment':
                    for k2, v2 in val.iteritems():
                        if k2 == 'positive':
                            overall_sentiment[0] += float(v2)
                        if k2 == 'neutral':
                            overall_sentiment[1] += float(v2)
                        if k2 == 'negative':
                            overall_sentiment[2] += float(v2)
                            
        print
        print '--------------------------------'
        print '------ overall sentiment -------'
        print '--------------------------------'
        print '|| positivity: ' + str(overall_sentiment[0] / int(num_tweets)) + '% ||'
        print '|| neutrality: ' + str(overall_sentiment[1] / int(num_tweets)) + '% ||'
        print '|| negativity: ' + str(overall_sentiment[2] / int(num_tweets)) + '% ||'
        print '--------------------------------'