import streamlit as st
import pandas as pd
import plotly.express as px

def show_dashboard(df):
    st.write("### Aperçu des données")
    st.dataframe(df.head())

    st.write("### Visualisation des données")
    fig = px.histogram(df, x="title", title="Répartition des titres")
    st.plotly_chart(fig)
