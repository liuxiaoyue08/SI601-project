# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 13:00:00 2016

@author: Platina
"""
#Step 1: generate movie ratings from review rating files for each movieid in netflix
import os
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
#Step2 Join the ratings with movie names and year
#Step2.1 read in the movie_id_year_title
os.chdir("E:\\thunder\\nf_prize_dataset")
movie_titles = open('movie_titles.txt','rU')
movie_id_year_title = []
for line in movie_titles:
    line = line.strip('\n').decode('latin1')
    (id, year, title) = (line.split(',')[0],line.split(',')[1],','.join(line.split(',')[2:]))
    movie_id_year_title.append((id,year,title))
    
#Step2.2 join the datasets using sql
os.chdir("D:\\MA 2015\\SI601\\project")
import sqlite3 as sqlite
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
    


    