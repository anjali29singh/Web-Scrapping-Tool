from urllib.parse import parse_qs, urlencode, urljoin, urlparse, urlunparse
from googlesearch import search
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_query(query):
    try:
        # process query , google search query and get urls of results 
        results  = search(query, num_results=1,unique=True,advanced=True,sleep_interval=0.25)
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
    
    return None

def get_project_info(response):
    
    projects = []
    
    project_selectors = [
        '.project', '.product', '.service', '.portfolio-item',
        '.work-item', '.case-study', '[class*="project"]',
        '[class*="product"]', '[class*="service"]'
    ]
    
    for selector in project_selectors:
        project_elements = response.select(selector)
        
        for element in project_elements:
            project_info = {}
            
            # Extract title
            title_element = element.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            if title_element:
                project_info['title'] = title_element.get_text().strip()
            
            # Extract description
            desc_element = element.find(['p', '.description', '.summary'])
            if desc_element:
                project_info['description'] = desc_element.get_text().strip()
            
            # Extract link
            link_element = element.find('a', href=True)
            if link_element:
                project_info['link'] = link_element.get('href')
            
            # Extract image
            img_element = element.find('img')
            if img_element:
                project_info['image'] = img_element.get('src')
            
            if project_info:
                projects.append(project_info)
    
    return projects

def get_social_links(response):
    social_domains = ['facebook.com', 'x.com', 'linkedin.com', 'instagram.com', 'youtube.com']
    social_links = {}
    for a in response.find_all('a', href=True):
        href = a['href']
        for domain in social_domains:
            if domain in href:
                social_links[domain.split('.')[0]] = href
    return social_links or None


def get_contact_info(response):

    contact_info = {}
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = set()
    
    # Find emails in text content
    page_text = response.get_text()
    found_emails = re.findall(email_pattern, page_text)
    emails.update(found_emails)
    
    # Find emails in mailto links
    mailto_links = response.find_all('a', href=re.compile(r'^mailto:'))
    for link in mailto_links:
        href = link.get('href', '')
        email = href.replace('mailto:', '').split('?')[0]
        if email:
            emails.add(email)
    
    if emails:
        contact_info['emails'] = list(emails)
    
    # Extract phone numbers
    phone_patterns = [
        r'\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}',
        r'\+?[0-9]{1,3}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,9}'
    ]
    
    phones = set()
    for pattern in phone_patterns:
        found_phones = re.findall(pattern, page_text)
        phones.update(found_phones)
    
    # Find phones in tel links
    tel_links = response.find_all('a', href=re.compile(r'^tel:'))
    for link in tel_links:
        href = link.get('href', '')
        phone = href.replace('tel:', '').strip()
        if phone:
            phones.add(phone)
    
    if phones:
        contact_info['phones'] = list(phones)
    
    # Extract address
    address_selectors = [
        '.address', '.contact-address', '.location',
        '[class*="address"]', '[class*="location"]'
    ]
    
    for selector in address_selectors:
        address_elements = response.select(selector)
        for element in address_elements:
            address_text = element.get_text().strip()
            if address_text and len(address_text) > 10:
                contact_info['address'] = address_text
                break
    
    return contact_info


def get_website_links(response):
    
    links = {
        'internal': set(),
        'external': set()
    }
    
    base_url = response.find('base')
    if base_url:
        base_href = base_url.get('href', '')
    else:
        base_href = ''
    
    all_links = response.find_all('a', href=True)
    
    for link in all_links:
        href = link.get('href', '').strip()
        
        if not href or href.startswith(('mailto:', 'tel:', 'javascript:', '#')):
            continue
        
        # Clean URL
        clean_href = href.split('#')[0]  # Remove fragments
        
        if href.startswith(('http://', 'https://')):
            if base_href and base_href in href:
                links['internal'].add(clean_href)
            else:
                links['external'].add(clean_href)
        elif href.startswith('/'):
            links['internal'].add(clean_href)
    
    return {k: list(v) for k, v in links.items() if v}

def get_company_description(response):
    
    meta_desc = response.find('meta', attrs={'name': 'description'})
    if meta_desc:
        content = meta_desc.get('content', '').strip()
        if content:
            return content
    
    og_desc = response.find('meta', property='og:description')
    if og_desc:
        content = og_desc.get('content', '').strip()
        if content:
            return content
    
    about_selectors = [
        '.about', '.about-us', '.company-description',
        '.description', '.intro', '.overview',
        '[class*="about"]', '[class*="description"]'
    ]
    
    for selector in about_selectors:
        about_elements = response.select(selector)
        for element in about_elements:
            text = element.get_text().strip()
            if text and len(text) > 50:
                return text
    
    h1 = response.find('h1')
    if h1:
        next_p = h1.find_next('p')
        if next_p:
            text = next_p.get_text().strip()
            if text and len(text) > 50:
                return text
    
    paragraphs = response.find_all('p')
    for p in paragraphs:
        text = p.get_text().strip()
        if text and len(text) > 50 and not text.startswith(('Copyright', '©')):
            return text
    
    return None


def extract_company_info(response,meta_data):

    company_info = {
        'company_name': meta_data.get('company_name') or get_company_name(response),
        'company_description': meta_data.get('company_description') or get_company_description(response),
        'projects':meta_data.get('projects') or  get_project_info(response),
        'social_links': meta_data.get('social_links') or get_social_links(response),
        'contact_info': meta_data.get('contact_info') or get_contact_info(response),
        'website_links': meta_data.get('website_links') or get_website_links(response),
    }
    
    return company_info
  
    
