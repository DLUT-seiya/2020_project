# -*-coding:utf-8-*-
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import sys
import re
reload(sys)
sys.setdefaultencoding('gb2312')
from tornado.options import define,options
define('port',8080)
from pymongo import MongoClient
from bson.objectid import ObjectId
def getDB():
    client = MongoClient('localhost', 27017)

    db = client.program
    collection = db.record
    return collection
class SelectByType(tornado.web.RequestHandler):
    def get(self):
        type=self.get_argument("type")
        args=self.get_argument('args')
        if type=='title':
            list=getDB().find({'title':re.compile(args)})
            self.render('one.html', bindex=0, cindex=1, my_list=list)
        elif type=='type':
            list=getDB().find({'type':re.compile(args)})
            self.render('one.html', bindex=0, cindex=1, my_list=list)
        elif type=='add':
            list=getDB().find({'add':re.compile(args)})
            self.render('one.html', bindex=0, cindex=1, my_list=list)
        elif type=='price':
            list=getDB().find({'money':re.compile(args)})
            self.render('one.html', bindex=0, cindex=1, my_list=list)
        self.redirect('/one')

class OneHandler(tornado.web.RequestHandler):
    def get(self):

        my_list=getDB().find().limit(10)


        self.render('one.html',bindex=0,cindex=1,my_list=my_list)
class NextCutpage (tornado.web.RequestHandler):
    def get(self):
       index=int( self.get_argument('cindex'))
       my_list = getDB().find().skip(index * 10).limit(10)
       num=getDB().count()

       if index*10<=num:
        self.render('one.html', bindex=index, cindex=index+1, my_list=my_list)
       else:
           self.write("已经是最后一页，没有页面了！<br> <a href='acutpage?bindex="+self.get_argument('cindex')+"'>返回上一页</a>")
class AfterCutpage (tornado.web.RequestHandler):
    def get(self):
       index=int( self.get_argument('bindex'))

       if index !=0:
        myindex=index-1
        my_list = getDB().find().skip(myindex * 10).limit(10)
        self.render('one.html', bindex=index-1, cindex=index, my_list=my_list)
       else:
           self.write("已经是第一页，没有页面了！<br><a href='/one'>返回上一页</a>")
class DeleteHandler(tornado.web.RequestHandler):
    def get(self):
        from bson.objectid import ObjectId
        ID=self.get_argument("id")
        getDB().post.remove({'_id':ObjectId(ID)})
        self.render('')

class DeleteHandler(tornado.web.RequestHandler):
    def get(self):
        id=self.get_argument("id")
        getDB().remove({'_id':ObjectId(id)})
        self.redirect('/one')

class ModifyHandler(tornado.web.RequestHandler):
    def get(self):
        id = self.get_argument("id")
        my_list=getDB().find_one({'_id':ObjectId(id)})

        self.render('modify.html',my_list=my_list)


class UpdateHandler(tornado.web.RequestHandler):
    def get(self):
        id=self.get_argument('id')
        title=self.get_argument('title')
        type=self.get_argument('type')
        add=self.get_argument('add')
        linkman=self.get_argument('linkman')
        detail=self.get_argument('detail')
        money=self.get_argument('money')
        getDB().update({'_id': ObjectId(id)}, {'$set': {'title':title,'add':add}})
        self.redirect('/one')



if __name__=='__main__':



    tornado.options.parse_command_line()
    app=tornado.web.Application(handlers=[
        (r'/one',OneHandler),
        (r'/delete',DeleteHandler),
        (r'/modify', ModifyHandler),
        (r'/update', UpdateHandler),
        (r'/select', SelectByType),
        (r'/ncutpage', NextCutpage),
        (r'/acutpage', AfterCutpage)


    ],
    template_path=os.path.join(os.path.dirname(__file__),"templates"),
    static_path=os.path.join(os.path.dirname(__file__),"static")
    )
    server=tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()