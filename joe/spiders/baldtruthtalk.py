from joe.utils.allfunctions import *
website = "www.baldtruthtalk.com"
class Baldtruthtalk(CrawlSpider):
    name = "f1"
    start_urls = [
        "http://www.baldtruthtalk.com/"
    ]
    rules = [
        Rule(lxml(allow=('/forums/',), restrict_xpaths="//div[@class='forumdata']//a"), callback='parse_cat',
             follow=True),
        Rule(lxml(allow=('/threads/',), ), callback='parse_product')
    ]

    def parse_cat(self, response):
        print response.url


    def parse_product(self, response):
        return self.create_comment(response)

    def create_comment(self, response):
        post_list = response.xpath("//div[@id='postlist']/ol/li")
        thread_name = html_to_text(response.xpath("//div[@id='pagetitle']//a/text()").extract())
        for post in post_list:
            try:

                raw_date = post.xpath("./div[@class='posthead']//span[@class='date']")
                date_text = html_to_text(raw_date.extract())
                link = response.url
                content = html_to_text(post.xpath(".//div[@class='postdetails']//div[@class='content']").extract())
                comment = Comment(link=link, content=content, date_time=convert_date(date_text), website=website,
                                  thread_name=thread_name)
                comment.start_index()
            except:
                traceback.print_exc()
                pass
    def closed(self, reason):
        collector = self.crawler.stats._stats
        collector['website'] = website
        collector['duration'] =  str(collector['finish_time'] - collector['start_time'])
        es_client.index(index=index_name, doc_type="reports", body=collector)