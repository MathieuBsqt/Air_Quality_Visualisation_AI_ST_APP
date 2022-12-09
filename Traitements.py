import pandas as pd
import streamlit
from matplotlib import image as mpimg, pyplot as plt
import datetime
from BaseDonnees import *
import pydeck as pdk
from PIL import Image, ImageColor
import json

def GetDataFrameVille(df,zone):
    """
    :param df: dataframe originale
    :param ville: ville sélectionnée par l'utilisateur
    :return: dataframe de la zone sélectionné
    """
    if(zone=="Bretagne"):
        return df
    else:
        return df.loc[df["lib_zone"]==zone]


def GetColorsDict(DataFrameComplete):
    """
    Cette fonction permet de récupérer les différents codes couleurs présents dans une DataFrame, et d'y aj
    :param DataFrameComplete: Fichier Csv ouvert avec pandas
    :return: Dictionnaire avec chaque code couleur lié à son code qualité correspondant
    """
    column_values = DataFrameComplete[["coul_qual","code_qual"]].values.ravel()
    unique_values = pd.unique(column_values) #liste des coul_qual

    #On convertit en dic
    color_rgb_dct = {unique_values[i]: unique_values[i + 1] for i in range(0, len(unique_values), 2)}

    #On ajoute manuellement au dic des couleurs non présentes dans le fichier .csv afin qu'elles soit présentes au cas où pour que les layers soient activés
    color_rgb_dct["#960032"]=5
    color_rgb_dct["#872181"]=6
    color_rgb_dct["#888888"]=7
    color_rgb_dct["#747474"]="Indisponible"
    return color_rgb_dct

def get_key(dic,val): #Get Key from a Dic
    for key, value in dic.items():
         if val == value:
             return key

    return "key doesn't exist"

def traitement1(DataSet):#si on a selectionne le fichier avec toutes les vars
    """
    :param DataFrame: Base de donnée complète
    :return: retourne une liste de moyenne dans l'ordre : moyenne air, moyenne no2, moyenne so2,moyene 03, moyenne pm10, moyenne pm25
            si la date du jour n'a pas de données renseigné alors la fonction renvoie False
    """
    liste=[]
    liste.append(round(DataSet['code_qual'].loc[DataSet['code_qual'] !=0].mean(axis=0),2))
    liste.append(round(DataSet['code_no2'].loc[DataSet['code_no2'] !=0].mean(axis=0),2))
    liste.append(round(DataSet['code_so2'].loc[DataSet['code_so2'] !=0].mean(axis=0),2))
    liste.append(round(DataSet['code_o3'].loc[DataSet['code_o3'] !=0].mean(axis=0),2))
    liste.append(round(DataSet['code_pm10'].loc[DataSet['code_pm10'] !=0].mean(axis=0),2))
    liste.append(round(DataSet['code_pm25'].loc[DataSet['code_pm25'] !=0].mean(axis=0),2))
    liste=[0 if x != x else x for x in liste]
    return liste


def traitement2(DataSet):#si on a selctionne le fichier avec une ville uniquement
    """
    :param DataFrame: Base de donnée complète
    :return: retourne une liste de moyenne dans l'ordre : moyenne air, moyenne no2, moyenne so2,moyene 03, moyenne pm10, moyenne pm25
            si la date du jour n'a pas de données renseigné alors la fonction renvoie False
    """
    if(DataSet.empty):
        return [0,0,0,0,0,0]

    #if(DataSet['code_no2'].iloc[0] ==0):
    #    return False #car ici manque de données

    liste=[]
    liste.append(round(DataSet['code_qual'].mean(axis=0),2))
    liste.append(round(DataSet['code_no2'].mean(axis=0),2))
    liste.append(round(DataSet['code_so2'].mean(axis=0),2))
    liste.append(round(DataSet['code_o3'].mean(axis=0),2))
    liste.append(round(DataSet['code_pm10'].mean(axis=0),2))
    liste.append(round(DataSet['code_pm25'].mean(axis=0),2))

    return liste

def ouvrir(file): #DESTINEE A OUVRIR UN FICHIER CSV
    return pd.read_csv(file,delimiter=";")


def ConcatenerDate(annee, mois, jour,DataFrame):
    """
    PERMET D'OBTENIR UNE DATE DE LA FORME "annee-mois-jourT01:00:00 à partir du calendrier du site
    :param annee, mois, jour: annee, mois, jour choisis par le user via le calendrier
    :param DataFrame: DataFrame de la ville sélectionnée.
    :return: Date sous le format présent dans la DataFrame
    """
    #On a des entiers on veut concatener donc on trsf en str
    annee=str(annee)
    mois=str(mois)
    jour=str(jour)

    #Si le mois est 8, on le fait devenir 08, pareil pour les jours. On veut un format du type :"2022-01-05T01:00:00"
    if(len(str(mois))==1):
        mois="0"+mois
    if(len(str(jour))==1):
        jour="0"+jour
    #On ajoute l'heure qui est la même quelque soit l'année considérée. (Rajouter l'heure en 2019-2020 a permis de résoudre un bug du .csv)
    Date=annee+"-"+mois+"-"+jour+"T01:00:00"

    DataFrameJourActuel=DataFrame.loc[DataFrame['date_ech'] == Date]
    if(len(DataFrameJourActuel.index)==0): #Si la longueur = 0. C'est que la date n'a pas pu être trouvé. On change donc 1h en 2h
        new_Date=list(Date) #On doit créer une liste car on ne peut pas modif un str en Python
        new_Date[12]="2"
        new_Date = "".join(new_Date)
        return new_Date
    else:
        return Date



