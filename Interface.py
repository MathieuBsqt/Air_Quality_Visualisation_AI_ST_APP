import pandas as pd
import streamlit as st
from BaseDonnees import *
import datetime
from Traitements import *
from PIL import Image
import pydeck as pdk
import json
from streamlit_option_menu import option_menu
from IA import *
from AboutUs import *
from Prediction import *
from ImpactCovid import *
from Info import *


class Interface:
    def __init__(self):
        # Initilisation de la date
        # est-ce utile ?
        self.day = 0
        self.month = 0
        self.year = 0

    def choix_fenetre(self):
        """
        CONFIGURATION GENERALE DE L'INTERFACE
        favicon : logo onglet du site
        set_page_config : Titre de l'interface Web, favicon attribuée, et dimensions de l'interface wide pour full screen
        selectedMenu : Menu de navigation, contenu et orientation, style.
        """
        favicon = Image.open("ressources/favicon.png")
        st.set_page_config(page_title="Qualité de l'air", page_icon=favicon, layout="wide")
        selectedMenu = option_menu("Qualité de l'air 🌦️",
                                   ["Visualisation", "Prédiction", 'Impact des confinements', 'Informations utiles', 'À propos'],
                                   icons=['eye-fill', 'clock-history', "graph-up", 'info-lg', "patch-question-fill"],
                                   menu_icon="cloud_sun", default_index=0, orientation="horizontal",
                                   styles={
                                       "container": {"text-align": "center"},
                                       "icon": {"color": "black"},
                                       "nav-link": {"--hover-color": "#C0C0C0"},
                                   }
                                   )
        # CSS APPEARANCE
        """
        #MainMenu : Menu streamlit par défaut
        footer : "Made with Streamlit
        css-eczf16.e16nr0p32 : Href sur les titres (visualisation, ...)
        .css-6awftf.e19lei0e0 : View Full Screen des éléments (graphiques, images, carte, ...)  
        """
        hide_content = """                    
                    <style>
                    
                    footer {visibility: hidden; }
                    
                    .css-eczf16.e16nr0p32{visibility: hidden;}
                        
                    .css-6awftf.e19lei0e0{display:None}
                    </style>
                    """

        st.markdown(hide_content, unsafe_allow_html=True)

        """LECTURE DATABASE ET PREPROCESSING"""
        df = pd.read_csv("BDD_fichier_csv/Bdd_complete.csv", delimiter=";")
        df = df.drop(columns=["FID", "date_dif", "source", "type_zone", "code_zone", "x_reg", "y_reg", "epsg_reg", "geom"],
                     axis=1)

        """MENU NAVIGATION DE L'INTERFACE"""
        if selectedMenu == 'Visualisation':
            self.fenetre_visualisation_menu(df)
        elif selectedMenu == "Prédiction":
            fenetre_prediction(df)
        elif selectedMenu == "Impact des confinements":
            fenetreImpactCovid(df)
        elif selectedMenu == "À propos":
            fenetre_a_propos()
        elif selectedMenu == "Informations utiles":
            fenetre_info_utiles()
        else:
            st.error("Une erreur est survenue, merci de recharger le site.")

    def fenetre_visualisation_menu(self, df):
        """PARTIE VISUALISATION DE L'INTERFACE
        Cette fonction permet de générer une page proposant deux modes de visualisation : le fichier par défaut (Bretagne), ou le fichier de l'utilisateur
        La page visualisation (quelque soit le mode choisi) est divisée en trois grandes parties : Une partie haute, une partie basse et une centrale
        """
        # Conservation de la zone sélectionnée par l'utilisateur
        # if 'choix_de_la_zone' not in st.session_state:
        #    st.session_state['choix_de_la_zone'] = 0

        st.title("Visualisation")
        # afficher les radios buttons en horizontal
        st.markdown('<style>div.row-widget.stRadio > div{flex-direction:row;} div.row-widget.stRadio{font-weight:bold;}</style>', unsafe_allow_html=True)
        mode_fonctionnement = st.radio("Mode de fonctionnement", ('Fichier par défaut', 'Votre fichier'))

        # dicoViews: dictionnaire contenant les différents types de vues disponibles pour la cartographie
        dicoviews = Viewsdico()
        if mode_fonctionnement == 'Fichier par défaut':
            self.fenetre_visualisation_default(df, dicoviews)
        else:
            self.fenetre_visualisation_own_file(dicoviews)

        """
        Code CSS - page visualisation
        css-177yq5e.e16nr0p30 > p : permet de centrer le texte "Indices moyens sur la période entrée"
        deckgl-wrapper : permet de passer le tooltip en premier plan par rapport à la légende pour éviter un bug d'affichage
        """
        css = """ 
            <style>

            .css-177yq5e.e16nr0p30 > p {
                text-align: center;
            }
                #deckgl-wrapper{
                    z-index:1 !important;
                }                                     
            </style>
            """
        st.markdown(css, unsafe_allow_html=True)

    def fenetre_visualisation_default(self, df, dicoviews):
        """
        Cette fonction permet de charger la fenêtre de visualisation avec le fichier par défaut (chargé localement)
        # 1 - Partie Haute#
        Cette partie consiste à afficher trois sélecteurs disposés en trois colonnes. L'utilisateur doit avoir la possibilité
        de choisir la zone à visualiser, pour une certaine date et via un certain mode de vue.

        #Initialisation dictionnaires
        dico: dictionnaire contenant les noms classiques des villes (ex: Au Pays De La Roche Aux Fees)
        chemin: dictionnaire contenant les noms des villes communautraires (ex : CC Au Pays de la Roche aux Fées)
        """
        dico = villedico()
        chemin = chemindico()

        # Definition de l'espace aloué à ces trois colonnes et remplissage des colonnes
        col1, col2, col3 = st.columns([2, 1, 1])
        # Remplissage des colonnes
        with col1:
            # Permet de choisir une zone parmi celles du fichier .csv (bretagne, ou une ville en particulier)
            self.b1 = st.selectbox(label="Choisir une zone:",
                                   options=[dico['v0'], dico['v1'], dico['v2'], dico['v3'], dico['v4'], dico['v5'],
                                            dico['v6'], dico['v7'], dico['v8'], dico['v9'], dico['v10'], dico['v11'],
                                            dico['v12'], dico['v13'], dico['v14'], dico['v15'], dico['v16'],
                                            dico['v17'], dico['v18'], dico['v19'], dico['v20'], dico['v21'],
                                            dico['v22'], dico['v23'], dico['v24'], dico['v25'], dico['v26'],
                                            dico['v27'], dico['v28'], dico['v29'], dico['v30'], dico['v31'],
                                            dico['v32'], dico['v33'], dico['v34'], dico['v35'], dico['v36'],
                                            dico['v37'], dico['v38'], dico['v39'], dico['v40'], dico['v41'],
                                            dico['v42'], dico['v43'], dico['v44'], dico['v45'], dico['v46'],
                                            dico['v47'], dico['v48'], dico['v49'], dico['v50'], dico['v51'],
                                            dico['v52'], dico['v53'], dico['v54'], dico['v55'], dico['v56'],
                                            dico['v57'], dico['v58'], dico['v59'], dico['v60']], index=0)
            # Conserver le choix de l'utilisateur si on revient sur la page après
            # st.session_state['choix_de_la_zone'] = int(get_key(dico,self.b1)[1:])
        with col2:
            self.date_min, self.date_max, __, __, __ = self.get_min_max_dates(df)
            # On decale de 1 jour Car ce fichier présente toujours le jour le plus récent avec que des 0
            # Choix de la date d'observation
            self.date_max -= datetime.timedelta(days=1)
            # d = col2.date_input(label="Choisir la date", min_value=datetime.date(2019, 12, 31),
            #                    max_value=datetime.date(2022, 3, 1), value=datetime.date(2022, 3, 1))
            d = col2.date_input(label="Choisir la date", min_value=datetime.date(self.date_min.year, self.date_min.month, self.date_min.day),
                                max_value=datetime.date(self.date_max.year, self.date_max.month, self.date_max.day), value=datetime.date(self.date_max.year, self.date_max.month, self.date_max.day))
            self.year = d.year
            self.month = d.month
            self.day = d.day

        with col3:
            # Choix du mode de vue de la carte
            self.modevisual = self.choisir_vue()
            # Conserver le mode de vue choisi
            # if 'choix_mode_de_vue' not in st.session_state:
            #    st.session_state['choix_mode_de_vue'] = 0

            # st.session_state['choix_mode_de_vue']=modevisual_options.index(self.modevisual)

        # 2 - Partie Centre
        """Cette partie consiste à afficher 5 colonnes. La première (carte) permet d'afficher une cartographie de la Dataframe.
        La deuxième (legende) permet d'afficher la légende des couleurs.
        Les suivantes permettent d'afficher correctement les indices moyens calculés sur la période considérée. La colonne b_2 est vide. Elle sert à espacer b_1 et b_3
        """
        carte, legende, b_1, b_2, b_3 = st.columns([4.1, 2, 1, 0.1, 1])
        if self.b1 != dico['v0']:
            # Recupération des données de la dataframe concernées par la date choisie par l'utilisateur
            DataFrameJourActuel, liste_moyenne = self.traitement(df, dico, chemin)
            # Récupération des différents codes couleurs utilisés dans le fichier csv.
            colorsdict = GetColorsDict(df)
            # Si jamais on a récupéré une Dataframe vide, cela signifie que les données sont indisponibles. On obtient le nom de la zone, la longitude, latitude de la zone en question, et on fixe tout à 0.
            if DataFrameJourActuel.empty:
                DataFrameJourActuel = df[df.lib_zone == (chemin[get_key(dico, self.b1)])]
                DataFrameJourActuel = DataFrameJourActuel.iloc[:1]
                DataFrameJourActuel['code_qual'] = 0
                DataFrameJourActuel['code_no2'] = 0
                DataFrameJourActuel['code_so2'] = 0
                DataFrameJourActuel['code_o3'] = 0
                DataFrameJourActuel['code_pm10'] = 0
                DataFrameJourActuel['pm25'] = 0
                DataFrameJourActuel['coul_qual'] = "#DDDDDD"

            with legende:
                st.image("ressources/legende.png")

            with carte:
                DataFrameJourActuel = DataFrameJourActuel.rename(columns={"x_wgs84": "longitude", "y_wgs84": "latitude"})  # inplace pour modifier la dataframe, sinon ça en créé une nouvelle
                self.afficher_carte(dicoviews, colorsdict, DataFrameJourActuel)

            lst = ["Qualité\nAIR", "Qualité\nNO2", "Qualité\nSO2", "Qualité\nO3", "Qualité\nPM10", "Qualité\nPM2.5"]
            color = []
            index = 0
            for i in liste_moyenne:
                color.append(get_key(colorsdict, int(round(i, 0))))

            with b_1:
                with st.container():
                    fig = AfficherCercle(lst[index], str(liste_moyenne[index]), color[index])
                    b_1.pyplot(fig)
                    index += 1
                    fig = AfficherCercle(lst[index], str(liste_moyenne[index]), color[index])
                    b_1.pyplot(fig)
                    index += 1
                    fig = AfficherCercle(lst[index], str(liste_moyenne[index]), color[index])
                    b_1.pyplot(fig)
                    index += 1

            with b_3:
                with st.container():
                    fig = AfficherCercle(lst[index], str(liste_moyenne[index]), color[index])
                    b_3.pyplot(fig)
                    index += 1
                    fig = AfficherCercle(lst[index], str(liste_moyenne[index]), color[index])
                    b_3.pyplot(fig)
                    index += 1
                    fig = AfficherCercle(lst[index], str(liste_moyenne[index]), color[index])
                    b_3.pyplot(fig)

            s1, s2, s3 = st.columns([2, 4, 2])
            with s3:
                st.write("Indices moyens sur la période entrée")

            """ 
            #2 - Partie Basse
            Cette partie consiste à laisser à l'utilisateur la possibilité d'accéder à une visualisation temporelle plus large,
            déterminée par deux calendriers. L'utilisateur a la possibilité de visualiser chacun des polluants
            """
            st.subheader("Indices détaillés - "+self.b1)

            a1, a2 = st.columns(2)
            with a1:
                self.options = st.multiselect("Choix de l'indice",
                                              ["Qualité de l'air", "NO2", "SO2", 'O3', 'PM10', "PM2.5"],
                                              help="Sélectionneur contenant un/des indice(s) correspondant à la mesure de la qualité de l'air")

            with a2:
                self.a_date = st.date_input("Choisir entre deux dates ou une date",
                                            (datetime.date(self.date_min.year, self.date_min.month, self.date_min.day), datetime.date(self.date_max.year, self.date_max.month, self.date_max.day)),
                                            min_value=datetime.date(self.date_min.year, self.date_min.month, self.date_min.day), max_value=datetime.date(self.date_max.year, self.date_max.month, self.date_max.day),
                                            help='Calendrier interactif permettant de visualiser sur différentes dates les indices sélectionnés')
            taille_date = len(self.a_date)
            taille = len(self.options)
            if taille_date == 1:
                date_debut = self.a_date[0]
                date_fin = self.a_date[0]
            else:
                date_debut = self.a_date[0]
                date_fin = self.a_date[1]

            if taille != 0:
                with st.spinner('Chargement...'):
                    if self.b1 == 'Bretagne':
                        chemin_fichier = (chemin["v1"])
                    else:
                        chemin_fichier = (chemin[get_key(dico, self.b1)])

                    if "Qualité de l'air" in self.options:
                        fig = AfficherGraphe1(df, "code_qual", chemin_fichier, "Moyenne de la qualité de l'air",
                                              colorsdict, "qualité air", date_debut, date_fin)
                        st.pyplot(fig)
                    if "NO2" in self.options:
                        fig = AfficherGraphe1(df, "code_no2", chemin_fichier, "Moyenne de la qualité de NO2",
                                              colorsdict, "NO2", date_debut, date_fin)
                        st.pyplot(fig)
                    if "SO2" in self.options:
                        fig = AfficherGraphe1(df, "code_so2", chemin_fichier, "Moyenne de la qualité de SO2",
                                              colorsdict, "SO3", date_debut, date_fin)
                        st.pyplot(fig)
                    if "O3" in self.options:
                        fig = AfficherGraphe1(df, "code_o3", chemin_fichier, "Moyenne de la qualité de O3",
                                              colorsdict, "O3", date_debut, date_fin)
                        st.pyplot(fig)
                    if "PM10" in self.options:
                        fig = AfficherGraphe1(df, "code_pm10", chemin_fichier, "Moyenne de la qualité de PM10",
                                              colorsdict, "PM10", date_debut, date_fin)
                        st.pyplot(fig)

                    if "PM2.5" in self.options:
                        fig = AfficherGraphe1(df, "code_pm25", chemin_fichier, "Moyenne de la qualité de PM2.5",
                                              colorsdict, "PM2.5", date_debut, date_fin)
                        st.pyplot(fig)

            st.caption(
                    "*:Pour changer la zone des Indices détaillés veuillez changer l'option Choisir une zone en haut de la page ")

    def fenetre_visualisation_own_file(self, dicoviews):
        """
        Cette seconde fenêtre visualisation permet à l'utilisateur d'uploader son propre fichier.
        Si celui-ci présente les bons noms de colonnes et n'est pas trop lourd,
        il pourra par exemple visualiser une autre région que la Bretagne.
        """
        # Initialisation de is_df_correct qui permet de check la structure de la dataframe proposee par l'utilisateur
        is_df_correct = 0
        # Creation de trois colonnes.
        upload_file, date, view = st.columns([1, 1, 1])
        with upload_file:
            uploaded_file = st.file_uploader("🌍 Visualisez votre propre région en important votre fichier .csv", help="Votre fichier doit contenir les colonnes suivantes: [lib_qual, date_ech, code_qual, coul_qual, lib_zone, code_no2, code_so2, code_o3, code_pm10, code_no2, code_pm25, x_wgs84, y_wgs84")
            if uploaded_file is not None:
                if uploaded_file.name.endswith(".csv"):
                    try:
                        df = pd.read_csv(uploaded_file, sep=None, engine='python')
                    except UnicodeDecodeError:
                        st.write("Assurez vous de fournir un fichier .csv au délimiteur ';' ou ','")
                    # Liste des colonnes nécéssaires à l'affichage correct
                    required_liste = ['lib_qual', 'date_ech', 'code_qual', "coul_qual", "lib_zone", "code_no2", "code_so2",
                                      "code_o3", "code_pm10", "code_no2", "code_pm25", "x_wgs84", "y_wgs84"]
                    # Création d'une liste qui contient les éventuelles colonnes manquantes dans le fichier propose par l'utilisateur
                    liste_error = []
                    for elt in required_liste:
                        if elt not in df.columns:
                            liste_error.append(elt)

                    if len(liste_error) == 1:
                        st.error("Merci de charger un fichier correct")
                        st.write("Votre fichier doit présenter la colonne", liste_error)
                        is_df_correct = -1
                    elif len(liste_error) > 1:
                        st.error("Merci de charger un fichier correct")
                        st.write("Votre fichier doit présenter les colonnes", liste_error)
                        is_df_correct = -1
                    else:
                        # Si le fichier contient au moins une date, on tente de le split selon - ou / (la structure des BDD des AASQA n'est pas uniforme)
                        if df['date_ech'].nunique() > 0:
                            self.date_min, self.date_max, annee, mois, jours = self.get_min_max_dates(df)
                            # Ajout des colonnes jours, mois, annee dans notre Dataframe
                            df2 = pd.DataFrame(data={'Annee': annee, 'Mois': mois, 'Jours': jours})
                            df = pd.concat([df2, df], axis=1)

                            # Si le premier jour contient full 0 comme dans le fichier bretagne, on décale d'un jour.
                            testdf = df.loc[(df['Annee'] == self.date_max.year) & (df['Mois'] == self.date_max.month) & (df['Jours'] == self.date_max.day) & (df["code_no2"] != 0) & (df["code_so2"] != 0) & (df["code_o3"] != 0) & (df["code_pm10"] != 0) & (df["code_pm25"] != 0) & (df["code_qual"] != 0)]

                            if testdf.empty:
                                self.date_max -= datetime.timedelta(days=1)

                            is_df_correct = 1
                        else:
                            st.warning("Merci de fournir un fichier contenant au moins une date")
                else:
                    st.warning("Le chargement du fichier n'a pas fonctionné. Assurez vous de fournir un fichier .csv au délimiteur ';' ou ','")

        if is_df_correct == 1:
            with date:
                d = date.date_input(label="Choisir la date", min_value=datetime.date(self.date_min.year, self.date_min.month, self.date_min.day),
                                    max_value=datetime.date(self.date_max.year, self.date_max.month, self.date_max.day), value=datetime.date(self.date_max.year, self.date_max.month, self.date_max.day))
                self.year = d.year
                self.month = d.month
                self.day = d.day

            with view:
                self.modevisual = self.choisir_vue()

        # 2 - Partie Centre

        carte, legende, b_1, b_2, b_3 = st.columns([4.1, 2, 1, 0.1, 1])
        if is_df_correct == 1:
            longitude_mean = df["x_wgs84"].mean()
            latitude_mean = df["y_wgs84"].mean()
            DataFrameJourActuel = df.loc[(df['Annee'] == self.year) & (df['Mois'] == self.month) & (df['Jours'] == self.day)]

            liste_moyenne = traitement1(DataFrameJourActuel)

            # Mise en place d'un dico qui contient nos couleurs car on ne sait pas comment est structuré le nouveau fichier
            colorsdict = {"#DDDDDD": 0, "#50F0E6": 1, "#50CCAA": 2, "#F0E641": 3, "#FF5050": 4, "#960032": 5, "#872181": 6,
                          "#888888": 7, "#747474": "Indisponible"}

            """????Il faudrait que l'on modifie les clés des couleurs qui ont potentiellement changé dans le nouveau fichier"""

            if DataFrameJourActuel.empty:
                st.error("Nous sommes navrés, il y a eu un problème dans la requête effectuée.")
            with legende:
                st.image("ressources/legende.png")

            with carte:
                DataFrameJourActuel = DataFrameJourActuel.rename(columns={"x_wgs84": "longitude", "y_wgs84": "latitude"})  # inplace pour modifier la dataframe, sinon ça en créé une nouvelle
                taille = len(DataFrameJourActuel.index)
                # Selon le nb d'échantillons, on adapte la taille des points par pas qu'ils se superposent et que la carte soit illisible
                if taille > 35000:
                    radius = 50
                else:
                    radius =  8112.6 - 406.8 * np.log(11451*taille - 29121)
                self.afficher_carte_own_file(dicoviews, colorsdict, DataFrameJourActuel, latitude_mean, longitude_mean, radius=radius)

            lst = ["Qualité\nAIR", "Qualité\nNO2", "Qualité\nSO2", "Qualité\nO3", "Qualité\nPM10", "Qualité\nPM2.5"]
            color = []
            index = 0
            for i in liste_moyenne:
                color.append(get_key(colorsdict, int(round(i, 0))))

            with b_1:
                with st.container():
                    fig = AfficherCercle(lst[index], str(liste_moyenne[index]), color[index])
                    b_1.pyplot(fig)
                    index += 1
                    fig = AfficherCercle(lst[index], str(liste_moyenne[index]), color[index])
                    b_1.pyplot(fig)
                    index += 1
                    fig = AfficherCercle(lst[index], str(liste_moyenne[index]), color[index])
                    b_1.pyplot(fig)
                    index += 1

            with b_3:
                with st.container():
                    fig = AfficherCercle(lst[index], str(liste_moyenne[index]), color[index])
                    b_3.pyplot(fig)
                    index += 1
                    fig = AfficherCercle(lst[index], str(liste_moyenne[index]), color[index])
                    b_3.pyplot(fig)
                    index += 1
                    fig = AfficherCercle(lst[index], str(liste_moyenne[index]), color[index])
                    b_3.pyplot(fig)

            s1, s2, s3 = st.columns([2, 4, 2])
            with s3:
                st.write("Indices moyens sur la période entrée")

            """ 
            #2 - Partie Basse
            Cette partie consiste à laisser à l'utilisateur la possibilité d'accéder à une visualisation temporelle plus large,
            déterminée par deux calendriers. L'utilisateur a la possibilité de visualiser chacun des polluants
            """
            st.subheader("Indices détaillés")

            a1, a2 = st.columns(2)
            with a1:
                self.options = st.multiselect("Choix de l'indice",
                                              ["Qualité de l'air", "NO2", "SO2", 'O3', 'PM10', "PM2.5"],
                                              help="Sélectionneur contenant un/des indice(s) correspondant à la mesure de la qualité de l'air")

            with a2:
                self.a_date = st.date_input("Choisir entre deux dates ou une date",
                                            (datetime.date(self.date_min.year, self.date_min.month, self.date_min.day), datetime.date(self.date_max.year, self.date_max.month, self.date_max.day)),
                                            min_value=datetime.date(self.date_min.year, self.date_min.month, self.date_min.day), max_value=datetime.date(self.date_max.year, self.date_max.month, self.date_max.day),
                                            help='Calendrier interactif permettant de visualiser sur différentes dates les indices sélectionnés')
            taille_date = len(self.a_date)
            taille = len(self.options)
            if taille_date == 1:
                date_debut = self.a_date[0]
                date_fin = self.a_date[0]
            else:
                date_debut = self.a_date[0]
                date_fin = self.a_date[1]

            if taille != 0:
                with st.spinner('Chargement...'):
                    if "Qualité de l'air" in self.options:
                        fig = AfficherGraphe1(df, "code_qual", 'own_file', "Moyenne de la qualité de l'air",
                                              colorsdict, "qualité air", date_debut, date_fin)
                        st.pyplot(fig)
                    if "NO2" in self.options:
                        fig = AfficherGraphe1(df, "code_no2", 'own_file', "Moyenne de la qualité de NO2",
                                              colorsdict, "NO2", date_debut, date_fin)
                        st.pyplot(fig)
                    if "SO2" in self.options:
                        fig = AfficherGraphe1(df, "code_so2", 'own_file', "Moyenne de la qualité de SO2",
                                              colorsdict, "SO3", date_debut, date_fin)
                        st.pyplot(fig)
                    if "O3" in self.options:
                        fig = AfficherGraphe1(df, "code_o3", 'own_file', "Moyenne de la qualité de O3",
                                              colorsdict, "O3", date_debut, date_fin)
                        st.pyplot(fig)
                    if "PM10" in self.options:
                        fig = AfficherGraphe1(df, "code_pm10", 'own_file', "Moyenne de la qualité de PM10",
                                              colorsdict, "PM10", date_debut, date_fin)
                        st.pyplot(fig)

                    if "PM2.5" in self.options:
                        fig = AfficherGraphe1(df, "code_pm25", 'own_file', "Moyenne de la qualité de PM2.5",
                                              colorsdict, "PM2.5", date_debut, date_fin)
                        st.pyplot(fig)

            st.caption(
                    "*:Pour changer la zone des Indices détaillés veuillez changer l'option Choisir une zone en haut de la page ")

    def traitement(self, df, dico, chemin):
        # Traitement des changements#
        zone = BDD(self.b1, dico, chemin)

        if zone is not None:  # si on selectionne un fichier
            DataFrame = GetDataFrameVille(df, zone)
            self.date = ConcatenerDate(self.year, self.month, self.day, DataFrame)

            DataFrameJourActuel = DataFrame.loc[DataFrame['date_ech'] == self.date]

            # on veut afficher la moyenne de la qualite de l'air sur 1 jour
            if zone == chemin['v1']:  # si on a selectionne le fichier avec toutes les vars
                liste_moyenne = traitement1(DataFrameJourActuel)

            else:  # si on a selctionne le fichier avec une ville uniquement
                liste_moyenne = traitement2(DataFrameJourActuel)

                # afficher les moyennes mais prendre en compte un return false si ça ne marche pas

            return DataFrameJourActuel, liste_moyenne
        # gerer le else
        else:
            return False, False

    def afficher_carte(self, dicoviews, colorsdict, dataframejouractuel):
        # Fonction permettant de créer une carte dédiée à l'étude de la Bretagne avec les contours de la région)
        st.pydeck_chart(pdk.Deck(
            map_style=get_key(dicoviews, self.modevisual),
            initial_view_state=pdk.ViewState(
                latitude=48,
                longitude=-3,
                zoom=7,
                max_zoom=12,
                min_zoom=6
            ),
            layers=[

                # REGIONS
                pdk.Layer("GeoJsonLayer", data=ReadJson("areas_json/region-bretagne.geojson", 'r'),
                          filled=False, stroked=True, get_line_color=[0, 0, 0, 50], getLineWidth=1000),
                # Pour refaire les contours de la region, car sinon les couleurs sont differentes puisqu'elles sont superposees entre les departements
                pdk.Layer("GeoJsonLayer", data=ReadJson("areas_json/departement-22-cotes-d-armor.geojson", 'r'),
                          filled=False, stroked=True, get_line_color=[0, 0, 0, 50], getLineWidth=1000),
                pdk.Layer("GeoJsonLayer", data=ReadJson("areas_json/departement-56-morbihan.geojson", 'r'),
                          filled=False, stroked=True, get_line_color=[0, 0, 0, 50], getLineWidth=1000),
                pdk.Layer("GeoJsonLayer", data=ReadJson("areas_json/departement-29-finistere.geojson", 'r'),
                          filled=False, stroked=True, get_line_color=[0, 0, 0, 50], getLineWidth=1000),
                pdk.Layer("GeoJsonLayer",
                          data=ReadJson("areas_json/departement-35-ille-et-vilaine.geojson", 'r'), filled=False,
                          stroked=True, get_line_color=[0, 0, 0, 50], getLineWidth=1000),

                # POINTS
                pdkLayer(dataframejouractuel.loc[dataframejouractuel['code_qual'] == 0], 0,
                         get_key(colorsdict, "Indisponible")),
                pdkLayer(dataframejouractuel.loc[dataframejouractuel['code_qual'] == 1], 1,
                         get_key(colorsdict, 1)),
                pdkLayer(dataframejouractuel.loc[dataframejouractuel['code_qual'] == 2], 2,
                         get_key(colorsdict, 2)),
                pdkLayer(dataframejouractuel.loc[dataframejouractuel['code_qual'] == 3], 3,
                         get_key(colorsdict, 3)),
                pdkLayer(dataframejouractuel.loc[dataframejouractuel['code_qual'] == 4], 4,
                         get_key(colorsdict, 4)),
                pdkLayer(dataframejouractuel.loc[dataframejouractuel['code_qual'] == 5], 5,
                         get_key(colorsdict, 5)),
                pdkLayer(dataframejouractuel.loc[dataframejouractuel['code_qual'] == 6], 6,
                         get_key(colorsdict, 6)),
                pdkLayer(dataframejouractuel.loc[dataframejouractuel['code_qual'] == 7], 7,
                         get_key(colorsdict, 7)),
            ],
            tooltip={

                'html': '<b>Zone:</b> {lib_zone}'
                        '<br><b>Indice Qualité</b> : {lib_qual}'
                        '<br><b>Indice NO2</b> : {code_no2}'
                        '<br><b>Indice SO2</b> : {code_so2}'
                        '<br><b>Indice O3</b> : {code_o3}'
                        '<br><b>Indice PM10</b> : {code_pm10}'
                        '<br><b>Indice PM2.5</b> : {code_pm25}',

                "style": {
                    "color": "white"
                }

            }
        ))

    def afficher_carte_own_file(self, dicoviews, colorsdict, dataframejouractuel, latitude_mean, longitude_mean, radius):
        # Fonction plus générale qui n'affiche aucun contour mais qui en revanche s'adapte automatiquement à la zone concernée.
        #  la position de la vue par défaut, le radius des points selon le nombre de données pour éviter qu'ils se superposent.
        st.pydeck_chart(pdk.Deck(
            map_style=get_key(dicoviews, self.modevisual),
            initial_view_state=pdk.ViewState(
                latitude=latitude_mean,
                longitude=longitude_mean,
                zoom=6,
                max_zoom=12,
                min_zoom=4
            ),
            layers=[
                # POINTS
                pdkLayer(dataframejouractuel.loc[dataframejouractuel['code_qual'] == 0], 0,
                         get_key(colorsdict, "Indisponible"), radius),
                pdkLayer(dataframejouractuel.loc[dataframejouractuel['code_qual'] == 1], 1,
                         get_key(colorsdict, 1), radius),
                pdkLayer(dataframejouractuel.loc[dataframejouractuel['code_qual'] == 2], 2,
                         get_key(colorsdict, 2), radius),
                pdkLayer(dataframejouractuel.loc[dataframejouractuel['code_qual'] == 3], 3,
                         get_key(colorsdict, 3), radius),
                pdkLayer(dataframejouractuel.loc[dataframejouractuel['code_qual'] == 4], 4,
                         get_key(colorsdict, 4), radius),
                pdkLayer(dataframejouractuel.loc[dataframejouractuel['code_qual'] == 5], 5,
                         get_key(colorsdict, 5), radius),
                pdkLayer(dataframejouractuel.loc[dataframejouractuel['code_qual'] == 6], 6,
                         get_key(colorsdict, 6), radius),
                pdkLayer(dataframejouractuel.loc[dataframejouractuel['code_qual'] == 7], 7,
                         get_key(colorsdict, 7), radius)

            ],
            tooltip={

                'html': '<b>Zone:</b> {lib_zone}'
                        '<br><b>Indice Qualité</b> : {lib_qual}'
                        '<br><b>Indice NO2</b> : {code_no2}'
                        '<br><b>Indice SO2</b> : {code_so2}'
                        '<br><b>Indice O3</b> : {code_o3}'
                        '<br><b>Indice PM10</b> : {code_pm10}'
                        '<br><b>Indice PM2.5</b> : {code_pm25}',

                "style": {
                    "color": "white"
                }

            }
        ))

    def get_min_max_dates(self, df):
        # Fonction permettant d'obtenir la date la plus récente et la plus ancienne d'une df
        Date = df["date_ech"].str.split("-")
        # Si on a moins de trois éléments (jours, mois, année) c'est que le split n'a pas fonctionné
        if len(Date[0]) < 3:
            Date = df["date_ech"].str.split("/")
        index_cpt = 0
        year_index = 0
        month_index = 1
        jours_index = 2
        time_index = None
        # Parmi nos 3 éléments, on recupere l'index de l'année (constituee normalement de 4 chiffres)
        for elt in Date[0]:
            if len(elt) == 4:
                year_index = index_cpt
            if len(elt) > 4:
                time_index = index_cpt  # Index qui contient le temps exemple "02T01:00:00", parfois présent dans les BDD
            index_cpt += 1
        # On attribue aux mois et aux jours un index autre que celui de l annee
        if year_index == 0:
            month_index = 1
            jours_index = 2
        elif year_index == 1:
            month_index = 0
            jours_index = 2
        if year_index == 2:
            month_index = 0
            jours_index = 1

        # Creation de trois listes qui vont nous permettre de stocker les dates
        annee = []
        mois = []
        jours = []
        # S'il n'y a pas de temps, on stocke directement
        if time_index is None:
            for cpt in range(len(Date)):
                annee.append(int(Date.iloc[cpt][year_index]))
                mois.append(int(Date.iloc[cpt][month_index]))
                jours.append(int(Date.iloc[cpt][jours_index]))
        else:
            for cpt in range(len(Date)):
                # Là où il y a le temps, on ne retient que les 2 premiers chiffres pour avoir le mois/jour
                Date.iloc[cpt][time_index] = Date.iloc[cpt][time_index][0:2]

                annee.append(int(Date.iloc[cpt][year_index]))
                mois.append(int(Date.iloc[cpt][month_index]))
                jours.append(int(Date.iloc[cpt][jours_index]))

        if (len(set(mois))) > len(set(jours)):  # ce n'est pas normal (12 mois possible  +=28jours, on a inversé les listes mois et jours
            jours_copy = jours
            jours = mois
            mois = jours_copy
        # On convertit en datetime pour pouvoir facilement recuperer le min/max des dates proposees
        datetime_list = []
        for i in range(0, len(jours)):
            datetime_list.append(datetime.datetime(annee[i], mois[i], jours[i]))

        return min(datetime_list), max(datetime_list), annee, mois, jours

    def choisir_vue(self):
        modevisual_options = ['Rues', 'Plein air', 'Lumineux', 'Sombre', 'Satellite', 'Rues satellite', 'Navigation de jour', 'Navigation de nuit']
        self.modevisual = st.selectbox(label="Mode de visualisation:", options=modevisual_options, index=0)
        return self.modevisual
