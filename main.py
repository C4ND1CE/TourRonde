import streamlit as st

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
</style>
"""

# Init session state
if "page" not in st.session_state:
    st.session_state.page = "Accueil"
if "show_submenu" not in st.session_state:
    st.session_state.show_submenu = False

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
                background-color: #45a049 !important;
                color: white !important;
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



# Barre latérale
with st.sidebar:
    st.markdown("### Navigation")
    if st.button("Accueil"):
        st.session_state.page = "Accueil"
    if st.button("Mon Travail"):
        st.session_state.page = "Travail"
    if st.button("Qualité"):
        st.session_state.show_submenu = not st.session_state.show_submenu
    if st.session_state.show_submenu:
        if st.button("Contrôle Qualité"):
            st.session_state.page = "Qualité"
        st.button("Planning Qualité", disabled=True)

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
        st.button("Tableau de Bord", key="btn_dashboard", disabled=True)

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
            st.button("Planning Qualité", key="btn_planning_accueil", disabled=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Page Mon Travail
def page_travail():
    st.markdown(STYLE, unsafe_allow_html=True)
    bouton_maison()
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown("<h2>Mon Travail</h2>", unsafe_allow_html=True)
    st.markdown("<h3>Tours de Ronde</h3>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 4, 3])

    with col1:
        st.markdown("<p style='margin-top: 12px;'>Vous avez</p>", unsafe_allow_html=True)

    with col2:
        if st.button("1 tour de ronde", key="btn_tour_ronde"):
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

# Page Qualité
def page_qualite():
    st.markdown(STYLE, unsafe_allow_html=True)
    bouton_maison()
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown("<h2>Liste d'Équipements à Vérifier</h2>", unsafe_allow_html=True)

    for i in range(1, 4):
        st.selectbox(f"Équipement {i}", ["OK", "Not OK"], key=f"eq_{i}")
    for i in range(4, 6):
        st.radio(f"Équipement {i}", ["😞", "😐", "😊"], horizontal=True, key=f"eq_{i}")
    for i in range(6, 9):
        st.number_input(f"Équipement {i}", key=f"eq_{i}")
    for i in range(9, 11):
        st.slider(f"Équipement {i}", 0, 10, 5, key=f"eq_{i}")

    if st.button("Valider", key="btn_retour_qualite"):
        st.session_state.page = "Accueil"
    st.markdown("</div>", unsafe_allow_html=True)

# Gestion des paramètres URL
params = st.query_params
if "page" in params:
    page_param = params["page"][0]
    if page_param in ["Accueil", "Travail", "Qualité"]:
        st.session_state.page = page_param

# Routing
if st.session_state.page == "Accueil":
    page_accueil()
elif st.session_state.page == "Travail":
    page_travail()
elif st.session_state.page == "Qualité":
    page_qualite()
