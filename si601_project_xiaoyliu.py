# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 23:55:06 2016

@author: Platina
"""

#Step 1.1: generate movie ratings from review rating files for each movieid in netflix
import os
import sqlite3 as sqlite
import urllib2
import json
import time
files = os.listdir("E:\\thunder\\nf_prize_dataset\\training_set\\training_set")
#function to get rating for each movieid
def get_rating(x):
    mvfile = open(x, "rU")
    count = 0
    ratings = []
    for line in mvfile:
        count += 1
        if count ==1:
            id = line.split(':')[0]
        else:
            (customerid, rating, date) = line.split(',')
            ratings.append(float(rating))
    avgrating = round(sum(ratings)/float(count),2)
    return (id,avgrating)

os.chdir("E:\\thunder\\nf_prize_dataset\\training_set\\training_set")

movie_rating = []
for file in files:
    movie_rating.append(get_rating(file))
#Save the ratings to a file
os.chdir("D:\\MA 2015\\SI601\\project")
movie_rating_file = open('movie_rating.txt','w')
for movie in movie_rating:
    movie_rating_file.write(movie[0]+'\t'+str(movie[1])+'\n')
movie_rating_file.close()   
#Step1.2 Join the ratings with movie names and year
#Step1.2.1 read in the movie_id_year_title
os.chdir("E:\\thunder\\nf_prize_dataset")
movie_titles = open('movie_titles.txt','rU')
movie_id_year_title = []
for line in movie_titles:
    line = line.strip('\n').decode('latin1')
    (id, year, title) = (line.split(',')[0],line.split(',')[1],','.join(line.split(',')[2:]))
    movie_id_year_title.append((id,year,title))
    
#Step1.2.2 join the datasets using sql
os.chdir("D:\\MA 2015\\SI601\\project")

with sqlite.connect('si601_project.db') as con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS movie_rating")
    cur.execute("CREATE TABLE movie_rating(id INT, rating REAL)")
    cur.executemany("INSERT INTO movie_rating VALUES(?,?)", movie_rating)
    con.commit()
    
with sqlite.connect('si601_project.db') as con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS movies")
    cur.execute("CREATE TABLE movies(id INT, year INT, title TEXT)")
    cur.executemany("INSERT INTO movies VALUES(?,?,?)", movie_id_year_title)
    con.commit()
    
with sqlite.connect('si601_project.db') as con:
    cur = con.cursor()
    cur.execute("SELECT movies.id, movies.year,movie_rating.rating,movies.title FROM movies JOIN movie_rating on (movies.id=movie_rating.id)")
    rows = cur.fetchall()
    
movie_info = open('movie_info.txt','w')
for row in rows:
    movie_info.write(str(row[0])+'\t'+str(row[1])+'\t'+str(row[2])+'\t'+row[3].encode('utf-8')+'\n')
movie_info.close()

#Step2: using API get the IMDB dataset
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

#Step3: Join dataset and compare

os.chdir("D:\\MA 2015\\SI601\\project")
imdbresult = []
imdbfile = open('movie_json2.txt', 'rU')
for line in imdbfile:
    (title, year, imrating, imdbid, genres, countrys) = line.decode('latin1').strip('\n').split('\t')
    for genre in genres.split(','):
        for country in countrys.split(','):
            imdbresult.append((imdbid, title, year, imrating, genre.strip(), country.strip()))
imdbfile.close()           
            
netflixresult = []
netflixfile = open('movie_info.txt','rU')
for line2 in netflixfile:
    (number, year, nfrating, title) = line2.decode('latin1').strip('\n').split('\t')
    netflixresult.append((title, year, nfrating))
netflixfile.close()


imdbraw = []
imdbrawfile = open('movie_json2.txt', 'rU')
for line in imdbrawfile:
    (title, year, imrating, imdbid, genres, countrys) = line.decode('latin1').strip('\n').split('\t')
    imdbraw.append((imdbid, title, year, genre.strip(), country.strip(), imrating))
imdbrawfile.close()

with sqlite.connect('si601_project_2.db') as con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS imdbraw")
    cur.execute("CREATE TABLE imdbraw(imdbid TEXT, title TEXT, year INT, genre TEXT, country TEXT, imrating REAL)")
    cur.executemany("INSERT INTO imdbraw VALUES(?,?,?,?,?,?)", imdbraw)
    con.commit()
with sqlite.connect('si601_project_2.db') as con:
    cur = con.cursor()
    cur.execute("SELECT count(*) as count_n FROM imdbraw WHERE imrating<>'0.0'")
    raw = cur.fetchall()
    print raw

with sqlite.connect('si601_project_2.db') as con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS imdb")
    cur.execute("CREATE TABLE imdb(imdbid TEXT, title TEXT, year INT, imrating TEXT, genre TEXT, country TEXT)")
    cur.executemany("INSERT INTO imdb VALUES(?,?,?,?,?,?)", imdbresult)
    con.commit()
with sqlite.connect('si601_project_2.db') as con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS netflix")
    cur.execute("CREATE TABLE netflix(title TEXT, year INT, nfrating TEXT)")
    cur.executemany("INSERT INTO netflix VALUES(?,?,?)", netflixresult)
    con.commit()

with sqlite.connect('si601_project_2.db') as con:
    cur = con.cursor()
    cur.execute("SELECT imdb.imdbid, imdb.title, imdb.year, imdb.genre, imdb.country, imdb.imrating, netflix.nfrating FROM imdb JOIN netflix ON (imdb.title=netflix.title and imdb.year=netflix.year) WHERE imdb.imrating<>'0.0' and imdb.imrating<>'N/A' and imdb.country<>'N/A' and imdb.genre<>'N/A'")
    rows = cur.fetchall()
    
movie_compare = open('movie_compare.txt','w')
for row in rows:
    movie_compare.write(str(row[0])+'\t'+row[1].encode('utf-8')+'\t'+str(row[2])+'\t'+str(row[3])+'\t'+str(row[4])+'\t'+str(row[5])+'\t'+str(float(row[6])*2)+'\n')
movie_compare.close()

with sqlite.connect('si601_project_2.db') as con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS movies")
    cur.execute("CREATE TABLE movies(imdbid TEXT, title TEXT, year INT, genre TEXT, country TEXT, imrating REAL, nfrating REAL)")
    cur.executemany("INSERT INTO movies VALUES(?,?,?,?,?,?,?)", rows)
    con.commit()

with sqlite.connect('si601_project_2.db') as con:
    cur = con.cursor()
    cur.execute("SELECT country, genre, count(*) as count_n, AVG((imrating+2*nfrating)/2) as rating_m FROM movies GROUP BY country,genre HAVING count_n>100 ORDER BY rating_m DESC LIMIT 10")
    movie_c_g =  cur.fetchall()
    for movie in movie_c_g:
        print "%s, %s, %s, %s" % (movie[0],movie[1],movie[2],movie[3])
        
movie_cg = open('movie_cg.txt','w')
movie_cg.write('country\tgenre\tnumber\taverage rating\n')
for movie in movie_c_g:
    movie_cg.write(str(movie[0])+'\t'+str(movie[1])+'\t'+str(movie[2])+'\t'+str(movie[3])+'\n')
movie_cg.close()

with sqlite.connect('si601_project_2.db') as con:
    cur = con.cursor()
    cur.execute("SELECT title, AVG((imrating+2*nfrating)/2) as rating_mean FROM movies GROUP BY title,year ORDER BY rating_mean DESC LIMIT 10")
    movie_top =  cur.fetchall()
    for movie in movie_top:
        print "%s, %s" % (movie[0],movie[1])
        
with sqlite.connect('si601_project_2.db') as con:
    cur = con.cursor()
    cur.execute("SELECT title, AVG(ABS(imrating-2*nfrating)) as rating_diff FROM movies GROUP BY title,year ORDER BY rating_diff DESC LIMIT 10")
    movie_diff =  cur.fetchall()
    for movie in movie_diff:
        print "%s, %s" % (movie[0],movie[1])

with sqlite.connect('si601_project_2.db') as con:
    cur = con.cursor()
    cur.execute("SELECT country,year, AVG((imrating+2*nfrating)/2) as rating_year FROM movies WHERE country='UK' or country ='USA' or country ='Japan' GROUP BY country,year ORDER BY country,year")
    movie_cy =  cur.fetchall()
    for movie in movie_cy:
        print "%s, %s, %s" % (movie[0],movie[1],movie[2])
    
