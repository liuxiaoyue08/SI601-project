# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 16:36:17 2016

@author: Platina
"""
import os
from bs4 import BeautifulSoup
import json
import time
import re
os.chdir("E:\\thunder\\SWDE_Dataset\\movie\\movie\\movie-imdb(2000)")
files = os.listdir("E:\\thunder\\SWDE_Dataset\\movie\\movie\\movie-imdb(2000)")

page= open("0000.htm", "rU")
html_doc = page.read()
soup = BeautifulSoup(html_doc)
rating_str = soup.find_all("span", class_="rating-rating")[0].text
#rating = soup.find("div", "rating").attrs['id'].split('|')[-2]
rating = eval(rating_str)*10