def AfficherMap(Date,DataFrame,carte,xmin, xmax, ymin, ymax): #Permet d'afficher une carte png et d'y plot la data
    bretagne_img = mpimg.imread(carte)
    # DataFrameComplete=ouvrir("BDD_fichier_csv/Bdd_Complete.csv")


    DataFrameJourActuel = DataFrame.loc[DataFrame['date_ech'] == Date]
    DataFrameJourActuel.plot(kind="scatter", x="x_wgs84", y="y_wgs84", alpha=0.4, c="coul_qual", label="coul_qual",
                             s=200, colormap='jet', colorbar=False, sharex=False,
                             figsize=(15, 10))
    plt.imshow(bretagne_img, extent=[xmin, xmax, ymin, ymax], aspect='auto', alpha=0.5, cmap=plt.get_cmap(
        "jet"))  # aspect auto sinon image deformee car trop grand ecart d'ordonnes par rapport a celui des abscisses
    # On legende notre figure
    plt.legend(["Indice de qualité de l'air"])
    plt.axis('off')
    return DataFrameJourActuel




def pdkLayer(Data,code_qual,Hex_color,radius=2800):
    color=ImageColor.getcolor(Hex_color, "RGB")
    Layer=pdk.Layer(
        'ScatterplotLayer',
        data=Data.loc[Data['code_qual'] == code_qual],
        get_position='[longitude, latitude]',
        #get_fill_color='[150 200 255]',  # Set an RGBA value for fill
        get_fill_color=color,  # Set an RGBA value for fill
        get_radius=radius,
        pickable=True,
        auto_highlight=True
    )
    return Layer


def ReadJson(path,mode):
    with open(path, mode) as myfile:
        data=myfile.read()
    obj = json.loads(data)
    myfile.close()
    return obj

def AfficherCercle(label,texte,color):
    figure, axes = plt.subplots()
    draw_circle = plt.Circle((0.5, 0.5), 0.46,color=color)
    draw_circle2=plt.Circle((0.5, 0.5), 0.49,fill=False,color=color,linewidth=3)
    axes.set_aspect(1)
    axes.add_artist(draw_circle)
    axes.add_artist(draw_circle2)
    plt.axis('off')
    plt.annotate(label+'\n\n'+texte,xy=(0.5,0.5),fontsize=30,verticalalignment='center', horizontalalignment='center')
    figure.patch.set_alpha(0.0) #Background Transparence pour le Dark Mode
    #plt.show()
    return figure

def moyene_col_1(colonne_DataFrame,DataFrame,date_debut,date_fin,mode):
    date_a = datetime.datetime(date_debut.year,date_debut.month,date_debut.day)
    liste,liste_2,liste_qual=[],[],[]
    date_b=datetime.datetime(date_fin.year,date_fin.month,date_fin.day)
    taille=(date_b-date_a).days
    if mode == "Bretagne":
        for i in range(taille+1):
            liste_2.append(date_a)
            liste.append(ConcatenerDate(date_a.year,date_a.month,date_a.day,DataFrame))
            a=DataFrame.loc[DataFrame['date_ech']==liste[i]]
            liste_qual.append(round(a[colonne_DataFrame].mean(axis=0),2))
            date_a += datetime.timedelta(days=1)
    elif mode =='own_file':
        for i in range(taille+1):
            liste_2.append(date_a)
            a = DataFrame.loc[(DataFrame['Annee'] == date_a.year)&(DataFrame['Mois'] == date_a.month)&(DataFrame['Jours'] == date_a.day)]
            liste_qual.append(round(a[colonne_DataFrame].mean(axis=0),2))
            date_a += datetime.timedelta(days=1)

    return liste_2,liste_qual

def moyene_col_2(colonne_DataFrame,DataFrame,date_debut,date_fin):
    date_a = datetime.datetime(date_debut.year,date_debut.month,date_debut.day)
    liste,liste_2,liste_qual=[],[],[]
    date_b=datetime.datetime(date_fin.year,date_fin.month,date_fin.day)
    taille=(date_b-date_a).days
    for i in range(taille+1):
        liste_2.append(date_a)
        date_a += datetime.timedelta(days=1)
        liste.append(ConcatenerDate(date_a.year,date_a.month,date_a.day,DataFrame))
        a=DataFrame.loc[DataFrame['date_ech']==liste[i]]

        #si c'est empty
        if(a.empty==True):
            liste_qual.append(0)
        else:
            liste_qual.append(a[colonne_DataFrame])

    return liste_2,liste_qual

def AfficherGraphe1(df,String,zone,title,dico_couleur,StringName,date_debut,date_fin):
    #max=2022-01-05 01:00:00
    #min=2021-01-04
    if zone=='Bretagne':
        liste_2,liste_qual=moyene_col_1(String,df,date_debut,date_fin,zone)
    elif zone=='own_file':
        liste_2,liste_qual=moyene_col_1(String,df,date_debut,date_fin,zone)
    else:
        DataFrame=GetDataFrameVille(df,zone)
        liste_2,liste_qual=moyene_col_2(String,DataFrame,date_debut,date_fin)


    couleur=[]
    for k in liste_qual:
        couleur.append(get_key(dico_couleur,int(round(k,0))))

    figure=plt.figure(figsize=(10,1.5))
    plt.scatter(liste_2,liste_qual,c=couleur)
    plt.title(title)
    plt.xlabel("Date AAAA-MM-JJ HH")
    plt.ylabel(StringName)
    plt.ylim(bottom=0)
    plt.ylim(top=4.5)


    return figure
