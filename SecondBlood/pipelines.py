# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class SecondbloodPipeline:
    #重写父类的一个方法，该方法只会在开始爬虫的时候被调用一次
    def open_spider(self,spider):
        print("开始爬虫......")
        self.fp = open('./freedomsecurity.txt','a+',encoding='utf-8')

    #专门用来处理item类型对象
    #该方法可以接受爬虫文件提交过来的item对象
    #该方法每接收到一个item就会被调用一次
    def process_item(self, item, spider):
        article_name = item['article_name']
        article_url = item['article_url']
        self.fp.write(article_name + ':' + article_url + '\n')
        return item

    def close_spider(self,spider):
        print('结束爬虫。')
        self.fp.close()

#管道文件中一个管道对应一组数据存储到数据库中
class mysqlPileLine(object):
    conn = None
    cursor = None
    #创建数据库连接
    def open_spider(self,spider):
        self.conn = pymysql.Connect(host='localhost',port=3306,user='root',passwd='XSP4436283asd.',db='freedomsecurityhacker',charset='utf8')
    #将数据存储到数据库
    def process_item(self,item,spider):
        article_name = item['article_name']
        article_url = item['article_url']
        self.cursor = self.conn.cursor()
        #异常处理，存储数据
        try:
            self.cursor.execute('insert into freedomsecurityhacker values("%s","%s")',(article_name,article_url))
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        return item
    #关闭数据库连接
    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()
