from Traitements import ouvrir
import pandas as pd

def BDD(choice,dicoville,dicochemin):
    """
    :param choice: choix de l'utilisateur sur le fichier à prendre "ex: Au Pays de la Roche aux Fées"
    :return: retourne le nom de la zone tel qu'il est écrit dans le fichier .csv "ex: CC Au Pays de la Roche aux Fées"
    """
    for cle, valeur in dicoville.items():
        if ((valeur == choice) & (cle != 'v0')):
            return dicochemin[cle]
    return None

def get_key(dico,val):
    for key, value in dico.items():
         if val == value:
             return key

    return None

def chemindico():
    return {'v0':'None',
            'v1':'Bretagne',
            'v2':'CC Au Pays de la Roche aux Fées',
            'v3':'CC Auray Quiberon Terre Atlantique',
            'v4':'CC de Belle-Ile-en-Mer',
            'v5':'CC de Blavet Bellevue Océan',
            'v6':'Brest Métropole',
            'v7':'CC Bretagne Porte de Loire Communauté',
            'v8':'CC Bretagne Romantique',
            'v9':"CC de l'Oust à Brocéliande Communauté",
            'v10':'CC Cap Sizun - Pointe du Raz',
            'v11':'CC Centre Morbihan Communauté',
            'v12':'CC Communauté Lesneven Côte des Légendes',
            'v13':'CA Concarneau Cornouaille',
            'v14':"CC Côte d'Émeraude",
            'v15':'CC Couesnon Marches de Bretagne',
            'v16':"CC de l'Oust à Brocéliande Communauté",
            'v17':'CA Dinan',
            'v18':'CC Douarnenez Communauté',
            'v19':'CA du Pays de Saint-Malo (Saint-Malo Agglomération)',
            'v20':'CA Fougères',
            'v21':'CA Golfe du Morbihan - Vannes',
            'v22':'CA Guingamp-Paimpol Armor-Argoat',
            'v23':'CC Haut-Léon Communauté',
            'v24':'CC du Haut Pays Bigouden',
            'v25':'CC de Haute-Cornouaille',
            'v26':'CC du Kreiz-Breizh (Cckb)',
            'v27':'CC Lamballe Terre et Mer',
            'v28':'CA Lannion-Trégor Communauté',
            'v29':'CC Leff Armor Communauté',
            'v30':'CC Liffré-Cormier Communauté',
            'v31':'CA Lorient',
            'v32':'CC Loudéac Communauté - Bretagne Centre',
            'v33':'CC Montfort CommunautÃ©',
            'v34':"CC Monts d'ArrÃ©e CommunautÃ©",
            'v35':'CA Morlaix Communauté',
            'v36':'CC du Pays Bigouden Sud',
            'v37':'CC du Pays de Châteaugiron',
            'v38':'CC du Pays de Dol et de la Baie du Mont-Saint-Michel',
            'v39':'CC du Pays de Landerneau-Daoulas',
            'v40':'CC du Pays de Landivisiau',
            'v41':'CA du Pays de Quimperlé',
            'v42':'CC du Pays de Redon (partie bretonne)',
            'v43':'CC du Pays des Abers',
            'v44':'CC du Pays Fouesnantais',
            'v45':"CC du Pays d'Iroise",
            'v46':'CC Pleyben-Châteaulin-Porzay',
            'v47':'CC de Ploërmel Communauté',
            'v48':'CC Poher Communauté',
            'v49':'CC Pontivy Communauté',
            'v50':"CA de la Presqu'île de Guérande Atlantique (Cap Atlantique) (partie bretonne)",
            'v51':"CC Presqu'île de Crozon-Aulne Maritime",
            'v52':'CC Questembert Communauté',
            'v53':'CA Quimper Bretagne Occidentale',
            'v54':'Rennes Métropole',
            'v55':'CC Roi Morvan Communauté',
            'v56':'CA Saint-Brieuc Armor',
            'v57':'CC de Saint-Méen Montauban',
            'v58':"CC du Val d'Ille-Aubigné",
            'v59':'CC Vallons de Haute-Bretagne Communauté',
            'v60':'CA Vitré Communauté'}

