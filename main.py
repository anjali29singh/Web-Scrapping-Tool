import typer
from scrapper.utils import process_query
from scrapper import process
from scrapper.scrapper import CompanySpider
def main(query):
    try:
        start_url_list = process_query(query=query)
        process.crawl(CompanySpider, start_urls=start_url_list)
        process.start()
    except Exception as e:
        typer.echo(f"An error occurred: {e}")
        raise typer.Exit(code=1)

    

if __name__ == "__main__":
    typer.run(main)
