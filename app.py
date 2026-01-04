import streamlit as st
import scraper
import matplotlib.pyplot as plt
import seaborn as sns
import evaluation 
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
DATA_FILE = "data/"
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

elif page == "Dashboard":
    st.title("Visualisation des données")
    selected_file = st.selectbox("Sélectionnez un dataset :", os.listdir(DATA_FILE))
    if selected_file:
        file_path = os.path.join(DATA_FILE, selected_file)
        
        try:
            df = pd.read_csv(file_path)

            st.write("### Aperçu des données")
            st.dataframe(df.head())

            # Vérifier si la colonne 'prix' existe
            if 'prix' in df.columns:
                # Convertir en numérique
                df['prix'] = pd.to_numeric(df['prix'], errors='coerce')
                df = df.dropna(subset=['prix'])

                st.write("### Distribution des prix")
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.histplot(df['prix'], bins=30, kde=True, color='skyblue', ax=ax)
                ax.set_xlabel("Prix (CFA)")
                ax.set_ylabel("Nombre d'annonces")
                ax.set_title("Distribution des prix des chiens")
                ax.grid(True)
                
                # Affichage dans Streamlit
                st.pyplot(fig)
            
            else:
                st.warning("Le dataset sélectionné ne contient pas de colonne 'prix'.")
        
        except:
            st.error("Erreur lors du chargement du fichier :")

elif page == "Évaluation":
    st.title("Formulaire d'évaluation")
    evaluation.show_evaluation_form()


