# py-stock-8k_crawler
"py-stock-8k_crawler" is utility for crawling historical data of US stocks,
including:
* Ticker symbols listed in NYSE, NASDAQ and AMEX from "NASDAQ.com"
* Get last closing price and save those higher than 1 dollar. 
* For companies from last step, crawl and output 8-k filing lists in given date range (default: 20190301-current) from "SEC EDGAR".  
* Able to parse 8-k file. Here as an example, py8k_crawler counts the occurrence frequency of word "item" in each 8-k file.
 

Prerequisites:
* Python 3.X
* Need to have Scrapy installed on computer for "py8k-crawler" is based on Scrapy 1.6.0 (latest until 2019-04-15). 


Usage: 
1. Unzip py8k_crawler. Or create a new Scrapy project and place "Aspider.py" and "Bspider.py" into spider folder. 
2. (For mac and Linux) Run spider "get_company_list":

               scrapy crawl get_company_list. 

   * The code is included in file "Aspider.py". 
   * Will generate a output file named "company_list.csv". 
   * The running time is few seconds. 
3. (For mac and Linux) Run spider "parse_8k": 

               scrapy crawl parse_8k --loglevel=INFO -o 8k_list.csv

   * The code is included in "Bsipder.py"
   * Date range can be user defined by simply changing "Bspider.py" line 14 to 15. The default date range is 20190301-current. 
   * The estimated running time for default is 7 minutes. (16 min if date range is 20190101-20190415)
   * The result will be listed in "output.csv". 
   * Notice that some companies do not release 8-k file. Some companies do not submit files on "SEC EDGAR".
     Those companies are automatically ignored in this step. 
4. For a second time running, be sure to remove previous outputs: "company_list.csv" and "8k_list.csv". Or the new output will be appended behind previous'. 
