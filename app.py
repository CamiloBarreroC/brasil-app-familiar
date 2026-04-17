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
        # Obtenemos la base USD para calcular COP y BRL
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        usd_cop = data['rates']['COP']
        usd_brl = data['rates']['BRL']
        return usd_cop, usd_cop / usd_brl
    except:
        # Valores de respaldo por si falla la API
        return 3950.0, 780.0

usd_hoy, brl_hoy = obtener_tasas()

# 2. Conexión a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ESTILOS MODO OSCURO PRO (BRASIL GOLD EDITION) ---
st.markdown(f"""
    <style>
    /* Fondo principal oscuro */
    .stApp {{
        background-color: #0e1117;
    }}
    
    /* Títulos en Dorado Brasil */
    h1, h2, h3 {{
        color: #ffdf00 !important;
        text-align: center;
        font-family: 'Arial Black', sans-serif;
    }}
    
    /* Textos generales en Blanco */
    p, span, label, .stMarkdown {{
        color: #ffffff !important;
    }}

    /* Estilo de las Pestañas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: #1a1c24;
        border-radius: 10px;
        padding: 5px;
        gap: 10px;
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

    /* Tablas y Dataframes en modo oscuro */
    .stTable, [data-testid="stTable"] {{
        background-color: #1a1c24;
        color: white !important;
        border-radius: 10px;
    }}
    
    [data-testid="stTable"] td, [data-testid="stTable"] th {{
        color: white !important;
        border-bottom: 1px solid #31333f;
    }}

    /* Sidebar Oscuro */
    section[data-testid="stSidebar"] {{
        background-color: #000b1a;
    }}
    
    /* Inputs y Botones */
    .stButton>button {{
        background-color: #009c3b;
        color: white;
        border-radius: 10px;
        border: none;
        font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO PRINCIPAL ---
st.markdown("<h1>🚀 MISIÓN BRASIL 2026</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2em;'>Un plan para toda la familia con unos detallitos para Mati y el abuelito</p>", unsafe_allow_html=True)
st.write("---")

# --- SIDEBAR (Conversor y Tasas) ---
st.sidebar.header("💰 Tasas de Cambio Hoy")
st.sidebar.metric("1 Dólar (USD)", f"${usd_hoy:,.0f} COP")
st.sidebar.metric("1 Real (BRL)", f"${brl_hoy:,.0f} COP")
st.sidebar.write("---")
moneda_v = st.sidebar.radio("Ver presupuesto en:", ["COP", "USD", "BRL"])

def format_money(usd_val):
    if moneda_v == "COP": return f"$ {usd_val * usd_hoy:,.0f} COP"
    if moneda_v == "BRL": return f"R$ {(usd_val * usd_hoy)/brl_hoy:,.2f}"
    return f"$ {usd_val:,.2f} USD"

# --- ESTRUCTURA DE PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["🗺️ ITINERARIO DETALLADO", "⚽ MATI Y EL ABUELITO", "💰 COTIZACIONES"])

with tab1:
    # Foto de Portada Centrada
    col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
    with col_img2:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/rio.jpg", 
                 caption="Nuestra meta: ¡Brasil en familia!", width=500)
    
    st.header("📅 Cronograma de Ruta")
    it_data = [
        {"Fecha": "26 Dic", "Ruta": "Sao Paulo ➔ Santos", "Manejo": "1.5 h", "Hospedaje": "Santos", "Plan": "Llegada, recoger auto y cena frente al mar."},
        {"Fecha": "27 Dic", "Ruta": "Santos ➔ Paraty", "Manejo": "4.5 h", "Hospedaje": "Paraty", "Plan": "Vila Belmiro (Mati/Abuelo) y ruta costera."},
        {"Fecha": "28 Dic", "Ruta": "Paraty", "Manejo": "---", "Hospedaje": "Paraty", "Plan": "Día de lancha privada por las islas."},
        {"Fecha": "29 Dic", "Ruta": "Paraty ➔ Río", "Manejo": "4 h", "Hospedaje": "Río", "Plan": "Check-in y atardecer en Copacabana."},
        {"Fecha": "30-31 Dic", "Ruta": "Río de Janeiro", "Manejo": "---", "Hospedaje": "Río", "Plan": "Reveillon (Año Nuevo) y Maracanã."},
        {"Fecha": "01-02 Ene", "Ruta": "Río ➔ Arraial", "Manejo": "3 h", "Hospedaje": "Arraial", "Plan": "Descanso en el caribe brasileño."},
        {"Fecha": "03-05 Ene", "Ruta": "Costa Norte", "Manejo": "Tramos", "Hospedaje": "Varios", "Plan": "Ruta panorámica hacia Salvador."},
        {"Fecha": "06 Ene", "Ruta": "Salvador", "Manejo": "---", "Hospedaje": "Salvador", "Plan": "Pelourinho y cultura bahiana."},
        {"Fecha": "07-08 Ene", "Ruta": "Salvador ➔ Chapada", "Manejo": "6 h", "Hospedaje": "Lençóis", "Plan": "Naturaleza en Chapada Diamantina."},
        {"Fecha": "09 Ene", "Ruta": "Regreso Interior", "Manejo": "8 h", "Hospedaje": "M. Claros", "Plan": "Cruce del interior (Tramo largo)."},
        {"Fecha": "10 Ene", "Ruta": "M. Claros ➔ Belo H.", "Manejo": "6 h", "Hospedaje": "Belo H.", "Plan": "Comida minera y visita al Mineirão (¡El del 1-7!)."},
        {"Fecha": "11 Ene", "Ruta": "Belo H. ➔ Sao Paulo", "Manejo": "7 h", "Hospedaje": "---", "Plan": "Entrega de carro y regreso a casa."}
    ]
    st.table(pd.DataFrame(it_data))

with tab2:
    st.header("🏟️ Ruta de los Templos")
    st.markdown("### ¡Las 4 paradas sagradas de Mati y el abuelito!")
    
    # Cuadrícula de 2x2 para los estadios
    fila1_col1, fila1_col2 = st.columns(2)
    with fila1_col1:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/maracana.jpg", 
                 caption="1. Maracanã (Río) - El Templo", width=300)
    with fila1_col2:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/pacaembu.jpg", 
                 caption="2. Museo del Fútbol (SP)", width=300)

    st.write("---")

    fila2_col1, fila2_col2 = st.columns(2)
    with fila2_col1:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/santos.jpg", 
                 caption="3. Vila Belmiro (Santos) - El Rey Pelé", width=300)
    with fila2_col2:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/mineirao.jpg", 
                 caption="4. Mineirão (BH) - ¡El del 1-7!", width=300)

with tab3:
    st.header("📝 Gestión de Presupuesto")
    try:
        df_gastos = conn.read(worksheet="Cotizaciones", ttl=0)
    except:
        df_gastos = pd.DataFrame(columns=["Item", "Categoría", "USD", "Notas"])

    with st.form("nuevo_gasto", clear_on_submit=True):
        st.subheader("Añadir Cotización")
        c_a, c_b = st.columns(2)
        item_n = c_a.text_input("Concepto (Ej: Hotel Río)")
        cat_n = c_b.selectbox("Categoría", ["Vuelos", "Carro", "Hospedaje", "Comida", "Entradas"])
        val_n = c_a.number_input("Precio en USD", min_value=0.0)
        not_n = c_b.text_input("Notas o Link")
        
        if st.form_submit_button("Guardar Cotización"):
            if item_n:
                nueva = pd.DataFrame([{"Item": item_n, "Categoría": cat_n, "USD": val_n, "Notas": not_n}])
                conn.update(worksheet="Cotizaciones", data=pd.concat([df_gastos, nueva], ignore_index=True))
                st.success("¡Datos guardados!")
                st.cache_data.clear()
                st.rerun()

    if not df_gastos.empty:
        st.write("---")
        st.subheader("💰 Resumen Consolidado")
        st.dataframe(df_gastos, use_container_width=True)
        total_usd = df_gastos["USD"].sum()
        st.metric("Total Acumulado", format_money(total_usd))