def villedico():
    """
    :return: retourne le dictionnaire dees villes de la region Bretagne
    """
    return {    'v0':'--Selection--',
                'v1':'Bretagne',
                'v2':'Au Pays De La Roche Aux Fees',
                'v3':'Auray Quiberon Terre Atlantique',
                'v4':'Belle île en Mer',
                'v5':'Blavet Bellevue Océan',
                'v6':'Brest Metropole',
                'v7':'Bretagne Porte de Loire Communaute',
                'v8':'Bretagne Romantique',
                'v9':'Broceliande',
                'v10':'Cap Sizun Pointe Du Raz',
                'v11':'Centre Morbihan Communaute',
                'v12':'Communaute Lesneven Cote Des Legendes',
                'v13':'Concarneau Cornouaille',
                'v14':'Cote D Emeraude',
                'v15':'Couesnon Marches de Bretagne',
                'v16':'De l Oust a Broceliande Communaute',
                'v17':'Dinan',
                'v18':'Douarmenez Communaute',
                'v19':'Du Pays de Saint Malo',
                'v20':'Fougere',
                'v21':'Golfe du Morbihan',
                'v22':'Guingamp Paimpol Armor Argot',
                'v23':'Haut Pays Bigouden',
                'v24':'Haute Cornouaille',
                'v25':'Haut Leon Communaute',
                'v26':'Kreiz Breizh',
                'v27':'Lamballe Terre et Mer',
                'v28':'Lannion Tregor Communaute',
                'v29':'Leff Armor Communate',
                'v30':'Liffre Cormier Communate',
                'v31':'Lorient',
                'v32':'Loudeac Communaute Bretagne Centre',
                'v33':'Monfort Communaute',
                'v34':'Monts D Arree Communate',
                'v35':'Morlaix Communaute',
                'v36':'Pays Bigouden Sud',
                'v37':'Pays De Chateaugiron',
                'v38':'Pays de dol et de la baie du Mont Saint Michel',
                'v39':'Pays de Landerneau Daoulas',
                'v40':'Pays de Landivisiau',
                'v41':'Pays de Quimperle',
                'v42':'Pays de Redon',
                'v43':'Pays des Abers',
                'v44':'Pays Fouestnantais',
                'v45':'Pays Iroise',
                'v46':'Pleyben Chateaulin Porzay',
                'v47':'Ploermel Communaute',
                'v48':'Poher Communaute',
                'v49':'Pontivy Communate',
                'v50':'Presque Ile de Guerande Atlantique',
                'v51':'Presque Ile de Crozon Aulne Maritime',
                'v52':'Questembert Communaute',
                'v53':'Quimpert Bretagne Occidentale',
                'v54':'Rennes Metropole',
                'v55':'Roi Morvan Communaute',
                'v56':'Saint Brieuc Armor',
                'v57':'Saint Meen Montauban',
                'v58':'Val Ile Aubigne',
                'v59':'Vallons de Haute Bretagne Communaute',
                'v60':'Vitre Communaute'}


def Viewsdico():
    """
    :return: retourne le dictionnaire dees villes de la region Bretagne
    """
    return {    'mapbox://styles/mapbox/streets-v11':'Rues',
                'mapbox://styles/mapbox/outdoors-v11':'Plein air',
                'mapbox://styles/mapbox/light-v10':'Lumineux',
                'mapbox://styles/mapbox/dark-v10':'Sombre',
                'mapbox://styles/mapbox/satellite-v9':'Satellite',
                'mapbox://styles/mapbox/satellite-streets-v11':'Rues satellite',
                'mapbox://styles/mapbox/navigation-day-v1':'Navigation de jour',
                'mapbox://styles/mapbox/navigation-night-v1':'Navigation de nuit'}

