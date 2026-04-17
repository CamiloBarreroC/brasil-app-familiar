import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests

# 1. Configuración de la página
st.set_page_config(page_title="Misión Brasil 2026", page_icon="🇧🇷", layout="wide")

# --- FUNCIÓN PARA TASAS DE CAMBIO EN VIVO ---
@st.cache_data(ttl=3600)  # Se actualiza cada hora para no saturar la API
def obtener_tasas():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        usd_cop = data['rates']['COP']
        usd_brl = data['rates']['BRL']
        return usd_cop, usd_cop / usd_brl
    except:
        # Valores de respaldo por si falla la conexión
        return 3950.0, 780.0

usd_hoy, brl_hoy = obtener_tasas()

# 2. Conexión a Google Sheets (Asegúrate de tener tus Secrets configurados)
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ESTILOS VISUALES (Pestañas legibles y colores Brasil) ---
st.markdown(f"""
    <style>
    .main {{ background-color: #f8fafc; }}
    
    /* Configuración de Pestañas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: #002776; /* Azul Oscuro */
        padding: 10px 10px 0px 10px;
        border-radius: 10px 10px 0 0;
        gap: 15px;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: white !important;
        font-weight: bold;
        font-size: 16px;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: #009c3b !important; /* Verde Brasil */
        color: white !important;
        border-bottom: 4px solid #ffdf00; /* Línea Amarilla */
    }}
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("<h1 style='text-align: center; color: #002776;'>🚀 Misión Brasil 2026: Nuestra Aventura Inolvidable</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555; font-size: 1.2em;'>Un plan para toda la familia con unos detallitos para Mati y el abuelito</p>", unsafe_allow_html=True)
st.write("---")

# --- SIDEBAR (Conversor Automático) ---
st.sidebar.header("📊 Valores del Mercado")
st.sidebar.write(f"💵 **1 Dólar:** ${usd_hoy:,.2f} COP")
st.sidebar.write(f"🇧🇷 **1 Real:** ${brl_hoy:,.2f} COP")
st.sidebar.write("---")
moneda = st.sidebar.radio("Ver presupuesto en:", ["COP", "USD", "BRL"])

def format_money(usd_val):
    if moneda == "COP": return f"$ {usd_val * usd_hoy:,.0f} COP"
    if moneda == "BRL": return f"R$ {(usd_val * usd_hoy)/brl_hoy:,.2f}"
    return f"$ {usd_val:,.2f} USD"

# --- PESTAÑAS PRINCIPALES ---
tab1, tab2, tab3 = st.tabs(["🗺️ ITINERARIO DETALLADO", "⚽ MATI Y EL ABUELITO", "💰 COTIZACIONES"])

with tab1:
    # Imagen de Portada desde GitHub
    st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/rio.jpg", 
             use_container_width=True)
    
    st.header("📅 Cronograma de Ruta")
    
    # Datos del Itinerario
    it_data = [
        {"Fecha": "26 Dic", "Ruta": "Sao Paulo ➔ Santos", "Manejo": "1.5 h", "Hospedaje": "Santos", "Plan": "Llegada, recoger auto y dormir frente al mar."},
        {"Fecha": "27 Dic", "Ruta": "Santos ➔ Paraty", "Manejo": "4.5 h", "Hospedaje": "Paraty", "Plan": "Vila Belmiro (Santos) y ruta costera."},
        {"Fecha": "28 Dic", "Ruta": "Paraty", "Manejo": "---", "Hospedaje": "Paraty", "Plan": "Día de barco por las islas vírgenes."},
        {"Fecha": "29 Dic", "Ruta": "Paraty ➔ Río", "Manejo": "4 h", "Hospedaje": "Río", "Plan": "Check-in y atardecer en Copacabana."},
        {"Fecha": "30-31 Dic", "Ruta": "Río de Janeiro", "Manejo": "---", "Hospedaje": "Río", "Plan": "Año Nuevo y visita al Maracaná."},
        {"Fecha": "01-02 Ene", "Ruta": "Río ➔ Arraial", "Manejo": "3 h", "Hospedaje": "Arraial", "Plan": "Playas turquesas (Caribe Brasileño)."},
        {"Fecha": "03-05 Ene", "Ruta": "Subida a Salvador", "Manejo": "Varios", "Hospedaje": "Tramos", "Plan": "Recorrido por la costa hacia el norte."},
        {"Fecha": "06 Ene", "Ruta": "Salvador", "Manejo": "---", "Hospedaje": "Salvador", "Plan": "Pelourinho y cultura bahiana."},
        {"Fecha": "07-08 Ene", "Ruta": "Salvador ➔ Chapada", "Manejo": "6 h", "Hospedaje": "Lençóis", "Plan": "Cascadas y cuevas en Chapada Diamantina."},
        {"Fecha": "09 Ene", "Ruta": "Lençóis ➔ M. Claros", "Manejo": "8 h", "Hospedaje": "M. Claros", "Plan": "Regreso por el interior de Brasil."},
        {"Fecha": "10 Ene", "Ruta": "M. Claros ➔ Belo H.", "Manejo": "6 h", "Hospedaje": "Belo H.", "Plan": "Mineirão y cena de despedida minera."},
        {"Fecha": "11 Ene", "Ruta": "Belo H. ➔ Sao Paulo", "Manejo": "7 h", "Hospedaje": "---", "Plan": "Entrega de carro y vuelo de regreso."}
    ]
    st.table(pd.DataFrame(it_data))

with tab2:
    st.header("🏟️ Ruta de los Templos")
    st.info("💡 Estas son las paradas especiales para Mati y el abuelito.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/maracana.jpg", 
                 caption="Maracanã (Río)", width=300)
    with col2:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/pacaembu.jpg", 
                 caption="Museo del Fútbol (SP)", width=300)
    with col3:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/santos.jpg", 
                 caption="Vila Belmiro (Santos)", width=300)

with tab3:
    st.header("📝 Cotizaciones y Presupuesto")
    
    # Leer datos del Google Sheet (Pestaña 'Cotizaciones')
    try:
        df_gastos = conn.read(worksheet="Cotizaciones", ttl=0)
    except:
        df_gastos = pd.DataFrame(columns=["Item", "Categoría", "USD", "Notas"])

    with st.form("nuevo_gasto", clear_on_submit=True):
        c_a, c_b = st.columns(2)
        item = c_a.text_input("¿Qué estamos cotizando?")
        cat = c_b.selectbox("Categoría", ["Vuelos", "Carro", "Hospedaje", "Comida", "Fútbol"])
        precio = c_a.number_input("Precio en Dólares (USD)", min_value=0.0)
        notas = c_b.text_input("Notas adicionales")
        
        if st.form_submit_button("Guardar en el Plan"):
            if item:
                nueva_fila = pd.DataFrame([{"Item": item, "Categoría": cat, "USD": precio, "Notas": notas}])
                df_actualizado = pd.concat([df_gastos, nueva_fila], ignore_index=True)
                conn.update(worksheet="Cotizaciones", data=df_actualizado)
                st.success("¡Cotización guardada exitosamente!")
                st.cache_data.clear()
            else:
                st.error("Por favor, ponle un nombre a la cotización.")

    st.write("---")
    st.subheader("💰 Resumen Actual")
    if not df_gastos.empty:
        st.dataframe(df_gastos, use_container_width=True)
        total_acumulado = df_gastos["USD"].sum()
        st.metric("Total Estimado", format_money(total_acumulado))
    else:
        st.info("Aún no hay cotizaciones guardadas. ¡Empecemos!")
