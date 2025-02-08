import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def show_dashboard(df):
    st.write("### Aperçu des données")
    st.dataframe(df.head())

    st.write("### Visualisation des données")
    # Charger le fichier CSV
    #file_path = "chemin/vers/ton_fichier.csv"  # Remplace par ton chemin réel
    #df = pd.read_csv(file_path)

    # Convertir les prix en numérique (enlevant d'éventuels caractères non numériques)
    #df['prix'] = pd.to_numeric(df['prix'], errors='coerce')

    # Supprimer les valeurs NaN dans la colonne prix
    #df = df.dropna(subset=['prix'])

    # 1. Distribution des prix des chiens
    if "prix" in df.columns :
        plt.figure(figsize=(10, 5))
        sns.histplot(df['prix'], bins=30, kde=True, color='skyblue')
        plt.xlabel("Prix (CFA)")
        plt.ylabel("Nombre d'annonces")
        plt.title("Distribution des prix des chiens")
        plt.grid(True)
        plt.show()

    """# 2. Diagramme circulaire des annonces par localisation
    location_counts = df['adresse'].value_counts().head(10)  # Top 10 localisations

    plt.figure(figsize=(8, 8))
    plt.pie(location_counts, labels=location_counts.index, autopct='%1.1f%%', colors=sns.color_palette("pastel"))
    plt.title("Répartition des annonces par localisation (Top 10)")
    plt.show()

    # 3. Prix moyen des chiens par ville (Top 10 villes)
    avg_price_per_city = df.groupby('adresse')['prix'].mean().sort_values(ascending=False).head(10)

    plt.figure(figsize=(12, 6))
    sns.barplot(x=avg_price_per_city.values, y=avg_price_per_city.index, palette="viridis")
    plt.xlabel("Prix moyen (CFA)")
    plt.ylabel("Localisation")
    plt.title("Prix moyen des chiens par localisation (Top 10)")
    plt.grid(axis="x")
    plt.show()"""

