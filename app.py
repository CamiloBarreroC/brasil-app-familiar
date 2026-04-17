import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests

# 1. Configuración de la página
st.set_page_config(page_title="Misión Brasil 2026", page_icon="🇧🇷", layout="wide")

# --- TASAS DE CAMBIO (API REAL) ---
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

# 2. Conexión a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ESTILOS MODO OSCURO PRO (ALTO CONTRASTE) ---
st.markdown(f"""
    <style>
    /* Fondo principal oscuro */
    .stApp {{
        background-color: #0e1117;
    }}
    
    /* Títulos y textos en blanco/dorado */
    h1, h2, h3 {{
        color: #ffdf00 !important; /* Dorado Brasil */
        text-align: center;
    }}
    
    p, span, label {{
        color: #ffffff !important; /* Blanco puro */
    }}

    /* Pestañas (Tabs) Estilo Oscuro */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: #1a1c24;
        border-radius: 10px;
        padding: 5px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        color: #ffffff !important;
        font-weight: bold;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: #009c3b !important; /* Verde Brasil */
        color: #ffffff !important;
        border-radius: 7px;
    }}

    /* Estilo de Tablas */
    .stTable {{
        background-color: #1a1c24;
        color: white !important;
        border-radius: 10px;
    }}
    
    /* Inputs y Formularios */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {{
        background-color: #262730;
        color: white !important;
        border: 1px solid #ffdf00;
    }}

    /* Sidebar Oscuro */
    section[data-testid="stSidebar"] {{
        background-color: #000b1a;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("<h1>🚀 MISIÓN BRASIL 2026</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2em; color: #ffffff;'>Un plan para toda la familia con unos detallitos para Mati y el abuelito</p>", unsafe_allow_html=True)
st.write("---")

# --- SIDEBAR (Conversor Pro) ---
st.sidebar.header("💰 Tasas en Vivo")
st.sidebar.metric("Dólar", f"${usd_hoy:,.0f} COP")
st.sidebar.metric("Real", f"${brl_hoy:,.0f} COP")
st.sidebar.write("---")
moneda_v = st.sidebar.radio("Ver presupuesto en:", ["COP", "USD", "BRL"])

def format_money(usd_val):
    if moneda_v == "COP": return f"$ {usd_val * usd_hoy:,.0f} COP"
    if moneda_v == "BRL": return f"R$ {(usd_val * usd_hoy)/brl_hoy:,.2f}"
    return f"$ {usd_val:,.2f} USD"

# --- PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["🗺️ ITINERARIO DETALLADO", "⚽ MATI Y EL ABUELITO", "💰 COTIZACIONES"])

with tab1:
    # Portada centrada
    st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/rio.jpg", width=750)
    
    st.header("📅 Nuestra Ruta")
    it_data = [
        {"Fecha": "26 Dic", "Ruta": "Sao Paulo ➔ Santos", "Hospedaje": "Santos", "Plan": "Llegada, recoger carro y cena."},
        {"Fecha": "27 Dic", "Ruta": "Santos ➔ Paraty", "Hospedaje": "Paraty", "Plan": "Visita Vila Belmiro y carretera costera."},
        {"Fecha": "28 Dic", "Ruta": "Paraty", "Hospedaje": "Paraty", "Plan": "Paseo en barco privado por islas."},
        {"Fecha": "29 Dic", "Ruta": "Paraty ➔ Río", "Hospedaje": "Río", "Plan": "Llegada a Copacabana."},
        {"Fecha": "30-31 Dic", "Ruta": "Río de Janeiro", "Hospedaje": "Río", "Plan": "Reveillon y Tour Maracaná."},
        {"Fecha": "01-02 Ene", "Ruta": "Río ➔ Arraial", "Hospedaje": "Arraial", "Plan": "Descanso en playas turquesas."},
        {"Fecha": "03-05 Ene", "Ruta": "Subida Costa", "Hospedaje": "Varios", "Plan": "Ruta hacia el norte (Salvador)."},
        {"Fecha": "06 Ene", "Ruta": "Salvador", "Hospedaje": "Salvador", "Plan": "Pelourinho e historia."},
        {"Fecha": "07-08 Ene", "Ruta": "Salvador ➔ Chapada", "Hospedaje": "Lençóis", "Plan": "Naturaleza en Chapada Diamantina."},
        {"Fecha": "09 Ene", "Ruta": "Regreso Interior", "Hospedaje": "M. Claros", "Plan": "Cruce del interior brasileño."},
        {"Fecha": "10 Ene", "Ruta": "M. Claros ➔ Belo H.", "Hospedaje": "Belo H.", "Plan": "Comida de Minas y Mineirão."},
        {"Fecha": "11 Ene", "Ruta": "Vuelta a SP", "Hospedaje": "---", "Plan": "Entrega auto y regreso."}
    ]
    st.table(pd.DataFrame(it_data))

with tab2:
    st.header("🏟️ Templos del Fútbol")
    st.write("Visitas especiales para los cracks de la casa:")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/maracana.jpg", caption="Maracanã", width=200)
    with c2:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/pacaembu.jpg", caption="Museo Fútbol", width=200)
    with c3:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/santos.jpg", caption="Vila Belmiro", width=200)

with tab3:
    st.header("📝 Cotizaciones")
    try:
        df_g = conn.read(worksheet="Cotizaciones", ttl=0)
    except:
        df_g = pd.DataFrame(columns=["Item", "USD"])

    with st.form("nuevo_gasto", clear_on_submit=True):
        it_n = st.text_input("¿Qué cotizaste?")
        pr_n = st.number_input("Precio USD", min_value=0.0)
        if st.form_submit_button("Guardar Cotización"):
            if it_n:
                nueva = pd.DataFrame([{"Item": it_n, "USD": pr_n}])
                conn.update(worksheet="Cotizaciones", data=pd.concat([df_g, nueva], ignore_index=True))
                st.cache_data.clear()
                st.rerun()

    if not df_g.empty:
        st.write("---")
        st.dataframe(df_g, use_container_width=True)
        st.metric("Total Acumulado", format_money(df_g["USD"].sum()))
