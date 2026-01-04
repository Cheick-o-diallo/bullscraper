import streamlit as st
import scraper
import matplotlib.pyplot as plt
import seaborn as sns
import evaluation 
import pandas as pd
import os

st.set_page_config(page_title="AutoScraper App", layout="wide")

st.title("🚗 AutoScraper – Dakar Auto")
st.markdown("Scraping, nettoyage et visualisation des données automobiles")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à :", ["Scraper", "Télécharger", "Dashboard", "Évaluation"])

# Charger les données
DATA_FILE = "data/"

if page == "Scraper":
    st.title("Scraping des données")
    url = st.text_input("Entrer l'URL de départ")
    num_pages = st.number_input("Nombre de pages à scraper", min_value=1, value=5)
    if st.button("Lancer le scraping"):
        if not url :
            st.error("Veuiller entrer une URL valide")
        else:
            output_file = os.path.join(DATA_FILE, "new_scraped_data.csv")
            try:
                scraper.scrape_data(url, num_pages, output_file)
                st.success("Scraping terminé ! Données enregistrées.")
            except Exception as e:
                st.error(f"Erreur lors du scraping : {e}")

elif page == "Télécharger":
    st.title("Téléchargement des données")
    def load_(dataframe, title, key) :
        st.markdown("""
        <style>
        div.stButton {text-align:center}
        </style>""", unsafe_allow_html=True)

        if st.button(title,key):
        
            st.subheader('Display data dimension')
            st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
            st.dataframe(dataframe)
    # Charger les données 
    load_(pd.read_csv('data/dogs_data.csv'), 'dogs data', '1')
    load_(pd.read_csv('data/sheets_data.csv'), 'sheets data', '2')
    load_(pd.read_csv('data/Rabbit&Chicken_data.csv'), 'Rabbit&Chicken data', '3')
    load_(pd.read_csv('data/Other_animals_data.csv'), 'Ohter_animals data', '4')

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

