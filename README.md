# 🌐 Web Scraping Tool

A powerful web scraping tool to extract company information from either a search query or a URL.

---

## 📦 Features

- Accepts either search queries or direct URLs
- Extracts company metadata including descriptions, contact info, social links, and external links
- Cleans and deduplicates scraped data
- Outputs raw and cleaned data in `.jsonl` format

---

## 🚀 Setup Instructions

### 1. Clone the Repository

git clone https://github.com/your-username/web-scraping-tool.git
cd web-scraping-tool 

### 2. Create a Virtual Environment

python3 -m venv venv
source venv/bin/activate

### 3. Install Dependencies
pip install -r requirements.txt

### 4. ⚙️ Usage Run the Scraper
Run the scraper with a search query or a URLs:
python main.py "AI companies in Berlin"

The tool will automatically detect whether the input is a search query or a list of URLs.

Output Files
output.jsonl: Raw scraped data

output_clean.jsonl: Deduplicated and cleaned version of the data

### 5.🛠 Tech Stack
Python
Scrapy – web scraping framework
googlesearch-python – for generating URLs from queries
Typer – for building CLI interfaces

### 7. 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Let me know if you want me to generate a `requirements.txt` or auto-link to your GitHub repo.
