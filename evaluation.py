import streamlit as st

def show_evaluation_form():
    with st.form("evaluation_form"):
        st.write("### Évaluation de l'application")
        name = st.text_input("Nom")
        rating = st.slider("Note", 1, 5)
        feedback = st.text_area("Commentaires")

        submitted = st.form_submit_button("Envoyer")
        if submitted:
            st.success("Merci pour votre retour !")
