import typer
import json
from scrapper.utils import process_query
from scrapper import process
from scrapper.scrapper import CompanySpider

def deduplicate_jsonl(input_path: str, output_path: str):
    seen = set()
    unique_items = []

    with open(input_path, "r", encoding="utf-8") as infile:
        for line in infile:
            try:
                item = json.loads(line)
                item_str = json.dumps(item, sort_keys=True)
                if item_str not in seen:
                    seen.add(item_str)
                    unique_items.append(item)
            except json.JSONDecodeError:
                continue

    with open(output_path, "w", encoding="utf-8") as outfile:
        for item in unique_items:
            json.dump(item, outfile, ensure_ascii=False)
            outfile.write("\n")

def main(query: str):
    try:
        start_url_list = process_query(query=query)
        process.crawl(CompanySpider, start_urls=start_url_list)
        process.start()

        # Remove duplicates after crawling
        typer.echo("Removing duplicates from output.jsonl...")
        deduplicate_jsonl("output.jsonl", "output_clean.jsonl")
        typer.echo("Deduplication complete. Cleaned file saved as output_clean.jsonl.")

    except Exception as e:
        typer.echo(f"An error occurred: {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    typer.run(main)
