from joe.utils.allfunctions import *
import json

website = "www.realself.com"
review_api = "http://www.realself.com/comment/api/thread?content_id=%s&content_type=ReviewEntry&limit=10&offset=0&sort=new"


class Hirlossexperiences(CrawlSpider):
    name = "f8"
    start_urls = [
        "http://www.realself.com/Hair-transplant-surgery/reviews",
    ]
    cpt = 0;
    rules = [
        Rule(lxml(allow=('.*'), restrict_xpaths="//h3[@class='content-title']/a"), callback='parse_product1',follow=True)
    ]

    def parse_cat(self, response):
        return self.create_comment(response)

    def parse_product1(self, response):
        content = html_to_text(response.xpath("//div[@id='review-view']").extract())
        date_text = response.xpath("//div[@id='review-entries']/div[1]/ul/li[1]/text()").extract()[0]
        date_time = convert_date(date_text)
        comment = Comment(link=response.url, content=content, date_time=date_time, website=website)
        comment.start_index()
        # process with review
        review_ids = response.xpath("//rs-commenting[@content-id]/@content-id").extract()
        for id in review_ids:
            yield Request(review_api % (id), callback=self.parse_product2)


    def parse_product2(self, response):
        link_parent = response.request.headers['Referer']
        comments = json.loads(response.body)
        for comment in comments:
            date_time = convert_date(comment['created'])
            comment = Comment(link=response.url, content=comment['comment'], date_time=date_time, website=website,link_parent=link_parent)
            comment.start_index()

    def closed(self, reason):
        collector = self.crawler.stats._stats
        collector['website'] = website
        collector['duration'] = str(collector['finish_time'] - collector['start_time'])
        es_client.index(index=index_name, doc_type="reports", body=collector)