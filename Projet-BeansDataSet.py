import streamlit as st
from PIL import Image
import pandas as pd
import seaborn as sns
import scipy as sp
from matplotlib import pyplot as plt


st.markdown(
    """
    <div style='text-align:center'>
    <h1>Statistique descriptive et Analyse des ventes ☕</h1>
    </div><br>
    """, unsafe_allow_html=True
)


fichier = 'data/BeansDataSet.csv'
try:
    data = pd.read_csv(fichier)
except Exception as e:
    st.error(f"Erreur lors du chargement des données : {e}")
    st.stop()

#Convertir les columns numériques
for col in data.columns:
    if col not in ["Channel", "Region"]:
        data[col] = pd.to_numeric(data[col], errors='coerce')


data.fillna(0, inplace=True)

st.sidebar.title('Menu')
menu = st.sidebar.selectbox('Sélectionnez une option',
                            ['Accueil', 'Aperçu des données', 'Visualisation', 'Recommandations','GITHub'])

if menu == 'Accueil':
    st.subheader("Affichage des données des ventes")
    st.dataframe(data)


elif menu == 'Aperçu des données':
    st.subheader("📊 Statistiques descriptives")
    st.write(data.describe())

    numeric_cols = data.select_dtypes(include=['number'])

    if not numeric_cols.empty:
        # matrice de corrélation
        correlation_matrix = numeric_cols.corr()

        st.subheader("📈 Matrice de corrélation")
        st.write(correlation_matrix)

        # heatmap
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
        st.pyplot(fig)
    else:
        st.error("Aucune colonne numérique disponible pour la corrélation.")

elif menu == 'Visualisation':
    st.subheader("📊 Histogrammes des ventes")
    data.hist(bins=20, figsize=(15, 10))
    st.pyplot(plt.gcf())

    st.subheader("📈 Matrice de corrélation")
    numeric_cols = data.select_dtypes(include=['number'])
    if not numeric_cols.empty:
        fig, ax_corr = plt.subplots(figsize=(10, 10))
        sns.heatmap(numeric_cols.corr(), annot=True, cmap='coolwarm', fmt='.2f', ax=ax_corr)
        st.pyplot(fig)
    else:
        st.error("Aucune colonne numérique disponible pour la corrélation.")


    if "Channel" in data.columns:
        sales_by_channel = data.groupby("Channel").sum(numeric_only=True).sum(axis=1)
        st.subheader("📊 Ventes par canal")
        st.bar_chart(sales_by_channel)
    else:
        st.error("La colonne 'Channel' est introuvable dans les données.")

    st.subheader("📊 Ventes par région")
    if "Region" in data.columns:
        sales_by_region = data.groupby("Region").sum(numeric_only=True).sum(axis=1)
        st.bar_chart(sales_by_region)

        regions = ["Tous"] + list(data["Region"].unique())
        selected_region = st.selectbox("Sélectionnez une région", regions)

        if selected_region == "Tous":
            filtered_data = data 
        else:
            filtered_data = data[data["Region"] == selected_region]

        st.subheader(f"📊 Ventes dans {selected_region} région")
        st.dataframe(filtered_data)
    else:
        st.error("La colonne 'Region' est introuvable dans les données.")


    

elif menu == 'Recommandations':
    st.subheader("📌 Recommandations basées sur l'analyse")
    
    st.write("""
    1. **Optimiser l'inventaire pour les préférences des consommateurs** : 
        - **Espresso**, **Latte**, et **Cappuccino** restent les plus populaires. Assurez-vous d'avoir une large offre de ces types de cafés, en particulier pour la vente en ligne.
        - **Robusta** et **Arabica** peuvent être mieux distribués dans les magasins physiques, car certains consommateurs préfèrent acheter ces cafés en personne.
    """)
    
    st.write("""
    2. **Accroître les ventes en ligne** :
        - Les ventes en ligne sont globalement plus fortes. Il est pertinent d'investir dans l'amélioration de la plateforme de vente en ligne (expérience utilisateur, options de paiement, livraison rapide).
        - **Campagnes de fidélisation en ligne** : Développer des programmes de fidélité ou des promotions ciblées pour les consommateurs réguliers d'Espresso, Latte, et Cappuccino.
    """)
    
    st.write("""
    3. **Analyse des horaires de vente** :
        - Identifiez les horaires de forte consommation pour mieux adapter l'approvisionnement et les promotions. Par exemple, des pics de consommation en fin de journée ou pendant les week-ends peuvent nécessiter un réajustement des stocks.
    """)
    
    st.write("""
    4. **Cibler des segments spécifiques selon les types de café** :
        - **Espresso** et **Latte** peuvent être ciblés pour les jeunes professionnels qui cherchent à acheter rapidement. Les **Cappuccino** et **Lungo** peuvent être mis en avant dans des campagnes visant des consommateurs recherchant des moments de détente.
        - Proposez des options personnalisées ou des **packs de dégustation** pour ceux qui souhaitent explorer différents types de café.
    """)
    
    st.write("""
    5. **Suivi des tendances régionales** :
        - Bien que la région Sud soit prédominante dans les données, il serait intéressant d'explorer la possibilité d'étendre les offres dans d'autres régions en fonction des tendances locales observées dans les magasins.
    """)
    
    st.write("""
    6. **Mise en avant des produits populaires dans les magasins physiques** :
        - Pour les magasins physiques, il est judicieux de mettre davantage l'accent sur **Robusta** et **Arabica**, en particulier pour les clients fidèles aux cafés plus intenses. Des promotions spécifiques pourraient être envisagées en fonction de la saisonnalité ou des préférences locales.
    """)
elif menu == 'GitHub':
    st.subheader("🔗 Lien vers le code source : ")
    st.markdown("https://github.com/votre-utilisateur/votre-repo")
