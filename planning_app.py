
import streamlit as st
import pandas as pd
import io

# Fonction pour recalculer le planning en cas d'absence
def reaffecter_assistante(df, semaine, jour, demi_journee, assistante_absente):
    mask = (df["semaine"] == semaine) & (df["jour"] == jour) & (df["demi_journée"] == demi_journee)
    row = df.loc[mask]

    if row.empty:
        return df, f"Aucune donnée trouvée pour {semaine}, {jour} {demi_journee}"

    current = row["assistantes_affectées"].values[0].split(", ")
    if assistante_absente not in current:
        return df, f"{assistante_absente} n'était pas affectée ce créneau."

    updated = [a for a in current if a != assistante_absente]

    assistantes_par_jour = {
        "lundi": ["amel", "julie", "elodie", "anne", "valentine", "charlotte"],
        "mardi": ["amel", "julie", "elodie", "anne", "valentine", "aïssatou"],
        "mercredi": ["julie", "charlotte", "saousan", "esra"],
        "jeudi": ["amel", "julie", "elodie", "anne", "valentine", "charlotte", "aïssatou", "esra"],
        "vendredi": ["amel", "elodie", "anne", "valentine", "aïssatou", "esra"],
        "samedi": ["esra", "saousan", "aïssatou", "charlotte"]
    }

    pool = assistantes_par_jour.get(jour, [])
    remplacantes = [a for a in pool if a not in updated and a != assistante_absente]

    suggestion = ""
    if remplacantes:
        updated.append(remplacantes[0])
        suggestion = f"{assistante_absente} remplacée par {remplacantes[0]}"
    else:
        suggestion = f"Aucune assistante disponible pour remplacer {assistante_absente}"

    df.loc[mask, "assistantes_affectées"] = ", ".join(updated)
    df.loc[mask, "commentaire"] = suggestion

    return df, suggestion

# Interface Streamlit
st.set_page_config(page_title="Planning IA - Absence Assistante", layout="wide")
st.title("🤖 IA de remplacement d'assistante en cas d'absence")

uploaded_file = st.file_uploader("📂 Charger le planning complet 52 semaines", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    semaine = st.selectbox("Semaine concernée", sorted(df["semaine"].unique()))
    jour = st.selectbox("Jour", ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"])
    demi = st.selectbox("Demi-journée", ["matin", "après-midi"])
    assistante = st.selectbox("Assistante absente", sorted(set(", ".join(df["assistantes_affectées"]).split(", "))))

    if st.button("💡 Lancer l'IA de suggestion"):
        df_new, message = reaffecter_assistante(df.copy(), semaine, jour, demi, assistante)
        st.success(message)
        st.write("📅 Planning mis à jour pour vérification :")
        st.dataframe(df_new[(df_new["semaine"] == semaine) & (df_new["jour"] == jour)], use_container_width=True)

        buffer = io.BytesIO()
        df_new.to_excel(buffer, index=False, engine="openpyxl")
        buffer.seek(0)

        st.download_button(
            label="📥 Télécharger le planning modifié",
            data=buffer,
            file_name=f"planning_{semaine}_modifié.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.warning("Veuillez charger un fichier de planning d'abord.")
