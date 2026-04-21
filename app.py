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

# --- ESTILOS MODO OSCURO PRO ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; }}
    h1, h2, h3 {{ color: #ffdf00 !important; text-align: center; font-family: 'Arial Black', sans-serif; }}
    p, span, label, .stMarkdown {{ color: #ffffff !important; }}
    .stTabs [data-baseweb="tab-list"] {{ background-color: #1a1c24; border-radius: 10px; padding: 5px; gap: 10px; }}
    .stTabs [aria-selected="true"] {{ background-color: #009c3b !important; color: white !important; border-radius: 7px; }}
    .stTable {{ background-color: #1a1c24; color: white !important; border-radius: 10px; }}
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
    
    # LÓGICA BLINDADA PARA EL MUSEO DEL FÚTBOL
    if "Mañana" in horario_vuelo:
        plan_26 = "⚽ Aterrizaje y Visita al MUSEO DEL FÚTBOL (Pacaembú). Cena de bienvenida."
        plan_27 = "🛍️ Compras en Oscar Freire (Jardins) y visita al Mercado Municipal."
    else:
        plan_26 = "🏨 Llegada al hotel, brindis de bienvenida y descanso del vuelo."
        plan_27 = "⚽ Mañana: MUSEO DEL FÚTBOL (Pacaembú). Tarde: Compras y Mercado Municipal."

    it_data = [
        {"Fecha": "26 Dic", "Trayecto": "Llegada SP", "Hospedaje": "São Paulo", "Plan": plan_26},
        {"Fecha": "27 Dic", "Trayecto": "Estancia SP", "Hospedaje": "São Paulo", "Plan": plan_27},
        {"Fecha": "28 Dic", "Trayecto": "SP -> Balneário", "Hospedaje": "Baln. Camboriú", "Plan": "Viaje al sur (6h). Cena en la 'Dubai' brasileña."},
        {"Fecha": "29 Dic", "Trayecto": "BC -> Beto Carrero", "Hospedaje": "Baln. Camboriú", "Plan": "🎢 DÍA 1 PARQUE: Adrenalina pura para Bianca y Mati."},
        {"Fecha": "30 Dic", "Trayecto": "BC -> Beto Carrero", "Hospedaje": "Baln. Camboriú", "Plan": "🎢 DÍA 2 PARQUE: Shows y repetición de favoritas."},
        {"Fecha": "31 Dic", "Trayecto": "Año Nuevo (BC)", "Hospedaje": "Baln. Camboriú", "Plan": "Reveillón de gala con fuegos artificiales en la playa."},
        {"Fecha": "01 Ene", "Trayecto": "BC -> Curitiba", "Hospedaje": "Curitiba", "Plan": "Salida 11 AM hacia Curitiba (3h). Cena y descanso."},
        {"Fecha": "02 Ene", "Trayecto": "Curitiba -> Santos", "Hospedaje": "Santos", "Plan": "🌿 Jardín Botánico (Mañana) y bajada a Santos (5h)."},
        {"Fecha": "03 Ene", "Trayecto": "Santos -> Paraty", "Hospedaje": "Paraty", "Plan": "⚽ Vila Belmiro y salida hacia Paraty (3.5h)."},
        {"Fecha": "04 Ene", "Trayecto": "Estancia Paraty", "Hospedaje": "Paraty", "Plan": "Centro Histórico y fotos coloniales para las chicas."},
        {"Fecha": "05 Ene", "Trayecto": "Paraty -> Río", "Hospedaje": "Río de Janeiro", "Plan": "Llegada a Copacabana. Atardecer frente al mar."},
        {"Fecha": "06 Ene", "Trayecto": "Estancia Río", "Hospedaje": "Río de Janeiro", "Plan": "⚽ Maracanã y AquaRio."},
        {"Fecha": "07 Ene", "Trayecto": "Estancia Río", "Hospedaje": "Río de Janeiro", "Plan": "Cristo Redentor y Pan de Azúcar."},
        {"Fecha": "08 Ene", "Trayecto": "Río -> Petrópolis", "Hospedaje": "Petrópolis", "Plan": "🏰 Subida a la Ciudad Imperial (2h). Tour de Palacios."},
        {"Fecha": "09 Ene", "Trayecto": "Petrópolis -> BH", "Hospedaje": "Belo Horizonte", "Plan": "Viaje a Minas (5h). Cena de comida minera."},
        {"Fecha": "10 Ene", "Trayecto": "Estancia BH", "Hospedaje": "Belo Horizonte", "Plan": "⚽ Mineirão y Mercado Central."},
        {"Fecha": "11 Ene", "Trayecto": "Ouro Preto", "Hospedaje": "Belo Horizonte", "Plan": "Historia barroca y almuerzo colonial de lujo."},
        {"Fecha": "12 Ene", "Trayecto": "BH -> São Paulo", "Hospedaje": "São Paulo", "Plan": "Regreso a base final y gran cena de despedida."},
        {"Fecha": "13 Ene", "Trayecto": "Vuelo Regreso", "Hospedaje": "---", "Plan": "Traslado al aeropuerto y vuelo a casa."}
    ]
    st.table(pd.DataFrame(it_data))

with tab_map:
    st.header("📍 Recorrido Maestro")
    st.image("https://via.placeholder.com/1000x500.png?text=Sube+aquí+recorrido_maestro_brasil.png", use_container_width=True)

with tab2:
    st.header("🏟️ Templos Sagrados")
    c1, c2 = st.columns(2)
    with c1: 
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/maracana.jpg", caption="Maracanã")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/santos.jpg", caption="Vila Belmiro")
    with c2: 
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/pacaembu.jpg", caption="Museo del Fútbol")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/mineirao.jpg", caption="Mineirão")

with tab3:
    st.header("🎢 Bianca & Mati")
    st.image("https://images.unsplash.com/photo-1513889959013-c2845acb46ad?q=80&w=800", caption="Beto Carrero World")

with tab4:
    st.header("🥂 Los Consentidos")
    st.image("https://images.unsplash.com/photo-1590424765651-f2305886617c?q=80&w=500")
    st.markdown("- **Petrópolis:** Elegancia imperial.\n- **Curitiba:** Naturaleza y orden.\n- **Minas:** Sabores inolvidables.")
