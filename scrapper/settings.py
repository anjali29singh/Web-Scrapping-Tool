# scrapy settings
from scrapy.settings import Settings

# Define the settings for the Scrapy project
crawler_settings = Settings({
    'DEPTH_LIMIT': 2,  # Set the depth limit for crawling
    'ROBOTSTXT_OBEY': True,  # Obey robots.txt rules
    'ITEM_PIPELINES': {

        'scrapper.scrapper.JSONWriterPipeline': 100, 
    },
    'FEEDS': {
        'output.jsonl': {
            'format': 'jsonl',
            'overwrite': True,  # Overwrite the file if it exists
        },
    },
   
        

})