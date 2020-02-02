# -*- coding: utf-8 -*-
import scrapy



class JobsSpider(scrapy.Spider):
    # name of the spider.
    name = 'jobs-titles'
    # allowed_domains contains the list of the domains that the spider is allowed scrape.
    allowed_domains = ['newyork.craigslist.org/search/egr']
    # start_urls contains the list of one or more URL(s) with which the spider starts crawling.
    """
    Warning: Scrapy adds extra http:// at the beginning of the URL in start_urls and it also adds a trailing slash.
    As we here already added https:// while creating the spider, we must delete the extra http://.
    => $ scrapy genspider jobs-titles https://newyork.craigslist.org/search/egr
    So double-check that the URL(s) in start_urls are correct or the spider will not work.
    """
    # start_urls = ['http://https://newyork.craigslist.org/search/egr/']
    start_urls = ['https://newyork.craigslist.org/search/egr/']

    # the main function of the spider. Do NOT change its name; however, you may add extra functions if needed.
    def parse(self, response):
        # pass
        """
        titles  is a [list] of text portions extracted based on a rule.

        response  is simply the whole html source code retrieved from the page.
        :param response:

        :return:
        - print(response) should return HTTP status code. 200 for OK.
        see https://en.wikipedia.org/wiki/List_of_HTTP_status_codes.
        - print(response.body) should return the whole source code of the page.
        - response.xpath(). xpath  is how we will extract portions of text and it has rules.
        """

        titles = response.xpath('//a[@class="result-title hdrlnk"]/text()').extract()
        """
        Inside response.xpath
        - //  means instead of starting from the <html>, just start from the tag that I will specify after it.
        - /a  simply refers to the <a> tag.
          
        -[@class="result-title hdrlnk"]  that is directly comes after /a means the <a> tag must have this class name in it.
        - text()  refers to the text of the  <a> tag, which is”Chief Engineer”.
        
        related methods
        - extract()  means extract every instance on the web page that follows the same XPath rule into a [list].
        - extract_first()  if you use it instead of extract() it will extract only the first item in the list.
        """

        for title in titles:
            yield {'Title': title}

        """
        In order to store result into CSV file, run :
        $ scrapy crawl -titles -o result-titles.csv
        'downloader/response_status_count/200' tells you how many requests succeeded
        'finish_reason and time tell the result and timestamp of the run.
        'item_scraped_count' refers to the number of titles scraped from the page. 
        'log_count/DEBUG'  and 'log_count/INFO' are okay; 
        however, if you received 
        'log_count/ERROR' you should find out which errors you get during scraping are fix your code.
        """