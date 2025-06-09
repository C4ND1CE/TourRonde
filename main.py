import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from calendar import monthrange
import matplotlib.pyplot as plt

STYLE = """
<style>
body {
    font-family: Arial, sans-serif;
}
.stButton > button {
    border-radius: 20px;
    background-color: #4CAF50;
    color: white;
    padding: 10px 24px;
    border: none;
    cursor: pointer;
    width: 150px;
    height: 50px;
    font-size: 16px;
}
.stButton > button:hover {
    background-color: #45a049;
}

.home-button-container {
    position: fixed;
    left: 150px;
    top: 150px;
    z-index: 1000;
}
.home-button {
    border-radius: 50%;
    width: 150px;
    height: 150px;
    font-size: 120px;
    cursor: pointer;
    background-color: #45a049;
    color: white;
    border: none;
}
.home-button:hover {
    background-color: #45a049;
}
#submenu {
    display: block;
    text-align: center;
    margin-top: 20px;
    border-radius: 8px;
    padding: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
#submenu button {
    background-color: #C8E6C9;
    color: #333;
    border-radius: 20px;
    padding: 10px 24px;
    border: none;
    cursor: pointer;
    width: 200px;
    margin: 5px;
    font-size: 16px;
}
#submenu button:hover {
    background-color: #A5D6A7;
}
/* Bouton Contrôle Qualité vert clair */
#submenu button.control-quality {
    background-color: #A5D6A7 !important;
}
#submenu button.control-quality:hover {
    background-color: #81C784 !important;
}

.calendar {
    font-family: Arial, sans-serif;
    width: 100%;
    border-collapse: collapse;
}
.weekdays {
    background-color: #f2f2f2;
}
.day {
    border: 1px solid #ddd;
    padding: 8px;
    height: 80px;
    vertical-align: top;
}
.week {
    border: 1px solid #ddd;
}
</style>
"""
st.set_page_config(
    page_title="Mon Planning Qualité",
    layout="wide",                # ← c’est cette option qui passe en mode large
    initial_sidebar_state="auto"  # ou "expanded" pour l’ouvrir d’emblée
)

CONTROLES_QUALITE = {
    "Ronde hebdo": ["Équipement 1", "Équipement 6", "Équipement 3"],
    "Ronde jour": ["Équipement 9", "Équipement 5"],
    "Ronde ligne 2": ["Équipement 3", "Équipement 7", "Équipement 8", "Équipement 9"]
}

# Init session state
if "page" not in st.session_state:
    st.session_state.page = "Accueil"
if "show_submenu" not in st.session_state:
    st.session_state.show_submenu = False
if "control_results" not in st.session_state:
    st.session_state.control_results = {}

# Bouton maison avec Streamlit + CSS fixe
def bouton_maison():
    if st.session_state.page != "Accueil":
        if st.button("🏠", key="home_btn", help="Retour à l'accueil"):
            st.session_state.page = "Accueil"
        st.markdown("""
            <style>
            div[aria-label="home_btn"] > button {
                position: fixed !important;
                left: 120px !important;
                top: 120px !important;
                z-index: 1000 !important;
                border-radius: 50% !important;
                width: 350px !important;
                height: 350px !important;
                font-size: 200px !important;
                background-color: #3b8b3a !important;
                color: green !important;
                border: none !important;
                cursor: pointer !important;
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
                padding: 0 !important;
            }
            div[aria-label="home_btn"] > button:hover {
                background-color: #3b8b3a !important;
            }
            </style>
        """, unsafe_allow_html=True)

