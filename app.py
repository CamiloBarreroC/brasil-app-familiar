import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests

# 1. Configuración de la página
st.set_page_config(page_title="Misión Brasil 2026", page_icon="🇧🇷", layout="wide")

# --- FUNCIÓN: TASAS DE CAMBIO ---
@st.cache_data(ttl=3600)
def obtener_tasas():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        return data['rates']['COP'], data['rates']['COP'] / data['rates']['BRL']
    except: return 3950.0, 780.0

usd_hoy, brl_hoy = obtener_tasas()
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ESTILOS MODO OSCURO PRO (BRASIL GOLD) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; }}
    h1, h2, h3 {{ color: #ffdf00 !important; text-align: center; font-family: 'Arial Black', sans-serif; }}
    p, span, label, .stMarkdown {{ color: #ffffff !important; }}
    .stTabs [data-baseweb="tab-list"] {{ background-color: #1a1c24; border-radius: 10px; padding: 5px; gap: 10px; }}
    .stTabs [data-baseweb="tab"] {{ color: #ffffff !important; font-weight: bold; }}
    .stTabs [aria-selected="true"] {{ background-color: #009c3b !important; color: white !important; border-radius: 7px; }}
    .stTable, [data-testid="stTable"] {{ background-color: #1a1c24; color: white !important; border-radius: 10px; }}
    [data-testid="stTable"] td, [data-testid="stTable"] th {{ color: white !important; border-bottom: 1px solid #31333f; }}
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("<h1>🚀 MISIÓN BRASIL 2026: EL EJE IMPERIAL</h1>", unsafe_allow_html=True)
st.write("---")

# --- PESTAÑAS ---
tab1, tab_map, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️ RUTA 19 DÍAS", "📍 RECORRIDO", "⚽ MATI Y ABUELO", "🎢 BIANCA Y MATI", "🥂 LOS CONSENTIDOS", "💰 PRESUPUESTO"
])

with tab1:
    st.markdown("### ✈️ Configuración de Llegada (26 Dic)")
    horario_vuelo = st.radio("Hora de aterrizaje en SP:", ["Mañana", "Tarde/Noche"], horizontal=True)
    
    p_26 = "Aterrizaje y Visita al MUSEO DEL FÚTBOL (Pacaembú)." if "Mañana" in horario_vuelo else "Llegada al hotel y descanso."
    
    it_data = [
        {"Fecha": "26 Dic", "Trayecto": "Llegada SP", "Hospedaje": "São Paulo", "Plan": p_26},
        {"Fecha": "27 Dic", "Trayecto": "Estancia SP", "Hospedaje": "São Paulo", "Plan": "Compras en Oscar Freire y cena familiar."},
        {"Fecha": "28 Dic", "Trayecto": "SP -> Balneário", "Hospedaje": "Baln. Camboriú", "Plan": "Viaje al sur (6h). Cena en la 'Dubai' brasileña."},
        {"Fecha": "29 Dic", "Trayecto": "BC -> Beto Carrero", "Hospedaje": "Baln. Camboriú", "Plan": "🎢 DÍA 1 PARQUE: Adrenalina pura."},
        {"Fecha": "30 Dic", "Trayecto": "BC -> Beto Carrero", "Hospedaje": "Baln. Camboriú", "Plan": "🎢 DÍA 2 PARQUE: Shows y Hot Wheels."},
        {"Fecha": "31 Dic", "Trayecto": "Año Nuevo (BC)", "Hospedaje": "Baln. Camboriú", "Plan": "Reveillón de gala con fuegos artificiales."},
        {"Fecha": "01 Ene", "Trayecto": "BC -> Curitiba", "Hospedaje": "Curitiba", "Plan": "Salida 11 AM (3h). Relax y cena en Curitiba."},
        {"Fecha": "02 Ene", "Trayecto": "Curitiba -> Santos", "Hospedaje": "Santos", "Plan": "🌿 Jardín Botánico y bajada a Santos."},
        {"Fecha": "03 Ene", "Trayecto": "Santos -> Paraty", "Hospedaje": "Paraty", "Plan": "⚽ Vila Belmiro y ruta escénica a Paraty."},
        {"Fecha": "04 Ene", "Trayecto": "Estancia Paraty", "Hospedaje": "Paraty", "Plan": "Caminata histórica y fotos coloniales."},
        {"Fecha": "05 Ene", "Trayecto": "Paraty -> Río", "Hospedaje": "Río de Janeiro", "Plan": "Llegada a Copacabana por la tarde."},
        {"Fecha": "06 Ene", "Trayecto": "Estancia Río", "Hospedaje": "Río de Janeiro", "Plan": "⚽ Maracanã y AquaRio."},
        {"Fecha": "07 Ene", "Trayecto": "Estancia Río", "Hospedaje": "Río de Janeiro", "Plan": "Cristo Redentor y Pan de Azúcar."},
        {"Fecha": "08 Ene", "Trayecto": "Río -> Petrópolis", "Hospedaje": "Petrópolis", "Plan": "🏰 Subida a la Ciudad Imperial (2h). Tour Histórico."},
        {"Fecha": "09 Ene", "Trayecto": "Petrópolis -> BH", "Hospedaje": "Belo Horizonte", "Plan": "Viaje a Minas (5h). Cena de comida minera."},
        {"Fecha": "10 Ene", "Trayecto": "Estancia BH", "Hospedaje": "Belo Horizonte", "Plan": "⚽ Mineirão y Mercado Central."},
        {"Fecha": "11 Ene", "Trayecto": "Ouro Preto", "Hospedaje": "Belo Horizonte", "Plan": "Historia barroca e iglesias de oro."},
        {"Fecha": "12 Ene", "Trayecto": "BH -> São Paulo", "Hospedaje": "São Paulo", "Plan": "Regreso a base final y cena despedida."},
        {"Fecha": "13 Ene", "Trayecto": "Vuelo Regreso", "Hospedaje": "---", "Plan": "Últimos detalles y traslado al aeropuerto."}
    ]
    st.table(pd.DataFrame(it_data))

with tab_map:
    st.header("📍 Mapa del Recorrido Maestro")
    st.image("https://via.placeholder.com/1000x500.png?text=Sube+aquí+tu+recorrido_maestro_brasil.png", caption="Trazado oficial SP-Sur-Río-Petrópolis-Minas-SP")

with tab2:
    st.header("🏟️ Ruta de los Templos Sagrados")
    c1, c2 = st.columns(2)
    with c1: st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/maracana.jpg", caption="Maracanã")
    with c2: st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/pacaembu.jpg", caption="Museo del Fútbol")
    c3, c4 = st.columns(2)
    with c3: st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/santos.jpg", caption="Vila Belmiro")
    with c4: st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/mineirao.jpg", caption="Mineirão")

with tab3:
    st.header("🎢 Territorio Bianca & Mati")
    st.image("https://images.unsplash.com/photo-1513889959013-c2845acb46ad?q=80&w=800", caption="Beto Carrero World: Adrenalina Pura")

with tab4:
    st.header("🥂 Los Consentidos: Estilo & Historia")
    st.image("https://images.unsplash.com/photo-1590424765651-f2305886617c?q=80&w=500")
    st.markdown("""
    - **Petrópolis:** Clima de montaña, palacios y cavas de vino.
    - **Curitiba:** Caminata por el Jardín Botánico.
    - **Minas:** La mejor hospitalidad y gastronomía de Brasil.
    """)

with tab5:
    st.header("💰 Gestión de Presupuesto")
    # (Mantenemos la lógica de guardado en GSheets)
