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
        usd_cop = data['rates']['COP']
        usd_brl = data['rates']['BRL']
        return usd_cop, usd_cop / usd_brl
    except:
        return 3950.0, 780.0

usd_hoy, brl_hoy = obtener_tasas()
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ESTILOS MODO OSCURO PRO (BRASIL GOLD) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; }}
    h1, h2, h3 {{ color: #ffdf00 !important; text-align: center; font-family: 'Arial Black', sans-serif; }}
    p, span, label, .stMarkdown {{ color: #ffffff !important; }}
    .stTabs [data-baseweb="tab-list"] {{ background-color: #1a1c24; border-radius: 10px; padding: 5px; gap: 10px; }}
    .stTabs [aria-selected="true"] {{ background-color: #009c3b !important; color: white !important; border-radius: 7px; }}
    .stTable, [data-testid="stTable"] {{ background-color: #1a1c24; color: white !important; border-radius: 10px; }}
    [data-testid="stTable"] td, [data-testid="stTable"] th {{ color: white !important; border-bottom: 1px solid #31333f; }}
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("<h1>🚀 MISIÓN BRASIL 2026: RUTA REFINADA</h1>", unsafe_allow_html=True)
st.write("---")

# --- PESTAÑAS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️ RUTA 19 DÍAS", "⚽ MATI Y ABUELO", "🎢 BIANCA Y MATI", "🥂 LOS CONSENTIDOS", "💰 PRESUPUESTO"
])

with tab1:
    st.markdown("### ✈️ Configuración de Llegada (26 Dic)")
    horario_vuelo = st.radio("Hora de aterrizaje en SP:", ["Mañana", "Tarde/Noche"], horizontal=True)
    
    # Lógica de primeros días
    p_26 = "Llegada y Museo del Fútbol." if "Mañana" in horario_vuelo else "Llegada, check-in y descanso."
    
    it_data = [
        {"Fecha": "26 Dic", "Trayecto": "Llegada SP", "Hospedaje": "São Paulo", "Plan": p_26},
        {"Fecha": "27 Dic", "Trayecto": "Estancia SP", "Hospedaje": "São Paulo", "Plan": "Compras en Jardins y gran cena familiar."},
        {"Fecha": "28 Dic", "Trayecto": "SP -> Balneário", "Hospedaje": "Baln. Camboriú", "Plan": "Viaje al sur (6h). Cena en la 'Dubai' brasileña."},
        {"Fecha": "29 Dic", "Trayecto": "BC -> Beto Carrero", "Hospedaje": "Baln. Camboriú", "Plan": "🎢 DÍA 1: Adrenalina pura para Bianca y Mati."},
        {"Fecha": "30 Dic", "Trayecto": "BC -> Beto Carrero", "Hospedaje": "Baln. Camboriú", "Plan": "🎢 DÍA 2: Repetición y shows imperdibles."},
        {"Fecha": "31 Dic", "Trayecto": "Año Nuevo (BC)", "Hospedaje": "Baln. Camboriú", "Plan": "Playa y fuegos artificiales de gala."},
        {"Fecha": "01 Ene", "Trayecto": "BC -> Curitiba", "Hospedaje": "Curitiba", "Plan": "Salida 11 AM hacia Curitiba (3h). Cena tranquila."},
        {"Fecha": "02 Ene", "Trayecto": "Curitiba -> Santos", "Hospedaje": "Santos", "Plan": "🌿 Jardín Botánico (Mañana) y bajada a Santos (5h)."},
        {"Fecha": "03 Ene", "Trayecto": "Santos -> Paraty", "Hospedaje": "Paraty", "Plan": "⚽ Vila Belmiro y salida por la tarde a Paraty (3.5h)."},
        {"Fecha": "04 Ene", "Trayecto": "Estancia Paraty", "Hospedaje": "Paraty", "Plan": "Caminata histórica y fotos coloniales."},
        {"Fecha": "05 Ene", "Trayecto": "Paraty -> Río", "Hospedaje": "Río de Janeiro", "Plan": "Llegada por la costa. Atardecer en Ipanema."},
        {"Fecha": "06 Ene", "Trayecto": "Estancia Río", "Hospedaje": "Río de Janeiro", "Plan": "⚽ Maracanã y AquaRio."},
        {"Fecha": "07 Ene", "Trayecto": "Estancia Río", "Hospedaje": "Río de Janeiro", "Plan": "Cristo Redentor y Pan de Azúcar."},
        {"Fecha": "08 Ene", "Trayecto": "Río -> Búzios", "Hospedaje": "Búzios", "Plan": "🥂 Paraíso chic: Playas y buena mesa."},
        {"Fecha": "09 Ene", "Trayecto": "Estancia Búzios", "Hospedaje": "Búzios", "Plan": "Relax total, compras y vino frente al mar."},
        {"Fecha": "10 Ene", "Trayecto": "Búzios -> BH", "Hospedaje": "Belo Horizonte", "Plan": "☕ Salida a Minas (8h). Cena de comida minera."},
        {"Fecha": "11 Ene", "Trayecto": "Estancia BH", "Hospedaje": "Belo Horizonte", "Plan": "⚽ Mineirão y Mercado Central."},
        {"Fecha": "12 Ene", "Trayecto": "BH -> Ouro Preto", "Hospedaje": "Belo Horizonte", "Plan": "Día de historia barroca y tesoros coloniales."},
        {"Fecha": "13 Ene", "Trayecto": "BH -> SP -> Vuelo", "Hospedaje": "---", "Plan": "Regreso a base y traslado al aeropuerto."}
    ]
    st.table(pd.DataFrame(it_data))

# --- LAS PESTAÑAS VISUALES (Se mantienen con el contenido previo) ---
with tab2:
    st.header("🏟️ El Tour de los Estadios")
    st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/maracana.jpg", caption="Maracanã")
    st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/santos.jpg", caption="Vila Belmiro")

with tab3:
    st.header("🎢 Territorio Bianca & Mati")
    st.image("https://images.unsplash.com/photo-1513889959013-c2845acb46ad?q=80&w=800", caption="Beto Carrero World")

with tab4:
    st.header("🥂 El Club de los Consentidos")
    st.write("Vinos en Búzios, Compras en SP y Gastronomía en Minas.")
