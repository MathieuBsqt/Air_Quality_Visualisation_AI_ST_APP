# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 10:56:45 2022

@author: Mathi
"""

ille_et_vilaine=["CA du Pays de Saint-Malo (Saint-Malo Agglomération)", "CC du Pays de Dol et de la Baie du Mont-Saint-Michel", "CC Bretagne Romantique", "CC Couesnon Marches de Bretagne", "CA Fougères", "CC du Val d'Ille-Aubigné", "CC Liffré-Cormier Communauté", "CC de Saint-Méen Montauban", "CC Montfort Communauté", "CC de Brocéliande", "Rennes Métropole", "CA Vitré Communauté", "CC du Pays de Châteaugiron", "CC Vallons de Haute-Bretagne Communauté", "CC Au Pays de la Roche aux Fées", "CC Bretagne Porte de Loire Communauté", "CC du Pays de Redon (partie bretonne)"]

import matplotlib.pyplot as plt
#import geopandas as gpd
import pandas as pd


df=pd.read_csv("C:/Users/Mathi/Documents/Travail/ISEN/A4/ProjetM1/BDD_fichier_csv/Bdd_Complete.csv",delimiter=";")






#preprocessing normalisation de la date
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


df=df.drop(columns=["FID","date_ech","lib_qual","coul_qual","date_dif","source","type_zone","code_zone","x_wgs84","y_wgs84","x_reg","y_reg","epsg_reg","geom"],axis=1)



df=df.loc[df["code_no2"] != 0 ]

#ZONE

# Get names of indexes for which column Age has value 

#for area_name in Finistere:
    #indexNames = df[ df["lib_zone"] == area_name ].index

print(df.shape[0])
indexNames = df[ (df['lib_zone'] !=ille_et_vilaine[0]) & (df['lib_zone'] !=ille_et_vilaine[1]) & (df['lib_zone'] !=ille_et_vilaine[2]) & (df['lib_zone'] !=ille_et_vilaine[3]) & (df['lib_zone'] !=ille_et_vilaine[4]) & (df['lib_zone'] !=ille_et_vilaine[5]) & (df['lib_zone'] !=ille_et_vilaine[6]) & (df['lib_zone'] !=ille_et_vilaine[7]) & (df['lib_zone'] !=ille_et_vilaine[8]) & (df['lib_zone'] !=ille_et_vilaine[9]) & (df['lib_zone'] !=ille_et_vilaine[10]) & (df['lib_zone'] !=ille_et_vilaine[11]) & (df['lib_zone'] !=ille_et_vilaine[12]) & (df['lib_zone'] !=ille_et_vilaine[13]) & (df['lib_zone'] !=ille_et_vilaine[14]) & (df['lib_zone'] !=ille_et_vilaine[15]) & (df['lib_zone'] !=ille_et_vilaine[16])].index
df.drop(indexNames , inplace=True)

print(df.shape[0])


#df=df.drop(["lib_zone"],axis=1)



y=df["code_qual"]
X=df.drop(["code_qual"],axis=1)



from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OrdinalEncoder,OneHotEncoder
from sklearn.preprocessing import StandardScaler
import numpy as np

model=make_column_transformer((OneHotEncoder(),["Annee","Mois","Jours"]),
                     (StandardScaler(),["code_no2","code_so2","code_o3","code_pm10","code_pm25"])
                     )


X=model.fit_transform(X)
X=pd.DataFrame(X.toarray())

X=X.drop([1,2,44],axis=1)

y=np.array(y)
y=y-1
model2=OneHotEncoder()
y=model2.fit_transform(y.reshape(-1,1)).toarray()
y=np.delete(y,[0],axis=1)


#Repartition des données
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.20,random_state=0)


#Deep learning
from keras.models import Sequential 
from keras.layers import Dense

network=Sequential()

# 47 -> 24
#activation= 'relu' , la fonction d'activation (si x >0 retourne x sinon retourne 0)
network.add(Dense(input_dim=X.shape[1],
                  units=24,
                  activation="relu",
                  kernel_initializer="uniform") 
            )

# 24 -> 24
network.add(Dense(units=24,
                  activation="relu",
                  kernel_initializer="uniform") 
            )

# 24 -> 
network.add(Dense(units=3,
                  activation="sigmoid",
                  kernel_initializer="uniform") 
            )


network.compile(optimizer= 'adam',
            loss='binary_crossentropy',
            metrics=['accuracy'])


############## Fit Network ############## 
network.fit(X_train,y_train,batch_size= 10, epochs=30)




y_pred=network.predict(X_test)

y_pred[np.arange(len(y_pred)), y_pred.argmax(1)] = 1
y_pred = np.int_(y_pred)

from sklearn.metrics import confusion_matrix, accuracy_score
y_test= np.int_(y_test)
#On stocke les index de nos valeurs = 1 
pred = list()
for i in range(len(y_pred)):
  pred.append(np.argmax(y_pred[i]))

test = list()
for i in range(len(y_test)):
  test.append(np.argmax(y_test[i]))



cm=confusion_matrix(test,pred)
print(cm)

print(accuracy_score(y_test, y_pred))