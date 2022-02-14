# -*- coding: utf-8 -*-
import scrapy
from SecondBlood.items import SecondbloodItem
from gc import callbacks
from scrapy.http import Request

class FreedomsecurityhackerSpider(scrapy.Spider):
    name = 'freedomsecurityhacker'
    #allowed_domains = ['https://freedomsecurityhacker.com']
    #第一个页面的url
    start_urls = ['https://freedomsecurityhacker.com/index.php/page/1']
    
    def parse(self, response):
        article_list = response.xpath('//*[@id="app-main"]/div[2]/div[6]')
        #print(article_list)
        for list in article_list:
            #获取文章名
            article_name = list.xpath('.//h3/a[2]/text()').extract()
            #将获取到的列表数据转换为字符串
            article_name = ''.join(article_name)
            #获取文章url
            article_url = list.xpath('.//h3/a[2]/@href').extract()
            article_url = ''.join(article_url)
            print(article_name,article_url)

            #实例化一个items对象
            item = SecondbloodItem()
            #将获取到的数据封装到items对象
            item['article_name'] = article_name
            item['article_url'] = article_url
            yield item

        #获得下一个页面的url
        new_page = response.xpath('//*[@id="app-main"]/div[2]/ol//a/@href').extract()
        for next_page in new_page:
            print(next_page)
            yield Request(url = next_page, callback = self.parse) 