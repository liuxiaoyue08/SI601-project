# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 16:39:48 2016

@author: Platina
"""
import os
import sqlite3 as sqlite

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
    cur.execute("SELECT country, genre, count(*) as count_n, AVG((imrating+nfrating)/2) as rating_m FROM movies GROUP BY country,genre HAVING count_n>100 ORDER BY rating_m DESC LIMIT 10")
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
    cur.execute("SELECT title, imrating+2*nfrating as rating_mean FROM movies WHERE title='Band of Brothers' ORDER BY rating_mean DESC LIMIT 10")
    movie_diff =  cur.fetchall()
    for movie in movie_diff:
        print "%s, %s" % (movie[0],movie[1])
        
with sqlite.connect('si601_project_2.db') as con:
    cur = con.cursor()
    cur.execute("SELECT title, AVG(imrating-nfrating) as rating_diff FROM movies GROUP BY title,year ORDER BY rating_diff DESC LIMIT 10")
    movie_diff =  cur.fetchall()
    for movie in movie_diff:
        print "%s, %s" % (movie[0],movie[1])


    