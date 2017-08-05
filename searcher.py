# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 11:43:36 2017

@author: akarchmer
"""
from keys import TDkeys as k
import tweepy
from geocoder import Geocoder
from sentimentAnalyzer import SentimentAnalyzer

class Searcher():

    def search(self, keyword=None, city=None, state=None, coordinates=None, radius='5mi', num=20):

        auth = tweepy.OAuthHandler(k.consumer_key, k.consumer_secret)
        auth.set_access_token(k.access_token, k.access_token_secret)
        api = tweepy.API(auth)

        geo = Geocoder()

        print '\nGathering tweets...\n'
        
        #kcs
        if keyword is not None and city is not None and state is not None and coordinates is None:
            coordinates = geo.getCoordinates(city, state)
            coordinate_str = '{lat},{lng},'.format(**coordinates) + radius
            tweets = api.search(q=keyword, geocode=coordinate_str, count=num)
        
        #cs
        if keyword is None and city is not None and state is not None and coordinates is None:
            coordinates = geo.getCoordinates(city, state)
            coordinate_str = '{lat},{lng},'.format(**coordinates) + radius
            tweets = api.search(geocode=coordinate_str, count=num)
            
        #kl
        if keyword is not None and city is None and state is None and coordinates is not None:
            coordinate_str = '{lat},{lng},'.format(**coordinates) + radius
            tweets = api.search(q=keyword, geocode=coordinate_str, count=num)
            
        #l
        if keyword is None and city is None and state is None and coordinates is not None:
            coordinate_str = '{lat},{lng},'.format(**coordinates) + radius
            tweets = api.search(geocode=coordinate_str, count=num)
            
        #k
        if keyword is not None and city is None and state is None and coordinates is None:
            tweets = api.search(q=keyword, count=num)
            
        #st
            
            
        tweets.sort(reverse=True, key=lambda x: x.author.followers_count)

        print '\nAnalyzing data...\n'
        a = SentimentAnalyzer()
        return [{'author': t.author.name, "tweet": t.text, "id": t.id, "sentiment": a.analyze(t.text)} for t in tweets]
