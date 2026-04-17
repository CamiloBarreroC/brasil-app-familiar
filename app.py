import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests

# 1. Configuración de la página
st.set_page_config(page_title="Misión Brasil 2026", page_icon="🇧🇷", layout="wide")

# --- FUNCIÓN PARA TASAS DE CAMBIO EN VIVO ---
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

# --- ESTILOS VISUALES ---
st.markdown(f"""
    <style>
    .main {{ background-color: #f8fafc; }}
    .stTabs [data-baseweb="tab-list"] {{
        background-color: #002776;
        padding: 10px 10px 0px 10px;
        border-radius: 10px 10px 0 0;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: white !important;
        font-weight: bold;
        font-size: 16px;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: #009c3b !important;
        color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("<h1 style='text-align: center; color: #002776;'>🚀 Misión Brasil 2026: Nuestra Aventura Inolvidable</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555; font-size: 1.1em;'>Un plan para toda la familia con unos detallitos para Mati y el abuelito</p>", unsafe_allow_html=True)
st.write("---")

# --- SIDEBAR ---
st.sidebar.header("📊 Valores del Mercado")
st.sidebar.write(f"💵 **1 Dólar:** ${usd_hoy:,.2f} COP")
st.sidebar.write(f"🇧🇷 **1 Real:** ${brl_hoy:,.2f} COP")
moneda = st.sidebar.radio("Ver presupuesto en:", ["COP", "USD", "BRL"])

def format_money(usd_val):
    if moneda == "COP": return f"$ {usd_val * usd_hoy:,.0f} COP"
    if moneda == "BRL": return f"R$ {(usd_val * usd_hoy)/brl_hoy:,.2f}"
    return f"$ {usd_val:,.2f} USD"

# --- PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["🗺️ ITINERARIO DETALLADO", "⚽ MATI Y EL ABUELITO", "💰 COTIZACIONES"])

with tab1:
    # Foto de Portada (Reducida para que no sea gigante)
    st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/rio.jpg", 
             width=600) # Tamaño controlado para la portada
    
    st.header("📅 Cronograma de Ruta")
    it_data = [
        {"Fecha": "26 Dic", "Ruta": "Sao Paulo ➔ Santos", "Manejo": "1.5 h", "Hospedaje": "Santos", "Plan": "Llegada, recoger auto y descanso."},
        {"Fecha": "27 Dic", "Ruta": "Santos ➔ Paraty", "Manejo": "4.5 h", "Hospedaje": "Paraty", "Plan": "Vila Belmiro y ruta costera."},
        {"Fecha": "28 Dic", "Ruta": "Paraty", "Manejo": "---", "Hospedaje": "Paraty", "Plan": "Día de barco por las islas."},
        {"Fecha": "29 Dic", "Ruta": "Paraty ➔ Río", "Manejo": "4 h", "Hospedaje": "Río", "Plan": "Check-in y Copacabana."},
        {"Fecha": "30-31 Dic", "Ruta": "Río de Janeiro", "Manejo": "---", "Hospedaje": "Río", "Plan": "Año Nuevo y Maracaná."},
        {"Fecha": "01-02 Ene", "Ruta": "Río ➔ Arraial", "Manejo": "3 h", "Hospedaje": "Arraial", "Plan": "Caribe Brasileño."},
        {"Fecha": "03-05 Ene", "Ruta": "Costa Norte", "Manejo": "Tramos", "Hospedaje": "Varios", "Plan": "Ruta hacia Salvador."},
        {"Fecha": "06 Ene", "Ruta": "Salvador", "Manejo": "---", "Hospedaje": "Salvador", "Plan": "Pelourinho y cultura."},
        {"Fecha": "07-08 Ene", "Ruta": "Salvador ➔ Chapada", "Manejo": "6 h", "Hospedaje": "Lençóis", "Plan": "Cascadas y cuevas."},
        {"Fecha": "09 Ene", "Ruta": "Regreso Interior", "Manejo": "8 h", "Hospedaje": "M. Claros", "Plan": "Cruzando el interior."},
        {"Fecha": "10 Ene", "Ruta": "Regreso Minas", "Manejo": "6 h", "Hospedaje": "Belo H.", "Plan": "Comida minera y Mineirão."},
        {"Fecha": "11 Ene", "Ruta": "Vuelta a SP", "Manejo": "7 h", "Hospedaje": "---", "Plan": "Entrega de carro y vuelo."}
    ]
    st.table(pd.DataFrame(it_data))

with tab2:
    st.header("🏟️ Ruta de los Templos")
    st.write("Fotos para Mati y el abuelito (Tamaño reducido para mejor calidad):")
    
    col1, col2, col3 = st.columns(3)
    
    # Tamaño ajustado a 200 para que se vean nítidas y pequeñas
    with col1:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/maracana.jpg", 
                 caption="Maracanã", width=200)
    with col2:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/pacaembu.jpg", 
                 caption="Museo Fútbol", width=200)
    with col3:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/santos.jpg", 
                 caption="Vila Belmiro", width=200)

with tab3:
    st.header("📝 Cotizaciones")
    try:
        df_gastos = conn.read(worksheet="Cotizaciones", ttl=0)
    except:
        df_gastos = pd.DataFrame(columns=["Item", "Categoría", "USD", "Notas"])

    with st.form("nuevo_gasto", clear_on_submit=True):
        c_a, c_b = st.columns(2)
        item = c_a.text_input("Concepto")
        cat = c_b.selectbox("Categoría", ["Vuelos", "Carro", "Hospedaje", "Comida", "Fútbol"])
        precio = c_a.number_input("Precio USD", min_value=0.0)
        notas = c_b.text_input("Notas")
        
        if st.form_submit_button("Guardar"):
            if item:
                nueva = pd.DataFrame([{"Item": item, "Categoría": cat, "USD": precio, "Notas": notas}])
                conn.update(worksheet="Cotizaciones", data=pd.concat([df_gastos, nueva], ignore_index=True))
                st.success("¡Guardado!")
                st.cache_data.clear()

    if not df_gastos.empty:
        st.write("---")
        st.dataframe(df_gastos, use_container_width=True)
        st.metric("Total Estimado", format_money(df_gastos["USD"].sum()))
