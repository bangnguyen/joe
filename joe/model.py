__author__ = 'bangnv'
class Comment:
    def __init__(self, link=None, content=None, author=None, date_time=None, thread_name=None,website=None):
        self.link = link
        self.content = content
        self.date_time = date_time
        self.website=website



    def to_dict(self):
        return self.__dict__



