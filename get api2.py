# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 17:51:16 2016

@author: Platina
"""

import urllib2
import json
import time

movie_info = open('movie_info.txt','rU')
movie_id_year_rating_title = []
for line in movie_info:
    line = line.strip('\n').decode('latin1')
    (id, year, rating, title) = line.split('\t')
    movie_id_year_rating_title.append((id,year,rating,title))
movie_info.close()

movie_json = open('movie_json2.txt','w')
for i in range(0,len(movie_id_year_rating_title)):
    try:
        response = urllib2.urlopen('http://www.omdbapi.com/?t='+'+'.join(movie_id_year_rating_title[i][3].encode('utf-8').split())+'&y='+movie_id_year_rating_title[i][1])
        content = response.read()
    except:
        time.sleep(5)
    try:
        imdbrating = json.loads(content)['imdbRating']
        imdbid = json.loads(content)['imdbID']
        genre = json.loads(content)['Genre']
        country = json.loads(content)['Country']
    except:
        imdbrating = 0.0
        imdbid = 'N/A'
        genre = 'N/A'
        country = 'N/A'
    try:
        movie_json.write(movie_id_year_rating_title[i][3].encode('utf-8')+"\t"+movie_id_year_rating_title[i][1]+"\t"+str(imdbrating)+'\t'+imdbid+'\t'+genre+'\t'+country+"\n")
    except:
        continue
movie_json.close()