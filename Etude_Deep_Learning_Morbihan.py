# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 11:14:10 2022

@author: Mathi
"""

morbihan=["CC Roi Morvan Communauté", "CC Pontivy Communauté", "CC de Ploërmel Communauté", "CA Lorient", "CC Centre Morbihan Communauté", "CC de l'Oust à Brocéliande Communauté", "CC de Blavet Bellevue Océan", "CC Auray Quiberon Terre Atlantique", "CA Golfe du Morbihan - Vannes", "CC Questembert Communauté", "CC Arc Sud Bretagne", "CA de la Presqu'île de Guérande Atlantique (Cap Atlantique) (partie bretonne)", "CC de Belle-Ile-en-Mer"]

import matplotlib.pyplot as plt
#import geopandas as gpd
import pandas as pd


#df=pd.read_csv("C:/Users/Mathi/Documents/Travail/ISEN/A4/ProjetM1/BDD_fichier_csv/Bdd_Complete.csv",delimiter=";",index_col="date_ech",parse_dates=True)

df=pd.read_csv("C:/Users/Mathi/Documents/Travail/ISEN/A4/ProjetM1/BDD_fichier_csv/Bdd_Complete.csv",delimiter=";")

df['date_ech'] = pd.to_datetime(df['date_ech'])
df['date_ech'] = df['date_ech'].dt.date
df=df.drop(columns=["FID","date_dif","source","type_zone","code_zone","x_reg","y_reg","epsg_reg","geom"],axis=1)


df.to_csv("BDD_completemodif.csv", index=False)