# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 15:38:34 2022

@author: Mathi
"""

import pandas as pd
import numpy as np

"""

df = pd.read_csv("C:/Users/Mathi/Documents/Travail/ISEN/A4/ProjetM1/lefichierreformate2020v3.csv", delimiter=";")

df["date_ech"]=df["date_ech"]+"T01:00:00"

df.to_csv("BDD_20192020cheat.csv",index=False)

"""
"""
df = pd.read_csv("C:/Users/Mathi/Documents/Travail/ISEN/A4/ProjetM1/BDD_fichier_csv/Bdd_complete.csv", delimiter=";", index_col="date_ech", parse_dates=True)
print(df.loc["2019"]["code_qual"].mean())
print(df.loc["2020"]["code_qual"].mean())
print(df.loc["2021"]["code_qual"].mean())
print(df.loc["2022"]["code_qual"].mean())

dft=df.loc["2022"]["code_qual"]

"""

#df = pd.read_csv("C:/Users/Mathi/Documents/Travail/ISEN/A4/ProjetM1/BDD_fichier_csv/Bdd_complete.csv", delimiter=";" ,index_col="date_ech", parse_dates=True)

#print(df.loc["2022"]["code_qual"].describe())

df = pd.read_csv("C:/Users/Mathi/Documents/Travail/ISEN/A4/ProjetM1/BDD_fichier_csv/Bdd_complete.csv", delimiter=";")
print(df.info()) #31850

print(df.head(1)) 

print(df.head(-1))
df2=df["date_ech"]

print(df2.nunique())