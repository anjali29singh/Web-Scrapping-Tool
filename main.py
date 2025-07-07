import typer
from scrapper.utils import process_query
def main(query):
    
    start_url_list = process_query(query=query)

    

if __name__ == "__main__":
    typer.run(main)
