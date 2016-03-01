#-*-coding:utf-8-*-
import urllib
import web
import os
import time

def get_poster(id,url):
	pic=urllib.urlopen(url).read()
	filename="/var/www/moviesite/static/poster/%d.jpg" %id
	f=file(filename,"wb")
	f.write(pic)
	f.close()

db=web.database(dbn="mysql",db="moviesite",user='root',passwd='1')
movies=db.select('movie')
count=0
for movie in movies:
        got_images=os.listdir("/var/www/moviesite/static/poster")
        movie_id=str(movie['id'])+'.jpg'
        if movie_id not in got_images:
                get_poster(movie['id'],movie['image'])
                count+=1
                print count,movie['title']
                time.sleep(2)
