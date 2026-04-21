import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests

# 1. Configuración de la página
st.set_page_config(page_title="Misión Brasil 2026", page_icon="🇧🇷", layout="wide")

# --- TASAS DE CAMBIO ---
@st.cache_data(ttl=3600)
def obtener_tasas():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        return data['rates']['COP'], data['rates']['COP'] / data['rates']['BRL']
    except: return 3950.0, 780.0

usd_hoy, brl_hoy = obtener_tasas()
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ESTILOS ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    h1, h2, h3 { color: #ffdf00 !important; text-align: center; }
    .stTabs [aria-selected="true"] { background-color: #009c3b !important; color: white !important; }
    .stTable { background-color: #1a1c24; color: white !important; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🚀 MISIÓN BRASIL 2026: EL ITINERARIO DEFINITIVO</h1>", unsafe_allow_html=True)

# --- PESTAÑAS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️ RUTA 19 DÍAS", "⚽ MATI Y ABUELO", "🎢 BIANCA Y MATI", "🥂 LOS CONSENTIDOS", "💰 PRESUPUESTO"
])

with tab1:
    st.markdown("### ✈️ Configuración de Llegada (26 Dic)")
    horario_vuelo = st.radio("Hora de aterrizaje en SP:", ["Mañana", "Tarde/Noche"], horizontal=True)
    
    plan_26 = "Llegada y Museo del Fútbol." if "Mañana" in horario_vuelo else "Llegada, check-in y descanso."
    
    # ITINERARIO CORREGIDO: El 1 de enero duermen en Curitiba
    it_data = [
        {"Fecha": "26 Dic", "Trayecto": "Llegada SP", "Hospedaje": "São Paulo", "Plan": plan_26},
        {"Fecha": "27 Dic", "Trayecto": "Estancia SP", "Hospedaje": "São Paulo", "Plan": "Compras en Jardins y cena familiar."},
        {"Fecha": "28 Dic", "Trayecto": "SP -> Balneário", "Hospedaje": "Baln. Camboriú", "Plan": "Viaje al sur (6h). Cena en la Dubai Brasileña."},
        {"Fecha": "29 Dic", "Trayecto": "BC -> Beto Carrero", "Hospedaje": "Baln. Camboriú", "Plan": "🎢 DÍA 1: Adrenalina pura en el parque."},
        {"Fecha": "30 Dic", "Trayecto": "BC -> Beto Carrero", "Hospedaje": "Baln. Camboriú", "Plan": "🎢 DÍA 2: Shows y repetición de favoritas."},
        {"Fecha": "31 Dic", "Trayecto": "Año Nuevo (BC)", "Hospedaje": "Baln. Camboriú", "Plan": "Playa y fuegos artificiales de gala."},
        {"Fecha": "01 Ene", "Trayecto": "BC -> Curitiba", "Hospedaje": "Curitiba", "Plan": "Salida 11 AM hacia Curitiba (3h). Cena tranquila y descanso."},
        {"Fecha": "02 Ene", "Trayecto": "Curitiba -> Santos", "Hospedaje": "Santos", "Plan": "🌿 Jardín Botánico (Mañana) y bajada a Santos (5h)."},
        {"Fecha": "03 Ene", "Trayecto": "Santos -> Paraty", "Hospedaje": "Paraty", "Plan": "⚽ Vila Belmiro y salida por la tarde a Paraty (3.5h)."},
        {"Fecha": "04 Ene", "Trayecto": "Estancia Paraty", "Hospedaje": "Paraty", "Plan": "Centro Histórico y fotos coloniales."},
        {"Fecha": "05 Ene", "Trayecto": "Paraty -> Río", "Hospedaje": "Río de Janeiro", "Plan": "Llegada por la costa. Atardecer en Copacabana."},
        {"Fecha": "06 Ene", "Trayecto": "Estancia Río", "Hospedaje": "Río de Janeiro", "Plan": "⚽ Maracanã y AquaRio."},
        {"Fecha": "07 Ene", "Trayecto": "Estancia Río", "Hospedaje": "Río de Janeiro", "Plan": "Cristo Redentor y Pan de Azúcar."},
        {"Fecha": "08 Ene", "Trayecto": "Río -> Búzios", "Hospedaje": "Búzios", "Plan": "🥂 Paraíso chic: Playas y buena mesa."},
        {"Fecha": "09 Ene", "Trayecto": "Estancia Búzios", "Hospedaje": "Búzios", "Plan": "Relax total, compras y vino frente al mar."},
        {"Fecha": "10 Ene", "Trayecto": "Búzios -> BH", "Hospedaje": "Belo Horizonte", "Plan": "☕ Viaje a Minas (8h). Cena de comida minera."},
        {"Fecha": "11 Ene", "Trayecto": "Estancia BH", "Hospedaje": "Belo Horizonte", "Plan": "⚽ Mineirão y Mercado Central."},
        {"Fecha": "12 Ene", "Trayecto": "BH -> Ouro Preto", "Hospedaje": "Belo Horizonte", "Plan": "Día de historia barroca y comida típica."},
        {"Fecha": "13 Ene", "Trayecto": "BH -> SP -> Vuelo", "Hospedaje": "---", "Plan": "Regreso a base en SP y traslado al aeropuerto."}
    ]
    st.table(pd.DataFrame(it_data))

with tab2:
    st.header("🏟️ El Tour de los Estadios")
    c1, c2 = st.columns(2)
    with c1: st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/maracana.jpg", caption="Maracanã")
    with c2: st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/santos.jpg", caption="Vila Belmiro")

with tab3:
    st.header("🎢 Territorio Bianca & Mati")
    st.image("https://images.unsplash.com/photo-1513889959013-c2845acb46ad?q=80&w=800", caption="Beto Carrero World")

with tab4:
    st.header("🥂 Los Consentidos")
    st.write("Vinos, compras y la mejor gastronomía de Brasil.")

with tab5:
    st.header("💰 Gestión de Presupuesto")
    st.info("Conectado a Google Sheets para centralizar los gastos de los 19 días.")
