import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests

# 1. Configuración de la página
st.set_page_config(page_title="Misión Brasil 2026", page_icon="🇧🇷", layout="wide")

# --- FUNCIÓN: TASAS DE CAMBIO ---
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
    .stTabs [aria-selected="true"] {{ background-color: #009c3b !important; color: white !important; border-radius: 7px; }}
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
st.markdown("<h1>🚀 MISIÓN BRASIL 2026: ¡EL SUEÑO FAMILIAR!</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2em;'>19 días diseñados para cada miembro de la familia.</p>", unsafe_allow_html=True)
st.write("---")

# --- SIDEBAR ---
st.sidebar.header("💰 Finanzas en Vivo")
st.sidebar.metric("Dólar (USD)", f"${usd_hoy:,.0f} COP")
st.sidebar.metric("Real (BRL)", f"${brl_hoy:,.0f} COP")
st.sidebar.write("---")
moneda_v = st.sidebar.radio("Ver presupuesto en:", ["COP", "USD", "BRL"])

def format_money(usd_val):
    if moneda_v == "COP": return f"$ {usd_val * usd_hoy:,.0f} COP"
    if moneda_v == "BRL": return f"R$ {(usd_val * usd_hoy)/brl_hoy:,.2f}"
    return f"$ {usd_val:,.2f} USD"

# --- PESTAÑAS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️ RUTA 19 DÍAS", 
    "⚽ MATI Y ABUELO", 
    "🎢 BIANCA Y MATI", 
    "🥂 LOS CONSENTIDOS", 
    "💰 PRESUPUESTO"
])

# --- PESTAÑA 1: ITINERARIO ---
with tab1:
    col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
    with col_img2:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/rio.jpg", caption="¡Río nos espera!", width=500)
    
    st.header("📅 Nuestra Gran Travesía")
    
    st.markdown("### ✈️ Configuración de Llegada")
    horario_vuelo = st.radio(
        "¿A qué hora aterrizamos en São Paulo el 26 de diciembre?",
        ["Mañana (Llegamos con energía)", "Tarde/Noche (Directo al descanso)"],
        index=0, horizontal=True
    )
    
    # Lógica de primeros días según llegada
    if "Mañana" in horario_vuelo:
        h1, h2, p1, p2 = "Santos", "Paraty", "Aterrizaje en SP, Museo del Fútbol y descanso en los jardines de Santos.", "Vila Belmiro y ruta escénica hacia Paraty."
    else:
        h1, h2, p1, p2 = "São Paulo", "Santos", "Traslado al hotel y brindis de bienvenida.", "Museo del Fútbol (SP) y tarde en Vila Belmiro (Santos)."

    it_data = [
        {"Fecha": "26 Dic", "Hospedaje": h1, "Plan": p1},
        {"Fecha": "27 Dic", "Hospedaje": h2, "Plan": p2},
        {"Fecha": "28 Dic", "Hospedaje": "Paraty", "Plan": "Caminata histórica por el centro y tarde de cascadas."},
        {"Fecha": "29 Dic", "Hospedaje": "Río de Janeiro", "Plan": "Tramo final de la Rio-Santos y primer atardecer en Copacabana."},
        {"Fecha": "30 Dic", "Hospedaje": "Río de Janeiro", "Plan": "Día de estadios: Maracanã y AquaRio para los chicos."},
        {"Fecha": "31 Dic", "Hospedaje": "Río de Janeiro", "Plan": "Reveillón: Año Nuevo en la playa de Copacabana."},
        {"Fecha": "01 Ene", "Hospedaje": "Río de Janeiro", "Plan": "Descanso total tras la fiesta. Rambla de Ipanema."},
        {"Fecha": "02 Ene", "Hospedaje": "Búzios", "Plan": "Visita al Cristo Redentor y salida hacia el glamour de Búzios."},
        {"Fecha": "03 Ene", "Hospedaje": "Búzios", "Plan": "Playas chic, Rua das Pedras y buen vino frente al mar."},
        {"Fecha": "04 Ene", "Hospedaje": "Búzios", "Plan": "Día de relax total en las playas de Búzios."},
        {"Fecha": "05 Ene", "Hospedaje": "Curitiba", "Plan": "Travesía hacia el sur. Cena en el barrio italiano."},
        {"Fecha": "06 Ene", "Hospedaje": "Curitiba", "Plan": "Jardín Botánico y Museos (Plan calmado para el abuelo)."},
        {"Fecha": "07 Ene", "Hospedaje": "Penha", "Plan": "Salida de Curitiba y llegada al mundo de Beto Carrero."},
        {"Fecha": "08 Ene", "Hospedaje": "Penha", "Plan": "Beto Carrero World: Día 1 de adrenalina pura."},
        {"Fecha": "09 Ene", "Hospedaje": "Penha", "Plan": "Beto Carrero World: Día 2 de shows y emociones."},
        {"Fecha": "10 Ene", "Hospedaje": "Balneário Camboriú", "Plan": "Teleféricos, yates y lujo en la ciudad moderna del sur."},
        {"Fecha": "11 Ene", "Hospedaje": "São Paulo", "Plan": "Regreso a la capital y descanso."},
        {"Fecha": "12 Ene", "Hospedaje": "São Paulo", "Plan": "Compras en Jardins, Mercado Municipal y cena de despedida."},
        {"Fecha": "13 Ene", "Hospedaje": "---", "Plan": "Últimas compras y vuelo de regreso a casa."}
    ]
    st.table(pd.DataFrame(it_data))

