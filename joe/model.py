__author__ = 'bangnv'
import time
import datetime
from time import gmtime, strftime

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
from elasticsearch import Elasticsearch

es_client = Elasticsearch()
index_name = "joe"
comments = "comments"


class Comment:
    def __init__(self, link=None, content=None, author=None, date_time=None, thread_name=None, website=None,link_parent = None):
        self.link = link
        self.content = content
        self.date_time = int(time.mktime(datetime.datetime.strptime(date_time, DATE_FORMAT).timetuple()))
        self.date_string = date_time
        self.website = website
        self.thread_name = thread_name
        self.update = strftime("%H:%M:%S %d-%m-%Y", gmtime())
        self.link_parent = link_parent


    def to_dict(self):
        return self.__dict__

    def start_index(self):
        two_days_ago = int(time.time()) - 3 * 24 * 3600
        if (self.date_time > two_days_ago):
            print "insert data"
            print self.to_dict()
            es_id = "%s_%s" % (self.link, self.date_time)
            es_client.index(index=index_name, doc_type=comments, id=es_id, body=self.to_dict())




