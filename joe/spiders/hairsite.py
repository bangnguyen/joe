from joe.utils.allfunctions import *

website = "www.hairsite.com"


class Hirlossexperiences(CrawlSpider):
    name = "f5"
    start_urls = [
        "http://www.hairsite.com/hair-loss/forum-category-2.html",
    ]
    cpt = 0;
    rules = [
        Rule(lxml(allow=('hair-loss/forum_entry-id-\d+.*html',)), callback='parse_cat',
             follow=True),
    ]

    def parse_cat(self, response):
        return self.create_comment(response)

    def create_comment(self, response):
        self.cpt +=1
        print self.cpt
        link = response.url
        text_date = response.xpath("//p[@class='author']//text()[3]").extract()[0]
        date_time = convert_date(text_date)
        if text_date:
            thread_name = response.xpath("//h2[@class='postingheadline']/text()").extract()[0]
            content = html_to_text(response.xpath("//p[@class='postingboard']//text()").extract())
            comment = Comment(link=link, content=content, date_time=date_time, website=website,
                              thread_name=thread_name)
            es_id = "%s_%s" % (link, comment.date_time)
            es_client.index(index=index_name, doc_type=comments, id=es_id, body=comment.to_dict())






