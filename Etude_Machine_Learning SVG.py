# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 10:25:18 2022

@author: Mathi
"""

#IMPORT
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OrdinalEncoder,OneHotEncoder
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.model_selection import train_test_split



#OUVERTURE DATABASE
df=pd.read_csv("C:/Users/Julian/Documents/ISEN/4emeannee/Projet/BDD/Bdd_Complete.csv",delimiter=";")




#PRE-PROCESSING

#split de la date dans 3 colonnes ["Annee", "Mois","Jours"]
Date=df["date_ech"].str.split("-")
cpt=0
annee=[]
mois=[]
jours=[]
for elt in Date:
  Date.iloc[cpt][2]= Date.iloc[cpt][2][0:2]
  annee.append(Date.iloc[cpt][0])
  mois.append(Date.iloc[cpt][1])
  jours.append(Date.iloc[cpt][2])
  cpt+=1
  
df2=pd.DataFrame(data= {'Annee':annee, 'Mois': mois,'Jours':jours})
df=pd.concat([df2,df],axis=1)

#On enleve les colonnes inutile à l'apprentissage
df=df.drop(columns=["FID","date_ech","lib_qual","coul_qual","date_dif","source","type_zone","code_zone","x_wgs84","y_wgs84","x_reg","y_reg","epsg_reg","geom"],axis=1)

#On enleve les valeurs vides
df=df.loc[df["code_no2"] != 0 ]




#CHOIX TYPE DE ZONE :
    #ZONE CC du Haut Pays Bigouden

#Selection de la zone
zone="CC du Haut Pays Bigouden"
df=df.loc[df["lib_zone"] == zone ]
df=df.drop(["lib_zone"],axis=1)


#Séparation de la target des données
y=df["code_qual"]
X=df.drop(["code_qual"],axis=1)


#ENCODAGE + NORMALISATION
model=make_column_transformer((OneHotEncoder(),["Annee","Mois","Jours"]),
                     (StandardScaler(),["code_no2","code_so2","code_o3","code_pm10","code_pm25"])
                     )


X=model.fit_transform(X)
X=pd.DataFrame(X.toarray())
X=X.drop([1,2,44],axis=1)

y=np.array(y)
y=y-1


#Repartition des données
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.20,random_state=0)


# MACHINE LEARNING
from sklearn.linear_model import SGDClassifier
model=SGDClassifier(max_iter=1000)
model.fit(X_train,y_train)
y_pred=model.predict(X_test)
score=model.score(X_test,y_test)
print(score)


from sklearn.metrics import confusion_matrix
print(confusion_matrix(y_test, y_pred))