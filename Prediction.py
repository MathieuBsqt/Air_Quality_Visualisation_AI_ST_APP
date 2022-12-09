import streamlit as st
from PIL import ImageColor
from IA import *
import pydeck as pdk
from Traitements import ReadJson, get_key


def fenetre_prediction(df):
    st.title("Prédiction de la qualité de l'air")
    st.info(
        "Cette page vous permet d'interagir avec notre modèle d'intelligence artificielle en sélectionnant vous-même les valeurs de chacun des facteurs.")
    # SIDEBAR
    st.sidebar.markdown("<h2 style='text-align: center;'>Options IA Concentration</h2>", unsafe_allow_html=True)
    concentration_no2 = st.sidebar.slider("Concentration du NO2 en μg/m3", 1, 230, 40, step=1)
    concentration_pm10 = st.sidebar.slider("Concentration du PM10 en μg/m3", 1, 100, 20, step=1)
    concentration_pm25 = st.sidebar.slider("Concentration du PM2.5 en μg/m3", 1, 50, 10, step=1)

    st.sidebar.markdown("<h2 style='text-align: center;'>Options IA Indice ATMO</h2>", unsafe_allow_html=True)
    no2 = st.sidebar.slider("Qualité NO2", 1, 4, 1, step=1)
    so2 = st.sidebar.slider("Qualité SO2", 1, 4, 1, step=1)  # inutile dans l'apprentissage
    o3 = st.sidebar.slider("Qualité O3", 1, 4, 1, step=1)
    pm10 = st.sidebar.slider("Qualité PM 10", 1, 4, 1, step=1)
    pm25 = st.sidebar.slider("Qualité PM2.5", 1, 4, 1, step=1)
    st.sidebar.text("1: Bon / 2: Moyen")
    st.sidebar.text("3: Dégradé / 4: Mauvais")

    st.subheader("En fonction des concentrations des polluants")
    st.write(
        "Réglez les concentrations des différents polluants via le menu afin de prédire la qualité de l'air aux différentes stations bretonnes")
    liste_prediction = machine_learning_concentration(concentration_no2, concentration_pm10, concentration_pm25)

    liste_ville = ["Brest", "Lorient", "Rennes", "Saint-Malo", "Vannes"]
    liste_coordonnees = [0 for _ in range(len(liste_ville))]
    liste_NO2 = [str(concentration_no2)+" μg/m3" for _ in range(len(liste_ville))]
    liste_PM25 = [str(concentration_pm25)+" μg/m3" for _ in range(len(liste_ville))]
    liste_PM10 = [str(concentration_pm10)+" μg/m3" for _ in range(len(liste_ville))]




    datajouractuel = {'ville': liste_ville, 'code_qual': liste_prediction, 'x_wgs84': liste_coordonnees,
                      "y_wgs84": liste_coordonnees, "concentration_NO2": liste_NO2, "concentration_PM25": liste_PM25,
                      "concentration_PM10": liste_PM10}
    datajouractuel = pd.DataFrame(data=datajouractuel)
    datajouractuel.loc[datajouractuel.ville == "Brest", "x_wgs84"] = -4.48
    datajouractuel.loc[datajouractuel.ville == "Brest", "y_wgs84"] = 48.37
    datajouractuel.loc[datajouractuel.ville == "Lorient", "x_wgs84"] = -3.37
    datajouractuel.loc[datajouractuel.ville == "Lorient", "y_wgs84"] = 47.72
    datajouractuel.loc[datajouractuel.ville == "Rennes", "x_wgs84"] = -1.68
    datajouractuel.loc[datajouractuel.ville == "Rennes", "y_wgs84"] = 48.1
    datajouractuel.loc[datajouractuel.ville == "Saint-Malo", "x_wgs84"] = -2
    datajouractuel.loc[datajouractuel.ville == "Saint-Malo", "y_wgs84"] = 48.62
    datajouractuel.loc[datajouractuel.ville == "Vannes", "x_wgs84"] = -2.75
    datajouractuel.loc[datajouractuel.ville == "Vannes", "y_wgs84"] = 47.64


    # Mise en place d'un dico qui contient nos couleurs car on ne sait pas comment est structuré le nouveau fichier
    colorsdict = {"#DDDDDD": 0, "#50F0E6": 1, "#50CCAA": 2, "#F0E641": 3, "#FF5050": 4, "#960032": 5, "#872181": 6,
                  "#888888": 7, "#747474": "Indisponible"}

    afficher_carte(colorsdict, datajouractuel)

    with st.expander("Informations sur le modèle de Machine Learning utilisé :"):
        st.markdown("""
                        <p>
                            <li>Le modèle choisi pour entraîner notre modèle est une descente de gradient stochastique.</li>
                            <li>5 modèles de Machine Learning ont été associé à chaque ville : Brest ,Lorient ,Renne ,Saint Malo ,Vannes.</li>
                            <li>Les entrées de notre modèle sont les concentrations des polluants : NO2,PM10,PM2.5 en μg/m3.</li>
                            <li>La sortie de notre modèle est l'indice qualité ATMO de l'air estimé sur une ville.</li>
                            <li>Les données concernent différentes villes de la région bretonne et sont issues du site Opendata AirBreizh.</li>
                            <li>La date n'a pas été utilisée lors de l'apprentissage du modèle de Machine Learning.</li>
                        </p>""", unsafe_allow_html=True)

    #############################################################################################
    st.subheader("En fonction des indices qualité ATMO des polluants")
    st.write(
        "Réglez les indices des différents polluants via le menu afin de prédire la qualité de l'air adéquate en Bretagne")
    modele_ia, model_normalisation = machine_learning_indice(df)
    predictionlibre = ia_ml_prediction(modele_ia, model_normalisation, no2, o3, pm10, pm25)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        col1.metric("NO2", no2)
    with col2:
        col2.metric("SO2", so2)  # inutile dans l'apprentissage
    with col3:
        col3.metric("O3", o3)
    with col4:
        col4.metric("PM10", pm10)
    with col5:
        col5.metric("PM2.5", pm25)

    st.metric("Qualité de l'air prédite", str(predictionlibre[0]))

    for _ in range(3):
        st.write('\n')
    with st.expander("Informations sur le modèle de Machine Learning utilisé :"):
        st.markdown("""
                        <p>
                            <li>Le modèle choisi pour entraîner notre modèle est un apprentissage ensembliste Soft contenant les algorithmes de descente de gradient stochastique et de forêts d'arbres décisionnels.</li>
                            <li>Les entrées de notre modèle sont les indices ATMO des polluants : NO2,O3,PM10,PM2.5.</li>
                            <li>La sortie de notre modèle est l'indice qualité ATMO de l'air estimé en Bretagne.</li>
                            <li>Les données concernent différentes villes de la région bretonne et sont issues du site Opendata AirBreizh.</li>
                            <li>Le polluant SO2 n'a pas servi lors de l'apprentissage car celui-ci ne varie jamais.</li>
                            <li>La date n'a pas été utilisée lors de l'apprentissage du modèle de Machine Learning.</li>
                        </p>""", unsafe_allow_html=True)


def afficher_carte(colorsdict, dataframejouractuel):
    # Fonction permettant de créer une carte dédiée à l'étude de la Bretagne avec les contours de la région)
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/streets-v11",
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

            'html': '<b>Zone:</b> {ville}'
                    '<br><b>Indice Qualité</b> : {code_qual}'
                    '<br><b>Concentration NO2</b> : {concentration_NO2}'
                    '<br><b>Concentration PM10</b> : {concentration_PM10}'
                    '<br><b>Concentration PM2.5</b> : {concentration_PM25}',
            "style": {
                "color": "white"
            }

        }
    ))


def pdkLayer(Data, code_qual, Hex_color, radius=4500):
    color = ImageColor.getcolor(Hex_color, "RGB")
    Layer = pdk.Layer(
        'ScatterplotLayer',
        data=Data.loc[Data['code_qual'] == code_qual],
        get_position='[x_wgs84, y_wgs84]',
        # get_fill_color='[150 200 255]',  # Set an RGBA value for fill
        get_fill_color=color,  # Set an RGBA value for fill
        get_radius=radius,
        pickable=True,
        auto_highlight=True
    )
    return Layer
