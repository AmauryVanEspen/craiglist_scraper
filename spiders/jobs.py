# -*- coding: utf-8 -*-
import scrapy
# Request is required to crawl multiple pages through a callback function included in the parse method.
from scrapy import Request


"""
Creation of a "Spider" containing a parse method.
loop on variable "job" containing the XPath response then return yield
the loop contains variable with relative "job" XPath.
yield contains the list of lists of objects.

        In order to store result into CSV file, run :
        $ scrapy crawl jobs -o result-jobs-one-page.csv
        # according to the extension used, you can export the output result as .csv .xml or .json
        'downloader/response_status_count/200' tells you how many requests succeeded
        'finish_reason and time tell the result and timestamp of the run.
        'item_scraped_count' refers to the number of titles scraped from the page. 
        'log_count/DEBUG'  and 'log_count/INFO' are okay; 
        however, if you received 
        'log_count/ERROR' you should find out which errors you get during scraping are fix your code.
        
In order to define the order of the output dictionary
add the following elements at the end of the ../settings.py file
FEED_EXPORT_FIELDS = ['Title','URL', 'Address', 'Compensation', 'Employment Type','Description']

moreover, uncomment the USER_AGENT and impersonate web browser
# get lists of recent user_agent details from 
# - http://www.useragentstring.com/pages/useragentstring.php?name=Chrome
# - http://www.useragentstring.com/pages/useragentstring.php?name=Firefox
# check with http://www.whoishostingthis.com/tools/user-agent/
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'

Update the Robots.txt obeying rule
ROBOTSTXT_OBEY = False

Add a RANDOMIZE_DOWNLOAD_DELAY = True and activate DOWNLOAD_DELAY
"""

class JobsSpider(scrapy.Spider):
    # name of the spider.
    name = 'jobs'
    # allowed_domains contains the list of the domains that the spider is allowed scrape.
    allowed_domains = ['craigslist.org']
    # start_urls contains the list of one or more URL(s) with which the spider starts crawling.
    """
    Warning: Scrapy adds extra http:// at the beginning of the URL in start_urls and it also adds a trailing slash.
    As we here already added https:// while creating the spider, we must delete the extra http://.
    => $ scrapy genspider jobs https://newyork.craigslist.org/search/egr
    So double-check that the URL(s) in start_urls are correct or the spider will not work.
    """
    # start_urls = ['http://https://newyork.craigslist.org/search/egr/']
    start_urls = ['https://newyork.craigslist.org/search/egr/']

    # the main function of the spider. Do NOT change its name; however, you may add extra functions if needed.
    def parse(self, response):
        # pass
        """
        jobs is a [list] of text portions extracted based on a rule.

        response  is simply the whole html source code retrieved from the page.
        :param response:

        :return:
        - print(response) should return HTTP status code. 200 for OK.
        see https://en.wikipedia.org/wiki/List_of_HTTP_status_codes.
        - print(response.body) should return the whole source code of the page.
        - response.xpath(). xpath  is how we will extract portions of text and it has rules.
        """

        jobs = response.xpath('//p[@class="result-info"]')
        """
        Inside response.xpath
        - //  means instead of starting from the <html>, just start from the tag that I will specify after it.
        - /p  simply refers to the <p> tag.
          
        -[@class="result-info"]  that is directly comes after /p means the <p> tag must have this class name in it.
        
        related methods
        - extract()  means extract every instance on the web page that follows the same XPath rule into a [list].
        - extract_first()  if you use it instead of extract() it will extract only the first item in the list.
        """

        for job in jobs:
            relative_url = job.xpath('a/@href').extract_first()
            """
            To extract the job URL, you refer to the <a> tag and the value of the href attribute, which is the URL. 
            Yes, @ means an attribute.
            However, if this is a relative URL, which looks like: /path/to/page.html 
            so, to get the absolute URL to be able to use it later, you can either use Python concatenation as follows:
            """
            # absolute_url = response.urljoin(relative_url)
            """
            Concatenation is another case in which you need to add quotes to extract_first("") 
            because concatenation works only on strings and cannot work on None values.
            """
            # you can simply use the urljoin() method, which builds a full absolute URL. Update the yield 'URL': variable if you update it.
            # absolute_url = response.urljoin(relative_url)

            # in the precise case of this page, the url is already stored as an absolute_url
            absolute_url = relative_url

            # - /a  simply refers to the <a> tag.
            # - text() refers to the text of the < p > tag, which is ””.
            title = job.xpath('a/text()').extract_first()
            """
            Also, as you can see, we started the XPath expression of “jobs” by // meaning it starts from <html> 
            until this <p> whose class name is  “result-info”.
            However, we started the XPath expression of “title” without any slashes, 
            because it complements or depends on the XPath expression of the job wrapper. 
            If you rather want to use slashes, you will have to precede it with a dot to refer to the current node as follows:
            """

            # title = job.xpath('.//a/text()').extract_first()

            address = job.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first("")[2:-1]
            """
            To extract the job address, you refer to the <span> tag whose class name is “result-meta” 
            and then the <span> tag whose class name is “result-hood” and then the text() in it. 
            The address is between brackets like (Brooklyn); so if you want to delete them, you can use string slicing [2:-1]. 
            However, this string slicing will not work if there is no address (which is the case for some jobs) 
            because the value will be None which is not a string! So you have to add empty quotes inside extract_first("") 
            which means if there is no result, the result is “”.
            """

            # yield {'URL': absolute_url, 'Title': title, 'Address': address}
            """
            In order to get the Job description content from url,
            you need to pass those values of titles and addresses from the parse() function to the parse_page() function as well, 
            using meta in a dictionary as follows:
            """
            yield Request(absolute_url, callback=self.parse_page,
                              meta={'URL': absolute_url, 'Title': title, 'Address': address})

        relative_next_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        absolute_next_url = response.urljoin(relative_next_url)

        # yield Request(absolute_next_url, callback=self.parse)
        """
        yield the Request() method with the absolute_next_url and this requires a callback function,
        which means a function to apply on this URL; 
        in this case, it is the same parse() function which extracts the titles, addresses and URLs of jobs from each page.
         
        Note that in the case the parse() function is the callback, 
        you can delete this callback=self.parse because the parse() function is a callback by default, 
        even if you do not explicitly state that.
         
        This required to import Request from scrapy package.
        """
        # yield Request(absolute_next_url)
        """
        According to the requirement of passing the data within the next yielding with a callback,
        you have to pass the URL of the job from the parse() function to the parse_page() function in a callback using the Request() method as follows
        """
        yield Request(absolute_next_url, callback=self.parse)

    #Get the content of the job description
    def parse_page(self, response):
        url = response.meta.get('URL')
        title = response.meta.get('Title')
        address = response.meta.get('Address')

        description = "".join(line for line in response.xpath('//*[@id="postingbody"]/text()').extract())

        compensation = response.xpath('//p[@class="attrgroup"]/span[1]/b/text()').extract_first()
        employment_type = response.xpath('//p[@class="attrgroup"]/span[2]/b/text()').extract_first()

        yield {'URL': url, 'Title': title, 'Address': address, 'Description': description,
               'Compensation': compensation,
               'Employment Type': employment_type}