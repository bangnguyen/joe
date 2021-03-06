from scrapy import Selector
from scrapy.http.response.html import HtmlResponse
from scrapy.http.response.html import TextResponse
from scrapy.selector.unified import SelectorList
from scrapy.utils.response import open_in_browser
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor as lxml
from joe.items import JoeItem
from joe.utils.html_string import *
from joe.utils.datetimefunctions import *
from  joe.model import *
import pdb
from elasticsearch import Elasticsearch
from itertools import izip
es_client = Elasticsearch()
index_name = "joe"
comments = "comments"
def mapping(value, mappings):
    for k in mappings:
        if contains_ignore_case(value, mappings[k]):
            return k
    return None\


def contains_ignore_case(v, l):
    return v.lower() in [k.lower() for k in l]


def is_existed_in_mapping(value, mappings):
    for k in mappings:
        if contains_ignore_case(value, mappings[k]):
            return True
    return False





def append_to_list(l, data, unique=True):
    l.extend(data) if isinstance(data, list) else l.append(data)
    l = list(set(l)) if unique else l
    return l


"""
return list[selector]
"""





"""
    # convert to product_type defined by balloon
    # input : product_type

"""

def view(data):
    if isinstance(data, HtmlResponse) or isinstance(data, TextResponse):
        open_in_browser(data)
    elif isinstance(data, Selector):
        open_in_browser(TextResponse(url="",encoding='utf-8', body=data.extract(), request=None))
    elif isinstance(data, SelectorList):
        content = ""
        for i in data:
            content += "%s <br>" % (i.extract())
        open_in_browser(TextResponse(url="",encoding='utf-8', body=content, request=None))
    else:
        open_in_browser(TextResponse(url="",encoding='utf-8', body=str(data), request=None))


def pairwise(iterable):
    a = iter(iterable)
    return izip(a, a)









