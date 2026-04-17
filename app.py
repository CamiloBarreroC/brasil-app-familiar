import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests

# 1. Configuración de página
st.set_page_config(page_title="Misión Brasil 2026", page_icon="🇧🇷", layout="wide")

# --- TASAS DE CAMBIO EN VIVO ---
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

# --- ESTILOS VISUALES (CONTRASTE ALTO) ---
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stTabs [data-baseweb="tab-list"] {
        background-color: #002776;
        padding: 10px 10px 0px 10px;
        border-radius: 10px 10px 0 0;
    }
    .stTabs [data-baseweb="tab"] {
        color: white !important; /* Letras blancas siempre */
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #009c3b !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("<h1 style='text-align: center; color: #002776;'>🚀 Misión Brasil 2026: Nuestra Aventura Inolvidable</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555; font-size: 1.1em;'>Un plan para toda la familia con unos detallitos para Mati y el abuelito</p>", unsafe_allow_html=True)
st.write("---")

# --- SIDEBAR ---
st.sidebar.header("📈 Tasas del Día")
st.sidebar.write(f"**Dólar:** ${usd_hoy:,.2f} COP")
st.sidebar.write(f"**Real:** ${brl_hoy:,.2f} COP")
moneda = st.sidebar.radio("Ver presupuesto en:", ["COP", "USD", "BRL"])

def format_money(usd_val):
    if moneda == "COP": return f"$ {usd_val * usd_hoy:,.0f} COP"
    if moneda == "BRL": return f"R$ {(usd_val * usd_hoy)/brl_hoy:,.2f}"
    return f"$ {usd_val:,.2f} USD"

# --- PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["🗺️ ITINERARIO DETALLADO", "⚽ MATI Y EL ABUELITO", "💰 COTIZACIONES"])

with tab1:
    st.header("📅 Cronograma de Ruta (4,200 km aprox.)")
    
    # Tabla detallada con tiempos de manejo
    it_data = [
        {"Fecha": "26 Dic", "Ruta": "Sao Paulo ➔ Santos", "Manejo": "1.5 h", "Hospedaje": "Santos", "Plan": "Llegada, entrega de carro y descanso frente al mar."},
        {"Fecha": "27 Dic", "Ruta": "Santos ➔ Paraty", "Manejo": "4.5 h", "Hospedaje": "Paraty", "Plan": "Visita a Vila Belmiro (Mati/Abuelo) y ruta costera."},
        {"Fecha": "28 Dic", "Ruta": "Paraty", "Manejo": "---", "Hospedaje": "Paraty", "Plan": "Día de barco por las islas y centro histórico."},
        {"Fecha": "29 Dic", "Ruta": "Paraty ➔ Río", "Manejo": "4 h", "Hospedaje": "Río", "Plan": "Llegada a Río y tarde en Copacabana."},
        {"Fecha": "30-31 Dic", "Ruta": "Río de Janeiro", "Manejo": "---", "Hospedaje": "Río", "Plan": "Año Nuevo (Reveillon) y Tour Maracaná."},
        {"Fecha": "01-02 Ene", "Ruta": "Río ➔ Arraial", "Manejo": "3 h", "Hospedaje": "Arraial", "Plan": "Descanso en el 'Caribe Brasileño'."},
        {"Fecha": "03-05 Ene", "Ruta": "Arraial ➔ Salvador", "Manejo": "Dividido", "Hospedaje": "Salvador", "Plan": "Subida por la costa hacia el Pelourinho."},
        {"Fecha": "06 Ene", "Ruta": "Salvador", "Manejo": "---", "Hospedaje": "Salvador", "Plan": "Cultura afro-brasileña y Mercado Modelo."},
        {"Fecha": "07-08 Ene", "Ruta": "Salvador ➔ Chapada", "Manejo": "6 h", "Hospedaje": "Lençóis", "Plan": "Aventura en cascadas y cuevas (Chapada Diamantina)."},
        {"Fecha": "09 Ene", "Ruta": "Chapada ➔ M. Claros", "Manejo": "8 h", "Hospedaje": "M. Claros", "Plan": "Tramo largo de regreso cruzando el interior."},
        {"Fecha": "10 Ene", "Ruta": "M. Claros ➔ Belo H.", "Manejo": "6 h", "Hospedaje": "Belo H.", "Plan": "Comida minera y visita al Mineirão."},
        {"Fecha": "11 Ene", "Ruta": "Belo H. ➔ Sao Paulo", "Manejo": "7 h", "Hospedaje": "---", "Plan": "Regreso, entrega de carro y vuelo a casa."}
    ]
    st.table(pd.DataFrame(it_data))
    
    # Imagen desde tu GitHub (Asegúrate de subir una foto a la carpeta img/rio.jpg)
    # Por ahora dejo un link de respaldo más robusto
    st.image("https://images.unsplash.com/photo-1516306580123-e6e52b1b7b5f?q=80&w=1200", caption="Vista de Río desde el Pan de Azúcar")

with tab2:
    st.header("🏟️ Ruta de los Templos: Mati y el abuelito")
    st.info("Estos son los 3 estadios que visitaremos en el viaje.")
    
    c1, c2, c3 = st.columns(3)
    # Estos links son de Wikipedia, suelen fallar menos que los de Unsplash
    with c1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Est%C3%A1dio_do_Maracan%C3%A3_-_Rio_de_Janeiro.jpg/640px-Est%C3%A1dio_do_Maracan%C3%A3_-_Rio_de_Janeiro.jpg", caption="Maracanã (Río)")
    with c2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Est%C3%A1dio_do_Pacaembu_2014.jpg/640px-Est%C3%A1dio_do_Pacaembu_2014.jpg", caption="Museo del Fútbol (SP)")
    with c3:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Est%C3%A1dio_Urbano_Caldeira_%28Vila_Belmiro%29_-_Santos_FC.jpg/640px-Est%C3%A1dio_Urbano_Caldeira_%28Vila_Belmiro%29_-_Santos_FC.jpg", caption="Vila Belmiro (Santos)")

with tab3:
    st.header("📝 Cotizaciones del Plan")
    try:
        df_g = conn.read(worksheet="Cotizaciones", ttl=0)
    except:
        df_g = pd.DataFrame(columns=["Item", "Categoría", "USD", "Notas"])

    with st.form("nuevo_gasto", clear_on_submit=True):
        c_a, c_b = st.columns(2)
        item = c_a.text_input("Concepto")
        cat = c_b.selectbox("Categoría", ["Vuelos", "Carro", "Hospedaje", "Comida", "Entradas"])
        precio = c_a.number_input("Valor en USD", min_value=0.0)
        notas = c_b.text_input("Notas")
        if st.form_submit_button("Guardar Cotización"):
            if item:
                new_row = pd.DataFrame([{"Item": item, "Categoría": cat, "USD": precio, "Notas": notas}])
                conn.update(worksheet="Cotizaciones", data=pd.concat([df_g, new_row], ignore_index=True))
                st.success("¡Guardado!")
                st.cache_data.clear()

    st.write("---")
    if not df_g.empty:
        st.dataframe(df_g, use_container_width=True)
        st.metric("Total Estimado", format_money(df_g["USD"].sum()))
