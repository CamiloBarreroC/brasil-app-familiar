import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests

# 1. Configuración de la página
st.set_page_config(page_title="Misión Brasil 2026", page_icon="🇧🇷", layout="wide")

# --- FUNCIÓN PARA BUSCAR PRECIOS DEL DÍA (API REAL) ---
def obtener_tasas():
    try:
        # Buscamos la tasa USD -> COP y USD -> BRL
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        usd_cop = data['rates']['COP']
        usd_brl = data['rates']['BRL']
        brl_cop = usd_cop / usd_brl
        return usd_cop, brl_cop
    except:
        # Si falla la API, dejamos unos valores de respaldo
        return 3950.0, 780.0

usd_hoy, brl_hoy = obtener_tasas()

# 2. Conexión a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ESTILOS VISUALES ---
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stTabs [data-baseweb="tab-list"] {
        background-color: #002776;
        padding: 10px 10px 0px 10px;
        border-radius: 10px 10px 0 0;
    }
    .stTabs [data-baseweb="tab"] {
        color: #ffffff !important;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #009c3b !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("<h1 style='text-align: center; color: #002776;'>🚀 Misión Brasil 2026: Nuestra Aventura Inolvidable</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555; font-size: 1.2em;'>Un plan para toda la familia con unos detallitos para Mati y el abuelito</p>", unsafe_allow_html=True)
st.write("---")

# --- SIDEBAR (CON PRECIOS EN VIVO) ---
st.sidebar.header("📈 Tasas de Cambio en Vivo")
st.sidebar.write(f"**1 USD:** ${usd_hoy:,.2f} COP")
st.sidebar.write(f"**1 BRL:** ${brl_hoy:,.2f} COP")
st.sidebar.info("Precios actualizados automáticamente vía API.")

moneda = st.sidebar.radio("Mostrar presupuesto en:", ["COP", "USD", "BRL"])

def format_money(usd_val):
    if moneda == "COP": return f"$ {usd_val * usd_hoy:,.0f} COP"
    if moneda == "BRL": return f"R$ {(usd_val * usd_hoy)/brl_hoy:,.2f}"
    return f"$ {usd_val:,.2f} USD"

# --- PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["🗺️ ITINERARIO", "⚽ ESTADIOS", "💰 COTIZACIONES"])

with tab1:
    st.header("📅 Cronograma del Viaje")
    
    # Itinerario organizado por filas
    it_df = pd.DataFrame([
        {"Fecha": "26 - 27 Dic", "Destino": "São Paulo / Santos", "Plan": "Llegada, Museos y visita a la casa de Pelé."},
        {"Fecha": "28 Dic", "Destino": "Paraty", "Plan": "Pueblo colonial, barquitos y descanso."},
        {"Fecha": "29 - 31 Dic", "Destino": "Río de Janeiro", "Plan": "Año Nuevo en la playa y visita al Maracanã."},
        {"Fecha": "01 - 02 Ene", "Destino": "Arraial do Cabo", "Plan": "Caribe brasileño: aguas cristalinas y sol."},
        {"Fecha": "03 - 06 Ene", "Destino": "Salvador de Bahía", "Plan": "Cultura, música y comida bahiana."},
        {"Fecha": "07 - 11 Ene", "Destino": "Regreso", "Plan": "Chapada Diamantina, Minas Gerais y vuelta a SP."}
    ])
    
    st.table(it_df)
    st.image("https://images.unsplash.com/photo-1518107616985-bd48230d3b20?q=80&w=1200", caption="¡Prepárense para el verano brasileño!")

with tab2:
    st.header("🏟️ Ruta de los Templos")
    st.write("Fotos exclusivas de los lugares que visitarán Mati y el abuelito.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.image("https://images.unsplash.com/photo-1619551730161-12f567840134?q=80&w=500", caption="El imponente Maracanã (Río)")
    with c2:
        st.image("https://images.unsplash.com/photo-1529900214229-1b606e391e1d?q=80&w=500", caption="Museo del Fútbol (Pacaembú)")
    with c3:
        st.image("https://images.unsplash.com/photo-1599341457639-968600d80e7d?q=80&w=500", caption="Vila Belmiro (Santos)")

with tab3:
    st.header("📝 Cotizaciones Guardadas")
    
    try:
        df_gastos = conn.read(worksheet="Cotizaciones", ttl=0)
    except:
        df_gastos = pd.DataFrame(columns=["Item", "Categoría", "USD", "Notas"])

    with st.form("nuevo_gasto", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        item = col_a.text_input("¿Qué estamos cotizando?")
        cat = col_b.selectbox("Categoría", ["Vuelos", "Hospedaje", "Comida", "Fútbol", "Otros"])
        precio = col_a.number_input("Precio en USD", min_value=0.0)
        notas = col_b.text_input("Notas adicionales")
        
        if st.form_submit_button("Guardar en el Plan"):
            if item:
                new_row = pd.DataFrame([{"Item": item, "Categoría": cat, "USD": precio, "Notas": notas}])
                updated_df = pd.concat([df_gastos, new_row], ignore_index=True)
                conn.update(worksheet="Cotizaciones", data=updated_df)
                st.success("¡Cotización guardada!")
                st.cache_data.clear()
            else:
                st.error("Ponle un nombre a la cotización.")

    st.write("---")
    if not df_gastos.empty:
        st.dataframe(df_gastos, use_container_width=True)
        total_acumulado = df_gastos["USD"].sum()
        st.metric("Total Estimado", format_money(total_acumulado))
