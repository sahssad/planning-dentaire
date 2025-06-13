
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestionnaire de Planning Dentaire", layout="wide")

st.title("🦷 Gestionnaire de Planning - Version Démo")

st.markdown("Ce prototype vous permet de charger un planning, signaler une absence, et obtenir une suggestion automatique de remplacement.")

uploaded_file = st.file_uploader("📂 Charger un fichier Excel de planning", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("✅ Planning chargé avec succès")
    st.subheader("📅 Planning actuel")
    st.dataframe(df)

    st.subheader("🚨 Signaler une absence")
    absence_type = st.radio("Qui est absent ?", ["Assistante", "Dentiste"])
    nom_absent = st.text_input(f"Nom de l'{absence_type.lower()} absent(e)")
    jour = st.selectbox("Jour concerné :", df["Jour"].unique())

    if st.button("🤖 Proposer un remplacement automatique"):
        df_updated = df.copy()
        col = "Assistante" if absence_type == "Assistante" else "Dentiste"
        mask = (df_updated["Jour"] == jour) & (df_updated[col].str.lower() == nom_absent.strip().lower())

        if mask.any():
            df_updated.loc[mask, col] = f"Remplaçant(e) auto ({absence_type})"
            st.success("🎉 Planning mis à jour avec remplacement automatique :")
        else:
            st.warning("⚠️ Aucun poste trouvé correspondant à cette absence pour ce jour.")

        st.dataframe(df_updated)

        st.download_button(
            label="📥 Télécharger le planning modifié (Excel)",
            data=df_updated.to_excel(index=False),
            file_name="planning_modifie.xlsx"
        )
else:
    st.info("Veuillez charger un fichier Excel pour commencer.")
