import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests

# 1. Configuración de la página
st.set_page_config(page_title="Misión Brasil 2026", page_icon="🇧🇷", layout="wide")

# --- FUNCION: TASAS DE CAMBIO (API REAL) ---
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

# --- DISEÑO VISUAL (CSS PERSONALIZADO) ---
st.markdown(f"""
    <style>
    /* Fondo de la app */
    .stApp {{
        background-color: #f0f2f6;
    }}
    
    /* Estilo del Header */
    .main-title {{
        text-align: center;
        color: #002776;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        margin-bottom: 0px;
    }}
    
    /* Estilo de las Pestañas */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: #002776;
        padding: 10px 10px 0px 10px;
        border-radius: 12px 12px 0 0;
        gap: 10px;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: #ffffff !important;
        font-weight: 600;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: #009c3b !important;
        border-bottom: 4px solid #ffdf00 !important;
    }}

    /* Tarjetas de Contenedor */
    .stTable {{
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO PRINCIPAL ---
st.markdown("<h1 class='main-title'>🚀 MISIÓN BRASIL 2026</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555; font-size: 1.2em; font-weight: 500;'>Un plan para toda la familia con unos detallitos para Mati y el abuelito</p>", unsafe_allow_html=True)
st.write("---")

# --- SIDEBAR ---
st.sidebar.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/rio.jpg", width=150)
st.sidebar.header("💰 Mercado de Divisas")
st.sidebar.metric("Dólar (USD/COP)", f"${usd_hoy:,.2f}")
st.sidebar.metric("Real (BRL/COP)", f"${brl_hoy:,.2f}")
st.sidebar.write("---")
moneda_v = st.sidebar.radio("Ver presupuesto en:", ["COP", "USD", "BRL"])

def format_money(usd_val):
    if moneda_v == "COP": return f"$ {usd_val * usd_hoy:,.0f} COP"
    if moneda_v == "BRL": return f"R$ {(usd_val * usd_hoy)/brl_hoy:,.2f}"
    return f"$ {usd_val:,.2f} USD"

# --- ESTRUCTURA DE PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["🗺️ ITINERARIO", "⚽ MATI Y EL ABUELITO", "💰 COTIZACIONES"])

with tab1:
    # Foto de Portada Centrada y nítida
    col_portada1, col_portada2, col_portada3 = st.columns([1, 2, 1])
    with col_portada2:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/rio.jpg", 
                 caption="Nuestra meta: ¡Brasil en familia!", width=500)
    
    st.subheader("📅 Cronograma de Ruta")
    it_data = [
        {"Fecha": "26 Dic", "Ruta": "Sao Paulo ➔ Santos", "Manejo": "1.5 h", "Hospedaje": "Santos", "Actividad": "Recogida de auto y cena frente al mar."},
        {"Fecha": "27 Dic", "Ruta": "Santos ➔ Paraty", "Manejo": "4.5 h", "Hospedaje": "Paraty", "Actividad": "Tour por Vila Belmiro y ruta Rio-Santos."},
        {"Fecha": "28 Dic", "Ruta": "Paraty", "Manejo": "---", "Hospedaje": "Paraty", "Actividad": "Día de lancha por playas e islas."},
        {"Fecha": "29 Dic", "Ruta": "Paraty ➔ Río", "Manejo": "4 h", "Hospedaje": "Río", "Actividad": "Check-in y atardecer en Copacabana."},
        {"Fecha": "30-31 Dic", "Ruta": "Río de Janeiro", "Manejo": "---", "Hospedaje": "Río", "Actividad": "Año Nuevo (Reveillon) y Maracaná."},
        {"Fecha": "01-02 Ene", "Ruta": "Río ➔ Arraial", "Manejo": "3 h", "Hospedaje": "Arraial", "Actividad": "Descanso total en el caribe brasileño."},
        {"Fecha": "03-05 Ene", "Ruta": "Costa Norte", "Manejo": "Tramos", "Hospedaje": "Varios", "Actividad": "Ruta panorámica hacia Salvador."},
        {"Fecha": "06 Ene", "Ruta": "Salvador", "Manejo": "---", "Hospedaje": "Salvador", "Actividad": "Tour cultural por el Pelourinho."},
        {"Fecha": "07-08 Ene", "Ruta": "Salvador ➔ Chapada", "Manejo": "6 h", "Hospedaje": "Lençóis", "Actividad": "Cascadas y naturaleza en Chapada."},
        {"Fecha": "09 Ene", "Ruta": "Regreso Interior", "Manejo": "8 h", "Hospedaje": "M. Claros", "Actividad": "Cruce del interior (Tramo largo)."},
        {"Fecha": "10 Ene", "Ruta": "M. Claros ➔ Belo H.", "Manejo": "6 h", "Hospedaje": "Belo H.", "Actividad": "Comida minera y visita al Mineirão."},
        {"Fecha": "11 Ene", "Ruta": "Belo H. ➔ Sao Paulo", "Manejo": "7 h", "Hospedaje": "---", "Actividad": "Entrega de carro y regreso a casa."}
    ]
    st.table(pd.DataFrame(it_data))

with tab2:
    st.header("🏟️ Ruta de los Templos")
    st.markdown("### ¡Fotos para los crack de la familia!")
    
    # Grid de fotos pequeñas y nítidas
    c1, c2, c3 = st.columns(3)
    with c1:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/maracana.jpg", 
                 caption="Maracanã (Río)", width=220)
    with c2:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/pacaembu.jpg", 
                 caption="Museo del Fútbol (SP)", width=220)
    with c3:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/santos.jpg", 
                 caption="Vila Belmiro (Santos)", width=220)

with tab3:
    st.header("📝 Gestión de Presupuesto")
    try:
        df_gastos = conn.read(worksheet="Cotizaciones", ttl=0)
    except:
        df_gastos = pd.DataFrame(columns=["Item", "Categoría", "USD", "Notas"])

    with st.form("nuevo_gasto", clear_on_submit=True):
        st.subheader("Agregar Cotización")
        c_a, c_b = st.columns(2)
        item_n = c_a.text_input("Concepto (Ej: Hotel Río)")
        cat_n = c_b.selectbox("Categoría", ["Vuelos", "Carro", "Hospedaje", "Comida", "Entradas"])
        val_n = c_a.number_input("Precio en Dólares (USD)", min_value=0.0, step=10.0)
        not_n = c_b.text_input("Notas o Link")
        
        if st.form_submit_button("Guardar en el Excel"):
            if item_n:
                nueva = pd.DataFrame([{"Item": item_n, "Categoría": cat_n, "USD": val_n, "Notas": not_n}])
                conn.update(worksheet="Cotizaciones", data=pd.concat([df_gastos, nueva], ignore_index=True))
                st.success("¡Datos guardados!")
                st.cache_data.clear()
            else:
                st.error("Escribe un nombre para el concepto.")

    if not df_gastos.empty:
        st.write("---")
        st.subheader("💰 Resumen Consolidado")
        st.dataframe(df_gastos, use_container_width=True)
        
        total_usd = df_gastos["USD"].sum()
        col_res1, col_res2 = st.columns(2)
        col_res1.metric("Presupuesto Total (USD)", f"$ {total_usd:,.2f}")
        col_res2.metric(f"Total en {moneda_v}", format_money(total_usd))
