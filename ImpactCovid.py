import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import calmap
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from scipy.signal import savgol_filter
from Traitements import *
import base64
def fenetreImpactCovid(dfbase):
    plt.rcParams["figure.figsize"] = (9,5)
    st.title("Étude de l'impact de la crise sanitaire")
    trait= "ressources/trait.png"
    df = pd.read_csv("BDD_fichier_csv/Bdd_complete.csv", delimiter=";", index_col="date_ech", parse_dates=True)
    # enlever les lignes avec un code_qual nul
    df = df.loc[df["code_qual"] != 0]
    df = df.drop(
        columns=["FID", "lib_qual", "lib_zone", "coul_qual", "date_dif", "source", "type_zone", "code_zone", "x_wgs84",
                 "y_wgs84", "x_reg", "y_reg", "epsg_reg", "geom"], axis=1)


    # on fait la moyenne de la df par jour
    df_mean = df["code_qual"].resample("D").agg(["mean"])

    # On arrondit et on convertit en numpy
    qualite_air = round(df_mean["mean"], 0).to_numpy()

    # date
    heatmap_series = pd.Series(data=qualite_air,
                               index=pd.date_range(start='1-1-19', end='3-25-22'))  # mois jours années


    liste_couleur = [ "#50F0E6", "#50CCAA", "#F0E641", "#FF5050"]
    daylabels = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

    cm = LinearSegmentedColormap.from_list("my_list", liste_couleur,N=4)
    fig, __ = calmap.calendarplot(data=heatmap_series, fillcolor="#dddddd", daylabels=daylabels, cmap=cm)

    fig.set_size_inches(30, 8)



    #Pour plus tard
    couleur = []
    dico_couleur = GetColorsDict(dfbase)
    for k in df["code_qual"].to_numpy():
        couleur.append(get_key(dico_couleur, k))


    texte, graphique = st.columns([2, 2])
    st.markdown("""
        <style>
        #root > div:nth-child(1) > div > div > div > div > section.main.css-1v3fvcr.egzxvld1 > div > div:nth-child(1) > div > div:nth-child(6) > div > div > div > img{
            margin-top: 3%;
            margin-bottom: 3%;
        }
        #root > div:nth-child(1) > div > div > div > div > section.main > div > div:nth-child(1) > div > div:nth-child(11) > div > div > div > img {
            width: 80% !important;
            margin-right: auto;
            margin-left: auto;
        }
        #root > div:nth-child(1) > div > div > div > div > section.main > div > div:nth-child(1) > div > div:nth-child(21) > div > div > div > img{
            width: 80% !important;
            margin-right: auto;
            margin-left: auto;
        }
        #root > div:nth-child(1) > div > div > div > div > section.main > div > div:nth-child(1) > div > div:nth-child(13) > div > div > div > img{
            width: 80% !important;
            margin-right: auto;
            margin-left: auto;
        }
        #root > div:nth-child(1) > div > div > div > div > section.main > div > div:nth-child(1) > div > div:nth-child(15) > div > div > div > img {
            width: 80% !important;
            margin-right: auto;
            margin-left: auto;
        }
        #root > div:nth-child(1) > div > div > div > div > section.main > div > div:nth-child(1) > div > div:nth-child(18) > div > div > div > img  {
            width: 80% !important;
            margin-right: auto;
            margin-left: auto;
        }
         #root > div:nth-child(1) > div > div > div > div > section.main > div > div:nth-child(1) > div > div:nth-child(28) > div > div > div > img{
            width: 80% !important;
            margin-right: auto;
            margin-left: auto;
        }
         #root > div:nth-child(1) > div > div > div > div > section.main > div > div:nth-child(1) > div > div:nth-child(30) > div > div > div > img{
            width: 80% !important;
            margin-right: auto;
            margin-left: auto;
        }
         #root > div:nth-child(1) > div > div > div > div > section.main > div > div:nth-child(1) > div > div:nth-child(32) > div > div > div > img{
            width: 80% !important;
            margin-right: auto;
            margin-left: auto;
        }  
        #root > div:nth-child(1) > div > div > div > div > section.main > div > div:nth-child(1) > div > div:nth-child(4) > div:nth-child(2) > div:nth-child(1) > div > div > div > div > div > img{
            margin-right: auto;
            margin-left: auto;
        } 
        .traitSeparation{
                            display: block;
                            margin-left: auto;
                            margin-right: auto;
                            width:100%;
                            height:1%;
        }
        </style>""", unsafe_allow_html=True)
    with texte:
        st.subheader("Calendrier de la qualité de l'air à Brest")
        st.markdown("""<h5>Date des confinements</h5>
                        <p><b>
                            <li>17 Mars au 11 Mai 2020</li>
                            <li>30 Octobre au 15 Décembre 2020</li>
                            <li>3 Avril au 3 Mai 2021</li>
                        </b></p>""", unsafe_allow_html=True)


    with graphique:
        st.pyplot(fig)

    st.image("ressources/legendeverticale.png")
    st.markdown(f"""<img class="traitSeparation" src="data:image/png;base64,{base64.b64encode(open(trait, "rb").read()).decode()}" alt=traitSeparation> """, unsafe_allow_html=True)

    #####################################Options sidebar
    st.sidebar.markdown("<h2 style='text-align: center;'>Options Générales</h2>", unsafe_allow_html=True)

    genre= st.sidebar.radio("TYPE D'AFFICHAGE",("Choix d'un intervalle",'Comparer les années'))

    if(genre=="Choix d'un intervalle"):
        date = st.sidebar.date_input("Choisir entre deux dates",
                                                (datetime.date(2020, 1, 1), datetime.date(2021, 12, 31)),
                                                min_value=datetime.date(2019, 1, 1), max_value=datetime.date(2022, 3, 1),
                                                help='Calendrier interactif permettant de visualiser sur différentes dates les indices sélectionnés')
        taille_date = len(date)
        if(taille_date<2):
            st.sidebar.warning("Choisir entre deux dates")
            return
        nmb_jour=(date[1]-date[0]).days
        if(nmb_jour<2):
            st.sidebar.warning("Augmenter la période")
            return
    else:
        annee2019 = st.sidebar.checkbox('Année 2019',value=True)
        annee2020 = st.sidebar.checkbox('Année 2020',value=True)
        annee2021 = st.sidebar.checkbox('Année 2021',value=True)
        nmb_jour=31

    if(genre=="Choix d'un intervalle"):
        type_moyenne = st.sidebar.radio(
                    "Type de Moyenne",
                    ('Moyenne mobile', 'Lissage Savitzky-Golay','Pas de moyenne'))
    else:
        type_moyenne = st.sidebar.radio(
                    "Type de Moyenne",
                    ('Moyenne mobile','Pas de moyenne'))
    erreur=0
    if(type_moyenne=="Moyenne mobile"):
        if(nmb_jour>30):
            jour_mobile = st.sidebar.slider('Choisir le nombre de jours pour la moyenne mobile', 1, 30, 14)
        else:
            jour_mobile = st.sidebar.slider('Choisir le nombre de jours pour la moyenne mobile', 1, nmb_jour, int(nmb_jour/2))
    elif(type_moyenne=="Lissage Savitzky-Golay"):
        if(nmb_jour<3):
            erreur=1
        else:
            if(nmb_jour>=20):
                window_length = st.sidebar.slider('Choisir la taille du filtre de la fenêtre', min_value=1, max_value=20, value=10,step=1)
                polyorder=st.sidebar.slider("Choisir l'ordre du polynome", min_value=1, max_value=15, value=3,step=1)
            else:
                window_length = st.sidebar.slider('Choisir la taille du filtre de la fenêtre', min_value=1, max_value=nmb_jour, value=int(nmb_jour/2),step=1)
                polyorder=st.sidebar.slider("Choisir l'ordre du polynome", min_value=1, max_value=nmb_jour-1, value=1,step=1)
            if(polyorder>=window_length):
                st.sidebar.warning("La taille du filtre de la fenêtre doit être plus grand que l'ordre du polynome")
                return
    if(erreur==1):
        st.sidebar.warning("Augmenter la période")
        return

    st.sidebar.markdown("<h2 style='text-align: center;'>Options Concentrations</h2>", unsafe_allow_html=True)
    type_moyenne_jour = st.sidebar.radio(
                "Type d'affichage",
                ('Moyenne par jour', 'Maximum par jour',"Minimum par jour","Pas de moyenne"))

    if(genre=="Choix d'un intervalle"):
        Semaine = st.sidebar.checkbox('Enlever le samedi et dimanche',value=False)
    else:
        Semaine=False



    if(genre=="Choix d'un intervalle"):
        st.sidebar.markdown("<h2 style='text-align: center;'>Option Concentration PM10</h2>", unsafe_allow_html=True)
        ville_pm10 = st.sidebar.selectbox(
                    "Selection de la ville",
                    ("Toutes","Vannes UTA","Saint Malo Rocabey","Brest Desmoulins","Saint Brieuc Balzac","Brest Mace","Lorient B. Bissonnet","Merleac Kergoff","Rennes Pays-Bas","Rennes Laennec","Quimper Pommiers"))

        st.sidebar.markdown("<h2 style='text-align: center;'>Option Concentration PM2.5</h2>", unsafe_allow_html=True)
        ville_pm25 = st.sidebar.selectbox(
                    "Selection de la ville",
                    ("Toutes","Brest Mace","Vannes UTA","Rennes Laennec","Rennes Pays-Bas","Lorient B. Bissonnet","Saint Brieuc Balzac","Merleac Kergoff","Saint Malo Rocabey"))

        st.sidebar.markdown("<h2 style='text-align: center;'>Option Concentration NO2</h2>", unsafe_allow_html=True)
        ville_no2 = st.sidebar.selectbox(
                    "Selection de la ville",
                    ("Toutes","Vannes UTA","Saint Malo Rocabey","Rennes St-Yves","Brest Desmoulins","Saint Brieuc Balzac","Brest Mace","Rennes Halles","Lorient B. Bissonnet","Merleac Kergoff","Lorient Normandie"))

        st.sidebar.markdown("<h2 style='text-align: center;'>Option Concentration O3</h2>", unsafe_allow_html=True)
        ville_o3 = st.sidebar.selectbox(
                    "Selection de la ville",
                    ("Toutes","Brest IMT","Saint Malo Rocabey","Vannes UTA","Brest Mace","Quimper Zola","Rennes St-Yves","Lorient B. Bissonnet","Merleac Kergoff","Saint Brieuc Balzac"))
    else:
        st.sidebar.markdown("<h2 style='text-align: center;'>Option Concentration PM10</h2>", unsafe_allow_html=True)
        ville_pm10 = st.sidebar.selectbox(
                    "Selection de la ville",
                    ("Urbain","Rural","Trafic","Vannes UTA","Saint Malo Rocabey","Brest Desmoulins","Saint Brieuc Balzac","Brest Mace","Lorient B. Bissonnet","Merleac Kergoff","Rennes Pays-Bas","Rennes Laennec","Quimper Pommiers"))

        st.sidebar.markdown("<h2 style='text-align: center;'>Option Concentration PM2.5</h2>", unsafe_allow_html=True)
        ville_pm25 = st.sidebar.selectbox(
                    "Selection de la ville",
                    ("Urbain","Rural","Trafic","Brest Mace","Vannes UTA","Rennes Laennec","Rennes Pays-Bas","Lorient B. Bissonnet","Saint Brieuc Balzac","Merleac Kergoff","Saint Malo Rocabey"))

        st.sidebar.markdown("<h2 style='text-align: center;'>Option Concentration NO2</h2>", unsafe_allow_html=True)
        ville_no2 = st.sidebar.selectbox(
                    "Selection de la ville",
                    ("Urbain","Rural","Trafic","Vannes UTA","Saint Malo Rocabey","Rennes St-Yves","Brest Desmoulins","Saint Brieuc Balzac","Brest Mace","Rennes Halles","Lorient B. Bissonnet","Merleac Kergoff","Lorient Normandie"))





    ####################################################################################################################
    st.markdown("<h2 style='text-align: center;'>Concentrations des polluants</h2>", unsafe_allow_html=True)
    c_1,c_2,c_3=st.columns(3)
    with c_2:
        if(genre=="Choix d'un intervalle"):
            option_polluant=st.multiselect("Choix de l'indice",
                           ["PM10","PM2.5",'NO2',"O3"],
                                   ["PM10"],
                           help="Sélectionneur contenant un/des indice(s) correspondant à des polluants dans l'air")
        else:
            option_polluant=st.multiselect("Choix de l'indice",
                           ["PM10","PM2.5",'NO2'],
                                   ["PM10"],
                           help="Sélectionneur contenant un/des indice(s) correspondant à des polluants dans l'air")


    if("PM10" in option_polluant):
        st.markdown("<h2 style='text-align: center;'>Moyenne de la concentration du PM10</h2>", unsafe_allow_html=True)
        df_pm10 = pd.read_csv("BDD_fichier_csv/mes_bretagne_horaire_pm10.csv", delimiter=";", index_col="date_fin", parse_dates=True,dayfirst=True)

        #On garde sur la ville ou pas
        if((ville_pm10!="Toutes")&(ville_pm10!="Urbain")&(ville_pm10!="Rural")&(ville_pm10!="Trafic")):
            df_pm10=df_pm10.loc[df_pm10["nom_station"]==ville_pm10]

        #On drop les lignes inutiles
        df_pm10 = df_pm10.drop(columns=["nom_dept","nom_com","nom_station","nom_poll","unite","date_debut"], axis=1)
        # enlever les lignes non valides
        df_pm10 = df_pm10.loc[df_pm10["statut_valid"] != 0]


        #On garde la df sur la date
        if(genre=="Choix d'un intervalle"):
            df_pm10=df_pm10[str(date[0].year)+"-"+str(date[0].month)+"-"+str(date[0].day):str(date[1].year)+"-"+str(date[1].month)+"-"+str(date[1].day)]
        else:
            if ((annee2019 == True) & (annee2020 == True) & (annee2021 == True)):
                df_pm10 = df_pm10["2019-01-01":"2021-12-31"]
            elif ((annee2019 == True) & (annee2020 == True) & (annee2021 == False)):
                df_pm10 = df_pm10["2019-01-01":"2020-12-31"]
            elif ((annee2019 == False) & (annee2020 == True) & (annee2021 == True)):
                df_pm10 = df_pm10["2020-01-01":"2021-12-31"]
            elif ((annee2019 == True) & (annee2020 == False) & (annee2021 == True)):
                df_pm10 = pd.concat([df_pm10["2019"], df_pm10["2021"]])
            elif ((annee2019 == True) & (annee2020 == False) & (annee2021 == False)):
                df_pm10 = df_pm10["2019"]
            elif ((annee2019 == False) & (annee2020 == True) & (annee2021 == False)):
                df_pm10 = df_pm10["2020"]
            elif((annee2019 == False) & (annee2020 == False) & (annee2021 == True)):
                df_pm10 = df_pm10["2021"]

        #On enleve Samedi et Dimanche
        if(Semaine):
            #1)Ajouter une colonne pour le jour de la semaine
            df_pm10["day_week"]=df_pm10.index.day_name()
            #2)on enleve samedi et dimanche
            df_pm10=df_pm10.loc[(df_pm10["day_week"]!="Sunday") & (df_pm10["day_week"]!="Saturday")]


        # on fait la moyenne de la df par Jour
        if(type_moyenne_jour=="Moyenne par jour"):
            string="mean"
        # on prend le max de la df par Jour
        elif(type_moyenne_jour=='Maximum par jour'):
            string="max"
        # on prend le min de la df par Jour
        elif(type_moyenne_jour=='Minimum par jour'):
            string="min"
        else:
            string="valeur"

        if((ville_pm10=="Toutes")|(ville_pm10=="Urbain")|(ville_pm10=="Rural")|(ville_pm10=="Trafic")):
            #Moyenne par typologie
            df_urbain=df_pm10.loc[(df_pm10["typologie"]=="urbaine")&(df_pm10["influence"]!="trafic")]
            df_rural=df_pm10.loc[(df_pm10["typologie"]=="rurale")&(df_pm10["influence"]!="trafic")]
            df_trafic=df_pm10.loc[df_pm10["influence"]=="trafic"]


            if(string!="valeur"):
                #Regrouper les valeurs par jour soit avec la moyenne, soit on prend le min, soit on prend le max
                df_mean_urbain = df_urbain["valeur"].resample("D").agg([string])
                df_mean_rural = df_rural["valeur"].resample("D").agg([string])
                df_mean_trafic = df_trafic["valeur"].resample("D").agg([string])
            else:
                df_mean_urbain = df_urbain
                df_mean_rural = df_rural
                df_mean_trafic = df_trafic

            #On drop les NaN
            df_mean_urbain=df_mean_urbain.dropna()
            df_mean_rural=df_mean_rural.dropna()
            df_mean_trafic=df_mean_trafic.dropna()
        else:
            if(string!="valeur"):
                #Regrouper les valeurs par jour soit avec la moyenne, soit on prend le min, soit on prend le max
                DF_mean=df_pm10["valeur"].resample("D").agg([string])
            else:
                DF_mean=df_pm10
            #On drop les NaN
            DF_mean=DF_mean.dropna()

        #Graphe
        if(genre=="Choix d'un intervalle"):
            fig, ax = plt.subplots()
            if(type_moyenne=="Lissage Savitzky-Golay"):
                if(ville_pm10=="Toutes"):
                    plt.plot(df_mean_urbain.index,savgol_filter(df_mean_urbain[string].values,window_length,polyorder),marker='o',label="Urbain")
                    plt.plot(df_mean_rural.index,savgol_filter(df_mean_rural[string].values,window_length,polyorder),marker='o',label="Rural")
                    plt.plot(df_mean_trafic.index,savgol_filter(df_mean_trafic[string].values,window_length,polyorder),marker='o',label="Trafic")
                else:
                    plt.plot(DF_mean.index,savgol_filter(DF_mean[string].values,window_length,polyorder),marker='o',label=ville_pm10)
            elif(type_moyenne=="Moyenne mobile"):
                if(ville_pm10=="Toutes"):
                    df_mean_urbain[string].rolling(window=jour_mobile,center=True).mean().plot(marker='o',label="Urbain") #moving average
                    df_mean_rural[string].rolling(window=jour_mobile,center=True).mean().plot(marker='o',label="Rural") #moving average
                    df_mean_trafic[string].rolling(window=jour_mobile,center=True).mean().plot(marker='o',label="Trafic") #moving average
                else:
                    DF_mean[string].rolling(window=jour_mobile,center=True).mean().plot(marker='o',label=ville_pm10) #moving average
            else:
                if(ville_pm10=="Toutes"):
                    df_mean_urbain[string].plot(marker='o',label="Urbain") #moving average
                    df_mean_rural[string].plot(marker='o',label="Rural") #moving average
                    df_mean_trafic[string].plot(marker='o',label="Trafic") #moving average
                else:
                    DF_mean[string].plot(marker='o',label=ville_pm10) #moving average


            __, axYmax = ax.get_ylim()
            if((pd.to_datetime(20200317,format='%Y%m%d')>=date[0])&(pd.to_datetime(20200317,format='%Y%m%d')<=date[1])):
                plt.axvline(x=pd.to_datetime(20200317,format='%Y%m%d'),lw=1, ls='--', alpha=1, color='#000000')
                plt.text(pd.to_datetime(20200317,format='%Y%m%d'),axYmax-2, "Confinement", fontsize=13)
            if((pd.to_datetime(20200511,format='%Y%m%d')>=date[0])&(pd.to_datetime(20200511,format='%Y%m%d')<=date[1])):
                plt.axvline(x=pd.to_datetime(20200511,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')
            if((pd.to_datetime(20201030,format='%Y%m%d')>=date[0])&(pd.to_datetime(20201030,format='%Y%m%d')<=date[1])):
                plt.axvline(x=pd.to_datetime(20201030,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')
                plt.text(pd.to_datetime(20201030,format='%Y%m%d'),axYmax-2, "Confinement", fontsize=13)
            if((pd.to_datetime(20201215,format='%Y%m%d')>=date[0])&(pd.to_datetime(20201215,format='%Y%m%d')<=date[1])):
                plt.axvline(x=pd.to_datetime(20201215,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')
            if((pd.to_datetime(20210403,format='%Y%m%d')>=date[0])&(pd.to_datetime(20210403,format='%Y%m%d')<=date[1])):
                plt.axvline(x=pd.to_datetime(20210403,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')
                plt.text(pd.to_datetime(20210403,format='%Y%m%d'),axYmax-2, "Confinement", fontsize=13)
            if((pd.to_datetime(20210503,format='%Y%m%d')>=date[0])&(pd.to_datetime(20210503,format='%Y%m%d')<=date[1])):
                plt.axvline(x=pd.to_datetime(20210503,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')

            plt.grid(True,axis="y")
            fig.set_figwidth(18)
            fig.set_figheight(10)
            plt.legend(fontsize=12,loc="upper right")
            plt.ylabel("Concentration en PM10 (μg/m3)",fontsize=16)
            plt.xlabel("Date",fontsize=16)
            st.pyplot(fig)
        else:
            if(type_moyenne=="Moyenne mobile"):
                if((ville_pm10=="Urbain")):
                    if(df_mean_urbain.empty==False):
                        df_mean_urbain=df_mean_urbain[string].to_frame()
                        df_mean_urbain['doy'] = df_mean_urbain.index.dayofyear  # day of the year
                        df_mean_urbain['Year'] = df_mean_urbain.index.year
                        df_mean_urbain = pd.pivot_table(df_mean_urbain, index=['doy'], columns=['Year'], values=[string])
                        df_mean_urbain.rolling(window=jour_mobile,center=True).mean().plot() #moving average

                elif(ville_pm10=="Rural"):
                    if(df_mean_rural.empty==False):
                        df_mean_rural=df_mean_rural[string].to_frame()
                        df_mean_rural['doy'] = df_mean_rural.index.dayofyear  # day of the year
                        df_mean_rural['Year'] = df_mean_rural.index.year
                        df_mean_rural = pd.pivot_table(df_mean_rural, index=['doy'], columns=['Year'], values=[string])
                        df_mean_rural.rolling(window=jour_mobile,center=True).mean().plot() #moving average

                elif(ville_pm10=="Trafic"):
                    if(df_mean_trafic.empty==False):
                        df_mean_trafic=df_mean_trafic[string].to_frame()
                        df_mean_trafic['doy'] = df_mean_trafic.index.dayofyear  # day of the year
                        df_mean_trafic['Year'] = df_mean_trafic.index.year
                        df_mean_trafic = pd.pivot_table(df_mean_trafic, index=['doy'], columns=['Year'], values=[string])
                        df_mean_trafic.rolling(window=jour_mobile,center=True).mean().plot() #moving average
                elif(DF_mean.empty==False):
                    DF_mean=DF_mean[string].to_frame()
                    DF_mean['doy'] = DF_mean.index.dayofyear  # day of the year
                    DF_mean['Year'] = DF_mean.index.year
                    DF_mean = pd.pivot_table(DF_mean, index=['doy'], columns=['Year'], values=[string])
                    DF_mean[string].rolling(window=jour_mobile,center=True).mean().plot() #moving average
            else:#pas de moyenne
                if(ville_pm10=="Urbain"):
                    if(df_mean_urbain.empty==False):
                        df_mean_urbain=df_mean_urbain[string].to_frame()
                        df_mean_urbain['doy'] = df_mean_urbain.index.dayofyear  # day of the year
                        df_mean_urbain['Year'] = df_mean_urbain.index.year
                        df_mean_urbain = pd.pivot_table(df_mean_urbain, index=['doy'], columns=['Year'], values=[string])
                        df_mean_urbain.plot() #moving average

                elif(ville_pm10=="Rural"):
                    if(df_mean_rural.empty==False):
                        df_mean_rural=df_mean_rural[string].to_frame()
                        df_mean_rural['doy'] = df_mean_rural.index.dayofyear  # day of the year
                        df_mean_rural['Year'] = df_mean_rural.index.year
                        df_mean_rural = pd.pivot_table(df_mean_rural, index=['doy'], columns=['Year'], values=[string])
                        df_mean_rural.plot() #moving average

                elif(ville_pm10=="Trafic"):
                    if(df_mean_trafic.empty==False):
                        df_mean_trafic=df_mean_trafic[string].to_frame()
                        df_mean_trafic['doy'] = df_mean_trafic.index.dayofyear  # day of the year
                        df_mean_trafic['Year'] = df_mean_trafic.index.year
                        df_mean_trafic = pd.pivot_table(df_mean_trafic, index=['doy'], columns=['Year'], values=[string])
                        df_mean_trafic.plot() #moving average

                elif(DF_mean.empty==False):
                    DF_mean=DF_mean[string].to_frame()
                    DF_mean['doy'] = DF_mean.index.dayofyear  # day of the year
                    DF_mean['Year'] = DF_mean.index.year
                    DF_mean = pd.pivot_table(DF_mean, index=['doy'], columns=['Year'], values=[string])
                    DF_mean[string].plot() #moving average


            # on recup les coordonnees min et max du plt en y (on a besoin du max pour ecrire confinement)
            __, top = plt.ylim()
            plt.axvline(x=76,lw=1, ls='--', alpha=1, color='#000000')
            plt.text(76,top-2, "Confinement 1", fontsize=8)
            plt.axvline(x=131, lw=1, ls='--', alpha=1, color='#000000')

            plt.axvline(x=303, lw=1, ls='--', alpha=1, color='#000000')
            plt.text(303,top-2, "Confinement 2", fontsize=8)
            plt.axvline(x=349, lw=1, ls='--', alpha=1, color='#000000')

            if(annee2021==True):
                plt.axvline(x=93, lw=1, ls='--', alpha=1, color='#717171')
                plt.text(93,top-4, "Confinement 3", fontsize=8,color='#717171')
                plt.axvline(x=123, lw=1, ls='--', alpha=1, color='#717171')


            plt.legend(fontsize=9,loc="lower left")
            plt.ylabel("Concentration en (μg/m3)",fontsize=16)
            plt.xlabel("Jour de l'année",fontsize=16)
            plt.grid(True,axis="y")
            st.pyplot(fig=plt)




    if("PM2.5" in option_polluant):
        st.markdown("<h2 style='text-align: center;'>Moyenne de la concentration du PM2.5</h2>", unsafe_allow_html=True)
        df_pm25 = pd.read_csv("BDD_fichier_csv/mes_bretagne_horaire_pm25.csv", delimiter=";", index_col="date_fin", parse_dates=True,dayfirst=True)

        #On garde sur la ville ou pas
        if((ville_pm25!="Toutes")&(ville_pm25!="Urbain")&(ville_pm25!="Rural")&(ville_pm25!="Trafic")):
            df_pm25=df_pm25.loc[df_pm25["nom_station"]==ville_pm25]

        #On drop les lignes inutiles
        df_pm25 = df_pm25.drop(columns=["nom_dept","nom_com","nom_station","nom_poll","unite","date_debut"], axis=1)
        # enlever les lignes non valides
        df_pm25 = df_pm25.loc[df_pm25["statut_valid"] != 0]


        #On garde la df sur la date
        if(genre=="Choix d'un intervalle"):
            df_pm25=df_pm25[str(date[0].year)+"-"+str(date[0].month)+"-"+str(date[0].day):str(date[1].year)+"-"+str(date[1].month)+"-"+str(date[1].day)]
        else:
            if((annee2019==True)&(annee2020==True)&(annee2021==True)):
                df_pm25 = df_pm25["2019-01-01":"2021-12-31"]
            elif ((annee2019 == True) & (annee2020 == True) & (annee2021 == False)):
                df_pm25 = df_pm25["2019-01-01":"2020-12-31"]
            elif ((annee2019 == False) & (annee2020 == True) & (annee2021 == True)):
                df_pm25 = df_pm25["2020-01-01":"2021-12-31"]
            elif ((annee2019 == True) & (annee2020 == False) & (annee2021 == True)):
                df_pm25 = pd.concat([df_pm25["2019"], df_pm25["2021"]])
            elif ((annee2019 == True) & (annee2020 == False) & (annee2021 == False)):
                df_pm25 = df_pm25["2019"]
            elif ((annee2019 == False) & (annee2020 == True) & (annee2021 == False)):
                df_pm25 = df_pm25["2020"]
            elif((annee2019 == False) & (annee2020 == False) & (annee2021 == True)):
                df_pm25 = df_pm25["2021"]

        #On enleve Samedi et Dimanche
        if(Semaine):
            #1)Ajouter une colonne pour le jour de la semaine
            df_pm25["day_week"]=df_pm25.index.day_name()
            #2)on enleve samedi et dimanche
            df_pm25=df_pm25.loc[(df_pm25["day_week"]!="Sunday") & (df_pm25["day_week"]!="Saturday")]


        # on fait la moyenne de la df par Jour
        if(type_moyenne_jour=="Moyenne par jour"):
            string="mean"
        # on prend le max de la df par Jour
        elif(type_moyenne_jour=='Maximum par jour'):
            string="max"
        # on prend le min de la df par Jour
        elif(type_moyenne_jour=='Minimum par jour'):
            string="min"
        else:
            string="valeur"

        if((ville_pm25=="Toutes")|(ville_pm25=="Urbain")|(ville_pm25=="Rural")|(ville_pm25=="Trafic")):
            #Moyenne par typologie
            df_urbain=df_pm25.loc[(df_pm25["typologie"]=="urbaine")&(df_pm25["influence"]!="trafic")]
            df_rural=df_pm25.loc[(df_pm25["typologie"]=="rurale")&(df_pm25["influence"]!="trafic")]
            df_trafic= df_pm25.loc[df_pm25["influence"]=="trafic"]


            if(string!="valeur"):
                #Regrouper les valeurs par jour soit avec la moyenne, soit on prend le min, soit on prend le max
                df_mean_urbain = df_urbain["valeur"].resample("D").agg([string])
                df_mean_rural = df_rural["valeur"].resample("D").agg([string])
                df_mean_trafic = df_trafic["valeur"].resample("D").agg([string])
            else:
                df_mean_urbain = df_urbain
                df_mean_rural = df_rural
                df_mean_trafic = df_trafic

            #On drop les NaN
            df_mean_urbain=df_mean_urbain.dropna()
            df_mean_rural=df_mean_rural.dropna()
            df_mean_trafic=df_mean_trafic.dropna()
        else:
            if(string!="valeur"):
                #Regrouper les valeurs par jour soit avec la moyenne, soit on prend le min, soit on prend le max
                DF_mean=df_pm25["valeur"].resample("D").agg([string])
            else:
                DF_mean=df_pm25
            #On drop les NaN
            DF_mean=DF_mean.dropna()

        #Graphe
        if(genre=="Choix d'un intervalle"):
            fig, ax = plt.subplots()
            if(type_moyenne=="Lissage Savitzky-Golay"):
                if(ville_pm25=="Toutes"):
                    plt.plot(df_mean_urbain.index,savgol_filter(df_mean_urbain[string].values,window_length,polyorder),marker='o',label="Urbain")
                    plt.plot(df_mean_rural.index,savgol_filter(df_mean_rural[string].values,window_length,polyorder),marker='o',label="Rural")
                    plt.plot(df_mean_trafic.index,savgol_filter(df_mean_trafic[string].values,window_length,polyorder),marker='o',label="Trafic")
                else:
                    plt.plot(DF_mean.index,savgol_filter(DF_mean[string].values,window_length,polyorder),marker='o',label=ville_pm25)
            elif(type_moyenne=="Moyenne mobile"):
                if(ville_pm25=="Toutes"):
                    df_mean_urbain[string].rolling(window=jour_mobile,center=True).mean().plot(marker='o',label="Urbain") #moving average
                    df_mean_rural[string].rolling(window=jour_mobile,center=True).mean().plot(marker='o',label="Rural") #moving average
                    df_mean_trafic[string].rolling(window=jour_mobile,center=True).mean().plot(marker='o',label="Trafic") #moving average
                else:
                    DF_mean[string].rolling(window=jour_mobile,center=True).mean().plot(marker='o',label=ville_pm25) #moving average
            else:
                if(ville_pm25=="Toutes"):
                    df_mean_urbain[string].plot(marker='o',label="Urbain") #moving average
                    df_mean_rural[string].plot(marker='o',label="Rural") #moving average
                    df_mean_trafic[string].plot(marker='o',label="Trafic") #moving average
                else:
                    DF_mean[string].plot(marker='o',label=ville_pm25) #moving average


            __, axYmax = ax.get_ylim()
            if((pd.to_datetime(20200317,format='%Y%m%d')>=date[0])&(pd.to_datetime(20200317,format='%Y%m%d')<=date[1])):
                plt.axvline(x=pd.to_datetime(20200317,format='%Y%m%d'),lw=1, ls='--', alpha=1, color='#000000')
                plt.text(pd.to_datetime(20200317,format='%Y%m%d'),axYmax-2, "Confinement", fontsize=13)
            if((pd.to_datetime(20200511,format='%Y%m%d')>=date[0])&(pd.to_datetime(20200511,format='%Y%m%d')<=date[1])):
                plt.axvline(x=pd.to_datetime(20200511,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')
            if((pd.to_datetime(20201030,format='%Y%m%d')>=date[0])&(pd.to_datetime(20201030,format='%Y%m%d')<=date[1])):
                plt.axvline(x=pd.to_datetime(20201030,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')
                plt.text(pd.to_datetime(20201030,format='%Y%m%d'),axYmax-2, "Confinement", fontsize=13)
            if((pd.to_datetime(20201215,format='%Y%m%d')>=date[0])&(pd.to_datetime(20201215,format='%Y%m%d')<=date[1])):
                plt.axvline(x=pd.to_datetime(20201215,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')
            if((pd.to_datetime(20210403,format='%Y%m%d')>=date[0])&(pd.to_datetime(20210403,format='%Y%m%d')<=date[1])):
                plt.axvline(x=pd.to_datetime(20210403,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')
                plt.text(pd.to_datetime(20210403,format='%Y%m%d'),axYmax-2, "Confinement", fontsize=13)
            if((pd.to_datetime(20210503,format='%Y%m%d')>=date[0])&(pd.to_datetime(20210503,format='%Y%m%d')<=date[1])):
                plt.axvline(x=pd.to_datetime(20210503,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')

            plt.grid(True,axis="y")
            fig.set_figwidth(18)
            fig.set_figheight(10)
            plt.legend(fontsize=12,loc="upper right")
            plt.ylabel("Concentration en PM2.5 (μg/m3)",fontsize=16)
            plt.xlabel("Date",fontsize=16)
            st.pyplot(fig)
        else:
            if(type_moyenne=="Moyenne mobile"):
                if((ville_pm25=="Urbain")):
                    if(df_mean_urbain.empty==False):
                        df_mean_urbain=df_mean_urbain[string].to_frame()
                        df_mean_urbain['doy'] = df_mean_urbain.index.dayofyear  # day of the year
                        df_mean_urbain['Year'] = df_mean_urbain.index.year
                        df_mean_urbain = pd.pivot_table(df_mean_urbain, index=['doy'], columns=['Year'], values=[string])
                        df_mean_urbain.rolling(window=jour_mobile,center=True).mean().plot() #moving average

                elif(ville_pm25=="Rural"):
                    if(df_mean_rural.empty==False):
                        df_mean_rural=df_mean_rural[string].to_frame()
                        df_mean_rural['doy'] = df_mean_rural.index.dayofyear  # day of the year
                        df_mean_rural['Year'] = df_mean_rural.index.year
                        df_mean_rural = pd.pivot_table(df_mean_rural, index=['doy'], columns=['Year'], values=[string])
                        df_mean_rural.rolling(window=jour_mobile,center=True).mean().plot() #moving average

                elif(ville_pm25=="Trafic"):
                    if(df_mean_trafic.empty==False):
                        df_mean_trafic=df_mean_trafic[string].to_frame()
                        df_mean_trafic['doy'] = df_mean_trafic.index.dayofyear  # day of the year
                        df_mean_trafic['Year'] = df_mean_trafic.index.year
                        df_mean_trafic = pd.pivot_table(df_mean_trafic, index=['doy'], columns=['Year'], values=[string])
                        df_mean_trafic.rolling(window=jour_mobile,center=True).mean().plot() #moving average
                elif(DF_mean.empty==False):
                    DF_mean=DF_mean[string].to_frame()
                    DF_mean['doy'] = DF_mean.index.dayofyear  # day of the year
                    DF_mean['Year'] = DF_mean.index.year
                    DF_mean = pd.pivot_table(DF_mean, index=['doy'], columns=['Year'], values=[string])
                    DF_mean[string].rolling(window=jour_mobile,center=True).mean().plot() #moving average
            else:#pas de moyenne
                if(ville_pm25=="Urbain"):
                    if(df_mean_urbain.empty==False):
                        df_mean_urbain=df_mean_urbain[string].to_frame()
                        df_mean_urbain['doy'] = df_mean_urbain.index.dayofyear  # day of the year
                        df_mean_urbain['Year'] = df_mean_urbain.index.year
                        df_mean_urbain = pd.pivot_table(df_mean_urbain, index=['doy'], columns=['Year'], values=[string])
                        df_mean_urbain.plot() #moving average

                elif(ville_pm25=="Rural"):
                    if(df_mean_rural.empty==False):
                        df_mean_rural=df_mean_rural[string].to_frame()
                        df_mean_rural['doy'] = df_mean_rural.index.dayofyear  # day of the year
                        df_mean_rural['Year'] = df_mean_rural.index.year
                        df_mean_rural = pd.pivot_table(df_mean_rural, index=['doy'], columns=['Year'], values=[string])
                        df_mean_rural.plot() #moving average

                elif(ville_pm25=="Trafic"):
                    if(df_mean_trafic.empty==False):
                        df_mean_trafic=df_mean_trafic[string].to_frame()
                        df_mean_trafic['doy'] = df_mean_trafic.index.dayofyear  # day of the year
                        df_mean_trafic['Year'] = df_mean_trafic.index.year
                        df_mean_trafic = pd.pivot_table(df_mean_trafic, index=['doy'], columns=['Year'], values=[string])
                        df_mean_trafic.plot() #moving average

                elif(DF_mean.empty==False):
                    DF_mean=DF_mean[string].to_frame()
                    DF_mean['doy'] = DF_mean.index.dayofyear  # day of the year
                    DF_mean['Year'] = DF_mean.index.year
                    DF_mean = pd.pivot_table(DF_mean, index=['doy'], columns=['Year'], values=[string])
                    DF_mean[string].plot() #moving average

            __, top = plt.ylim()
            plt.axvline(x=76,lw=1, ls='--', alpha=1, color='#000000')
            plt.text(76,top-2, "Confinement 1", fontsize=8)
            plt.axvline(x=131, lw=1, ls='--', alpha=1, color='#000000')

            plt.axvline(x=303, lw=1, ls='--', alpha=1, color='#000000')
            plt.text(303,top-2, "Confinement 2", fontsize=8)
            plt.axvline(x=349, lw=1, ls='--', alpha=1, color='#000000')

            if(annee2021==True):
                plt.axvline(x=93, lw=1, ls='--', alpha=1, color='#717171')
                plt.text(93,top-4, "Confinement 3", fontsize=8,color='#717171')
                plt.axvline(x=123, lw=1, ls='--', alpha=1, color='#717171')

            plt.legend(fontsize=9,loc="lower left")
            plt.ylabel("Concentration en (μg/m3)",fontsize=16)
            plt.xlabel("Jour de l'année",fontsize=16)
            plt.grid(True,axis="y")
            st.pyplot(fig=plt)




    if("NO2" in option_polluant):
        st.markdown("<h2 style='text-align: center;'>Moyenne de la concentration du NO2</h2>", unsafe_allow_html=True)
        df_no2 = pd.read_csv("BDD_fichier_csv/mes_bretagne_horaire_no2.csv", delimiter=";", index_col="date_fin", parse_dates=True,dayfirst=True)
        #On garde sur la ville ou pas
        if((ville_no2!="Toutes")&(ville_no2!="Urbain")&(ville_no2!="Rural")&(ville_no2!="Trafic")):
            df_no2=df_no2.loc[df_no2["nom_station"]==ville_no2]

        #On drop les lignes inutiles
        df_no2 = df_no2.drop(columns=["nom_dept","nom_com","nom_station","nom_poll","unite","date_debut"], axis=1)
        # enlever les lignes non valides
        df_no2 = df_no2.loc[df_no2["statut_valid"] != 0]


        #On garde la df sur la date
        if(genre=="Choix d'un intervalle"):
            df_no2=df_no2[str(date[0].year)+"-"+str(date[0].month)+"-"+str(date[0].day):str(date[1].year)+"-"+str(date[1].month)+"-"+str(date[1].day)]
        else:
            if ((annee2019 == True) & (annee2020 == True) & (annee2021 == True)):
                df_no2 = df_no2["2019-01-01":"2021-12-31"]
            elif ((annee2019 == True) & (annee2020 == True) & (annee2021 == False)):
                df_no2 = df_no2["2019-01-01":"2020-12-31"]
            elif ((annee2019 == False) & (annee2020 == True) & (annee2021 == True)):
                df_no2 = df_no2["2020-01-01":"2021-12-31"]
            elif ((annee2019 == True) & (annee2020 == False) & (annee2021 == True)):
                df_no2 = pd.concat([df_no2["2019"], df_no2["2021"]])
            elif ((annee2019 == True) & (annee2020 == False) & (annee2021 == False)):
                df_no2 = df_no2["2019"]
            elif ((annee2019 == False) & (annee2020 == True) & (annee2021 == False)):
                df_no2 = df_no2["2020"]
            elif((annee2019 == False) & (annee2020 == False) & (annee2021 == True)):
                df_no2 = df_no2["2021"]

        #On enleve Samedi et Dimanche
        if(Semaine):
            #1)Ajouter une colonne pour le jour de la semaine
            df_no2["day_week"]=df_no2.index.day_name()
            #2)on enleve samedi et dimanche
            df_no2=df_no2.loc[(df_no2["day_week"]!="Sunday") & (df_no2["day_week"]!="Saturday")]


        # on fait la moyenne de la df par Jour
        if(type_moyenne_jour=="Moyenne par jour"):
            string="mean"
        # on prend le max de la df par Jour
        elif(type_moyenne_jour=='Maximum par jour'):
            string="max"
        # on prend le min de la df par Jour
        elif(type_moyenne_jour=='Minimum par jour'):
            string="min"
        else:
            string="valeur"

        if((ville_no2=="Toutes")|(ville_no2=="Urbain")|(ville_no2=="Rural")|(ville_no2=="Trafic")):
            #Moyenne par typologie
            df_urbain=df_no2.loc[(df_no2["typologie"]=="urbaine")&(df_no2["influence"]!="trafic")]
            df_rural=df_no2.loc[(df_no2["typologie"]=="rurale")&(df_no2["influence"]!="trafic")]
            df_trafic=df_no2.loc[df_no2["influence"]=="trafic"]


            if(string!="valeur"):
                #Regrouper les valeurs par jour soit avec la moyenne, soit on prend le min, soit on prend le max
                df_mean_urbain = df_urbain["valeur"].resample("D").agg([string])
                df_mean_rural = df_rural["valeur"].resample("D").agg([string])
                df_mean_trafic = df_trafic["valeur"].resample("D").agg([string])
            else:
                df_mean_urbain = df_urbain
                df_mean_rural = df_rural
                df_mean_trafic = df_trafic

            #On drop les NaN
            df_mean_urbain=df_mean_urbain.dropna()
            df_mean_rural=df_mean_rural.dropna()
            df_mean_trafic=df_mean_trafic.dropna()
        else:
            if(string!="valeur"):
                #Regrouper les valeurs par jour soit avec la moyenne, soit on prend le min, soit on prend le max
                DF_mean=df_no2["valeur"].resample("D").agg([string])
            else:
                DF_mean=df_no2
            #On drop les NaN
            DF_mean=DF_mean.dropna()

        #Graphe
        if(genre=="Choix d'un intervalle"):
            fig, ax = plt.subplots()
            if(type_moyenne=="Lissage Savitzky-Golay"):
                if(ville_no2=="Toutes"):
                    plt.plot(df_mean_urbain.index,savgol_filter(df_mean_urbain[string].values,window_length,polyorder),marker='o',label="Urbain")
                    plt.plot(df_mean_rural.index,savgol_filter(df_mean_rural[string].values,window_length,polyorder),marker='o',label="Rural")
                    plt.plot(df_mean_trafic.index,savgol_filter(df_mean_trafic[string].values,window_length,polyorder),marker='o',label="Trafic")
                else:
                    plt.plot(DF_mean.index,savgol_filter(DF_mean[string].values,window_length,polyorder),marker='o',label=ville_no2)
            elif(type_moyenne=="Moyenne mobile"):
                if(ville_no2=="Toutes"):
                    df_mean_urbain[string].rolling(window=jour_mobile,center=True).mean().plot(marker='o',label="Urbain") #moving average
                    df_mean_rural[string].rolling(window=jour_mobile,center=True).mean().plot(marker='o',label="Rural") #moving average
                    df_mean_trafic[string].rolling(window=jour_mobile,center=True).mean().plot(marker='o',label="Trafic") #moving average
                else:
                    DF_mean[string].rolling(window=jour_mobile,center=True).mean().plot(marker='o',label=ville_no2) #moving average
            else:
                if(ville_no2=="Toutes"):
                    df_mean_urbain[string].plot(marker='o',label="Urbain") #moving average
                    df_mean_rural[string].plot(marker='o',label="Rural") #moving average
                    df_mean_trafic[string].plot(marker='o',label="Trafic") #moving average
                else:
                    DF_mean[string].plot(marker='o',label=ville_no2) #moving average


            __, axYmax = ax.get_ylim()
            if((pd.to_datetime(20200317,format='%Y%m%d')>=date[0])&(pd.to_datetime(20200317,format='%Y%m%d')<=date[1])):
                plt.axvline(x=pd.to_datetime(20200317,format='%Y%m%d'),lw=1, ls='--', alpha=1, color='#000000')
                plt.text(pd.to_datetime(20200317,format='%Y%m%d'),axYmax-2, "Confinement", fontsize=13)
            if((pd.to_datetime(20200511,format='%Y%m%d')>=date[0])&(pd.to_datetime(20200511,format='%Y%m%d')<=date[1])):
                plt.axvline(x=pd.to_datetime(20200511,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')
            if((pd.to_datetime(20201030,format='%Y%m%d')>=date[0])&(pd.to_datetime(20201030,format='%Y%m%d')<=date[1])):
                plt.axvline(x=pd.to_datetime(20201030,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')
                plt.text(pd.to_datetime(20201030,format='%Y%m%d'),axYmax-2, "Confinement", fontsize=13)
            if((pd.to_datetime(20201215,format='%Y%m%d')>=date[0])&(pd.to_datetime(20201215,format='%Y%m%d')<=date[1])):
                plt.axvline(x=pd.to_datetime(20201215,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')
            if((pd.to_datetime(20210403,format='%Y%m%d')>=date[0])&(pd.to_datetime(20210403,format='%Y%m%d')<=date[1])):
                plt.axvline(x=pd.to_datetime(20210403,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')
                plt.text(pd.to_datetime(20210403,format='%Y%m%d'),axYmax-2, "Confinement", fontsize=13)
            if((pd.to_datetime(20210503,format='%Y%m%d')>=date[0])&(pd.to_datetime(20210503,format='%Y%m%d')<=date[1])):
                plt.axvline(x=pd.to_datetime(20210503,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')

            plt.grid(True,axis="y")
            fig.set_figwidth(18)
            fig.set_figheight(10)
            plt.legend(fontsize=12,loc="upper right")
            plt.ylabel("Concentration en NO2 (μg/m3)",fontsize=16)
            plt.xlabel("Date",fontsize=16)
            st.pyplot(fig)
        else:
            if(type_moyenne=="Moyenne mobile"):
                if((ville_no2=="Urbain")):
                    if(df_mean_urbain.empty==False):
                        df_mean_urbain=df_mean_urbain[string].to_frame()
                        df_mean_urbain['doy'] = df_mean_urbain.index.dayofyear  # day of the year
                        df_mean_urbain['Year'] = df_mean_urbain.index.year
                        df_mean_urbain = pd.pivot_table(df_mean_urbain, index=['doy'], columns=['Year'], values=[string])
                        df_mean_urbain.rolling(window=jour_mobile,center=True).mean().plot() #moving average

                elif(ville_no2=="Rural"):
                    if(df_mean_rural.empty==False):
                        df_mean_rural=df_mean_rural[string].to_frame()
                        df_mean_rural['doy'] = df_mean_rural.index.dayofyear  # day of the year
                        df_mean_rural['Year'] = df_mean_rural.index.year
                        df_mean_rural = pd.pivot_table(df_mean_rural, index=['doy'], columns=['Year'], values=[string])
                        df_mean_rural.rolling(window=jour_mobile,center=True).mean().plot() #moving average

                elif(ville_no2=="Trafic"):
                    if(df_mean_trafic.empty==False):
                        df_mean_trafic=df_mean_trafic[string].to_frame()
                        df_mean_trafic['doy'] = df_mean_trafic.index.dayofyear  # day of the year
                        df_mean_trafic['Year'] = df_mean_trafic.index.year
                        df_mean_trafic = pd.pivot_table(df_mean_trafic, index=['doy'], columns=['Year'], values=[string])
                        df_mean_trafic.rolling(window=jour_mobile,center=True).mean().plot() #moving average
                elif(DF_mean.empty==False):
                    DF_mean=DF_mean[string].to_frame()
                    DF_mean['doy'] = DF_mean.index.dayofyear  # day of the year
                    DF_mean['Year'] = DF_mean.index.year
                    DF_mean = pd.pivot_table(DF_mean, index=['doy'], columns=['Year'], values=[string])
                    DF_mean[string].rolling(window=jour_mobile,center=True).mean().plot() #moving average
            else:#pas de moyenne
                if(ville_no2=="Urbain"):
                    if(df_mean_urbain.empty==False):
                        df_mean_urbain=df_mean_urbain[string].to_frame()
                        df_mean_urbain['doy'] = df_mean_urbain.index.dayofyear  # day of the year
                        df_mean_urbain['Year'] = df_mean_urbain.index.year
                        df_mean_urbain = pd.pivot_table(df_mean_urbain, index=['doy'], columns=['Year'], values=[string])
                        df_mean_urbain.plot() #moving average

                elif(ville_no2=="Rural"):
                    if(df_mean_rural.empty==False):
                        df_mean_rural=df_mean_rural[string].to_frame()
                        df_mean_rural['doy'] = df_mean_rural.index.dayofyear  # day of the year
                        df_mean_rural['Year'] = df_mean_rural.index.year
                        df_mean_rural = pd.pivot_table(df_mean_rural, index=['doy'], columns=['Year'], values=[string])
                        df_mean_rural.plot() #moving average

                elif(ville_no2=="Trafic"):
                    if(df_mean_trafic.empty==False):
                        df_mean_trafic=df_mean_trafic[string].to_frame()
                        df_mean_trafic['doy'] = df_mean_trafic.index.dayofyear  # day of the year
                        df_mean_trafic['Year'] = df_mean_trafic.index.year
                        df_mean_trafic = pd.pivot_table(df_mean_trafic, index=['doy'], columns=['Year'], values=[string])
                        df_mean_trafic.plot() #moving average

                elif(DF_mean.empty==False):
                    DF_mean=DF_mean[string].to_frame()
                    DF_mean['doy'] = DF_mean.index.dayofyear  # day of the year
                    DF_mean['Year'] = DF_mean.index.year
                    DF_mean = pd.pivot_table(DF_mean, index=['doy'], columns=['Year'], values=[string])
                    DF_mean[string].plot() #moving average

            __, top = plt.ylim()
            plt.axvline(x=76,lw=1, ls='--', alpha=1, color='#000000')
            plt.text(76,top-2, "Confinement 1", fontsize=8)
            plt.axvline(x=131, lw=1, ls='--', alpha=1, color='#000000')

            plt.axvline(x=303, lw=1, ls='--', alpha=1, color='#000000')
            plt.text(303,top-2, "Confinement 2", fontsize=8)
            plt.axvline(x=349, lw=1, ls='--', alpha=1, color='#000000')

            if(annee2021==True):
                plt.axvline(x=93, lw=1, ls='--', alpha=1, color='#717171')
                plt.text(93,top-4, "Confinement 3", fontsize=8,color='#717171')
                plt.axvline(x=123, lw=1, ls='--', alpha=1, color='#717171')

            plt.legend(fontsize=9,loc="lower left")
            plt.ylabel("Concentration en (μg/m3)",fontsize=16)
            plt.xlabel("Jour de l'année",fontsize=16)
            plt.grid(True,axis="y")
            st.pyplot(fig=plt)


    if("O3" in option_polluant):
        st.markdown("<h2 style='text-align: center;'>Moyenne de la concentration du O3</h2>", unsafe_allow_html=True)
        df_o3 = pd.read_csv("BDD_fichier_csv/mes_bretagne_horaire_o3.csv", delimiter=";", index_col="date_fin", parse_dates=True,dayfirst=True)
        #On garde sur la ville ou pas
        if(ville_o3!="Toutes"):
            df_o3=df_o3.loc[df_o3["nom_station"]==ville_o3]
        #On drop les lignes inutiles
        df_o3 = df_o3.drop(columns=["nom_dept","nom_com","nom_station","nom_poll","unite","date_debut"], axis=1)
        # enlever les lignes non valides
        df_o3 = df_o3.loc[df_o3["statut_valid"] != 0]

        #On garde la df sur la date
        #Attention ici les données sont de 31/12/2020 jusqu'en 2022
        if((date[0].year>2020)&(date[1].year>2020)):
            df_o3=df_o3[str(date[0].year)+"-"+str(date[0].month)+"-"+str(date[0].day):str(date[1].year)+"-"+str(date[1].month)+"-"+str(date[1].day)]
            D=date[0]#date min
        elif((date[1].year>2020)):
            D=pd.to_datetime(20210403,format='%Y%m%d')#date min
            df_o3=df_o3["2020-12-31":str(date[1].year)+"-"+str(date[1].month)+"-"+str(date[1].day)]
            st.info("Les données des concentrations en O3 sont disponibles uniquement à partir de 2021")
        else:
            D=pd.to_datetime(20210403,format='%Y%m%d')#date min
            st.info("Les données des concentrations en O3 sont disponibles uniquement à partir de 2021")
        #sinon on affiche tout le fichier en entière

        #On enleve Samedi et Dimanche
        if(Semaine):
            #1)Ajouter une colonne pour le jour de la semaine
            df_o3["day_week"]=df_o3.index.day_name()
            #2)on enleve samedi et dimanche
            df_o3=df_o3.loc[(df_o3["day_week"]!="Sunday") & (df_o3["day_week"]!="Saturday")]

        # on fait la moyenne de la df par Jour
        if(type_moyenne_jour=="Moyenne par jour"):
            string="mean"
        # on prend le max de la df par Jour
        elif(type_moyenne_jour=='Maximum par jour'):
            string="max"
        # on prend le min de la df par Jour
        elif(type_moyenne_jour=='Minimum par jour'):
            string="min"
        else:
            string="valeur"

        if(ville_o3=="Toutes"):
            #Moyenne par typologie
            df_urbain=df_o3.loc[df_o3["typologie"]=="urbaine"]
            df_rural=df_o3.loc[df_o3["typologie"]=="rurale"]
            df_suburbain=df_o3.loc[df_o3["typologie"]=="suburbaine"]


            if(string!="valeur"):
                #Regrouper les valeurs par jour soit avec la moyenne, soit on prend le min, soit on prend le max
                df_mean_urbain = df_urbain["valeur"].resample("D").agg([string])
                df_mean_rural = df_rural["valeur"].resample("D").agg([string])
                df_mean_suburbain = df_suburbain["valeur"].resample("D").agg([string])
            else:
                df_mean_urbain = df_urbain
                df_mean_rural = df_rural
                df_mean_suburbain = df_suburbain

            #On drop les NaN
            df_mean_urbain=df_mean_urbain.dropna()
            df_mean_rural=df_mean_rural.dropna()
            df_mean_suburbain=df_mean_suburbain.dropna()
        else:
            if(string!="valeur"):
                #Regrouper les valeurs par jour soit avec la moyenne, soit on prend le min, soit on prend le max
                DF_mean=df_o3["valeur"].resample("D").agg([string])
            else:
                DF_mean=df_o3
            #On drop les NaN
            DF_mean=DF_mean.dropna()


        #Graphe
        fig, ax = plt.subplots()
        if(type_moyenne=="Lissage Savitzky-Golay"):
            if(ville_o3=="Toutes"):
                plt.plot(df_mean_urbain.index,savgol_filter(df_mean_urbain[string].values,window_length,polyorder),marker='o',label="Urbain")
                plt.plot(df_mean_rural.index,savgol_filter(df_mean_rural[string].values,window_length,polyorder),marker='o',label="Rural")
                plt.plot(df_mean_suburbain.index,savgol_filter(df_mean_suburbain[string].values,window_length,polyorder),marker='o',label="Suburbain")
            else:
                plt.plot(DF_mean.index,savgol_filter(DF_mean[string].values,window_length,polyorder),marker='o',label=ville_o3)
        elif(type_moyenne=="Moyenne mobile"):
            if(ville_o3=="Toutes"):
                df_mean_urbain[string].rolling(window=jour_mobile,center=True).mean().plot(marker='o',label="Urbain") #moving average
                df_mean_rural[string].rolling(window=jour_mobile,center=True).mean().plot(marker='o',label="Rural") #moving average
                df_mean_suburbain[string].rolling(window=jour_mobile,center=True).mean().plot(marker='o',label="Suburbain") #moving average
            else:
                DF_mean[string].rolling(window=jour_mobile,center=True).mean().plot(marker='o',label=ville_o3) #moving average
        else:
            if(ville_o3=="Toutes"):
                df_mean_urbain[string].plot(marker='o',label="Urbain") #moving average
                df_mean_rural[string].plot(marker='o',label="Rural") #moving average
                df_mean_suburbain[string].plot(marker='o',label="Trafic") #moving average
            else:
                DF_mean[string].plot(marker='o',label=ville_pm10) #moving average


        __, axYmax = ax.get_ylim()
        if((pd.to_datetime(20210403,format='%Y%m%d')>=D)&(pd.to_datetime(20210403,format='%Y%m%d')<=date[1])):
            plt.axvline(x=pd.to_datetime(20210403,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')
            plt.text(pd.to_datetime(20210403,format='%Y%m%d'),axYmax-2, "Confinement", fontsize=13)
        if((pd.to_datetime(20210503,format='%Y%m%d')>=D)&(pd.to_datetime(20210503,format='%Y%m%d')<=date[1])):
            plt.axvline(x=pd.to_datetime(20210503,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')

        plt.grid(True,axis="y")
        fig.set_figwidth(18)
        fig.set_figheight(10)
        plt.legend(fontsize=13,loc="upper right")
        plt.ylabel("Concentration en O3 (μg/m3)",fontsize=16)
        plt.xlabel("Date",fontsize=16)
        st.pyplot(fig)

    creating_space(5)
    st.markdown(f"""<img class="traitSeparation" src="data:image/png;base64,{base64.b64encode(open(trait, "rb").read()).decode()}" alt=traitSeparation> """, unsafe_allow_html=True)
    ##############################################################################################
    ####Graphes
    if(genre=="Choix d'un intervalle"):
        st.markdown("<h2 style='text-align: center;'>Indice qualité</h2>", unsafe_allow_html=True)
        Cl1,Cl2,Cl3=st.columns(3)
        with Cl2:
            options=st.multiselect("Choix de l'indice",
                           ["Qualité de l'air",'PM10', 'O3'],
                           help="Sélectionneur contenant un/des indice(s) correspondant à la mesure de la qualité de l'air")

        if(len(options)!=0):
            if("Qualité de l'air" in options):
                st.markdown("<h2 style='text-align: center;'>Qualité de l'air</h2>", unsafe_allow_html=True)
                fig, ax = plt.subplots()

                #On garde la df sur la date
                debut=str(date[0].year)+"-"+str(date[0].month)+"-"+str(date[0].day)
                fin=str(date[1].year)+"-"+str(date[1].month)+"-"+str(date[1].day)
                df_mean=df_mean[debut:fin]

                if(type_moyenne=="Moyenne mobile"):
                    Data=df_mean["mean"].rolling(window=jour_mobile,center=True).mean()
                    couleur=[]
                    for k in Data:
                        if(np.isnan(k)==True):k=0
                        couleur.append(get_key(dico_couleur,int(round(k,0))))
                    df_mean["mean"].rolling(window=jour_mobile,center=True).mean().plot(zorder=1,color="#000000",label="Moyenne mobile",alpha=0.5)#exponential weight function
                    Data=Data.to_numpy()
                elif(type_moyenne=="Lissage Savitzky-Golay"):
                    Data=savgol_filter(df_mean["mean"].values,window_length,polyorder)
                    couleur=[]
                    for k in Data:
                        if(np.isnan(k)==True):k=0
                        couleur.append(get_key(dico_couleur,int(round(k,0))))
                    plt.plot(df_mean.index,Data,zorder=1,color="#000000",label="Lissage Savitzky-Golay",alpha=0.5)
                else:
                    Data=df_mean["mean"]
                    couleur=[]
                    for k in Data:
                        if(np.isnan(k)==True):k=0
                        couleur.append(get_key(dico_couleur,int(round(k,0))))
                    df_mean["mean"].plot(zorder=1,color="#000000",label="Affichage brut",alpha=0.5)#exponential weight function
                    Data=Data.to_numpy()



                #Dessiner par dessus
                plt.scatter(pd.date_range(start=debut,end=fin),Data,c=couleur,marker = 'o')

                __, axYmax = ax.get_ylim()
                if(pd.to_datetime(2020317,format='%Y%m%d') in df_mean.index):
                    plt.axvline(x=pd.to_datetime(2020317,format='%Y%m%d'),lw=1, ls='--', alpha=1, color='#000000')
                    plt.text(pd.to_datetime(2020317,format='%Y%m%d'),axYmax-0.1, "Confinement", fontsize=13)
                if(pd.to_datetime(2020511,format='%Y%m%d') in df_mean.index):
                    plt.axvline(x=pd.to_datetime(2020511,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')
                if(pd.to_datetime(20201030,format='%Y%m%d') in df_mean.index):
                    plt.axvline(x=pd.to_datetime(20201030,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')
                    plt.text(pd.to_datetime(20201030,format='%Y%m%d'),axYmax-0.1, "Confinement", fontsize=13)
                if(pd.to_datetime(20201215,format='%Y%m%d') in df_mean.index):
                    plt.axvline(x=pd.to_datetime(20201215,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')
                if(pd.to_datetime(202143,format='%Y%m%d') in df_mean.index):
                    plt.axvline(x=pd.to_datetime(202143,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')
                    plt.text(pd.to_datetime(202143,format='%Y%m%d'),axYmax-0.1, "Confinement", fontsize=13)
                if(pd.to_datetime(202153,format='%Y%m%d') in df_mean.index):
                    plt.axvline(x=pd.to_datetime(202153,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')

                fig.set_figwidth(18)
                fig.set_figheight(10)
                plt.ylabel("Qualité de l'air",fontsize=16)
                plt.xlabel("Date",fontsize=16)
                plt.legend(fontsize=13,loc="upper right")
                st.pyplot(fig)

            if("PM10" in options):
                st.markdown("<h2 style='text-align: center;'>Qualité du PM10</h2>", unsafe_allow_html=True)
                df_mean = df["code_pm10"].resample("D").agg(["mean"])
                fig, ax = plt.subplots()

                #On garde la df sur la date
                debut=str(date[0].year)+"-"+str(date[0].month)+"-"+str(date[0].day)
                fin=str(date[1].year)+"-"+str(date[1].month)+"-"+str(date[1].day)
                df_mean=df_mean[debut:fin]

                if(type_moyenne=="Moyenne mobile"):
                    Data=df_mean["mean"].rolling(window=jour_mobile,center=True).mean()
                    couleur=[]
                    for k in Data:
                        if(np.isnan(k)==True):k=0
                        couleur.append(get_key(dico_couleur,int(round(k,0))))
                    df_mean["mean"].rolling(window=jour_mobile,center=True).mean().plot(zorder=1,color="#000000",label="Moyenne mobile",alpha=0.5)#exponential weight function
                    Data=Data.to_numpy()
                elif(type_moyenne=="Lissage Savitzky-Golay"):
                    Data=savgol_filter(df_mean["mean"].values,window_length,polyorder)
                    couleur=[]
                    for k in Data:
                        if(np.isnan(k)==True):k=0
                        couleur.append(get_key(dico_couleur,int(round(k,0))))
                    plt.plot(df_mean.index,Data,zorder=1,color="#000000",label="Lissage Savitzky-Golay",alpha=0.5)
                else:
                    Data=df_mean["mean"]
                    couleur=[]
                    for k in Data:
                        if(np.isnan(k)==True):k=0
                        couleur.append(get_key(dico_couleur,int(round(k,0))))
                    df_mean["mean"].plot(zorder=1,color="#000000",label="Affichage brut",alpha=0.5)#exponential weight function
                    Data=Data.to_numpy()

                #Dessiner par dessus
                plt.scatter(pd.date_range(start=debut,end=fin),Data,c=couleur,marker = 'o')

                __, axYmax = ax.get_ylim()
                if(pd.to_datetime(2020317,format='%Y%m%d') in df_mean.index):
                    plt.axvline(x=pd.to_datetime(2020317,format='%Y%m%d'),lw=1, ls='--', alpha=1, color='#000000')
                    plt.text(pd.to_datetime(2020317,format='%Y%m%d'),axYmax-0.1, "Confinement", fontsize=13)
                if(pd.to_datetime(2020511,format='%Y%m%d') in df_mean.index):
                    plt.axvline(x=pd.to_datetime(2020511,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')
                if(pd.to_datetime(20201030,format='%Y%m%d') in df_mean.index):
                    plt.axvline(x=pd.to_datetime(20201030,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')
                    plt.text(pd.to_datetime(20201030,format='%Y%m%d'),axYmax-0.1, "Confinement", fontsize=13)
                if(pd.to_datetime(20201215,format='%Y%m%d') in df_mean.index):
                    plt.axvline(x=pd.to_datetime(20201215,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')
                if(pd.to_datetime(202143,format='%Y%m%d') in df_mean.index):
                    plt.axvline(x=pd.to_datetime(202143,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')
                    plt.text(pd.to_datetime(202143,format='%Y%m%d'),axYmax-0.1, "Confinement", fontsize=13)
                if(pd.to_datetime(202153,format='%Y%m%d') in df_mean.index):
                    plt.axvline(x=pd.to_datetime(202153,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')

                fig.set_figwidth(18)
                fig.set_figheight(10)
                plt.ylabel("Qualité du PM10",fontsize=16)
                plt.xlabel("Date",fontsize=16)
                plt.legend(fontsize=13,loc="upper right")
                st.pyplot(fig)

            if("O3" in options):
                st.markdown("<h2 style='text-align: center;'>Qualité du O3</h2>", unsafe_allow_html=True)
                df_mean = df["code_o3"].resample("D").agg(["mean"])
                fig, ax = plt.subplots()

                #On garde la df sur la date
                debut=str(date[0].year)+"-"+str(date[0].month)+"-"+str(date[0].day)
                fin=str(date[1].year)+"-"+str(date[1].month)+"-"+str(date[1].day)
                df_mean=df_mean[debut:fin]

                if(type_moyenne=="Moyenne mobile"):
                    Data=df_mean["mean"].rolling(window=jour_mobile,center=True).mean()
                    couleur=[]
                    for k in Data:
                        if(np.isnan(k)==True):k=0
                        couleur.append(get_key(dico_couleur,int(round(k,0))))
                    df_mean["mean"].rolling(window=jour_mobile,center=True).mean().plot(zorder=1,color="#000000",label="Moyenne mobile",alpha=0.5)#exponential weight function
                    Data=Data.to_numpy()
                elif(type_moyenne=="Lissage Savitzky-Golay"):
                    Data=savgol_filter(df_mean["mean"].values,window_length,polyorder)
                    couleur=[]
                    for k in Data:
                        if(np.isnan(k)==True):k=0
                        couleur.append(get_key(dico_couleur,int(round(k,0))))
                    plt.plot(df_mean.index,Data,zorder=1,color="#000000",label="Lissage Savitzky-Golay",alpha=0.5)
                else:
                    Data=df_mean["mean"]
                    couleur=[]
                    for k in Data:
                        if(np.isnan(k)==True):k=0
                        couleur.append(get_key(dico_couleur,int(round(k,0))))
                    df_mean["mean"].plot(zorder=1,color="#000000",label="Affichage brut",alpha=0.5)#exponential weight function
                    Data=Data.to_numpy()

                #Dessiner par dessus
                plt.scatter(pd.date_range(start=debut,end=fin),Data,c=couleur,marker = 'o')

                __, axYmax = ax.get_ylim()
                if(pd.to_datetime(2020317,format='%Y%m%d') in df_mean.index):
                    plt.axvline(x=pd.to_datetime(2020317,format='%Y%m%d'),lw=1, ls='--', alpha=1, color='#000000')
                    plt.text(pd.to_datetime(2020317,format='%Y%m%d'),axYmax-0.1, "Confinement", fontsize=13)
                if(pd.to_datetime(2020511,format='%Y%m%d') in df_mean.index):
                    plt.axvline(x=pd.to_datetime(2020511,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')
                if(pd.to_datetime(20201030,format='%Y%m%d') in df_mean.index):
                    plt.axvline(x=pd.to_datetime(20201030,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')
                    plt.text(pd.to_datetime(20201030,format='%Y%m%d'),axYmax-0.1, "Confinement", fontsize=13)
                if(pd.to_datetime(20201215,format='%Y%m%d') in df_mean.index):
                    plt.axvline(x=pd.to_datetime(20201215,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')
                if(pd.to_datetime(202143,format='%Y%m%d') in df_mean.index):
                    plt.axvline(x=pd.to_datetime(202143,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')
                    plt.text(pd.to_datetime(202143,format='%Y%m%d'),axYmax-0.1, "Confinement", fontsize=13)
                if(pd.to_datetime(202153,format='%Y%m%d') in df_mean.index):
                    plt.axvline(x=pd.to_datetime(202153,format='%Y%m%d'), lw=1, ls='--', alpha=1, color='#000000')

                fig.set_figwidth(18)
                fig.set_figheight(10)
                plt.ylabel("Qualité du O3",fontsize=16)
                plt.xlabel("Date",fontsize=16)
                plt.legend(fontsize=13,loc="upper right")
                st.pyplot(fig)

        creating_space(5)
        st.markdown(f"""<img class="traitSeparation" src="data:image/png;base64,{base64.b64encode(open(trait, "rb").read()).decode()}" alt=traitSeparation> """, unsafe_allow_html=True)
    ######################################################################################
    st.markdown("<h2 style='text-align: center;'>Moyenne annuelle</h2>", unsafe_allow_html=True)
    col1,col2=st.columns(2)
    with col1:
        st.markdown("<h5 style='text-align: center;'>Moyenne annuelle de la concentration du PM10 en µg/m3</h5>", unsafe_allow_html=True)
        dico={"urbain":[16,15.5,15.1667,16.15 ],
              "rural":[16,16,12,10.99 ],
              "trafic":[18,17.6667,16.6667,16.77 ]}
        dataframe=pd.DataFrame(data=dico,index=["2018","2019","2020","2021"])
        dataframe = dataframe.astype({'urbain':'int','rural':'int','trafic':'int'})
        dataframe=dataframe.style.applymap(color_survived, subset=['urbain','rural','trafic'])
        st.table(dataframe)

        st.markdown("<h5 style='text-align: center;'>Moyenne annuelle de la concentration du NO2 en µg/m3</h5>", unsafe_allow_html=True)
        dico={"urbain":[12.5,11.1667,8.4286,9.7 ],
              "rural":[4,5,4,3.41 ],
              "trafic":[26.6667,28,20.5,18.09 ]}
        dataframe=pd.DataFrame(data=dico,index=["2018","2019","2020","2021"])
        dataframe = dataframe.astype({'urbain':'int','rural':'int','trafic':'int'})
        dataframe=dataframe.style.applymap(color_survived, subset=['urbain','rural','trafic'])
        st.table(dataframe)
    with col2:
        st.markdown("<h5 style='text-align: center;'>Moyenne annuelle de la concentration du PM2.5 en µg/m3</h5>", unsafe_allow_html=True)
        dico={"urbain":[8.6667,8.5,7.75,9.24 ],
              "rural":[8,7,5,7.36 ]}
        dataframe=pd.DataFrame(data=dico,index=["2018","2019","2020","2021"])
        dataframe = dataframe.astype({'urbain':'int','rural':'int'})
        dataframe=dataframe.style.applymap(color_survived, subset=['urbain','rural'])
        st.table(dataframe)

        st.markdown("<h5 style='text-align: center;'>Moyenne annuelle de la concentration du O3 en µg/m3</h5>", unsafe_allow_html=True)
        dico={"urbain":[58.8333,57.5714,60,58.21 ],
              "rural":[61,57,65,61.13]}

        dataframe=pd.DataFrame(data=dico,index=["2018","2019","2020","2021"])
        dataframe = dataframe.astype({'urbain':'int','rural':'int'})
        dataframe=dataframe.style.applymap(color_survived, subset=['urbain','rural'])
        st.table(dataframe)


def color_survived(val):
    if val>40:
        color="#50CCAA"
    else:

        color="#50F0E6"
    return f'background-color: {color}'

def creating_space(height):
    for _ in range(height):
        st.write('\n')
