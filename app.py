import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode

# ------------------------------------------------------------------------------
# 1. Configuration de l'application
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Analyse Automobile - Auto MPG",
    page_icon="🚘",
    layout="wide"
)

# ------------------------------------------------------------------------------
# 2. Chargement et préparation des données
# ------------------------------------------------------------------------------
url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/mpg.csv"
try:
    df = pd.read_csv(url)
except Exception:
    df = pd.read_csv("mpg.csv")

# Conversions des unités américaines vers les unités internationales
df["year"] = 1900 + df["model_year"]
df["consumption_l_100km"] = (235.215 / df["mpg"]).round(2)
df["weight_kg"] = (df["weight"] * 0.453592).round(2)

colonnes_affichage = [
    "name", "origin", "year", "cylinders", "mpg",
    "consumption_l_100km", "horsepower", "weight_kg", "acceleration"
]

# ------------------------------------------------------------------------------
# 3. Barre latérale : Composants de filtres (st.sidebar)
# ------------------------------------------------------------------------------
st.sidebar.header("⚙️ Filtres de recherche")

# 1. Filtre par origine
options_origines = ["Toutes", "usa", "japan", "europe"]
origine_selectionnee = st.sidebar.selectbox("Région / Origine", options_origines)

# 2. Filtre par cylindres
liste_cylindres = sorted(df["cylinders"].dropna().unique().tolist())
cylindres_selectionnes = st.sidebar.multiselect(
    "Nombre de cylindres",
    options=liste_cylindres,
    default=liste_cylindres
)

# 3. Filtre par année
annee_min = int(df["year"].min())
annee_max = int(df["year"].max())
periode = st.sidebar.slider(
    "Année de fabrication",
    min_value=annee_min,
    max_value=annee_max,
    value=(annee_min, annee_max)
)

# 4. Filtre par efficacité minimale
mpg_min_dataset = float(df["mpg"].min())
mpg_max_dataset = float(df["mpg"].max())
seuil_mpg = st.sidebar.slider(
    "Efficacité minimale (MPG)",
    min_value=mpg_min_dataset,
    max_value=mpg_max_dataset,
    value=mpg_min_dataset,
    step=0.5
)

# Application des filtres sur le DataFrame
df_filtre = df.copy()

if origine_selectionnee != "Toutes":
    df_filtre = df_filtre[df_filtre["origin"] == origine_selectionnee]

if cylindres_selectionnes:
    df_filtre = df_filtre[df_filtre["cylinders"].isin(cylindres_selectionnes)]
else:
    df_filtre = df_filtre.head(0)

df_filtre = df_filtre[
    (df_filtre["year"] >= periode[0]) & 
    (df_filtre["year"] <= periode[1])
]

df_filtre = df_filtre[df_filtre["mpg"] >= seuil_mpg]

# Petit résumé dans la barre latérale
st.sidebar.divider()
st.sidebar.caption(f"📌 **{len(df_filtre)}** véhicules trouvés sur **{len(df)}**")

# ------------------------------------------------------------------------------
# 4. En-tête principal
# ------------------------------------------------------------------------------
st.title("🚘 Tableau de Bord — Analyse des Véhicules (Auto MPG)")
st.markdown(
    "Exploration descriptive des données automobiles historiques (sans machine learning). "
    "Ce projet permet d'analyser la consommation, la puissance et l'impact du poids des véhicules."
)

# ------------------------------------------------------------------------------
# 5. Indicateurs clés (KPIs avec st.columns & st.metric)
# ------------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

if not df_filtre.empty:
    moy_conso = df_filtre["consumption_l_100km"].mean()
    moy_puissance = df_filtre["horsepower"].mean()
    moy_mpg = df_filtre["mpg"].mean()
    
    col1.metric("Véhicules filtrés", f"{len(df_filtre)}")
    col2.metric("Consommation moyenne", f"{moy_conso:.2f} L/100 km")
    col3.metric("Puissance moyenne", f"{moy_puissance:.1f} HP")
    col4.metric("Efficacité moyenne", f"{moy_mpg:.1f} MPG")
else:
    col1.metric("Véhicules filtrés", "0")
    col2.metric("Consommation moyenne", "—")
    col3.metric("Puissance moyenne", "—")
    col4.metric("Efficacité moyenne", "—")

st.divider()

# ------------------------------------------------------------------------------
# 6. Organisation en Onglets (st.tabs) pour structurer le travail
# ------------------------------------------------------------------------------
tab_donnees, tab_graphiques, tab_details = st.tabs([
    "📋 Données & AgGrid",
    "📈 Graphiques & Comparaisons",
    "🔍 Fiche Véhicule"
])

