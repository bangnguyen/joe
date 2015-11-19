from joe.utils.allfunctions import *

website = "www.hairlosstalk.com"


class hairlosstalk(CrawlSpider):
    name = "f7"
    start_urls = [
        "http://www.hairlosstalk.com/interact/forum.php",
    ]
    cpt = 0;
    rules = [
        Rule(lxml(allow=('.*'), restrict_xpaths="//h2[@class='forumtitle']/a"), callback='parse_cat',
             follow=True),
        Rule(lxml(allow=('.*'), restrict_xpaths="//h3[@class='threadtitle']//a[contains(@class,'title')]"),
             callback='parse_product'),
        #Rule(lxml(allow=('.*'), restrict_xpaths="//*[@class='pagination']//a"), callback='parse_product',),
    ]

    def parse_cat(self, response):
        self.cpt +=1
        print "cpt  %s" % (self.cpt)

    def parse_product(self, response):
        self.cpt +=1
        print "cpt  %s" % (self.cpt)
        return self.create_comment(response)

    def create_comment(self, response):
        tables = response.xpath("//ol[@id='posts']/li")
        for table in tables:
            date_text = html_to_text(table.xpath(".//span[@class='date']//text()").extract())
            date_time = convert_date(date_text)
            content = html_to_text(table.xpath(".//div[@class='content']//text()").extract())
            comment = Comment(link=response.url, content=content, date_time=date_time, website=website)
            comment.start_index()






    def closed(self, reason):
        collector = self.crawler.stats._stats
        collector['website'] = website
        collector['duration'] =  str(collector['finish_time'] - collector['start_time'])
        es_client.index(index=index_name, doc_type="reports", body=collector)

