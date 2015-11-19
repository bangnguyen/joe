from joe.utils.allfunctions import *

website = "www.baldgossip.com"


class baldgossip(CrawlSpider):
    name = "f6"
    start_urls = [
        "http://www.baldgossip.com/forum/viewforum.php?f=4&sid=a529e9b13e0207c998069bed47232b79",
    ]
    cpt = 0;
    rules = [
        Rule(lxml(allow=('viewtopic.php\?f=\d+',)), callback='parse_cat',
             follow=True),
    ]

    def parse_cat(self, response):
        return self.create_comment(response)


    def create_comment(self, response):
        tables = response.xpath("//div[@id='page-body-inner']//div[contains(@class,'post')]")
        link = response.url
        thread_name = html_to_text(response.xpath("//div[@id='page-body']/h1/text()").extract())
        for table in tables:
            self.cpt += 1
            text_date =html_to_text( table.xpath(".//p[@class='author']/text()[2]").extract())
            date_time = convert_date(text_date)
            if date_time:
                content = html_to_text(table.xpath(".//div[@class='content']//text()").extract())
                comment = Comment(link=link, content=content, date_time=date_time, website=website,thread_name=thread_name)
                comment.start_index()




    def closed(self, reason):
        collector = self.crawler.stats._stats
        collector['website'] = website
        collector['duration'] =  str(collector['finish_time'] - collector['start_time'])
        es_client.index(index=index_name, doc_type="reports", body=collector)

