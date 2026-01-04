import streamlit as st
from scraper import *
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

st.set_page_config(page_title="AutoScraper App", layout="wide")

st.title("🚗 AutoScraper")
st.markdown("Scraping, nettoyage et visualisation des données automobiles")

# Sidebar navigation
menu = st.sidebar.selectbox(
    "Navigation",
    ["Scraping", "Télécharger données brutes", "Dashboard", "Évaluation"]
)

# Charger les données
#DATA_FILE = "data/"
# Scraping
if menu == "Scraping":
    st.header("🔎 Scraper des données")

    pages = st.number_input("Nombre de pages à scraper", min_value=1, max_value=50, value=5)

    if st.button("Lancer le scraping"):
        with st.spinner("Scraping en cours..."):
            df = scrape_voitures("https://dakar-auto.com/senegal/voitures-4", pages)
            df.to_csv("data/raw/voitures_raw.csv", index=False)
            st.success("Scraping terminé ✅")

        st.dataframe(df.head())
        
elif menu == "Télécharger données brutes":
    st.header("📥 Données brutes (Web Scraper)")

    st.markdown("Ces données ont été collectées automatiquement via Web Scraper.")

    fichiers = {
        "Voitures": "data/raw/voitures_raw.csv",
        "Motos & Scooters": "data/raw/motos_raw.csv",
        "Location de voitures": "data/raw/location_raw.csv"
    }

    choix = st.selectbox("Choisir un jeu de données", list(fichiers.keys()))

    df_raw = pd.read_csv(fichiers[choix])

    # 👀 Aperçu limité
    st.subheader("Aperçu des données")
    st.dataframe(df_raw.head(10), use_container_width=True)

    # 📥 Téléchargement
    st.download_button(
        label="📥 Télécharger les données brutes",
        data=df_raw.to_csv(index=False),
        file_name=f"{choix.lower().replace(' ', '_')}_raw.csv",
        mime="text/csv"
    )

elif menu == "Dashboard":
    st.header("📊 Dashboard – Données nettoyées (BeautifulSoup)")

    fichiers = {
        "Voitures": "data/cleaned/voitures.csv",
        "Motos & Scooters": "data/cleaned/motos.csv",
        "Location de voitures": "data/cleaned/location_voitures.csv"
    }

    choix = st.selectbox("Choisir un jeu de données", list(fichiers.keys()))

    df = pd.read_csv(fichiers[choix])

    st.caption("Données issues du scraping BeautifulSoup – déjà nettoyées")

    # --------------------
    # Filtres dynamiques
    # --------------------
    filtres = st.columns(3)

    with filtres[0]:
        if "marque" in df.columns:
            marques = st.multiselect(
                "Marque",
                sorted(df["marque"].dropna().unique())
            )
        else:
            marques = []

    with filtres[1]:
        if "annee" in df.columns:
            annee_min, annee_max = st.slider(
                "Année",
                int(df["annee"].min()),
                int(df["annee"].max()),
                (int(df["annee"].min()), int(df["annee"].max()))
            )
        else:
            annee_min = annee_max = None

    with filtres[2]:
        if "carburant" in df.columns:
            carburants = st.multiselect(
                "Carburant",
                sorted(df["carburant"].dropna().unique())
            )
        else:
            carburants = []

    # --------------------
    # Application filtres
    # --------------------
    df_filtre = df.copy()

    if marques:
        df_filtre = df_filtre[df_filtre["marque"].isin(marques)]

    if carburants:
        df_filtre = df_filtre[df_filtre["carburant"].isin(carburants)]

    if annee_min and annee_max:
        df_filtre = df_filtre[
            (df_filtre["annee"] >= annee_min) &
            (df_filtre["annee"] <= annee_max)
        ]

    # --------------------
    # KPI
    # --------------------
    st.subheader("Indicateurs clés")

    c1, c2, c3 = st.columns(3)
    c1.metric("Nombre d'annonces", len(df_filtre))
    c2.metric("Prix moyen", int(df_filtre["prix"].mean()) if "prix" in df_filtre else "N/A")
    c3.metric("Année moyenne", int(df_filtre["annee"].mean()) if "annee" in df_filtre else "N/A")

    # --------------------
    # Visualisations
    # --------------------
    st.subheader("Visualisations")

    col1, col2 = st.columns(2)

    with col1:
        if "carburant" in df_filtre.columns:
            st.bar_chart(df_filtre["carburant"].value_counts())

    with col2:
        if "annee" in df_filtre.columns and "prix" in df_filtre.columns:
            st.line_chart(
                df_filtre.groupby("annee")["prix"].mean()
            )

    # --------------------
    # Aperçu
    # --------------------
    st.subheader("Aperçu des données")
    st.dataframe(df_filtre.head(20), use_container_width=True)


elif menu == "Évaluation":
    st.header("📝 Évaluer l'application")

    st.markdown("""
    Merci de prendre quelques secondes pour évaluer cette application 👇  
    👉 [Accéder au formulaire Google Forms](https://forms.gle/XXXX)
    """)




