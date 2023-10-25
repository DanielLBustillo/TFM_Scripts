"""
EJECUCION: 
para instalar paquete: pip install pytest-playwright
para instalar playwright: python -m playwright install
"""

from parsel import Selector
from playwright.sync_api import sync_playwright
import json
import time
import pandas as pd

JSON_CREATED = False
MAX_DOCUMENTS = 1000000

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

                # checks if next page arrow key is greyed out `attr(rel)` (inactive) and breaks out of the loop
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
    df = pd.DataFrame(results)
    print(df)
    resultsJSON = json.dumps(results, indent=2, ensure_ascii=False)
    print("\n\nFinish API calls")
    df.to_csv("responseAPI.csv", index=False)  # El parámetro 'index=False' evita guardar el índice de las filas en el archivo CSV
    rutaArchivo = "responseAPI.json"
    with open(rutaArchivo, 'w') as archivo:
        json.dump(resultsJSON, archivo)
    print("JSON file created\n")
else:
    print(" \n*** JSON ya creado. Cambie la variable de ejecución: JSON_CREATED a False si quieres volver a crearlo. ***\n ")



