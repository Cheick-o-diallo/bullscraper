import streamlit as st
import scraper
import data_cleaning 
import dashboard
import evaluation 
import pandas as pd
import os

st.set_page_config(page_title="Scraper App", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à :", ["Scraper", "Télécharger", "Dashboard", "Évaluation"])

# Charger les données
DATA_FILE = "Beautifulsoup_scrapped_data/"

if page == "Scraper":
    st.title("Scraping des données")
    url = st.text_input("Entrer l'URL de départ")
    num_pages = st.number_input("Nombre de pages à scraper", min_value=1, value=5)
    if st.button("Lancer le scraping"):
        output_file = os.path.join(DATA_FILE, "new_scraped_data.csv")
        scraper.scrape_data(url, num_pages, output_file)
        st.success("Scraping terminé ! Données enregistrées.")

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
        df = pd.read_csv(os.path.join(DATA_FILE, selected_file))
        cleaned_df = data_cleaning.clean_data(df)
        dashboard.show_dashboard(cleaned_df)

elif page == "Évaluation":
    st.title("Formulaire d'évaluation")
    evaluation.show_evaluation_form()
