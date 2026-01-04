import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
import re


def clean_text(text):
    if text:
        return re.sub(r"\s+", " ", text).strip()
    return None

def clean_price(price):
    if price:
        return re.sub(r"[^\d]", "", price)
    return None

#SCRAPER URL 1 – VOITURES
def scrape_voitures(base_url, pages=5):
    data = []

    for page in range(1, pages + 1):
        url = f"{base_url}?page={page}"
        print(f"Scraping : {url}")

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        annonces = soup.find_all("div", class_="listings-cards__list-item mb-md-3 mb-3")

        for annonce in annonces:
            titre = annonce.find("h2",class_="listing-card__header__title")
            marque = annee = None
            if titre:
                a_tag = titre.find("a")
                if a_tag:
                    texte = a_tag.get_text(strip=True)
                    match = re.search(r"(\d{4})$", texte)
                    if match:
                        annee = match.group(1)
                        marque = texte.replace(annee, "").strip()
                    else:
                        marque = texte
            prix = annonce.find("h3")
            adresse = annonce.find("div", class_="col-12 entry-zone-address")
            proprietaire = None
            author_div = annonce.find("div", class_="author-meta")
            if author_div:
                a_tag = author_div.find("a")
                if a_tag:
                    proprietaire = a_tag.get_text().replace("Par ", "")
            # ATTRIBUTS (UL / LI)
            kilometrage = carburant = boite_vitesse = None

            ul = annonce.find("ul", class_="listing-card__attribute-list list-inline mb-0")
            if ul:
                items = ul.find_all("li")

                for item in items:
                    text = item.get_text(strip=True)

                    if "km" in text.lower():
                        kilometrage = text
                    elif text.lower() in ["essence", "diesel", "hybride", "électrique"]:
                        carburant = text
                    elif text.lower() in ["automatique", "manuelle"]:
                        boite_vitesse = text

            data.append({
                "marque": marque,
                "annee": annee,
                "prix": clean_price(prix.text if prix else None),
                "adresse": clean_text(adresse.text if adresse else None),
                "kilometrage": kilometrage,
                "boite_vitesse": boite_vitesse,
                "carburant": carburant,
                "proprietaire": clean_text(proprietaire)
            })

    return pd.DataFrame(data)

#SCRAPER URL 2 – MOTOS & SCOOTERS
def scrape_motos(base_url, pages=5):
    data = []

    for page in range(1, pages + 1):
        url = f"{base_url}?page={page}"
        print(f"Scraping : {url}")

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        annonces = soup.find_all("div", class_="listings-cards__list-item mb-md-3 mb-3")

        for annonce in annonces:
            titre = annonce.find("h2",class_="listing-card__header__title mb-md-2 mb-0")
            marque = annee = None
            if titre:
                a_tag = titre.find("a")
                if a_tag:
                    texte = a_tag.get_text(strip=True)
                    match = re.search(r"(\d{4})$", texte)
                    if match:
                        annee = match.group(1)
                        marque = texte.replace(annee, "").strip()
                    else:
                        marque = texte
            prix = annonce.find("h3")
            adresse = annonce.find("div", class_="col-12 entry-zone-address")
            proprietaire = None
            author_div = annonce.find("div", class_="author-meta")
            if author_div:
                a_tag = author_div.find("a")
                if a_tag:
                    proprietaire = a_tag.get_text().replace("Par ", "")
            # ATTRIBUT (UL / LI)
            kilometrage = None

            ul = annonce.find("ul", class_="listing-card__attribute-list list-inline mb-0")
            if ul:
                items = ul.find_all("li")

                for item in items:
                    text = item.get_text(strip=True)

                    if "km" in text.lower():
                        kilometrage = text

            data.append({
                "marque": marque,
                "annee": annee,
                "prix": clean_price(prix.text if prix else None),
                "adresse": clean_text(adresse.text if adresse else None),
                "kilometrage": kilometrage,
                "proprietaire": clean_text(proprietaire)
            })

    return pd.DataFrame(data)

#SCRAPER URL 3 – LOCATION DE VOITURES
def scrape_location(base_url, pages=5):
    data = []
    for page in range(1, pages + 1):
        url = f"{base_url}?page={page}"
        print(f"Scraping : {url}")

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        annonces = soup.find_all("div", class_="listings-cards__list-item mb-md-3 mb-3")

        for annonce in annonces:
            titre = annonce.find("h2",class_="listing-card__header__title mb-md-2 mb-0")
            marque = annee = None
            if titre:
                a_tag = titre.find("a")
                if a_tag:
                    texte = a_tag.get_text(strip=True)
                    match = re.search(r"(\d{4})$", texte)
                    if match:
                        annee = match.group(1)
                        marque = texte.replace(annee, "").strip()
                    else:
                        marque = texte
            prix = annonce.find("h3")
            adresse = annonce.find("div", class_="col-12 entry-zone-address")
            proprietaire = None
            author_div = annonce.find("div", class_="author-meta")
            if author_div:
                a_tag = author_div.find("a")
                if a_tag:
                    proprietaire = a_tag.get_text().replace("Par ", "")

            data.append({
                "marque": marque,
                "annee": annee,
                "prix": clean_price(prix.text if prix else None),
                "adresse": clean_text(adresse.text if adresse else None),
                "proprietaire": clean_text(proprietaire)
            })

    return pd.DataFrame(data)
#Exécution + sauvegarde CSV
df_voitures = scrape_voitures("https://dakar-auto.com/senegal/voitures-4", pages=10)
df_voitures.to_csv("voitures.csv", index=False)

df_motos = scrape_motos("https://dakar-auto.com/senegal/motos-and-scooters-3", pages=10)
df_motos.to_csv("motos.csv", index=False)

df_location = scrape_location("https://dakar-auto.com/senegal/location-de-voitures-19", pages=10)
df_location.to_csv("location_voitures.csv", index=False)