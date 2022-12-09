import streamlit as st
import datetime
from ImpactCovid import creating_space


def fenetre_a_propos():
    """PARTIE A PROPOS DE L'INTERFACE
        Cette page consiste à nous présenter ainsi que notre projet, notre interface, et nous permettre d'avoir un retour d'un utilisateur lambda.
    """
    # Premiere partie
    st.subheader("Qui sommes-nous?")
    st.markdown("""
    <style>
        .text{
            text-align: justify;
            text-justify: inter-word;
        }         
        .users{ 
          display: flex;
          justify-content: space-evenly;
          margin-bottom:2%;
        }
        .Mathieu {
            display: inline-block;
            text-align: center;
            margin-left:25%;
        }
        .users a {
            display: block;  
        }
        a:hover {
            color: #ff4b4b;
        }
        .Julian {
            display: inline-block;
            text-align: center;
            margin-right:25%;  
        }
        p{
            font-size: 1.2rem;
        }
    </style>
    <p>Véritables passionnés de data, notre binôme s'est formé il y a quelques années sur le site de l'ISEN Nantes, une école d'ingénieurs généraliste ancrée dans le monde du numérique. Cette année, nous avons décidé de rejoindre l'ISEN de Brest afin de poursuivre notre formation dans le domaine de l'intelligence artificielle, un secteur en pleine expension et à travers duquel nous nous sommes complètement retrouvés.</p>
    <div class="users">
        <div class="Mathieu">
            <img class="Mathieu-picture"
             src="https://media-exp1.licdn.com/dms/image/C4E03AQENLncwukCxTA/profile-displayphoto-shrink_400_400/0/1636026221630?e=1651708800&v=beta&t=HMYN3BcesQWpJvoVHOm6Co6FQl5GROxGqcBk0JLVJZo"
             alt="Mathieu" width=150>
             <a id="linkedin" href="https://www.linkedin.com/in/mathieu-busquet/" target="_blank" rel="noopener noreferrer">Mathieu Busquet</a>  
        </div>
        <div class="Julian">
            <img class="Julian-picture"
             src="https://media-exp1.licdn.com/dms/image/C4E03AQH-jjd9-gROkA/profile-displayphoto-shrink_800_800/0/1633625900128?e=1652918400&v=beta&t=fWQMrA-hfopVVF908CwhuaQfgSzkhpqBZvebIrxMzPc"
             alt="Julian" width=150>
             <br>
             <a id="linkedin" href="https://www.linkedin.com/in/julian-burtin-b02840222/" target="_blank" rel="noopener noreferrer">Julian Burtin</a>  
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Deuxième partie
    st.subheader("Notre projet, \"Qualité de l'air en bretagne\"")
    # Texte
    st.markdown(
        """
        <p>Dans le cadre de cette formation, nous avons sélectionné un projet d'étude autour de la qualité de l'air. Les consignes sont dans l'ensemble plutôt libres afin de favoriser une prise d'initiatives et une certaine autonomie de notre part.</p>

        <p>Pour élaborer ce projet, nous avons récupérer des relevés sur plusieurs années de la qualité de l'air fournis par l'association <a id="source"href="https://data.airbreizh.asso.fr/contenu/services_didon.html" target="_blank" rel="noopener noreferrer"> Air Breizh</a> et basés sur l'indice ATMO. Ces derniers sont disponibles en Open Data.</p>

        <p>Le but de notre étude est de permettre à un utilisateur lambda de pouvoir étudier et d'analyser la pollution atmosphérique à l'échelle de la région bretonne à travers des graphiques et des cartographies. Nous devons aussi être capable de proposer un modèle de prédiction des données pour les jours à venir.</p>

        <p>Enfin, l'interface proposée devra permettre de tenter d'effectuer un constat de l'impact de la pandémie de COVID-19 accompagnée de ses confinements sur la pollution atmosphérique de la région.</p>

        """, unsafe_allow_html=True)
    # Saut de lignes
    creating_space(2)

    # Formulaire de contact
    st.subheader("📧 Nous contacter")
    with st.form("my_form"):
        user = st.text_input('Identité / Pseudo (Optionnel)')
        feedback = st.text_area("Afin que nous améliorons votre expérience, laissez-nous une remarque.")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Envoyer")
        if submitted and feedback != "":
            now = datetime.datetime.now()
            # feedback=unidecode.unidecode(feedback) #Permet d'enlever les accents pour éviter les pb de caracteres
            date = now.strftime("%Y-%m-%d %H:%M:%S")
            sauvegarde("Feedbacks/fb.txt", user, date, feedback)
            st.write("Votre message s'est bien envoyé, Merci.")

        if submitted and feedback == "":
            st.write("Merci de compléter la case remarque afin de nous l'envoyer.")


def sauvegarde(path, user, date, text):
    """
    :param text: Remarque écrite
    :param date: Date à laquelle le message a été écrit et reçu
    :param user: Nom d'utilisateur / Identité de la personne
    :param path: Chemin du fichier txt contenant les remarques

    Objectif: sauvegarder la remarque de l'utilisateur dans un fichier txt
    """
    file = open_file(path)
    file.write(user+" - "+date+"\n"+text+"\n\n")
    file.close()


def open_file(path):
    """
    :param path: chemin du fichier
    :return: ouverture et/ou création du fichier
    """
    return open(path, "a+")
