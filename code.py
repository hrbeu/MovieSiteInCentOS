#-*- coding:utf-8 -*-
import web

urls=(
      '/','index',
      '/(.*?)/', 'redirect',        #保证网址有无'/'结尾，都能指向同一个类
      '/movie/(\d+)','movie',
      '/cast/(.*[^/])$','cast',
      '/director/(.*[^/])$','director',
      )

render=web.template.render('/var/www/moviesite/templates/')
#格式：db=web.database(dbn='postgres', db='mydata', user='dbuser', pw='')
db=web.database(dbn='mysql',db='moviesite',user='root',pw='1')

class index:
     def GET(self):
          movies=db.select('movie')# Select all entries from table
          statement='SELECT COUNT(*) AS COUNT FROM movie'
          count=db.query(statement)[0]['COUNT']
          out=render.index(movies,count,None)
          print ' %s Method from IP: %s' % (web.ctx.method,web.ctx.ip)
          print ' Request page %s ' % out.title
          return out

     def POST(self):
          data=web.input()
          condition=r'title like "%'+data.title+r'%"'
          movies=db.select('movie',where=condition)
          statement='SELECT COUNT(*) AS COUNT FROM movie WHERE '+condition
          result=db.query(statement)
          #print result
          result_one=result[0]
          #print result_one
          count=result_one['COUNT']
          out=render.index(movies,count,data.title)
          print ' %s Method from IP: %s' % (web.ctx.method,web.ctx.ip)
          print ' Request page %s ' % out.title
          return out
#保证网址有无'/'结尾，都能指向同一个类
class redirect:
      def GET(self,path):
          print ' %s Method from IP: %s' % (web.ctx.method,web.ctx.ip)
          raise web.seeother('/'+path)

class movie:
     def GET(self,movie_id):
          movie_id=int(movie_id)
          movie=db.select('movie',where='id=$movie_id',vars=locals())[0]
          out=render.movie(movie)
          print ' %s Method from IP: %s' % (web.ctx.method,web.ctx.ip)
          print ' Request page %s ' % out.title
          return out

class cast:
     def GET(self,cast_name):
          condition=r'casts like "%'+cast_name +r'%"'
          movies=db.select('movie',where=condition)
          statement='SELECT COUNT(*)  FROM movie  WHERE '+condition
          count=db.query(statement)[0]['COUNT(*)']
          out=render.index(movies,count,cast_name)
          print ' %s Method from IP: %s' % (web.ctx.method,web.ctx.ip)
          print ' Request page %s ' % out.title
          return out

class director:
      def GET(self,director_name):
          condition=r'directors like "%'+director_name+r'%"'
          movies=db.select('movie',where=condition)
          statement='SELECT COUNT(*) AS COUNT FROM movie WHERE '+condition
          count=db.query(statement)[0]['COUNT']
          out=render.index(movies,count,director_name)
          print ' %s Method from IP: %s' % (web.ctx.method,web.ctx.ip)
          print ' Request page %s ' % out.title
          return out


def notfound():
    print ' %s Method from IP: %s' % (web.ctx.method,web.ctx.ip)
    #return web.notfound("Sorry,the page you were looking for was not found.")
    return web.notfound(render.notfound())
def internalerror():
    print ' %s Method from IP: %s' % (web.ctx.method,web.ctx.ip)
    #return web.internalerror('Bad, bad server. No donut for you.')
    return web.internalerror(render.notfound())

print 'The value of name is'+__name__
app=web.application(urls,globals())
app.notfound=notfound
app.internalerror=internalerror
application=app.wsgifunc()
