#!/usr/bin/python 
#-*-coding:utf-8-*-
import json
import MySQLdb
import urllib
import time
import web


movie_ids=[]

#读取top250电影的id号
for index in range(0,250,50):
	print index 
	response=urllib.urlopen('http://api.douban.com/v2/movie/top250?start=%d&count=50'%index)
	data_json=json.loads(response.read())
	movie250=data_json['subjects']
	for movie in movie250:
        #以整数形式存储电影id号
		movie_ids.append(int(movie['id']))
		print movie['id'],movie['title']
	time.sleep(3) 
#访问本地数据库
conn=MySQLdb.connect(host='localhost',port=3306,user='root',passwd='1',db='moviesite')
cur=conn.cursor()
result=cur.execute("select id from movie")
print result
info=cur.fetchmany(result)
movie_in_db=[]
for i in info:
    d=i[0]
    d=int(d)
    movie_in_db.append(d)
print  "======================================================"
for movie_id in movie_ids:
    if movie_id not in movie_in_db:
        print movie_id
