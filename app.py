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
    except:
        return 3950.0, 780.0

usd_hoy, brl_hoy = obtener_tasas()

# 2. Conexión a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ESTILOS MODO OSCURO PRO ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; }}
    h1, h2, h3 {{ color: #ffdf00 !important; text-align: center; font-family: 'Arial Black', sans-serif; }}
    p, span, label, .stMarkdown {{ color: #ffffff !important; }}
    .stTabs [data-baseweb="tab-list"] {{ background-color: #1a1c24; border-radius: 10px; padding: 5px; gap: 10px; }}
    .stTabs [data-baseweb="tab"] {{ color: #ffffff !important; font-weight: bold; }}
    .stTabs [aria-selected="true"] {{ background-color: #009c3b !important; color: #ffffff !important; border-radius: 7px; }}
    .stTable, [data-testid="stTable"] {{ background-color: #1a1c24; color: white !important; border-radius: 10px; }}
    [data-testid="stTable"] td, [data-testid="stTable"] th {{ color: white !important; border-bottom: 1px solid #31333f; }}
    section[data-testid="stSidebar"] {{ background-color: #000b1a; }}
    .stButton>button {{ background-color: #009c3b; color: white; border-radius: 10px; border: none; font-weight: bold; width: 100%; }}
    
    /* Estilo para los inputs de conversión */
    .conversion-box {{
        background-color: #1a1c24;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #ffdf00;
        margin-bottom: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("<h1>🚀 MISIÓN BRASIL 2026</h1>", unsafe_allow_html=True)
st.write("---")

# --- SIDEBAR ---
st.sidebar.header("💰 Tasas de Cambio Hoy")
st.sidebar.metric("1 Dólar (USD)", f"${usd_hoy:,.0f} COP")
st.sidebar.metric("1 Real (BRL)", f"${brl_hoy:,.0f} COP")
st.sidebar.write("---")
moneda_v = st.sidebar.radio("Ver presupuesto en:", ["COP", "USD", "BRL"])

def format_money(usd_val):
    if moneda_v == "COP": return f"$ {usd_val * usd_hoy:,.0f} COP"
    if moneda_v == "BRL": return f"R$ {(usd_val * usd_hoy)/brl_hoy:,.2f}"
    return f"$ {usd_val:,.2f} USD"

# --- PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["🗺️ ITINERARIO DETALLADO", "⚽ MATI Y EL ABUELITO", "💰 COTIZACIONES"])

with tab1:
    col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
    with col_img2:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/rio.jpg", caption="¡Brasil en familia!", width=500)
    
    st.header("📅 Cronograma de Ruta")
    it_data = [
        {"Fecha": "26 Dic", "Ruta": "Sao Paulo ➔ Santos", "Hospedaje": "Santos", "Plan": "Llegada y cena frente al mar."},
        {"Fecha": "27 Dic", "Ruta": "Santos ➔ Paraty", "Hospedaje": "Paraty", "Plan": "Vila Belmiro y ruta costera."},
        {"Fecha": "28 Dic", "Ruta": "Paraty", "Hospedaje": "Paraty", "Plan": "Lancha por las islas."},
        {"Fecha": "29 Dic", "Ruta": "Paraty ➔ Río", "Hospedaje": "Río", "Plan": "Atardecer en Copacabana."},
        {"Fecha": "30-31 Dic", "Ruta": "Río de Janeiro", "Hospedaje": "Río", "Plan": "Año Nuevo y Maracaná."},
        {"Fecha": "01-02 Ene", "Ruta": "Río ➔ Arraial", "Hospedaje": "Arraial", "Plan": "Caribe brasileño."},
        {"Fecha": "03-05 Ene", "Ruta": "Costa Norte", "Hospedaje": "Varios", "Plan": "Hacia Salvador."},
        {"Fecha": "06 Ene", "Ruta": "Salvador", "Hospedaje": "Salvador", "Plan": "Pelourinho."},
        {"Fecha": "07-08 Ene", "Ruta": "Salvador ➔ Chapada", "Hospedaje": "Lençóis", "Plan": "Chapada Diamantina."},
        {"Fecha": "09 Ene", "Ruta": "Regreso Interior", "Hospedaje": "M. Claros", "Plan": "Tramo largo."},
        {"Fecha": "10 Ene", "Ruta": "M. Claros ➔ Belo H.", "Hospedaje": "Belo H.", "Plan": "Mineirão (¡El del 1-7!)."},
        {"Fecha": "11 Ene", "Ruta": "Vuelta a SP", "Hospedaje": "---", "Plan": "Regreso a casa."}
    ]
    st.table(pd.DataFrame(it_data))

with tab2:
    st.header("🏟️ Ruta de los Templos")
    f1c1, f1c2 = st.columns(2)
    with f1c1: st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/maracana.jpg", caption="Maracanã", width=300)
    with f1c2: st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/pacaembu.jpg", caption="Museo Fútbol", width=300)
    st.write("---")
    f2c1, f2c2 = st.columns(2)
    with f2c1: st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/santos.jpg", caption="Vila Belmiro", width=300)
    with f2c2: st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/mineirao.jpg", caption="Mineirão (7-1)", width=300)

with tab3:
    st.header("📝 Gestión de Presupuesto")
    
    # 1. Lógica de Conversión Dinámica
    if 'usd_input' not in st.session_state: st.session_state.usd_input = 0.0
    if 'cop_input' not in st.session_state: st.session_state.cop_input = 0.0

    def update_usd():
        st.session_state.usd_input = st.session_state.cop_input / usd_hoy

    def update_cop():
        st.session_state.cop_input = st.session_state.usd_input * usd_hoy

    st.subheader("💰 Calculadora de Cotización")
    with st.container():
        st.markdown('<div class="conversion-box">', unsafe_allow_html=True)
        col_c1, col_c2, col_c3 = st.columns(3)
        
        with col_c1:
            cop_val = st.number_input("Precio en Pesos (COP)", min_value=0.0, key="cop_input", on_change=update_usd, step=50000.0)
        
        with col_c2:
            usd_val = st.number_input("Precio en Dólares (USD)", min_value=0.0, key="usd_input", on_change=update_cop, step=10.0)
        
        with col_c3:
            # Cálculo de Reales solo para visualización
            brl_val = (st.session_state.usd_input * usd_hoy) / brl_hoy
            st.metric("Equivale en Reales", f"R$ {brl_val:,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. Formulario para guardar
    try:
        df_g = conn.read(worksheet="Cotizaciones", ttl=0)
    except:
        df_g = pd.DataFrame(columns=["Item", "Categoría", "USD", "Notas"])

    with st.form("nuevo_gasto", clear_on_submit=True):
        col_f1, col_f2 = st.columns(2)
        item_n = col_f1.text_input("¿Qué estás cotizando? (Ej: Hotel en Paraty)")
        cat_n = col_f2.selectbox("Categoría", ["Vuelos", "Carro", "Hospedaje", "Comida", "Entradas"])
        not_n = st.text_input("Notas adicionales (Ej: 'Visto en Booking')")
        
        enviar = st.form_submit_button("Guardar Cotización en el Plan")
        
        if enviar:
            if item_n and st.session_state.usd_input > 0:
                nueva = pd.DataFrame([{"Item": item_n, "Categoría": cat_n, "USD": st.session_state.usd_input, "Notas": not_n}])
                conn.update(worksheet="Cotizaciones", data=pd.concat([df_g, nueva], ignore_index=True))
                st.success(f"¡Guardado! {item_n} por {format_money(st.session_state.usd_input)}")
                st.cache_data.clear()
                st.rerun()
            else:
                st.error("Por favor ingresa un nombre y un valor mayor a cero.")

    # 3. Resumen
    if not df_g.empty:
        st.write("---")
        st.subheader("📋 Cotizaciones Guardadas")
        st.dataframe(df_g, use_container_width=True)
        total_usd = df_g["USD"].sum()
        st.metric("TOTAL ESTIMADO DEL VIAJE", format_money(total_usd))
