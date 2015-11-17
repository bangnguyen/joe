from joe.utils.allfunctions import *

website = "www.hairlossexperiences.com/"
import pdb
import re
class Hirlossexperiences(CrawlSpider):
    name = "f2"
    start_urls = [
        # "http://www.hairlossexperiences.com",
        "http://www.hairlossexperiences.com/view_topic.php?forum_id=3&id=5051&page=10"
    ]
    cpt = 0;
    rules = [
        Rule(lxml(allow=('view_forum.php\?id=\d+',)), callback='parse_cat',
             follow=True),
        Rule(lxml(allow=('/view_topic.php\?id=\d+',), ), callback='parse_product')
    ]

    def parse_cat(self, response):
        print "parse_cat " + response.url


    def parse_product(self, response):
        print "parse_product " + response.url
        return self.create_comment(response)



    def create_comment(self, response):
        link = response.url
        tables = response.xpath("/html/body/center/center[2]/table/table")
        if (len(tables) >= 4):
            thread_name = html_to_text(tables[0].xpath("./tr/td/text()").extract())
            tables.pop(0)
            tables.pop(0)
            for table1, table2 in pairwise(tables):
                text_date = table1.xpath("./tr/td/text()")[0].extract()
                is_date = re.search("Posted:(.*)", text_date)
                if is_date:
                    date_time = convert_date(is_date.group(1))
                    content = html_to_text(table2.xpath("./tr/td[2]//text()").extract())
                    comment = Comment(link=link, content=content, date_time=date_time, website=website,
                                      thread_name=thread_name)
                    es_id = "%s_%s" % (link, comment.date_time)
                    es_client.index(index=index_name, doc_type=comments, id=es_id, body=comment.to_dict())




