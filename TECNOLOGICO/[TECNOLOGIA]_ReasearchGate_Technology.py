"""
EJECUCION:
para instalar paquete: pip install pytest-playwright
para instalar playwright: python -m playwright install
"""

from parsel import Selector
from playwright.sync_api import sync_playwright
import json
import time
import json
import csv
import pandas as pd


JSON_CREATED = False
MAX_DOCUMENTS = 2

def scrape_researchgate_publications(query: str, max_pages=MAX_DOCUMENTS):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=50)
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36")

        publications = []
        page_num = 1

        while page_num <= max_pages:
            try:
                page.goto(f"https://www.researchgate.net/search/publication?q={query}&page={page_num}")
                selector = Selector(text=page.content())

                for publication in selector.css(".nova-legacy-c-card__body--spacing-inherit"):
                    title = publication.css(
                        ".nova-legacy-v-publication-item__title .nova-legacy-e-link--theme-bare::text").get().title()
                    title_link = f'https://www.researchgate.net{publication.css(".nova-legacy-v-publication-item__title .nova-legacy-e-link--theme-bare::attr(href)").get()}'
                    publication_type = publication.css(".nova-legacy-v-publication-item__badge::text").get()
                    publication_date = publication.css(
                        ".nova-legacy-v-publication-item__meta-data-item:nth-child(1) span::text").get()
                    publication_doi = publication.css(
                        ".nova-legacy-v-publication-item__meta-data-item:nth-child(2) span").xpath(
                        "normalize-space()").get()
                    authors = publication.css(".nova-legacy-v-person-inline-item__fullname::text").getall()
                    source_link = f'https://www.researchgate.net{publication.css(".nova-legacy-v-publication-item__preview-source .nova-legacy-e-link--theme-bare::attr(href)").get()}'
                    publications.append({
                        "title": title,
                        "link": title_link,
                        "source_link": source_link,
                        "publication_type": publication_type,
                        "publication_date": publication_date,
                        "publication_doi": publication_doi,
                        "authors": authors
                    })

                print(f"Processed page number: {page_num}")

                # checks if next page arrow key is greyed out attr(rel) (inactive) and breaks out of the loop
                if selector.css(".nova-legacy-c-button-group__item:nth-child(9) a::attr(rel)").get():
                    break
                else:
                    page_num += 1
                    time.sleep(2)  # Adding a delay to be respectful to the server

            except Exception as e:
                print(f"Error on page {page_num}: {e}")
                break

        browser.close()
        return publications

if(JSON_CREATED is False):

    results = scrape_researchgate_publications(query="tuberculosis")
    #print(json.dumps(results, indent=2, ensure_ascii=False))
    resultsJSON = json.dumps(results, indent=2, ensure_ascii=False)
    print("\n\nFinish API calls")
    # Abre el archivo en modo escritura y guarda el JSON en él
    rutaArchivo = "c:/TFM/researchgateAPI.json"
    with open(rutaArchivo, 'w') as archivo:
        json.dump(resultsJSON, archivo)
    print("JSON file created\n")

#transformar JSON -> CSV
# Leer el archivo JSON
with open(rutaArchivo, 'r') as json_file:
    data = json.load(json_file)

# Crear o sobrescribir un archivo CSV
with open('c:/TFM/researchgateAPI.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)

    # Escribir la cabecera del CSV
    header = ['title', 'link', 'source_link', 'publication_type', 'publication_date', 'publication_doi', 'authors']
    writer.writerow(header)

    # Escribir el contenido del JSON en el CSV
    json = json.loads(data)
    todos_autores = set()
    for item in json:
        todos_autores.update(item['authors'])
        cadena_autores = ', '.join([author.strip() for author in todos_autores])
        writer.writerow(
            [item['title'], item['link'], item['source_link'], item['publication_type'], item['publication_date'],
             item.get('publication_doi', ''), cadena_autores])

print("Conversión completada!")
