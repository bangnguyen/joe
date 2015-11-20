from joe.utils.allfunctions import *
website = "www.hairlossexperiences.com/"
import re


class Hirlossexperiences(CrawlSpider):
    name = "f2"
    url="http://www.hairlossexperiences.com/"
    start_urls = [
        "http://www.hairlossexperiences.com",
        # "http://www.hairlossexperiences.com/view_topic.php?forum_id=3&id=5051&page=10"
    ]
    # rules = [
    # Rule(lxml(allow=('view_forum.php\?id=\d+',),restrict_xpaths=""), callback='parse_cat',
    #         follow=True),
    #    Rule(lxml(allow=('/view_topic.php\?id=\d+',), ), callback='parse_product')
    #]
    def parse(self, response):
        trs = response.xpath("//center//table//tr")
        links = []
        for tr in trs:
            try:
                date_raw = html_to_text(tr.xpath("./td[5]/text()").extract())
                date_text = re.search("(.*)by", date_raw).group(1)
                time_stamp = int(
                    time.mktime(datetime.datetime.strptime(convert_date(date_text), "%Y-%m-%d %H:%M:%S").timetuple()))
                two_days_ago = int(time.time()) - 5 * 24 * 3600
                if time_stamp > two_days_ago:
                    link = tr.xpath("./td[2]/a/@href").extract()[0]
                    links.append(link)
            except:
                pass
        for link in links:
            yield Request(urljoin(self.url,link), callback=self.parse1)

    def parse1(self, response):
        trs = response.xpath("//center//table//tr")
        links = []
        for tr in trs:
            try:
                date_raw = html_to_text(tr.xpath("./td[7]/text()").extract())
                date_text = re.search("(.*)by", date_raw).group(1)
                time_stamp = int(
                    time.mktime(datetime.datetime.strptime(convert_date(date_text), "%Y-%m-%d %H:%M:%S").timetuple()))
                two_days_ago = int(time.time()) - 5 * 24 * 3600
                if time_stamp > two_days_ago:
                    link = tr.xpath("./td[2]/a/@href").extract()[0]
                    links.append(link)
            except:
                pass
        for link in links:
            yield Request(urljoin(self.url,link), callback=self.parse_product)


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
                    comment.start_index()


    def closed(self, reason):
        collector = self.crawler.stats._stats
        collector['website'] = website
        collector['duration'] = str(collector['finish_time'] - collector['start_time'])
        es_client.index(index=index_name, doc_type="reports", body=collector)
