import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def show_dashboard(df):
    st.write("### Aperçu des données")
    st.dataframe(df.head())

    st.write("### Visualisation des données")
    # Charger le fichier CSV
    file_path = "data/" 
    selected_file = st.selectbox("Sélectionnez un dataset :", os.listdir(file_path))
    if selected_file:
        df = pd.read_csv(os.path.join(file_path, selected_file))
        plt.figure(figsize=(10, 5))
        sns.histplot(df['prix'], bins=30, kde=True, color='skyblue')
        plt.xlabel("Prix (CFA)")
        plt.ylabel("Nombre d'annonces")
        plt.title("Distribution des prix des chiens")
        plt.grid(True)
        plt.show()
    plt.show()"""

