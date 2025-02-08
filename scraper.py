import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def scrape_data(start_url, num_pages, output_file):
    start_url = input("")
    output_file = os.path.join("Beautifulsoup_scrapped_data", "new_scraped_data.csv")
    data = []
    while True:
        for page in range(1, num_pages + 1):
            url = f"{start_url}?page={page}"
            print(f"Scraping page: {url}")
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Echec d'afficge de la page {page}. Arrêt.")
                break
            soup = BeautifulSoup(response.content, "html.parser")
            _cards = soup.find_all("div", class_ = "ad__card")
            if not _cards:
                print("Limite de donnée atteinte. Arrêt.")
                break
            
            for i in _cards:
                try:
                    nom = i.find('a')['title']
                    prix = i.find('a').find('span')['data-ad-price']
                    adresse = i.find('p', class_ = "ad__card-location").find('span').text.strip()
                    image = i.find('img')['src'] 
                    data.append({
                        'nom' : nom,
                        'prix' : prix,
                        'adresse' : adresse,
                        'image' : image})
                except AttributeError:
                    continue
            page += 1

        return data

    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)