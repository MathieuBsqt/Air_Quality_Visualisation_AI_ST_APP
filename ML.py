





#IMPORT
import pandas as pd
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OrdinalEncoder,OneHotEncoder
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier
import datetime
from sklearn.metrics import confusion_matrix,classification_report,accuracy_score

from sklearn.metrics import mean_squared_error
#########################################################################################################
#OUVERTURE DATABASE
df=pd.read_csv("C:/Users/Mathi/Documents/Travail/ISEN/A4/ProjetM1/BDD_fichier_csv/Bdd_Complete.csv",delimiter=";")


def splitdate(df):
    c=df["lib_zone"].unique()
    lst=[]
    for i in c:
        lst.append(i)

    Date=df["date_ech"].str.split("-")
    cpt=0
    annee=[]
    mois=[]
    jours=[]
    for elt in Date:
      Date.iloc[cpt][2]= Date.iloc[cpt][2][0:2]
      annee.append(int(Date.iloc[cpt][0]))
      mois.append(int(Date.iloc[cpt][1]))
      jours.append(int(Date.iloc[cpt][2]))
      cpt+=1

    df2=pd.DataFrame(data= {'Annee':annee, 'Mois': mois,'Jours':jours})
    df=pd.concat([df2,df],axis=1)
    return df





df=splitdate(df)
    
df=df.loc[(df["Annee"] !=2019)]
df=df.loc[(df["Annee"] !=2020)]
#On enleve la premiere ligne inutile
df=df.loc[df["code_no2"] != 0 ]


df=df.drop(columns=["Annee","code_so2","Mois","Jours","FID","date_ech","lib_zone","lib_qual","coul_qual","date_dif","source","type_zone","code_zone","x_wgs84","y_wgs84","x_reg","y_reg","epsg_reg","geom"],axis=1)


print(df["code_qual"].value_counts())
print(df["code_no2"].value_counts())
print(df["code_o3"].value_counts())
print(df["code_pm10"].value_counts())
print(df["code_pm25"].value_counts())

#On garde le même nombre de valeur pour l'apprentissage

"""
df1=df.loc[df["code_qual"]==1][:417]
df2=df.loc[df["code_qual"]==2][:417]
df3=df.loc[df["code_qual"]==3][:417]
df4=df.loc[df["code_qual"]==4][:417]
df=pd.concat([df1,df2,df3,df4])


print(df["code_qual"].value_counts())
print(df["code_no2"].value_counts())
print(df["code_o3"].value_counts())
print(df["code_pm10"].value_counts())
print(df["code_pm25"].value_counts())
"""



X=df.drop(["code_qual"],axis=1)
y=df["code_qual"]



from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)



#Normalisation
model_normalisation=StandardScaler()
X_train=model_normalisation.fit_transform(X_train)
X_test=model_normalisation.fit_transform(X_test)


# MACHINE LEARNING
from sklearn.linear_model import SGDClassifier
SDG=SGDClassifier(max_iter=1000,penalty='l1',loss='log',average=False)
SDG.fit(X_train,y_train)
y_pred=SDG.predict(X_test)
score=SDG.score(X_test,y_test)
print(f'score SGDClassifier sans equilibrage = { round(score,2)} ')


from sklearn.ensemble import RandomForestClassifier
random_forest = RandomForestClassifier(max_depth=2, random_state=0)
random_forest.fit(X_train,y_train)
y_pred=random_forest.predict(X_test)
score=random_forest.score(X_test,y_test)
print(f'score RandomForestClassifier sans equilibrage = { round(score,2)} ')


#Voting Soft
VoteClassificationSoft=VotingClassifier(estimators=[('SDG', SDG),('random_forest', random_forest)], voting='soft')
VoteClassificationSoft.fit(X_train,y_train)


testpredictionSoft=VoteClassificationSoft.predict(X_test)
scoreTestSoft=VoteClassificationSoft.score(X_test,y_test)
print("SOFT:")
print("score test soft=",scoreTestSoft)

print("Matrice de confusion SOFT")
print(confusion_matrix(y_test, testpredictionSoft, labels=range(4)))

print("Report de la matrice de confusion")
print(classification_report(y_test, testpredictionSoft))





from sklearn.linear_model import LinearRegression
reg = LinearRegression().fit(X_train, y_train)

y_pred=reg.predict(X_test)
rmse= (mean_squared_error(y_test, y_pred))**0.5

print("valeur +- ",rmse)



dico={"code_no2":[1],
      "code_o3":[2],
      "code_pm10":[1],
      "code_pm25":[1]
      }

Xnew=pd.DataFrame(data=dico)
#model_normalisation=StandardScaler()
Xnew= model_normalisation.transform(Xnew) +1 #Car on avait mis y=y-1

print("Classification : ")
print("Prediction SDG : ",SDG.predict(Xnew))

print("Prediction random forest : ",random_forest.predict(Xnew))

print("Prediction Voting Soft : ",VoteClassificationSoft.predict(Xnew))

print("Regression : ")
print("Prediction : ",reg.predict(Xnew))

print("\n")