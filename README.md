# Projet : Dashboard d'Analyse Automobile (Auto MPG)

Application Streamlit d'analyse descriptive et exploratoire développée dans le cadre du module **DEV IA**.

## Objectifs et fonctionnalités

- **Exploration des données sans ML** : Analyse statistique et visuelle du jeu de données Seaborn Auto MPG.
- **Filtres interactifs (`st.sidebar`)** :
  - Origine géographique (`usa`, `japan`, `europe`)
  - Nombre de cylindres (`3`, `4`, `5`, `6`, `8`)
  - Année de fabrication (`1970` à `1982`)
  - Seuil d'efficacité minimale (`MPG`)
- **Indicateurs statistiques clés (`st.metric` & `st.columns`)** :
  - Nombre total de véhicules filtrés
  - Consommation moyenne (`L/100 km`)
  - Puissance moyenne (`HP`)
  - Efficacité moyenne (`MPG`)
- **Organisation en onglets (`st.tabs`)** :
  - **Onglet 1 (`📋 Données & AgGrid`)** : Tableau interactif avec tri, recherche, pagination et colonnes renommées.
  - **Onglet 2 (`📈 Graphiques & Comparaisons`)** :
    - Comparaison des véhicules par origine (`st.bar_chart`)
    - Évolution de l'efficacité par année (`st.line_chart`)
    - Nuage de points poids vs consommation (`st.scatter_chart`)
  - **Onglet 3 (`🔍 Fiche Véhicule`)** : Fiche détaillée avec toutes les caractéristiques d'un véhicule sélectionné.

## Dépendances

```bash
pip install -r requirements.txt
```

## Démarrage

```bash
cd "C:\Users\user\DEV IA 2"
streamlit run app.py
```
