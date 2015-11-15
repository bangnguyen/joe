from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor as lxml
from joe.items import JoeItem
from joe.utils.html_string import *
from joe.utils.datetimefunctions import *
from  joe.model import *
import pdb
from elasticsearch import Elasticsearch
es_client = Elasticsearch()
index_name="joe"
comments= "comments"
website="www.baldtruthtalk.com"
class Baldtruthtalk(CrawlSpider):
    name = "bald"
    #allowed_domains = ["www.baldtruthtalk.com"]
    start_urls = [
        "https://www.baldtruthtalk.com"
        #"https://www.baldtruthtalk.com/threads/20438-Recommendations-to-Sell-Stock-Systems"
    ]
    cpt =0;
    rules = [
        Rule(lxml(allow=('/forums/',),restrict_xpaths="//div[@class='forumdata']//a"),callback='parse_cat', follow=True),
        Rule(lxml(allow=('/threads/',),), callback='parse_product')
    ]

    #def parse(self, response):
    #    print response.url
    #    return self.create_comment(response)

    def parse_cat(self, response):
        print response.url


    def parse_product(self, response):
        return self.create_comment(response)
        self.cpt += 1
        print self.cpt
        return None

    def create_comment(self,response):
        post_list= response.xpath("//div[@id='postlist']/ol/li")
        for post in post_list:
            date_text= post.xpath("./div[@class='posthead']//span[@class='date']")
            link=response.url
            date=convert_date(html_to_text(date_text.extract()))
            content=html_to_text(post.xpath(".//div[@class='postdetails']//div[@class='content']").extract())
            time_stamp = date_to_timestamp(date)
            es_id="%s_%s"%(link,time_stamp)
            comment = Comment(link=link,content=content,date_time=time_stamp,website=website)
            es_client.index(index=index_name, doc_type=comments, id=es_id, body=comment.to_dict())
            print date
            print link
            print content
