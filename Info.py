import streamlit as st
import base64
from ImpactCovid import creating_space


def fenetre_info_utiles():
    # Import des images png en local file
    tableauimage = "ressources/tableau.png"
    no2 = "ressources/no2.jpg"
    so2 = "ressources/so2.jpg"
    o3 = "ressources/O3.jpg"
    pm = "ressources/pm.jpg"
    # Mise en place du css
    st.markdown("""
    <style>
        .text{
            text-align: justify;
        }
        .tableaulegende{
            width:65%;
            text-align:center;
            margin-left: auto;
            margin-right: auto;
        }
        p{
            font-size: 1.2rem;
        }
       .no2image{
            margin-left:auto;
            display:block;
        }
        .no2image2{
            margin-right:auto;
            display:block;
        }
        .o3image{
            margin-left:auto;
            display:block;
        }
        .pmimage{
            margin-right:auto;
            display:block;
        }
    </style>               
    """, unsafe_allow_html=True)

    # Mise en place du texte et des images
    st.markdown(f"""
    <div class="infopage">
        <div class="text">
            <h3>Pourquoi l’étude de la qualité de l’air est importante ?</h3>
            <p>La qualité de l’air s’est nettement dégradée ces dernières décennies, notamment dans les contextes très urbains c'est-à-dire les villes et agglomérations de plus de 100 000 habitants.  Or, nous savons que l’air, accompagné des nombreux polluants qu’il véhicule, a un impact non négligeable sur la santé humaine. En effet, selon l’OMS, la pollution de l’air est le principal risque environnemental pour la santé dans le monde. L’exposition à la pollution de l’air extérieur conduirait ainsi chaque année au décès d'un peu plus de <a id="source"href="https://www.euro.who.int/fr/health-topics/environment-and-health/air-quality/news/news/2014/03/almost-600-000-deaths-due-to-air-pollution-in-europe-new-who-global-report" target="_blank" rel="noopener noreferrer">5 millions de personnes dans le monde</a> dont près de <a id="source"href="https://www.santepubliquefrance.fr/presse/2021/pollution-de-l-air-ambiant-nouvelles-estimations-de-son-impact-sur-la-sante-des-francais#:~:text=Elle%20conclut%20que%20la%20mortalit%C3%A9,(PM2%2C5)." target="_blank" rel="noopener noreferrer">40 000 décès annuels en France</a>. Elle devient ainsi dans notre pays la troisième cause de mortalité, derrière le tabagisme (78 000 décès) et l'alcoolisme (49 000 décès).
                <br> 
                <br> 
                En plus d’entraîner des conséquences néfastes sur notre santé, la qualité de l’air peut également entraîner impacter celle des êtres vivants, mais aussi le climat et les biens matériels. C’est pourquoi son étude est primordiale et c’est d’ailleurs grâce aux réglementions appliquées en conséquence que la qualité de l’air tend à s’améliorer depuis vingt ans.
            </p>    
            <h3>Comment se déroule son étude ? </h3>
            <p>En France, Il existe principalement deux indices de qualité d'air, appliqués selon la taille de l'agglomération. Si cette dernière comporte plus de 100 000 habitants, c’est l’indice ATMO qui est mis en place. En revanche, si la zone concernée regroupe moins de 100 000 habitants, c’est l’indice IQA, une version plus simplifiée, qui est au rendez-vous.
                <br> 
                <br> 
                Dans le cas de la région bretonne, c’est donc l’indice ATMO qui est appliqué. Cet indice est diffusé par des associations agréées de surveillance de la qualité de l’air (AASQA). Parmi elles, nous retrouvons <a id="source"href="https://data.airbreizh.asso.fr/contenu/services_didon.html" target="_blank" rel="noopener noreferrer"> Air Breizh</a>, organisme dont nous avons exploiter l’Open Data.  
                <br> 
                <br> 
                À sa création, l’indice ATMO classait la qualité de l’air selon 10 classes, allant de "Très mauvais" à "Très bon" selon l’étude de différents polluants détaillés ci-dessous. Mais depuis le 1er janvier 2021, l’indice intègre un nouveau polluant réglementé : les particules fines PM2,5, aux effets sanitaires avérés. La révision de cet indice est également accompagnée d’une nouvelle échelle, composée de 6 catégories allant de "Extrêmement mauvais" à "Bon". 
                <br> 
                <br> 
                Cet indice est calculé quotidiennement à partir des concentrations des 5 polluants réglementés suivants : 
                <br> - les particules fines dont le diamètre est inférieur à 10 micromètres (PM10)
                <br> - les particules fines dont le diamètre est inférieur à 2.5 micromètres (PM2.5)
                <br> - le dioxyde d’azote (NO2)
                <br> - l’ozone (O3)
                <br> - le dioxyde de soufre (SO2)
                <br><br>
                Grâce au tableau ci-dessous, chaque concentration peut être classée selon sa valeur dans une des catégories de l'indice ATMO.
            </p>
        </div>
        <div class="tableaulegende">   
            <img class="tableaulegende" src="data:image/png;base64,{base64.b64encode(open(tableauimage, "rb").read()).decode()}" alt=legendetableau> 
            <p>Source de l'infographie : <a id="source"href="http://www.atmo-grandest.eu/" target="_blank" rel="noopener noreferrer">ATMO Grand Est</a></p> 
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Description des polluants
    st.subheader("En savoir plus sur chaque polluant")
    # NO2
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        <div class="text">
            <p><b>Oxyde d'azote(NO2):</b> Ils apparaissent par oxydation de l’azote atmosphérique (N2) lors de toutes combustions, à haute température, de combustibles fossiles (charbon, fuel, pétrole…). Le dioxyde d’azote (NO2) pénètre dans les voies respiratoires profondes, où il fragilise la muqueuse pulmonaire face aux agressions infectieuses, notamment chez les enfants. Les NOx contribuent aux phénomènes des pluies acides (qui affectent les végétaux et les sols) et à l’augmentation de la concentration des nitrates dans le sol. Sous l’effet du soleil, ils participent à la formation d’ozone troposphérique et donc indirectement à l’accroissement de l’effet de serre.<p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <img class="no2image" src="data:image/jpg;base64,{base64.b64encode(open(no2, "rb").read()).decode()}" alt=no2image width=80%>
        """, unsafe_allow_html=True)

    creating_space(4)
    # SO2
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"""
        <img class="so2image" src="data:image/jpg;base64,{base64.b64encode(open(so2, "rb").read()).decode()}" alt=so2image width=80%>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="text">
            <p><b>Dioxyde de soufre(SO2):</b> C'est un gaz sans couleur et ininflammable avec une odeur pénétrante qui irrite les yeux et les voies respiratoires. Il provient principalement de la combustion des combustibles fossiles (charbons, fuels, …), au cours de laquelle les impuretés soufrées contenus dans les combustibles sont oxydées par l’oxygène de l’air O2 en dioxyde de soufre SO2. La combustion du charbon est la plus grande source synthétique de dioxyde de soufre représentant environ 50% des émissions globales annuelles, avec la brûlure de pétrole représentant 25-30% en plus. Les volcans sont la source naturelle la plus commune de dioxyde de soufre.</p>            
        </div>
        """, unsafe_allow_html=True)

    creating_space(4)
    # O3
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        <div class="text">
            <p><b>Ozone(O3):</b> Dans la stratosphère (10 à 50 km d’altitude en moyenne), l’ozone est présent naturellement. Il forme la couche d’ozone qui filtre une partie des rayons ultraviolets (UV) émis par le soleil et nocifs pour notre santé d’atteindre la surface de la terre. Dans la troposphère (0 à 10 km d’altitude), là où nous respirons c’est un polluant secondaire, c’est-à-dire qu’il n’est pas rejeté directement dans l’atmosphère, mais qu’il se forme par réaction photochimique à partir de précurseurs (NOx, COV…) d’origine automobile et industrielle. Capable de pénétrer profondément dans les poumons, l’ozone provoque à forte concentration une inflammation et une hyper-réactivité des bronches. Des irritations du nez et de la gorge surviennent généralement, accompagnées d’une gêne respiratoire. L’ozone a des effets néfastes sur la végétation et perturbe la croissance de certaines espèces. Il contribue à l’effet de serre.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <img class="o3image" src="data:image/jpg;base64,{base64.b64encode(open(o3, "rb").read()).decode()}" alt=o3image width=90%>
        """, unsafe_allow_html=True)

    creating_space(4)
    # PM
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"""
        <img class="pmimage" src="data:image/jpg;base64,{base64.b64encode(open(pm, "rb").read()).decode()}" alt=pmimage width=60%>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="text">
            <p><b>Particules en suspension(PM10/PM2.5):</b> Les particules fines sont d’origine naturelle ou anthropique, émises lors de la combustion de matières fossiles, transport routier, activités agricoles et industrielles. Les particules les plus grosses sont retenues par les voies aériennes supérieures. Plus elles sont fines et plus elles pénètrent profond dans l’arbre pulmonaire, elles atteignent les voies respiratoires inférieures et peuvent altérer la fonction respiratoire dans son ensemble. Certaines de ces poussières très fines servent aussi de vecteurs à différentes substances toxiques voire cancérigènes ou mutagènes, qui sont alors susceptibles de pénétrer dans le sang. La plupart des particules contribuent au refroidissement de l’atmosphère alors que d’autres, participent au réchauffement de l’atmosphère en absorbant la lumière.</b>
        </div>
        """, unsafe_allow_html=True)
