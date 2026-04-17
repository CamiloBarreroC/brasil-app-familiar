import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests

# 1. Configuración de la página
st.set_page_config(page_title="Misión Brasil 2026", page_icon="🇧🇷", layout="wide")

# --- TASAS DE CAMBIO AUTOMÁTICAS ---
@st.cache_data(ttl=3600) # Se actualiza cada hora
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

# --- ESTILOS VISUALES (Pestañas legibles y colores Brasil) ---
st.markdown(f"""
    <style>
    .main {{ background-color: #f8fafc; }}
    
    /* Pestañas (Tabs) */
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
        border-bottom: 4px solid #ffdf00;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("<h1 style='text-align: center; color: #002776;'>🚀 Misión Brasil 2026: Nuestra Aventura Inolvidable</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555; font-size: 1.2em;'>Un plan para toda la familia con unos detallitos para Mati y el abuelito</p>", unsafe_allow_html=True)
st.write("---")

# --- SIDEBAR (Precios del día) ---
st.sidebar.header("📊 Valores del Día")
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
    # IMAGEN DESDE TU GITHUB
    st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/rio.jpg", 
             use_container_width=True)
    
    st.header("📅 Cronograma de Ruta")
    st.write("Este es el plan día a día para que la familia sepa dónde estaremos.")
    
    # Itinerario con fechas, tiempos de manejo y hospedaje
    it_data = [
        {"Fecha": "26 Dic", "Ruta": "Sao Paulo ➔ Santos", "Manejo": "1.5 h", "Hospedaje": "Santos", "Plan": "Llegada, recoger auto y dormir frente al mar."},
        {"Fecha": "27 Dic", "Ruta": "Santos ➔ Paraty", "Manejo": "4.5 h", "Hospedaje": "Paraty", "Plan": "Vila Belmiro por la mañana y ruta costera."},
        {"Fecha": "28 Dic", "Ruta": "Paraty", "Manejo": "---", "Hospedaje": "Paraty", "Plan": "Día de barco por las islas vírgenes."},
        {"Fecha": "29 Dic", "Ruta": "Paraty ➔ Río", "Manejo": "4 h", "Hospedaje": "Río", "Plan": "Check-in y atardecer en Copacabana."},
        {"Fecha": "30-31 Dic", "Ruta": "Río de Janeiro", "Manejo": "---", "Hospedaje": "Río", "Plan": "Año Nuevo y visita al Maracaná."},
        {"Fecha": "01-02 Ene", "Ruta": "Río ➔ Arraial", "Manejo": "3 h", "Hospedaje": "Arraial", "Plan": "Playas turquesas (Caribe Brasileño)."},
        {"Fecha": "03-05 Ene", "Ruta": "Subida a Salvador", "Manejo": "Tramos", "Hospedaje": "Varios", "Plan": "Recorrido por la costa hacia el norte."},
        {"Fecha": "06 Ene", "Ruta": "Salvador", "Manejo": "---", "Hospedaje": "Salvador", "Plan": "Pelourinho y cultura bahiana."},
        {"Fecha": "07-08 Ene", "Ruta": "Salvador ➔ Chapada", "Manejo": "6 h", "Hospedaje": "Lençóis", "Plan": "Cascadas y cuevas en Chapada Diamantina."},
        {"Fecha": "09 Ene", "Ruta": "Lençóis ➔ M. Claros", "Manejo": "8 h", "Hospedaje": "M. Claros", "Plan": "Regreso por el interior de Brasil."},
        {"Fecha": "10 Ene", "Ruta": "M. Claros ➔ Belo H.", "Manejo": "6 h", "Hospedaje": "Belo H.", "Plan": "Mineirão y cena de despedida minera."},
        {"Fecha": "11 Ene", "Ruta": "Belo H. ➔ Sao Paulo", "Manejo": "7 h", "Hospedaje": "---", "Plan": "Entrega de carro y vuelo de regreso."}
    ]
    st.table(pd.DataFrame(it_data))

with tab2:
    st.header("🏟️ Ruta de los Templos")
    st.info("💡 Consejo: Sube las fotos 'maracana.jpg', 'pacaembu.jpg' y 'santos.jpg' a la carpeta 'img' para que aparezcan aquí.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/maracana.jpg", caption="Maracanã (Río)", fallback="Sube maracana.jpg a GitHub")
    with c2:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/pacaembu.jpg", caption="Museo del Fútbol (SP)", fallback="Sube pacaembu.jpg a GitHub")
    with c3:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/santos.jpg", caption="Vila Belmiro (Santos)", fallback="Sube santos.jpg a GitHub")

with tab3:
    st.header("📝 Cotizaciones y Presupuesto")
    try:
        df_g = conn.read(worksheet="Cotizaciones", ttl=0)
    except:
        df_g = pd.DataFrame(columns=["Item", "Categoría", "USD", "Notas"])

    with st.form("nuevo_gasto", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        item = col_a.text_input("¿Qué cotizaste?")
        cat = col_b.selectbox("Categoría", ["Vuelos", "Carro", "Hospedaje", "Comida", "Fútbol"])
        precio = col_a.number_input("Precio en Dólares (USD)", min_value=0.0)
        notas = col_b.text_input("Notas adicionales")
        if st.form_submit_button("Guardar en el Plan"):
            if item:
                new_row = pd.DataFrame([{"Item": item, "Categoría": cat, "USD": precio, "Notas": notas}])
                conn.update(worksheet="Cotizaciones", data=pd.concat([df_g, new_row], ignore_index=True))
                st.success("¡Guardado!")
                st.cache_data.clear()

    st.write("---")
    if not df_g.empty:
        st.dataframe(df_g, use_container_width=True)
        st.metric("Total Proyectado", format_money(df_g["USD"].sum()))
