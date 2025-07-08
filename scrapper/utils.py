from googlesearch import search
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_query(query):
    try:
        # process query , google search query and get urls of results 
        results  = search(query, num_results=2,unique=True,advanced=True,sleep_interval=0.25)
        if not results:
            logging.warning(f"No results found for query: {query}")
            return []
        
        url_list = [result.url for result in results]
        return url_list
    
    except Exception as e:
        logging.error(f"Error processing query '{query}': {e}")
        return []

def get_company_name(response):
    # og:site_name
    og_site_name = response.find('meta', property='og:site_name')

    if og_site_name:
        return og_site_name.get('content', '').strip()
    
    title = response.find('title')

    if title:

        title_text = title.get_text().strip()
        # Remove common suffixes
        clean_title = re.sub(r'\s*[-|–]\s*(Home|Welcome|Official Site).*$', '', title_text)
        return clean_title
    
    logo_selectors = ['header img[alt]', '.logo img[alt]', '.brand img[alt]']

    for selector in logo_selectors:
        img = response.select_one(selector)
        if img and img.get('alt'):
            return img.get('alt')


    copyright_text = response.find(string=re.compile(r'©.*\d{4}'))
    if copyright_text:
        match = re.search(r'©\s*\d{4}\s*([^.]+)', copyright_text)
        if match:
            return match.group(1).strip()
    
    return "No company name found"

def get_social_links(response):
    pass

def get_project_info(response):
    pass

def get_contact_info(response):
    pass
def get_website_links(response):
    pass

def get_company_description(response):
    pass

def extract_company_info(response):
    # print("response is",response)
    company_name = get_company_name(response)   

    return {
        "company_name":company_name
    } 
    pass