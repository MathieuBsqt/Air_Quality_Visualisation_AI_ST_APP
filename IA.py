import pandas as pd
import streamlit
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import VotingClassifier

def machine_learning_concentration(no2,pm10,pm25):
    df_Brest=pd.read_csv("BDD_fichier_csv/IA_Brest_Mace_2020.csv",delimiter=";")
    df_Brest=df_Brest.drop(columns=["date","nom_station",'typologie',"influence","lib_zone"])
    df_Brest=df_Brest.dropna()
    df_Lorient=pd.read_csv("BDD_fichier_csv/IA_Lorient_Bissonnet_2020.csv",delimiter=";")
    df_Lorient=df_Lorient.drop(columns=["date","nom_station",'typologie',"influence","lib_zone"])
    df_Lorient=df_Lorient.dropna()
    #df_Merleac=pd.read_csv("BDD_fichier_csv/IA_Merleac_Kergoff_2021.csv",delimiter=";")
    #df_Merleac=df_Merleac.drop(columns=["date","nom_station",'typologie',"influence","lib_zone"])
    #df_Merleac=df_Merleac.dropna()
    df_Rennes=pd.read_csv("BDD_fichier_csv/IA_Rennes_Metropole_2020.csv",delimiter=";")
    df_Rennes=df_Rennes.drop(columns=["date","nom_station",'typologie',"influence","lib_zone"])
    df_Rennes=df_Rennes.dropna()
    #df_Saint_Brieux=pd.read_csv("BDD_fichier_csv/IA_Saint_Brieuc_Balzac.csv",delimiter=";")
    #df_Saint_Brieux=df_Saint_Brieux.drop(columns=["date","nom_station",'typologie',"influence","lib_zone"])
    df_Saint_Malo=pd.read_csv("BDD_fichier_csv/IA_Saint_Malo_Rocabey_2020.csv",delimiter=";")
    df_Saint_Malo=df_Saint_Malo.drop(columns=["date","nom_station",'typologie',"influence","lib_zone"])
    df_Saint_Malo=df_Saint_Malo.dropna()
    df_Vannes=pd.read_csv("BDD_fichier_csv/IA_Vannes_UTA_2020.csv",delimiter=";")
    df_Vannes=df_Vannes.drop(columns=["date","nom_station",'typologie',"influence","lib_zone"])
    df_Vannes=df_Vannes.dropna()

    liste_df=[df_Brest,df_Lorient,df_Rennes,df_Saint_Malo,df_Vannes]
    liste_prediction=[]
    for df in liste_df:
        X=df.drop("code_qual",axis=1)
        y=df["code_qual"]
        #Normalisation
        model_normalisation=StandardScaler()
        X=model_normalisation.fit_transform(X)
        SDG = SGDClassifier(max_iter=1000, penalty='l1', loss='log', average=False).fit(X, y)
        liste_prediction.append(int(prediction_concentration(SDG,model_normalisation,no2,pm10,pm25)[0]))
    return liste_prediction


def prediction_concentration(modele_ia, model_normalisation, code_no2, code_pm10, code_pm25):
    dico = {"code_no2": [int(code_no2)],
            "code_pm10": [int(code_pm10)],
            "code_pm25": [int(code_pm25)]
            }
    Xnew = pd.DataFrame(data=dico)
    Xnew = model_normalisation.transform(Xnew)
    return modele_ia.predict(Xnew)




def machine_learning_indice(file):
    df = splitdate(file)
    # On garde les données de 2021 et 2022
    df = df.loc[(df["Annee"] != 2019)]
    df = df.loc[(df["Annee"] != 2020)]

    # On enleve la premiere ligne inutile
    df = df.loc[df["code_no2"] != 0]
    df = df.drop(
        columns=["Annee", "code_so2", "Mois", "Jours", "date_ech", "lib_zone", "lib_qual", "coul_qual", "x_wgs84",
                 "y_wgs84"], axis=1)

    X = df.drop(["code_qual"], axis=1)
    y = df["code_qual"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Normalisation
    model_normalisation = StandardScaler()
    X_train = model_normalisation.fit_transform(X_train)

    forest = RandomForestClassifier(max_depth=2).fit(X_train, y_train)
    SGD = SGDClassifier(max_iter=1000, penalty='l1', loss='log', average=False).fit(X_train, y_train)

    VoteClassificationSoft = VotingClassifier(estimators=[('SGD', SGD), ('forest', forest)], voting='soft')
    VoteClassificationSoft.fit(X_train, y_train)
    return VoteClassificationSoft, model_normalisation


def ia_ml_prediction(modele_ia, model_normalisation, code_no2, code_o3, code_pm10, code_pm25):
    dico = {"code_no2": [int(code_no2)],
            "code_o3": [int(code_o3)],
            "code_pm10": [int(code_pm10)],
            "code_pm25": [int(code_pm25)]
            }

    Xnew = pd.DataFrame(data=dico)
    Xnew = model_normalisation.transform(Xnew) + 1  # Car on avait mis y=y-1

    return modele_ia.predict(Xnew)


def splitdate(df):
    c = df["lib_zone"].unique()
    lst = []
    for i in c:
        lst.append(i)

    Date = df["date_ech"].str.split("-")
    annee = []
    mois = []
    jours = []
    for cpt in range(len(Date)):
        Date.iloc[cpt][2] = Date.iloc[cpt][2][0:2]
        annee.append(int(Date.iloc[cpt][0]))
        mois.append(int(Date.iloc[cpt][1]))
        jours.append(int(Date.iloc[cpt][2]))

    df2 = pd.DataFrame(data={'Annee': annee, 'Mois': mois, 'Jours': jours})
    df = pd.concat([df2, df], axis=1)
    return df
