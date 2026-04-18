import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests

# 1. Configuración de la página
st.set_page_config(page_title="Misión Brasil 2026", page_icon="🇧🇷", layout="wide")

# --- FUNCIÓN: TASAS DE CAMBIO (API REAL EN VIVO) ---
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

# --- ESTILOS MODO OSCURO PRO (BRASIL GOLD) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; }}
    h1, h2, h3 {{ color: #ffdf00 !important; text-align: center; font-family: 'Arial Black', sans-serif; }}
    p, span, label, .stMarkdown {{ color: #ffffff !important; }}
    .stTabs [data-baseweb="tab-list"] {{ background-color: #1a1c24; border-radius: 10px; padding: 5px; gap: 10px; }}
    .stTabs [data-baseweb="tab"] {{ color: #ffffff !important; font-weight: bold; }}
    .stTabs [aria-selected="true"] {{ background-color: #009c3b !important; color: white !important; border-radius: 7px; }}
    .stTable {{ background-color: #1a1c24; color: white !important; border-radius: 10px; }}
    .input-container {{ background-color: #1a1c24; padding: 20px; border-radius: 15px; border: 2px solid #009c3b; margin-bottom: 25px; }}
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("<h1>🚀 MISIÓN BRASIL 2026: ¡EL SUEÑO FAMILIAR!</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2em;'>19 días de risas, aventuras y momentos inolvidables.</p>", unsafe_allow_html=True)
st.write("---")

# --- SIDEBAR ---
st.sidebar.header("💰 Finanzas del Viaje")
st.sidebar.metric("Dólar (USD)", f"${usd_hoy:,.0f} COP")
st.sidebar.metric("Real (BRL)", f"${brl_hoy:,.0f} COP")
st.sidebar.write("---")
moneda_v = st.sidebar.radio("Ver presupuesto en:", ["COP", "USD", "BRL"])

def format_money(usd_val):
    if moneda_v == "COP": return f"$ {usd_val * usd_hoy:,.0f} COP"
    if moneda_v == "BRL": return f"R$ {(usd_val * usd_hoy)/brl_hoy:,.2f}"
    return f"$ {usd_val:,.2f} USD"

# --- PESTAÑAS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️ RUTA 19 DÍAS", 
    "⚽ MATI Y ABUELO", 
    "🎢 BIANCA Y MATI", 
    "🥂 LOS CONSENTIDOS", 
    "💰 PRESUPUESTO"
])

# --- PESTAÑA 1: RUTA COMPLETA ---
with tab1:
    st.header("📅 Nuestra Gran Travesía")
    
    it_data = [
        {"Día": "26-27 Dic", "Lugar": "São Paulo / Santos", "Plan": "Inicio futbolero, museo y caminata por los jardines frente al mar."},
        {"Día": "28-29 Dic", "Lugar": "Paraty", "Plan": "Historia colonial, calles de piedra y aire puro de montaña."},
        {"Día": "29-02 Ene", "Lugar": "Río de Janeiro", "Plan": "Año Nuevo (Reveillón), Cristo, Pan de Azúcar y Maracanã."},
        {"Día": "03-04 Ene", "Lugar": "Búzios", "Plan": "Playas de cristal, compras en la Rua das Pedras y buen vino."},
        {"Día": "05-06 Ene", "Lugar": "Rumbo al Sur", "Plan": "Camino a Curitiba. Cena italiana en el barrio Santa Felicidade."},
        {"Día": "07-09 Ene", "Lugar": "Beto Carrero", "Plan": "Emociones fuertes y shows increíbles para Bianca y Mati."},
        {"Día": "10 Ene", "Lugar": "Baln. Camboriú", "Plan": "Lujo, teleféricos y yates en la ciudad más moderna del sur."},
        {"Día": "11-13 Ene", "Lugar": "São Paulo Final", "Plan": "Regreso a la capital, compras finales en Jardins y gran cena de despedida."}
    ]
    st.table(pd.DataFrame(it_data))

# --- PESTAÑA 2: MATI Y EL ABUELO ---
with tab2:
    st.header("🏟️ Templos del Fútbol y Paz")
    st.write("**Para los dos caballeros:** Momentos de historia, estadios legendarios y caminatas tranquilas.")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.subheader("La Gira Sagrada")
        st.write("- Pacaembú (Museo del Fútbol)\n- Vila Belmiro (La casa de Pelé)\n- Maracanã (El templo mayor)\n- Allianz Parque (Modernidad)")
    with col_f2:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/santos.jpg", caption="Un legado para compartir")

# --- PESTAÑA 3: BIANCA Y MATI ---
with tab3:
    st.header("🎢 Gritos y Adrenalina")
    st.write("**Para Bianca y Mati:** Donde la emoción no tiene límites.")
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.image("https://images.unsplash.com/photo-1513889959013-c2845acb46ad?q=80&w=400", caption="Beto Carrero World")
    with col_a2:
        st.subheader("¡No se pueden perder!")
        st.write("- **FireWhip:** La montaña rusa invertida.\n- **Big Tower:** ¡100 metros de caída libre!\n- **AquaRio:** Túnel de tiburones en Río.\n- **Teleférico:** Vistas de infarto en Balneário.")

# --- PESTAÑA 4: LOS CONSENTIDOS (AMPA, JIME, DIANA Y GIOR) ---
with tab4:
    st.header("🥂 El Club del Disfrute")
    st.write("**Amparo, Jime, Diana y Giorgio:** Aquí mandan el buen paladar, el estilo y la naturaleza.")
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.subheader("🍷 Sabor y Brindis")
        st.write("Desde las pizzas de São Paulo hasta el vino blanco en Búzios y la comida minera en el camino. ¡Cada comida será un evento!")
        st.subheader("🛍️ Shopping & Tesoros")
        st.write("La Rua das Pedras en Búzios y la calle Oscar Freire en SP los esperan para encontrar esas cosas únicas.")
    with col_g2:
        st.subheader("🌿 Paseos con Alma")
        st.write("El Jardín Botánico de Curitiba y los atardeceres en el Arpoador con una copa de espumante. Naturaleza con total confort.")
        st.image("https://images.unsplash.com/photo-1590424765651-f2305886617c?q=80&w=400", caption="Momentos para brindar")

# --- PESTAÑA 5: PRESUPUESTO ---
with tab5:
    st.header("💰 Gestión de Gastos")
    st.info("Centralicemos aquí las cotizaciones de los hoteles en Búzios y las entradas al Beto Carrero.")
    # (Lógica de formulario de presupuesto igual que la anterior)