# Page Accueil
def page_accueil():
    st.markdown(STYLE, unsafe_allow_html=True)
    st.markdown('<div class="section" style="text-align: center;">', unsafe_allow_html=True)
    st.markdown("<h1>Bienvenue sur LINA Web</h1>", unsafe_allow_html=True)
    st.markdown("<p>Nous sommes ravis de vous voir ici. Explorez les fonctionnalités pour gérer vos tâches et contrôles qualité.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Mon Travail", key="btn_mon_travail"):
            st.session_state.page = "Travail"
    with col2:
        if st.button("Qualité", key="btn_qualite"):
            st.session_state.show_submenu = not st.session_state.show_submenu
    with col3:
        if st.button("Tableau de Bord", key="btn_dashboard"):
            st.session_state.page = "Tableau de Bord"

    if st.session_state.show_submenu:
        st.markdown('<div id="submenu">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            # Ajout de la classe CSS control-quality pour bouton vert clair
            if st.button("Contrôle Qualité", key="btn_controle_accueil"):
                st.session_state.page = "Qualité"
            # Hack CSS pour ce bouton spécifique (il faut injecter un style JS, donc on fera par CSS)
            st.markdown("""
            <style>
            div[aria-label="btn_controle_accueil"] button {
                background-color: #A5D6A7 !important;
            }
            div[aria-label="btn_controle_accueil"] button:hover {
                background-color: #81C784 !important;
            }
            </style>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("Planning Qualité", key="btn_planning_accueil"):
                st.session_state.page = "Planning"
            st.markdown("""
            <style>
            div[aria-label="btn_controle_accueil"] button {
                background-color: #A5D6A7 !important;
            }
            div[aria-label="btn_controle_accueil"] button:hover {
                background-color: #81C784 !important;
            }
            </style>
            """, unsafe_allow_html=True)

# Page Mon Travail
def page_travail():
    st.markdown(STYLE, unsafe_allow_html=True)
    bouton_maison()
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown("<h2>Mon Travail</h2>", unsafe_allow_html=True)
    st.markdown("<h3>Tours de Ronde</h3>", unsafe_allow_html=True)

    today_str = datetime.now().strftime("%Y-%m-%d")

    # Vérifiez si 'controls' existe dans session_state et s'il contient des entrées pour aujourd'hui
    if 'controls' not in st.session_state or today_str not in st.session_state.controls:
        nb_tours = 0
    else:
        # Comptez le nombre de contrôles pour aujourd'hui
        nb_tours = len(st.session_state.controls[today_str])

    # Afficher le nombre de tours
    st.write(f"Nombre de tours aujourd'hui : {nb_tours}")


    col1, col2, col3 = st.columns([1, 4, 3])

    with col1:
        st.markdown("<p style='margin-top: 12px;'>Vous avez</p>", unsafe_allow_html=True)

    with col2:
        if st.button(f"{nb_tours} tour{'s' if nb_tours != 1 else ''} de ronde", key="btn_tour_ronde"):
            st.session_state.page = "Qualité"

    with col3:
        st.markdown("<p style='margin-top: 12px;'>à effectuer aujourd'hui.</p>", unsafe_allow_html=True)

    st.markdown("<h3>Liste d'Observations à Traiter</h3>", unsafe_allow_html=True)
    st.markdown("""
    <table>
        <thead>
            <tr>
                <th>Date</th><th>Thème</th><th>Zone Usine</th><th>Équipement</th>
                <th>Auteur</th><th>Niveau de Gravité</th><th>Risque</th>
                <th>Transmettre au service</th><th>Statut</th><th>Modifier le statut</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>2025-01-15</td><td>SupplyChain</td><td>réception</td><td>balance</td>
                <td>Phil</td><td>Sécurité des hommes</td><td>Moyen</td><td>Maintenance</td>
                <td>En cours de traitement</td>
                <td><select><option selected>En cours de traitement</option><option>Problème déclaré</option><option>Résolu</option></select></td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("<h3>To-Do Liste</h3>", unsafe_allow_html=True)
    st.checkbox("Tâche 1", key="todo_1")
    st.checkbox("Tâche 2", key="todo_2")
    st.checkbox("Tâche 3", key="todo_3")
    if st.button("Retour", key="btn_retour_travail"):
        st.session_state.page = "Accueil"
    st.markdown("</div>", unsafe_allow_html=True)

def page_qualite():
    st.markdown(STYLE, unsafe_allow_html=True)
    bouton_maison()
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown("<h2>Liste d'Équipements à Vérifier</h2>", unsafe_allow_html=True)

    # Sélectionnez une date pour voir les contrôles planifiés
    selected_date = st.date_input("Sélectionnez une date", datetime.now(), key="date_input_qualite")

    # Récupérer les contrôles pour la date sélectionnée
    selected_date_str = selected_date.strftime("%Y-%m-%d")
    controls_for_date = st.session_state.controls.get(selected_date_str, [])

    # Afficher les contrôles planifiés pour la date sélectionnée
    for control in controls_for_date:
        st.markdown(f"### Contrôle: {control}")
        st.markdown("#### Équipements à contrôler:")

        for equipement in CONTROLES_QUALITE.get(control, []):
            equipement_num = int(equipement.split()[1])

            if equipement_num < 4:
                result = st.selectbox(f"{equipement}", ["OK", "Not OK"], key=f"eq_{equipement_num}_{control}")
            elif equipement_num < 6:
                result = st.radio(f"{equipement}", ["😞", "😐", "😊"], horizontal=True, key=f"eq_{equipement_num}_{control}")
            elif equipement_num < 9:
                result = st.number_input(f"{equipement}", key=f"eq_{equipement_num}_{control}")
            else:
                result = st.slider(f"{equipement}", 0, 10, 5, key=f"eq_{equipement_num}_{control}")

            # Enregistrer le résultat du contrôle
            if selected_date_str not in st.session_state.control_results:
                st.session_state.control_results[selected_date_str] = {}
            st.session_state.control_results[selected_date_str][equipement] = result

    if st.button("Valider", key="btn_valider_qualite"):
        st.success("Résultats des contrôles enregistrés avec succès!")
        # Vous pouvez ajouter ici une logique pour traiter les résultats enregistrés

    if st.button("Retour", key="btn_retour_qualite"):
        st.session_state.page = "Accueil"
    st.markdown("</div>", unsafe_allow_html=True)



def display_calendar(year, month):
    num_days = monthrange(year, month)[1]
    start_day = monthrange(year, month)[0]

    month_str = str(month).zfill(2)

    days = [""] * start_day + [str(i) for i in range(1, num_days + 1)]
    weeks = [days[i:i + 7] for i in range(0, len(days), 7)]

    st.markdown(f"<h3>{datetime(year, month, 1).strftime('%B')} {year}</h3>", unsafe_allow_html=True)

    calendar_html = """
    <table class="calendar">
        <tr class="weekdays">
            <th class="day">Lundi</th>
            <th class="day">Mardi</th>
            <th class="day">Mercredi</th>
            <th class="day">Jeudi</th>
            <th class="day">Vendredi</th>
            <th class="day">Samedi</th>
            <th class="day">Dimanche</th>
        </tr>
    """

    for week in weeks:
        calendar_html += "<tr class='week'>"
        for day in week:
            if day:
                day_key = f"{year}-{month_str}-{day.zfill(2)}"
                controls = st.session_state.controls.get(day_key, [])
                content = f"{day}<br>" + "<br>".join(controls)
            else:
                content = "&nbsp;"
            calendar_html += f"<td class='day'>{content}</td>"
        calendar_html += "</tr>"

    calendar_html += "</table>"
    st.markdown(calendar_html, unsafe_allow_html=True)

def page_planning():
    st.markdown(STYLE, unsafe_allow_html=True)
    bouton_maison()

    if 'controls' not in st.session_state:
        st.session_state.controls = {}

    col1, col2 = st.columns([3, 1])
    today = datetime.now()

    with col1:
        st.markdown("### Calendrier")
        display_calendar(today.year, today.month)

    with col2:
        st.markdown("### Ajouter un Contrôle Qualité")
        selected_date = st.date_input("Sélectionnez une date", today, key="date_input")

        # Sélectionnez un contrôle qualité prédéfini
        controle_selectionne = st.selectbox(
            "Sélectionnez un type de contrôle",
            options=list(CONTROLES_QUALITE.keys()),
            key="select_controle_planning"
        )

        if st.button("Ajouter", key="add_button"):
            sd = selected_date.strftime("%Y-%m-%d")

            if sd in st.session_state.controls:
                st.session_state.controls[sd].append(controle_selectionne)
            else:
                st.session_state.controls[sd] = [controle_selectionne]

            st.success(f"✅ Contrôle ajouté le {sd} : « {controle_selectionne} »")

    if st.button("Retour"):
        st.session_state.page = "Accueil"

def page_tableau_de_bord():
    st.markdown(STYLE, unsafe_allow_html=True)
    bouton_maison()
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown("<h2>Tableau de Bord</h2>", unsafe_allow_html=True)

    # Compter le nombre total de contrôles et de non-conformités
    total_controls = 0
    non_conformes = 0

    for date, results in st.session_state.control_results.items():
        for equipement, result in results.items():
            total_controls += 1
            if result == "Not OK" or result == "😞":
                non_conformes += 1

    # Afficher les statistiques
    st.write(f"Total des contrôles effectués: {total_controls}")
    st.write(f"Nombre de non-conformités: {non_conformes}")

    # Créer un graphique en camembert
    if total_controls > 0:
        conformes = total_controls - non_conformes
        data = [conformes, non_conformes]
        labels = ['Conformes', 'Non Conformes']

        # Utiliser des colonnes pour organiser la mise en page
        col1, col2 = st.columns(2)

        with col1:
            # Créer un graphique en camembert
            fig, ax = plt.subplots()
            ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#4CAF50', '#F44336'])
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig)

# Gestion des paramètres URL
params = st.query_params
if "page" in params:
    page_param = params["page"][0]
    if page_param in ["Accueil", "Travail", "Qualité", "Planning","Tableau de Bord"]:
        st.session_state.page = page_param

# Routing
if st.session_state.page == "Accueil":
    page_accueil()
elif st.session_state.page == "Travail":
    page_travail()
elif st.session_state.page == "Qualité":
    page_qualite()
elif st.session_state.page == "Planning":
    page_planning()
elif st.session_state.page == "Tableau de Bord":
    page_tableau_de_bord()
