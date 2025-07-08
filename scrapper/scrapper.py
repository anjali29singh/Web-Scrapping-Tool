from pathlib import Path
import scrapy
import bs4
import scrapy
import scrapy
import scrapy.exporters
from scrapy.linkextractors import LinkExtractor
from scrapper.utils import extract_company_info 

linkextractor = LinkExtractor()

class CompanySpider(scrapy.Spider):
    name = "company_spider"
    start_urls = []

    async def start(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
        
    
    def parse(self,response):
        # Extract data from the response
        bs4_response = bs4.BeautifulSoup(response.text, 'html.parser')

        scrapped_data = extract_company_info(bs4_response)

        yield scrapped_data
        list_links = linkextractor.extract_links(response)
        
        # create new requests for each link to be crawled next
        for link in list_links:
            yield scrapy.Request(url=link.url, callback=self.parse)


class JSONWriterPipeline:
    def open_spider(self, spider):
        self.file = open('output.jsonl', 'wb')
        self.exporter = scrapy.exporters.JsonLinesItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
