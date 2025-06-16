
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Planning Dentaire", layout="wide")

st.title("📅 Planning Dentaire — Rotation des Assistantes le Samedi")

# Charger le fichier
uploaded_file = st.file_uploader("📂 Charger le fichier de planning (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    semaine_selection = st.selectbox(
        "🗓️ Choisir une semaine du mois :", 
        sorted(df["semaine_du_mois"].unique())
    )

    df_filtered = df[df["semaine_du_mois"] == semaine_selection]
    df_filtered = df_filtered.sort_values(by=["jour", "demi_journée"])

    st.write(f"### 📆 Planning pour la semaine : {semaine_selection}")
    st.dataframe(df_filtered, use_container_width=True)

    # Export
    with st.expander("⬇️ Télécharger le planning filtré"):
        st.download_button(
            label="📥 Télécharger en Excel",
            data=df_filtered.to_excel(index=False),
            file_name=f"planning_{semaine_selection}.xlsx"
        )
else:
    st.info("Veuillez charger un fichier Excel de planning.")
