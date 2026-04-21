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
st.markdown("<h1>🚀 MISIÓN BRASIL 2026: EL SUEÑO FAMILIAR</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2em;'>Fútbol, Adrenalina, Vinos e Historia.</p>", unsafe_allow_html=True)
st.write("---")

# --- PESTAÑAS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️ RUTA 19 DÍAS", "⚽ MATI Y ABUELO", "🎢 BIANCA Y MATI", "🥂 LOS CONSENTIDOS", "💰 PRESUPUESTO"
])

with tab1:
    st.markdown("### ✈️ Configuración de Llegada (26 Dic)")
    horario_vuelo = st.radio("Hora de aterrizaje en SP:", ["Mañana", "Tarde/Noche"], horizontal=True)
    
    # Lógica de los primeros días incluyendo el MUSEO DEL FÚTBOL
    if "Mañana" in horario_vuelo:
        p_26 = "Aterrizaje y Visita al MUSEO DEL FÚTBOL (Pacaembú). Cena italiana."
        p_27 = "Día de Compras en Jardins (Oscar Freire) y Mercado Municipal."
    else:
        p_26 = "Llegada al hotel y brindis de bienvenida. Descanso."
        p_27 = "Mañana de MUSEO DEL FÚTBOL (Pacaembú) y tarde de compras."

    it_data = [
        {"Fecha": "26 Dic", "Trayecto": "Llegada SP", "Hospedaje": "São Paulo", "Plan": p_26},
        {"Fecha": "27 Dic", "Trayecto": "Estancia SP", "Hospedaje": "São Paulo", "Plan": p_27},
        {"Fecha": "28 Dic", "Trayecto": "SP -> Balneário", "Hospedaje": "Baln. Camboriú", "Plan": "Viaje al sur (6h). Cena en la 'Dubai' brasileña."},
        {"Fecha": "29 Dic", "Trayecto": "BC -> Beto Carrero", "Hospedaje": "Baln. Camboriú", "Plan": "🎢 DÍA 1 PARQUE: Adrenalina pura para Bianca y Mati."},
        {"Fecha": "30 Dic", "Trayecto": "BC -> Beto Carrero", "Hospedaje": "Baln. Camboriú", "Plan": "🎢 DÍA 2 PARQUE: Shows y repetición de favoritas."},
        {"Fecha": "31 Dic", "Trayecto": "Año Nuevo (BC)", "Hospedaje": "Baln. Camboriú", "Plan": "Playa y fuegos artificiales de gala en la Avenida Atlântica."},
        {"Fecha": "01 Ene", "Trayecto": "BC -> Curitiba", "Hospedaje": "Curitiba", "Plan": "Salida 11 AM hacia Curitiba (3h). Tarde de relax y cena."},
        {"Fecha": "02 Ene", "Trayecto": "Curitiba -> Santos", "Hospedaje": "Santos", "Plan": "🌿 Jardín Botánico (Mañana) y bajada a Santos (5h)."},
        {"Fecha": "03 Ene", "Trayecto": "Santos -> Paraty", "Hospedaje": "Paraty", "Plan": "⚽ Vila Belmiro y salida por la tarde a Paraty (3.5h)."},
        {"Fecha": "04 Ene", "Trayecto": "Estancia Paraty", "Hospedaje": "Paraty", "Plan": "Caminata histórica y fotos coloniales."},
        {"Fecha": "05 Ene", "Trayecto": "Paraty -> Río", "Hospedaje": "Río de Janeiro", "Plan": "Llegada por la costa. Atardecer en Ipanema."},
        {"Fecha": "06 Ene", "Trayecto": "Estancia Río", "Hospedaje": "Río de Janeiro", "Plan": "⚽ Maracanã y AquaRio."},
        {"Fecha": "07 Ene", "Trayecto": "Estancia Río", "Hospedaje": "Río de Janeiro", "Plan": "Cristo Redentor y Pan de Azúcar."},
        {"Fecha": "08 Ene", "Trayecto": "Río -> Búzios", "Hospedaje": "Búzios", "Plan": "🥂 Paraíso chic: Playas y buena mesa."},
        {"Fecha": "09 Ene", "Trayecto": "Estancia Búzios", "Hospedaje": "Búzios", "Plan": "Relax total, compras y vino frente al mar."},
        {"Fecha": "10 Ene", "Trayecto": "Búzios -> BH", "Hospedaje": "Belo Horizonte", "Plan": "☕ Viaje a Minas (8h). Cena de comida minera."},
        {"Fecha": "11 Ene", "Trayecto": "Estancia BH", "Hospedaje": "Belo Horizonte", "Plan": "⚽ Mineirão y Mercado Central."},
        {"Fecha": "12 Ene", "Trayecto": "BH -> Ouro Preto", "Hospedaje": "Belo Horizonte", "Plan": "Día de historia barroca e iglesias de oro."},
        {"Fecha": "13 Ene", "Trayecto": "BH -> SP -> Vuelo", "Hospedaje": "---", "Plan": "Regreso a base en SP y traslado al aeropuerto."}
    ]
    st.table(pd.DataFrame(it_data))

with tab2:
    st.header("🏟️ Ruta de los Templos Sagrados")
    st.write("Para el Abuelito y Mati: Historia viva en el césped.")
    c1, c2 = st.columns(2)
    with c1: 
        st.markdown("**Maracanã (Río)**")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/maracana.jpg", use_container_width=True)
    with c2: 
        st.markdown("**Museo del Fútbol - Pacaembú (SP)**")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/pacaembu.jpg", use_container_width=True)
    
    c3, c4 = st.columns(2)
    with c3: 
        st.markdown("**Vila Belmiro (Santos)**")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/santos.jpg", use_container_width=True)
    with c4: 
        st.markdown("**Mineirão (Belo Horizonte)**")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/mineirao.jpg", use_container_width=True)

with tab3:
    st.header("🎢 Territorio Bianca & Mati")
    st.image("https://images.unsplash.com/photo-1513889959013-c2845acb46ad?q=80&w=800", caption="Beto Carrero World: 2 días de pura adrenalina")
    st.markdown("### 🎯 Los Desafíos de Bianca:\n- **FireWhip** (Montaña rusa invertida)\n- **Big Tower** (100 metros de caída)\n- **Hot Wheels Show** (Acrobacias reales)")

with tab4:
    st.header("🥂 El Club de los Consentidos")
    st.image("https://images.unsplash.com/photo-1590424765651-f2305886617c?q=80&w=500", caption="Momentos para brindar en familia")
    st.markdown("""
    - **Búzios:** Vinos blancos frente a la Orla Bardot.
    - **Curitiba:** El icónico Jardín Botánico.
    - **Minas:** Tour gastronómico de quesos y dulces.
    - **São Paulo:** Shopping en la Oscar Freire.
    """)

with tab5:
    st.header("💰 Gestión de Presupuesto")
    st.info("Conectado a Google Sheets para controlar cada Real invertido.")
