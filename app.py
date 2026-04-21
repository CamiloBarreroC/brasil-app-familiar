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
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ESTILOS MODO OSCURO PRO (BRASIL GOLD) ---
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
st.markdown("<p style='text-align: center; font-size: 1.2em;'>19 días: SP, Río, Búzios, Curitiba y Beto Carrero.</p>", unsafe_allow_html=True)
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
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/rio.jpg", caption="¡Un viaje para recordar por siempre!", width=500)
    
    st.header("📅 Nuestra Ruta Paso a Paso")
    
    st.markdown("### ✈️ Configuración de Llegada")
    horario_vuelo = st.radio(
        "¿A qué hora aterrizamos en São Paulo el 26 de diciembre?",
        ["Mañana", "Tarde/Noche"],
        index=0, horizontal=True
    )
    
    # Lógica dinámica según llegada
    if "Mañana" in horario_vuelo:
        dia_1 = {"Fecha": "26 Dic", "Trayecto": "SP -> Santos", "Hospedaje": "Santos", "Plan": "Aterrizaje, Museo del Fútbol y caminata por los jardines de Santos."}
        dia_2 = {"Fecha": "27 Dic", "Trayecto": "Santos -> Paraty", "Hospedaje": "Paraty", "Plan": "Vila Belmiro y ruta escénica por la costa hacia Paraty."}
    else:
        dia_1 = {"Fecha": "26 Dic", "Trayecto": "Aeropuerto -> Hotel", "Hospedaje": "São Paulo", "Plan": "Traslado y brindis de bienvenida. Descanso del vuelo."}
        dia_2 = {"Fecha": "27 Dic", "Trayecto": "SP -> Santos", "Hospedaje": "Santos", "Plan": "Mañana en Museo del Fútbol (SP) y tarde en Vila Belmiro (Santos)."}

    it_base = [
        {"Fecha": "28 Dic", "Trayecto": "Estancia Paraty", "Hospedaje": "Paraty", "Plan": "Centro Histórico y tarde de cascadas (suelo firme para el abuelo)."},
        {"Fecha": "29 Dic", "Trayecto": "Paraty -> Río", "Hospedaje": "Río de Janeiro", "Plan": "Tramo final de la Rio-Santos y primer atardecer en Copacabana."},
        {"Fecha": "30 Dic", "Trayecto": "Río (Estadios)", "Hospedaje": "Río de Janeiro", "Plan": "Maracanã para el abuelo y AquaRio para Bianca y Mati."},
        {"Fecha": "31 Dic", "Trayecto": "Río (Año Nuevo)", "Hospedaje": "Río de Janeiro", "Plan": "Reveillón: Cena y fuegos artificiales en Copacabana."},
        {"Fecha": "01 Ene", "Trayecto": "Río Relax", "Hospedaje": "Río de Janeiro", "Plan": "Descanso total tras la fiesta. Paseo por la rambla de Ipanema."},
        {"Fecha": "02 Ene", "Trayecto": "Río -> Búzios", "Hospedaje": "Búzios", "Plan": "Cristo Redentor por la mañana y salida hacia el glamour de Búzios."},
        {"Fecha": "03 Ene", "Trayecto": "Estancia Búzios", "Hospedaje": "Búzios", "Plan": "Playas chic, Rua das Pedras y buen vino frente al mar."},
        {"Fecha": "04 Ene", "Trayecto": "Estancia Búzios", "Hospedaje": "Búzios", "Plan": "Día de relax total en las playas de la península."},
        {"Fecha": "05 Ene", "Trayecto": "Búzios -> Curitiba", "Hospedaje": "Curitiba", "Plan": "Travesía hacia el sur. Cena en el barrio italiano de Santa Felicidade."},
        {"Fecha": "06 Ene", "Trayecto": "Estancia Curitiba", "Hospedaje": "Curitiba", "Plan": "Jardín Botánico y Museos (Plan calmado para el abuelo y Amparo)."},
        {"Fecha": "07 Ene", "Trayecto": "Curitiba -> Penha", "Hospedaje": "Penha", "Plan": "Salida de Curitiba y llegada al mundo de Beto Carrero."},
        {"Fecha": "08 Ene", "Trayecto": "Beto Carrero", "Hospedaje": "Penha", "Plan": "Día 1: Adrenalina pura para Bianca y Mati (FireWhip/Hot Wheels)."},
        {"Fecha": "09 Ene", "Trayecto": "Beto Carrero", "Hospedaje": "Penha", "Plan": "Día 2: Shows y últimas montañas rusas para los chicos."},
        {"Fecha": "10 Ene", "Trayecto": "Penha -> Balneário", "Hospedaje": "Baln. Camboriú", "Plan": "Teleféricos, yates y lujo en la ciudad moderna del sur."},
        {"Fecha": "11 Ene", "Trayecto": "Balneário -> SP", "Hospedaje": "São Paulo", "Plan": "Regreso a la capital brasileña y descanso nocturno."},
        {"Fecha": "12 Ene", "Trayecto": "Estancia SP", "Hospedaje": "São Paulo", "Plan": "Compras en Oscar Freire, Mercado Municipal y cena de despedida."},
        {"Fecha": "13 Ene", "Trayecto": "SP -> Aeropuerto", "Hospedaje": "---", "Plan": "Últimas compras de recuerdos y vuelo de regreso a casa."}
    ]
    
    it_completo = [dia_1, dia_2] + it_base
    st.table(pd.DataFrame(it_completo))

# --- LAS DEMÁS PESTAÑAS (Fútbol, Adrenalina, Consentidos, Presupuesto) SIGUEN IGUAL ---
with tab2:
    st.header("🏟️ Ruta de los Templos Sagrados")
    f1c1, f1c2 = st.columns(2)
    with f1c1: st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/maracana.jpg", caption="Maracanã", width=400)
    with f1c2: st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/pacaembu.jpg", caption="Museo del Fútbol", width=400)
    st.write("---")
    f2c1, f2c2 = st.columns(2)
    with f2c1: st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/santos.jpg", caption="Vila Belmiro", width=400)
    with f2c2: st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/mineirao.jpg", caption="Mineirão", width=400)

with tab3:
    st.header("🎢 Gritos y Adrenalina")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.image("https://images.unsplash.com/photo-1513889959013-c2845acb46ad?q=80&w=500", caption="Beto Carrero World")
    with col_p2:
        st.subheader("Para Bianca y Mati:")
        st.write("- **FireWhip:** Montaña rusa invertida.\n- **Big Tower:** Caída de 100m.\n- **Hot Wheels Show:** Acrobacias reales.")

with tab4:
    st.header("🥂 El Club de los Consentidos")
    st.write("**Amparo, Jime, Diana y Giorgio:**")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.subheader("🍴 Gastronomía y Vinos")
        st.write("- Cena frente al mar en Búzios.\n- Pizza gourmet en São Paulo.\n- Brunch en Leblon.")
    with col_c2:
        st.subheader("🛍️ Compras y Caminatas")
        st.write("- Oscar Freire (SP).\n- Jardín Botánico (Curitiba).\n- Atardeceres en el Arpoador.")

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
    except: st.info("Sin cotizaciones.")