# ------------------------------------------------------------------------------
# Onglet 1 : Données interactives avec AgGrid
# ------------------------------------------------------------------------------
with tab_donnees:
    st.subheader("Tableau interactif des données filtrées")
    st.caption("Vous pouvez trier les colonnes, utiliser les filtres d'en-tête et naviguer avec la pagination.")

    if not df_filtre.empty:
        donnees_aggrid = df_filtre[colonnes_affichage].reset_index(drop=True)
        
        # Configuration AgGrid
        gb = GridOptionsBuilder.from_dataframe(donnees_aggrid)
        gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=10)
        gb.configure_default_column(sortable=True, filter=True, resizable=True)
        gb.configure_column("name", minWidth=200, header_name="Modèle")
        gb.configure_column("origin", header_name="Origine")
        gb.configure_column("year", header_name="Année")
        gb.configure_column("cylinders", header_name="Cylindres")
        gb.configure_column("mpg", header_name="Efficacité (MPG)")
        gb.configure_column("consumption_l_100km", minWidth=160, header_name="Conso (L/100km)")
        gb.configure_column("horsepower", header_name="Puissance (HP)")
        gb.configure_column("weight_kg", header_name="Poids (kg)")
        gb.configure_column("acceleration", header_name="Accélération")
        
        grid_options = gb.build()

        AgGrid(
            donnees_aggrid,
            gridOptions=grid_options,
            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
            height=380
        )
    else:
        st.warning("Aucun véhicule ne correspond aux filtres appliqués.")

# ------------------------------------------------------------------------------
# Onglet 2 : Visualisations graphiques (st.bar_chart, st.scatter_chart, st.line_chart)
# ------------------------------------------------------------------------------
with tab_graphiques:
    st.subheader("Analyses visuelles et relations")

    if not df_filtre.empty:
        col_g1, col_g2 = st.columns(2)

        with col_g1:
            st.markdown("#### 1. Comparaison du nombre de véhicules par origine")
            comptage_origine = df_filtre["origin"].value_counts().reset_index()
            comptage_origine.columns = ["Origine", "Nombre"]
            st.bar_chart(comptage_origine, x="Origine", y="Nombre", color="Origine")

        with col_g2:
            st.markdown("#### 2. Évolution de l'efficacité moyenne par année")
            moyenne_par_an = df_filtre.groupby("year")["mpg"].mean().reset_index()
            moyenne_par_an.columns = ["Année", "MPG Moyen"]
            st.line_chart(moyenne_par_an, x="Année", y="MPG Moyen")

        st.markdown("#### 3. Relation entre le poids (kg) et la consommation (L/100 km)")
        st.caption("Chaque point représente un véhicule, coloré selon son origine.")
        st.scatter_chart(
            df_filtre,
            x="weight_kg",
            y="consumption_l_100km",
            color="origin",
            size="horsepower"
        )
    else:
        st.info("Sélectionnez des filtres pour afficher les graphiques.")

# ------------------------------------------------------------------------------
# Onglet 3 : Sélection et fiche détaillée d'un véhicule
# ------------------------------------------------------------------------------
with tab_details:
    st.subheader("Consulter les détails d'un véhicule précis")

    if not df_filtre.empty:
        noms_vehicules = [
            f"{row['name']} ({row['year']}) — {row['origin']}"
            for _, row in df_filtre.iterrows()
        ]
        
        vehicule_choisi = st.selectbox("Sélectionnez un véhicule dans la liste", noms_vehicules)
        index_choisi = noms_vehicules.index(vehicule_choisi)
        vehicule_info = df_filtre.iloc[index_choisi]

        # Affichage sous forme de fiches métriques (st.columns)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Modèle", str(vehicule_info["name"]))
        c2.metric("Origine", str(vehicule_info["origin"]).upper())
        c3.metric("Année", str(vehicule_info["year"]))
        c4.metric("Cylindres", f"{int(vehicule_info['cylinders'])} cyl.")

        c5, c6, c7, c8 = st.columns(4)
        c5.metric("Consommation", f"{vehicule_info['consumption_l_100km']} L/100km")
        c6.metric("Puissance", f"{vehicule_info['horsepower']} HP")
        c7.metric("Poids", f"{vehicule_info['weight_kg']} kg")
        c8.metric("Accélération", f"{vehicule_info['acceleration']} s")

        st.divider()

        # Mini tableau AgGrid de la sélection
        st.caption("Ligne complète du véhicule :")
        ligne_df = df_filtre.iloc[[index_choisi]][colonnes_affichage].reset_index(drop=True)
        gb_mini = GridOptionsBuilder.from_dataframe(ligne_df)
        AgGrid(ligne_df, gridOptions=gb_mini.build(), height=100)
    else:
        st.warning("Aucun véhicule disponible.")
