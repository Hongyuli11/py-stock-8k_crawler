#For step 1. 
import io
import re

from scrapy import Spider

def generate_urls(exchanges):
    for exchange in exchanges:
        yield 'http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=%s&render=download' % exchange


class NasdaqSpider(Spider):

    name = 'get_company_list'
    allowed_domains = ['www.nasdaq.com']

    def __init__(self, **kwargs):
        super(NasdaqSpider, self).__init__(**kwargs)
        exchanges = ['NASDAQ','NYSE','AMEX']
        self.start_urls = generate_urls(exchanges)

    def parse(self, response):
        filename = 'company_list.csv'
        message_output_filename = 'message.txt'
        try:
            with open(filename, 'a+') as f:
                item_counter = 0
                target_counter=0
                file_like1 = io.BytesIO(response.body)#response.body will always be byte.
                file_like2 = io.TextIOWrapper(file_like1, encoding='utf-8')

                # Ignore first row
                next(file_like2)

                for line in file_like2:
                    item_counter = item_counter + 1
                    tokens = line.split('"')
                    symbol = tokens[0].strip('"')
                    last_sale_str = tokens[5].strip('"')
                    if('n/a' in last_sale_str):
                        last_sale = 0.0
                    else:
                        last_sale = float(last_sale_str)
                    
                    if last_sale>1.0:
                        #name = tokens[1].strip('"')
                        f.write('"'+tokens[1]+'"' +','+ '"'+tokens[3]+'"'  +','+ '"'+tokens[5]+'"'  +','+ '"'+tokens[17]+'"' +'\n')
                        target_counter = target_counter +1
                    self.log('Saved file %s' % filename)
            f.close()
        finally:
            file_like2.close()