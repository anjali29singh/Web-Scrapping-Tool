from googlesearch import search
import logging

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
