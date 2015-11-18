from joe.utils.allfunctions import *
website = "www.hairrestorationnetwork.com/eve/"
class Hirlossexperiences(CrawlSpider):
    name = "f3"
    start_urls = [
        "http://www.hairrestorationnetwork.com/eve/",
    ]
    cpt = 0;
    rules = [
        Rule(lxml(allow=('hairrestorationnetwork\.com/eve/[a-zAA-z-]+/$',)), callback='parse_cat',
             follow=True),
           Rule(lxml(allow=('hairrestorationnetwork\.com/eve/[a-zAA-z-]+/index\d+\.html$',)), callback='parse_cat',
             follow=True),
        Rule(lxml(allow=('hairrestorationnetwork\.com/eve/\d+[a-zAA-z-]+\.html$',), ), callback='parse_product')
    ]

    def parse_cat(self, response):
        return
        print "parse_cat " + response.url


    def parse_product(self, response):
        print "parse_product " + response.url
        return self.create_comment(response)



    def create_comment(self, response):
        tables = response.xpath("//div[@id='posts']//div[@align='center']//div/div/div/table")
        link = response.url
        for table in tables:
            text_date = html_to_text( table.xpath(".//tr[1]/td/div[2]//text()").extract())
            date_time = convert_date(text_date)
            if date_time:
                try:
                    content= html_to_text( table.xpath(".//tr[4]//text()").extract())
                    comment = Comment(link=link, content=content, date_time=date_time, website=website)
                    es_id = "%s_%s" % (link, comment.date_time)
                    es_client.index(index=index_name, doc_type=comments, id=es_id, body=comment.to_dict())
                    print comment.to_dict()
                except:
                    traceback.print_exc()
                    pass







