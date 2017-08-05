# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 11:42:53 2017

@author: akarchmer
"""

import requests

class SentimentAnalyzer():

    def analyze(self, t):

        url = 'http://text-processing.com/api/sentiment/'
        r = requests.post(url, data={'text': t, 'language': 'english'})
        res = r.content.split(':')
        # print res
        return {"negative": str(100*float(res[2].split(',')[0][1:])), 
            "neutral": str(100*float(res[3].split(',')[0][1:])), 
            "positive": str(100*float(res[4].split(',')[0][1:-2]))}