# --- PESTAÑA 2: MATI Y EL ABUELO ---
with tab2:
    st.header("🏟️ Ruta de los Templos Sagrados")
    f1c1, f1c2 = st.columns(2)
    with f1c1: st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/maracana.jpg", caption="Maracanã", width=400)
    with f1c2: st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/pacaembu.jpg", caption="Museo del Fútbol", width=400)
    st.write("---")
    f2c1, f2c2 = st.columns(2)
    with f2c1: st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/santos.jpg", caption="Vila Belmiro", width=400)
    with f2c2: st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/mineirao.jpg", caption="Mineirão", width=400)

# --- PESTAÑA 3: BIANCA Y MATI ---
with tab3:
    st.header("🎢 Adrenalina y Gritos")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.image("https://images.unsplash.com/photo-1513889959013-c2845acb46ad?q=80&w=500", caption="Beto Carrero World")
    with col_p2:
        st.subheader("¡Imperdibles!")
        st.write("- **FireWhip:** Montaña rusa invertida.\n- **Big Tower:** Caída de 100m.\n- **AquaRio:** Tiburones en Río.")

# --- PESTAÑA 4: LOS CONSENTIDOS ---
with tab4:
    st.header("🥂 El Club de los Consentidos")
    st.write("**Amparo, Jime, Diana y Giorgio:** Aquí mandan los placeres.")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.subheader("🍴 Gastronomía y Vinos")
        st.write("- Cena frente al mar en Búzios.\n- Pizza gourmet en São Paulo.\n- Brunch chic en Leblon (Río).")
    with col_c2:
        st.subheader("🛍️ Shopping y Paseos")
        st.write("- Rua Oscar Freire en SP.\n- Jardín Botánico de Curitiba.\n- Rua das Pedras en Búzios.")

# --- PESTAÑA 5: PRESUPUESTO ---
with tab5:
    st.header("💰 Gestión de Presupuesto")
    if 'usd_input' not in st.session_state: st.session_state.usd_input = 0.0
    if 'cop_input' not in st.session_state: st.session_state.cop_input = 0.0
    def sync_to_usd(): st.session_state.usd_input = st.session_state.cop_input / usd_hoy
    def sync_to_cop(): st.session_state.cop_input = st.session_state.usd_input * usd_hoy

    st.subheader("➕ Agregar Nueva Cotización")
    with st.container():
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        col_f1, col_f2 = st.columns(2)
        nombre_item = col_f1.text_input("¿Qué cotizamos?", placeholder="Ej: Hotel en Búzios")
        categoria = col_f2.selectbox("Categoría", ["Vuelos", "Carro", "Hospedaje", "Comida", "Parques"])
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1: st.number_input("Pesos (COP)", min_value=0.0, key="cop_input", on_change=sync_to_usd, step=50000.0)
        with col_p2: st.number_input("Dólares (USD)", min_value=0.0, key="usd_input", on_change=sync_to_cop, step=10.0)
        with col_p3:
            brl_ref = (st.session_state.usd_input * usd_hoy) / brl_hoy
            st.metric("Referencia en Reales", f"R$ {brl_ref:,.2f}")
        if st.button("🚀 GUARDAR COTIZACIÓN"):
            if nombre_item and st.session_state.usd_input > 0:
                try: df_actual = conn.read(worksheet="Cotizaciones", ttl=0)
                except: df_actual = pd.DataFrame(columns=["Item", "Categoría", "USD", "Notas"])
                nueva_fila = pd.DataFrame([{"Item": nombre_item, "Categoría": categoria, "USD": st.session_state.usd_input, "Notas": ""}])
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
    except: st.info("Sin cotizaciones guardadas.")
        
