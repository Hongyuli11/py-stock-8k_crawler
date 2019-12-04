#For step 2. 
import io
import re
import scrapy

from datetime import date
from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

today = date.today().strftime('%Y%m%d')

#date range setting
start_date = '20190301'
end_date = today #end_date can be a usr define str as start_date, like '20190322'

input_filename = 'company_list.csv' # we take company list from pre-process as input

class k8_item(scrapy.Item):
    ticker_symbol = scrapy.Field()
    file_type = scrapy.Field()
    file_link = scrapy.Field()
    file_date = scrapy.Field()
    item_num = scrapy.Field()

class EdgarSpider(Spider):
    name = 'parse_8k'
    allowed_domains = ['sec.gov']
    custom_settings = {
    # specifies exported fields and order
    'FEED_EXPORT_FIELDS': ["ticker_symbol","file_type", "file_date", "item_num", "file_link"]
    }
    '''
    rules = (
        Rule(LinkExtractor(allow=('/Archives/edgar/data/[^\"]+\-index\.htm',)), callback='parse_index', cb_kwargs = dict(theurl='6666666')),
    )
    '''
    def __init__(self, **kwargs):
        super(EdgarSpider, self).__init__(**kwargs)
        self.start_date = start_date
        self.end_date = end_date

    def start_requests(self):
        url_template_8k = 'http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=%s&type=8-k&dateb=%s&datea=%s&owner=exclude&count=300'
        with open(input_filename,'r') as f_readin:
            for line in f_readin:
                tokens = line.split('"')
                symbol = tokens[1].strip('"')
                url8 = (url_template_8k % (symbol, self.end_date, self.start_date))
                yield scrapy.Request(url = url8, callback = self.link_extract, meta={'ticker_symbol':symbol, 'file_type':'8-k'})
        f_readin.close()

    def link_extract(self,response):
        ticker_symbol = response.meta['ticker_symbol']
        filetype = response.meta['file_type']
        link_extractor = LinkExtractor(allow=('/Archives/edgar/data/[^\"]+\-index\.htm')).extract_links(response)
        for linker in link_extractor:
            yield scrapy.Request(linker.url, callback = self.parse_index, meta={'ticker_symbol':ticker_symbol,'file_type':filetype})

    def parse_index(self, response):
        message1 = response.xpath('//*[@id="formDiv"]/div/table/tr[2]/td[3]/a/@href').get()
        file_url = 'http://www.sec.gov' + message1
        date = response.xpath('//*[@id="formDiv"]/div[2]/div[1]/div[2]/text()').get()
        symbol = response.meta['ticker_symbol']
        filetype = response.meta['file_type']

        return scrapy.Request(file_url, callback = self.parse_8kfile, meta={'ticker_symbol':symbol,
                                                                           'file_type':filetype, 
                                                                           'file_date': date})

    def parse_8kfile(self,response):
        symbol = response.meta['ticker_symbol']
        filetype = response.meta['file_type']
        date = response.meta['file_date']

        ItemXXXs = response.xpath('/html/body/document/type/sequence/filename/*').re(r'(I[Tt][Ee][Mm])')
        number = len(ItemXXXs)

        realItem = k8_item()
        realItem['ticker_symbol'] = symbol
        realItem['file_type'] = filetype
        realItem['file_link'] = response.url
        realItem['file_date'] = date
        realItem['item_num'] = number
        yield realItem




