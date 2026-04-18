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
    except: return 3950.0, 780.0

usd_hoy, brl_hoy = obtener_tasas()
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ESTILOS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; }}
    h1, h2, h3 {{ color: #ffdf00 !important; text-align: center; font-family: 'Arial Black', sans-serif; }}
    p, span, label, .stMarkdown {{ color: #ffffff !important; }}
    .stTabs [data-baseweb="tab-list"] {{ background-color: #1a1c24; border-radius: 10px; padding: 5px; }}
    .stTabs [aria-selected="true"] {{ background-color: #009c3b !important; color: white !important; }}
    .stTable {{ background-color: #1a1c24; color: white !important; border-radius: 10px; }}
    .input-container {{ background-color: #1a1c24; padding: 20px; border-radius: 15px; border: 2px solid #009c3b; margin-bottom: 25px; }}
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("<h1>🚀 MISIÓN BRASIL 2026: EL SUEÑO FAMILIAR</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>19 días, 4 estados y una historia para cada uno de nosotros.</p>", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.header("💰 Finanzas del Viaje")
st.sidebar.metric("Dólar (USD)", f"${usd_hoy:,.0f} COP")
st.sidebar.metric("Real (BRL)", f"${brl_hoy:,.0f} COP")
moneda_v = st.sidebar.radio("Ver en:", ["COP", "USD", "BRL"])

def format_money(usd_val):
    if moneda_v == "COP": return f"$ {usd_val * usd_hoy:,.0f} COP"
    if moneda_v == "BRL": return f"R$ {(usd_val * usd_hoy)/brl_hoy:,.2f}"
    return f"$ {usd_val:,.2f} USD"

# --- PESTAÑAS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️ RUTA 19 DÍAS", 
    "⚽ MATI Y ABUELO", 
    "🎢 BIANCA Y MATI", 
    "🍷 GOURMET & CHIC", 
    "💰 PRESUPUESTO"
])

# --- PESTAÑA 1: ITINERARIO COMPLETO ---
with tab1:
    st.header("📅 El Itinerario Maestro")
    horario_vuelo = st.radio("Aterrizaje en SP:", ["Mañana", "Tarde/Noche"], horizontal=True)
    
    it_data = [
        {"Día": "26 Dic", "Ruta": "SP -> Santos", "Plan": "Aterrizaje, Museo del Fútbol y atardecer en los jardines de Santos."},
        {"Día": "27 Dic", "Ruta": "Santos -> Paraty", "Plan": "Vila Belmiro y ruta escénica hacia la joya colonial."},
        {"Día": "28 Dic", "Ruta": "Paraty", "Plan": "Caminata histórica y cena gourmet en el centro (Sin lanchas)."},
        {"Día": "29 Dic", "Ruta": "Paraty -> Río", "Plan": "Entrada triunfal por la costa hacia Copacabana."},
        {"Día": "30-31 Dic", "Ruta": "Río de Janeiro", "Plan": "Reveillón: Blanco, champagne y el Cristo Redentor."},
        {"Día": "01 Ene", "Ruta": "Río Relax", "Plan": "Descanso total en Ipanema/Leblon."},
        {"Día": "02 Ene", "Ruta": "Río / Búzios", "Plan": "Pan de Azúcar y salida hacia el glamour de Búzios."},
        {"Día": "03-04 Ene", "Ruta": "Búzios", "Plan": "Playas chic, Rua das Pedras y vinos frente al mar."},
        {"Día": "05 Ene", "Ruta": "Búzios -> SP", "Plan": "Regreso estratégico a la capital para compras."},
        {"Día": "06 Ene", "Ruta": "SP -> Curitiba", "Plan": "Ruta hacia el sur. Cena en el barrio italiano de Santa Felicidade."},
        {"Día": "07 Ene", "Ruta": "Curitiba -> Penha", "Plan": "Jardín Botánico y llegada al mundo de Beto Carrero."},
        {"Día": "08-09 Ene", "Ruta": "Beto Carrero", "Plan": "Dos días de adrenalina pura para Bianca y Mati."},
        {"Día": "10 Ene", "Ruta": "Balneário Camboriú", "Plan": "La 'Dubai Brasileña': Lujo, yates y vistas impresionantes."},
        {"Día": "11 Ene", "Ruta": "B. Camboriú -> SP", "Plan": "Travesía de regreso con paradas gastronómicas."},
        {"Día": "12 Ene", "Ruta": "São Paulo Chic", "Plan": "Shopping en Jardins, Mercado Municipal y cena de despedida."},
        {"Día": "13 Ene", "Ruta": "Cierre de Ciclo", "Plan": "Últimas compras y vuelo de regreso."}
    ]
    st.table(pd.DataFrame(it_data))

# --- PESTAÑA 2: MATI Y EL ABUELO (FÚTBOL Y CALMA) ---
with tab2:
    st.header("🏟️ Territorio Sagrado")
    st.write("Para el Abuelito y Mati: Historia, templos y caminatas con alma.")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Los 4 Templos")
        st.write("1. Museo del Fútbol (Pacaembú)\n2. Vila Belmiro (Santos)\n3. Maracanã (Río)\n4. Allianz Parque o Morumbí (SP)")
    with col2:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/santos.jpg", caption="Donde nació la magia")

# --- PESTAÑAS 3: BIANCA Y MATI (ADRENALINA) ---
with tab3:
    st.header("🎢 Mundo de Emociones")
    st.write("Para los que no le temen a nada: Bianca y Mati.")
    col_a, col_b = st.columns(2)
    with col_a:
        st.image("https://images.unsplash.com/photo-1513889959013-c2845acb46ad?q=80&w=400", caption="Beto Carrero World")
    with col_b:
        st.subheader("Imperdibles de Adrenalina")
        st.write("- **FireWhip:** La montaña rusa invertida.\n- **Big Tower:** Caída libre de 100 metros.\n- **Hot Wheels Show:** Acrobacias de película.\n- **AquaRio:** Tiburones en Río.")

# --- PESTAÑA 4: GOURMET & CHIC (EL EQUIPO GOURMET) ---
with tab4:
    st.header("🍷 Experiencias Chic & Gourmet")
    st.write("Para Jimena, Giorgio, Diana y Amparo: Los placeres de la vida.")
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.subheader("📍 Paradas Estratégicas")
        st.markdown("""
        * **Búzios:** Cena en la *Rua das Pedras* con vino blanco frente al mar.
        * **Río (Leblon):** El barrio más chic para un brunch sofisticado.
        * **São Paulo (Jardins):** Los mejores restaurantes del continente (D.O.M o Mani).
        * **Curitiba:** Cena romántica en una ópera de cristal.
        """)
    with col_g2:
        st.subheader("🌿 Naturaleza & Confort")
        st.write("Caminatas suaves en el Jardín Botánico de Curitiba y atardeceres en el Arpoador con una copa de espumante brasileño.")

# --- PESTAÑA 5: PRESUPUESTO ---
with tab5:
    st.header("💰 Gestión de Gastos")
    # (Lógica de guardado en GSheets que ya teníamos)
    st.info("Utiliza esta sección para centralizar las cotizaciones de hoteles y entradas a los parques.")
