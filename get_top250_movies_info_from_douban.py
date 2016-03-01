#!/usr/bin/python 
#-*-coding:utf-8-*-
import json
import urllib
import time
import web


db=web.database(dbn='mysql',user='root',pw='1',db='moviesite')
movie_ids=[]

#读取top250电影的id号
for index in range(0,250,50):
	print index 
	response=urllib.urlopen('http://api.douban.com/v2/movie/top250?start=%d&count=50'%index)
	data_json=json.loads(response.read())
	movie250=data_json['subjects']
	for movie in movie250:
		movie_ids.append(movie['id'])
		print movie['id'],movie['title']
	time.sleep(3)  	
print movie_ids	

#每条电影信息写入数据库
def add_database(data):
    movie=json.loads(data)
    print movie['id'],movie['title']
    
    db.insert('movie',
		id=int(movie['id']),
		title=movie['title'],
		origin=movie['original_title'],
		url=movie['alt'],
		rating=movie['rating']['average'],
		image=movie['images']['large'],
		directors=','.join([d['name'] for d in movie['directors']]),
		casts=','.join([c['name'] for c in movie['casts']]),
		year=movie['year'],
		genres=','.join(movie['genres']),
		countries=','.join(movie['countries']),
		summary=movie['summary'],
		)


count=0
for movie_id in movie_ids:
    print count,movie_id
    response=urllib.urlopen('http://api.douban.com/v2/movie/subject/%s' % movie_id)
    try:
        add_database(response.read())
    except KeyError:
        print movie_id+"cant't get ,try next one..."
        continue
    count+=1
    print count
    time.sleep(3)
