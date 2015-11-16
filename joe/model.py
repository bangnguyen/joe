__author__ = 'bangnv'
import time
import datetime
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
class Comment:
    def __init__(self, link=None, content=None, author=None, date_time=None, thread_name=None,website=None):
        self.link = link
        self.content = content
        self.date_time = int(time.mktime(datetime.datetime.strptime(date_time,DATE_FORMAT).timetuple()))
        self.date_string = date_time
        self.website=website
        self.thread_name = thread_name



    def to_dict(self):
        return self.__dict__



