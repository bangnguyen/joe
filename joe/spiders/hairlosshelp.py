from joe.utils.allfunctions import *
website = "www.hairlosshelp.com/forums/"
import pdb
class Hairlosshelp(CrawlSpider):
    name = "f4"
    start_urls = [
        "http://www.hairlosshelp.com/forums/"
    ]
    cpt = 0;
    rules = [
        Rule(lxml(allow=('forums/categories.cfm\?catid=\d+',)), callback='parse_cat',
             follow=True),
        Rule(lxml(allow=('forums.*threadid=\d+',), ), callback='parse_product')
    ]

    def parse_cat(self, response):
        print "parse_cat " + response.url


    def parse_product(self, response):
        print "parse_product " + response.url
        return self.create_comment(response)



    def create_comment(self, response):
        trs = response.xpath("//*[@id='Forums']/div[2]/table//tr")
        if (len(trs)>=3):
            for i in range((len(trs)/4)+1):
                try:
                    index = i*4
                    item1= trs[index]
                    item2=trs[index+1]
                    date_text =html_to_text(item1.xpath("./td/div[1]/text()").extract())
                    date_time= convert_date(date_text)
                    if date_time:
                        content=html_to_text(item2.xpath("./td[2]//text()").extract())
                        comment = Comment(link=response.url, content=content, date_time=date_time, website=website)
                        comment.start_index()

                except:
                    traceback.print_exc()
                    pass




    def closed(self, reason):
        collector = self.crawler.stats._stats
        collector['website'] = website
        collector['duration'] =  str(collector['finish_time'] - collector['start_time'])
        es_client.index(index=index_name, doc_type="reports", body=collector)