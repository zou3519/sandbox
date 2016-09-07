import scrapy
import re
import urllib
import logging

base_url = "http://www.eecs.harvard.edu/~margo/cs261/"
retrieve_path = "C:\\Users\\Richard\\Dropbox\\College\\2016-Fall\\cs261\\"

class DlSpider(scrapy.Spider):
    name = "dl"
    allowed_domains = ["www.eecs.harvard.edu"]
    start_urls = ["http://www.eecs.harvard.edu/~margo/cs261/syllabus.html"]

    def parse(self, response):
        for row in response.xpath('//tr'):

            # try to find the date first
            texts = row.select('td/text()').extract()
            datere = re.compile('[0-9]+\/[0-9]+')
            date = ""
            if (len(texts) < 2):
                continue
            elif datere.match(texts[0]):
                date = texts[0]
            elif datere.match(texts[1]):
                date = texts[1]
            else:
                continue

            split = date.split("/")
            date = split[0].zfill(2) + split[1].zfill(2)

            # now, find links
            for link in row.select('td/a/@href').extract():
                url = base_url + link
                paper = link.split("/")
                if len(paper) < 2:
                    continue
                paper = paper[1]
                pdf = re.compile('.+\.pdf')
                if not pdf.match(paper):
                    logging.debug("skipping " + paper)
                    continue
                filename = date + " " + paper
                logging.debug("Retrieving " + url + " as " + filename)
                urllib.urlretrieve(url, retrieve_path + filename)





