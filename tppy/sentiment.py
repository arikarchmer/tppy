import requests
from keys import TDkeys as k
import tweepy
import sys
from geocoder import Geocoder
import subprocess as sp


class Searcher():

    def search(self, keyword=None, city=None, state=None, coordinates=None, radius='5mi', num=20):

        auth = tweepy.OAuthHandler(k.consumer_key, k.consumer_secret)
        auth.set_access_token(k.access_token, k.access_token_secret)
        api = tweepy.API(auth)

        if coordinates is None and city is not None and state is not None:
            geo = Geocoder()
            coordinates = geo.getCoordinates(city, state)
            # tweets = api.search(q=keyword, geocode=coordinates)

        coordinate_str = '{lat},{lng},'.format(**coordinates) + radius
        tweets = api.search(q=keyword, geocode=coordinate_str, count=num, include_entities=True)

        tweets.sort(reverse=True, key=lambda x: x.author.followers_count)

        a = SentimentAnalyzer()
        return [{'author': t.author.name, "tweet": t.text, "id": t.id, "sentiment": a.analyze(t.text)} for t in tweets]



class SentimentAnalyzer():

    def analyze(self, t):

        url = 'http://text-processing.com/api/sentiment/'
        r = requests.post(url, data={'text': t, 'language': 'english'})
        res = r.content.split(':')
        # print res
        return {"negative": str(100*float(res[2].split(',')[0][1:])), "neutral": str(100*float(res[3].split(',')[0][1:])), "positive": str(100*float(res[4].split(',')[0][1:-2]))}

if __name__ == '__main__':

    def print_result():
        for r in range(len(results)):
            print "\n\n"
            print "*****"
            print "* " + str(r) + " *"
            print "*****"
            t = results[r]
            for k, v in t.iteritems():
                print str(k) + ': '
                print v


    keyword, city, state, num_tweets = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

    s = Searcher()
    results = s.search(keyword=keyword, city=city, state=state, num=num_tweets)

    print_result()

    overall_sentiment = [0, 0, 0]
    for r in results:
        for k, v in r.iteritems():
            if k == 'sentiment':
                for k2, v2 in v.iteritems():
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





