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
    .stButton>button {{ background-color: #009c3b; color: white; border-radius: 10px; border: none; font-weight: bold; width: 100%; height: 3em; }}
    
    .input-container {{
        background-color: #1a1c24;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #009c3b;
        margin-bottom: 25px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("<h1>🚀 MISIÓN BRASIL 2026</h1>", unsafe_allow_html=True)
st.write("---")

# --- SIDEBAR ---
st.sidebar.header("💰 Tasas de Cambio")
st.sidebar.metric("Dólar (USD)", f"${usd_hoy:,.0f} COP")
st.sidebar.metric("Real (BRL)", f"${brl_hoy:,.0f} COP")
st.sidebar.write("---")
moneda_v = st.sidebar.radio("Ver presupuesto en:", ["COP", "USD", "BRL"])

def format_money(usd_val):
    if moneda_v == "COP": return f"$ {usd_val * usd_hoy:,.0f} COP"
    if moneda_v == "BRL": return f"R$ {(usd_val * usd_hoy)/brl_hoy:,.2f}"
    return f"$ {usd_val:,.2f} USD"

# --- PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["🗺️ ITINERARIO FLEXIBLE", "⚽ MATI Y EL ABUELITO", "💰 COTIZACIONES"])

with tab1:
    col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
    with col_img2:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/rio.jpg", caption="¡Brasil en familia!", width=500)
    
    st.header("📅 Cronograma Detallado")
    
    # --- SELECTOR DE OPCIÓN DE VUELO ---
    st.markdown("### ✈️ Configuración de Llegada")
    horario_vuelo = st.radio(
        "¿A qué hora llega el vuelo a São Paulo?",
        ["Llegada en la Mañana", "Llegada en la Tarde/Noche"],
        index=0,
        horizontal=True
    )
    
    # Definición de datos según el horario
    if horario_vuelo == "Llegada en la Mañana":
        st.success("✅ Opción A: Museo el Día 1")
        dia_1_plan = "Llegada, almuerzo y visita al Museo del Fútbol (Pacaembú). Viaje a Santos por la tarde."
        dia_2_plan = "Mañana en Vila Belmiro (Santos). Salida hacia Paraty al mediodía."
    else:
        st.warning("🌙 Opción B: Descanso y Museo el Día 2")
        dia_1_plan = "Llegada a São Paulo, traslado al hotel y descanso total de viaje largo."
        dia_2_plan = "9:00 AM Museo del Fútbol. 12:00 PM Salida a Santos. 3:00 PM Vila Belmiro. Dormir en Santos."

    it_data = [
        {"Fecha": "26 Dic", "Ruta": "Sao Paulo ➔ Santos", "Hospedaje": "Santos", "Plan": dia_1_plan},
        {"Fecha": "27 Dic", "Ruta": "Santos ➔ Paraty", "Hospedaje": "Paraty", "Plan": dia_2_plan},
        {"Fecha": "28 Dic", "Ruta": "Paraty", "Hospedaje": "Paraty", "Plan": "Día de lancha privada por las islas y bahía."},
        {"Fecha": "29 Dic", "Ruta": "Paraty ➔ Río", "Hospedaje": "Río", "Plan": "Ruta panorámica y atardecer en Copacabana."},
        {"Fecha": "30-31 Dic", "Ruta": "Río de Janeiro", "Hospedaje": "Río", "Plan": "Año Nuevo (Reveillon) y Tour Maracaná."},
        {"Fecha": "01-02 Ene", "Ruta": "Río ➔ Arraial", "Hospedaje": "Arraial", "Plan": "Prainhas do Pontal y relax total."},
        {"Fecha": "03-05 Ene", "Ruta": "Subida por Costa", "Hospedaje": "Varios", "Plan": "Hacia el norte con paradas en playas."},
        {"Fecha": "06 Ene", "Ruta": "Salvador", "Hospedaje": "Salvador", "Plan": "Centro histórico (Pelourinho)."},
        {"Fecha": "07-08 Ene", "Ruta": "Salvador ➔ Chapada", "Hospedaje": "Lençóis", "Plan": "Naturaleza y cascadas en Chapada."},
        {"Fecha": "09 Ene", "Ruta": "Regreso Interior", "Hospedaje": "M. Claros", "Plan": "Tramo largo de carretera."},
        {"Fecha": "10 Ene", "Ruta": "M. Claros ➔ Belo H.", "Hospedaje": "Belo H.", "Plan": "Mineirão (¡El del 1-7!) y comida minera."},
        {"Fecha": "11 Ene", "Ruta": "Vuelta a SP", "Hospedaje": "---", "Plan": "Entrega de auto y vuelo de regreso."}
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
    
    if 'usd_input' not in st.session_state: st.session_state.usd_input = 0.0
    if 'cop_input' not in st.session_state: st.session_state.cop_input = 0.0

    def sync_to_usd(): st.session_state.usd_input = st.session_state.cop_input / usd_hoy
    def sync_to_cop(): st.session_state.cop_input = st.session_state.usd_input * usd_hoy

    st.subheader("➕ Agregar Nueva Cotización")
    with st.container():
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        col_f1, col_f2 = st.columns(2)
        nombre_item = col_f1.text_input("¿Qué estás cotizando?", placeholder="Ej: Hotel en Río")
        categoria = col_f2.selectbox("Categoría", ["Vuelos", "Carro", "Hospedaje", "Comida", "Entradas"])
        st.write("**Ingresa el precio en la moneda que tengas:**")
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1: st.number_input("Precio en Pesos (COP)", min_value=0.0, key="cop_input", on_change=sync_to_usd, step=50000.0)
        with col_p2: st.number_input("Precio en Dólares (USD)", min_value=0.0, key="usd_input", on_change=sync_to_cop, step=10.0)
        with col_p3:
            brl_ref = (st.session_state.usd_input * usd_hoy) / brl_hoy
            st.metric("Referencia en Reales", f"R$ {brl_ref:,.2f}")
        notas = st.text_input("Notas adicionales")
        if st.button("🚀 GUARDAR ESTA COTIZACIÓN"):
            if nombre_item and st.session_state.usd_input > 0:
                try: df_actual = conn.read(worksheet="Cotizaciones", ttl=0)
                except: df_actual = pd.DataFrame(columns=["Item", "Categoría", "USD", "Notas"])
                nueva_fila = pd.DataFrame([{"Item": nombre_item, "Categoría": categoria, "USD": st.session_state.usd_input, "Notas": notas}])
                conn.update(worksheet="Cotizaciones", data=pd.concat([df_actual, nueva_fila], ignore_index=True))
                st.success("✅ ¡Guardado!")
                st.cache_data.clear()
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    try:
        df_mostrar = conn.read(worksheet="Cotizaciones", ttl=0)
        if not df_mostrar.empty:
            st.write("---")
            st.subheader("📋 Resumen de Gastos")
            st.dataframe(df_mostrar, use_container_width=True)
            st.metric("VALOR TOTAL ESTIMADO", format_money(df_mostrar["USD"].sum()))
    except: st.info("Aún no hay cotizaciones.")
