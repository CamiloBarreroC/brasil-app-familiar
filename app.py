import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests

# 1. Configuración de la página
st.set_page_config(page_title="Misión Brasil 2026", page_icon="🇧🇷", layout="wide")

# --- FUNCIÓN: TASAS DE CAMBIO (API REAL) ---
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
    .input-container {{ background-color: #1a1c24; padding: 20px; border-radius: 15px; border: 2px solid #009c3b; margin-bottom: 25px; }}
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("<h1>🚀 MISIÓN BRASIL 2026: EL SUEÑO FAMILIAR</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2em;'>19 días recorriendo lo mejor de Brasil: SP, Sur, Río y Minas.</p>", unsafe_allow_html=True)
st.write("---")

# --- SIDEBAR ---
st.sidebar.header("💰 Finanzas del Viaje")
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
    "🗺️ RUTA 19 DÍAS", "⚽ MATI Y ABUELO", "🎢 BIANCA Y MATI", "🥂 LOS CONSENTIDOS", "💰 PRESUPUESTO"
])

# --- PESTAÑA 1: ITINERARIO ---
with tab1:
    col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
    with col_img2:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/rio.jpg", caption="¡Bienvenidos a bordo!", width=500)
    
    st.header("📅 Itinerario Maestro")
    
    st.markdown("### ✈️ Configuración de Llegada")
    horario_vuelo = st.radio(
        "¿A qué hora aterrizamos en São Paulo el 26 de diciembre?",
        ["Mañana", "Tarde/Noche"], index=0, horizontal=True
    )
    
    if "Mañana" in horario_vuelo:
        h1, p1 = "São Paulo", "Aterrizaje y primer almuerzo brasileño. Tarde de Museo del Fútbol."
        h2, p2 = "São Paulo", "Día completo en SP: Compras en Jardins y cena familiar."
    else:
        h1, p1 = "São Paulo", "Traslado al hotel y descanso tras el vuelo. Brindis inicial."
        h2, p2 = "São Paulo", "Mañana de descanso y tarde de Museo del Fútbol en Pacaembú."

    it_data = [
        {"Fecha": "26 Dic", "Trayecto": "Llegada", "Hospedaje": h1, "Plan": p1},
        {"Fecha": "27 Dic", "Trayecto": "Estancia SP", "Hospedaje": h2, "Plan": p2},
        {"Fecha": "28 Dic", "Trayecto": "SP -> Balneário", "Hospedaje": "Balneário Camboriú", "Plan": "Bajada al sur (6-7h). Llegada a la ciudad de los rascacielos."},
        {"Fecha": "29 Dic", "Trayecto": "Estancia BC", "Hospedaje": "Balneário Camboriú", "Plan": "Teleférico Unipraias, playa y caminata por la costanera."},
        {"Fecha": "30 Dic", "Trayecto": "BC -> Beto Carrero", "Hospedaje": "Balneário Camboriú", "Plan": "Día 1 de Adrenalina en el parque (a 40 min de BC)."},
        {"Fecha": "31 Dic", "Trayecto": "Año Nuevo (Reveillón)", "Hospedaje": "Balneário Camboriú", "Plan": "Día de playa y gran cena de Año Nuevo con fuegos artificiales."},
        {"Fecha": "01 Ene", "Trayecto": "Descanso", "Hospedaje": "Balneário Camboriú", "Plan": "Mañana de relax. Tarde de yates y vistas modernas."},
        {"Fecha": "02 Ene", "Trayecto": "BC -> Santos", "Hospedaje": "Santos", "Plan": "Iniciamos subida por la costa. Noche en la ciudad de Pelé."},
        {"Fecha": "03 Ene", "Trayecto": "Santos -> Paraty", "Hospedaje": "Paraty", "Plan": "Vila Belmiro por la mañana. Salida a la joya colonial Paraty."},
        {"Fecha": "04 Ene", "Trayecto": "Estancia Paraty", "Hospedaje": "Paraty", "Plan": "Centro Histórico, arquitectura y fotos familiares."},
        {"Fecha": "05 Ene", "Trayecto": "Paraty -> Río", "Hospedaje": "Río de Janeiro", "Plan": "Tramo escénico Rio-Santos. Atardecer en Copacabana."},
        {"Fecha": "06 Ene", "Trayecto": "Estancia Río", "Hospedaje": "Río de Janeiro", "Plan": "Estadio Maracanã y AquaRio para Bianca y Mati."},
        {"Fecha": "07 Ene", "Trayecto": "Estancia Río", "Hospedaje": "Río de Janeiro", "Plan": "Cristo Redentor y Pan de Azúcar. Postales de Brasil."},
        {"Fecha": "08 Ene", "Trayecto": "Río -> Búzios", "Hospedaje": "Búzios", "Plan": "Viaje corto al norte. Llegada al paraíso chic."},
        {"Fecha": "09 Ene", "Trayecto": "Estancia Búzios", "Hospedaje": "Búzios", "Plan": "Playa, compras en Rua das Pedras y vino frente al mar."},
        {"Fecha": "10 Ene", "Trayecto": "Búzios -> Belo Horiz.", "Hospedaje": "Belo Horizonte", "Plan": "Travesía a las montañas mineras (8h). Cena de bienvenida."},
        {"Fecha": "11 Ene", "Trayecto": "Estancia BH", "Hospedaje": "Belo Horizonte", "Plan": "Mineirão para el abuelo y Mercado Central para probar de todo."},
        {"Fecha": "12 Ene", "Trayecto": "BH -> São Paulo", "Hospedaje": "São Paulo", "Plan": "Regreso a la base final. Gran cena de despedida."},
        {"Fecha": "13 Ene", "Trayecto": "Regreso", "Hospedaje": "---", "Plan": "Últimas compras y traslado al aeropuerto."}
    ]
    st.table(pd.DataFrame(it_data))

# --- PESTAÑA 2: MATI Y EL ABUELO ---
with tab2:
    st.header("🏟️ Territorio Futbolero")
    st.write("Para el Abuelito y Mati: Historia y piel de gallina en cada estadio.")
    c1, c2 = st.columns(2)
    with c1: st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/maracana.jpg", caption="Maracanã", width=400)
    with c2: st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/pacaembu.jpg", caption="Museo del Fútbol", width=400)
    c3, c4 = st.columns(2)
    with c3: st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/santos.jpg", caption="Vila Belmiro (Santos)", width=400)
    with c4: st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/mineirao.jpg", caption="Mineirão (Belo Horizonte)", width=400)

# --- PESTAÑA 3: BIANCA Y MATI ---
with tab3:
    st.header("🎢 Gritos y Adrenalina")
    st.write("Para Bianca y Mati: El mundo temático los espera.")
    col_a1, col_a2 = st.columns(2)
    with col_a1: st.image("https://images.unsplash.com/photo-1513889959013-c2845acb46ad?q=80&w=500", caption="Beto Carrero World")
    with col_a2:
        st.subheader("¡Imperdibles!")
        st.write("- **FireWhip:** La invertida más rápida.\n- **Big Tower:** Caída de 100 metros.\n- **Hot Wheels Show:** Acrobacias en vivo.\n- **AquaRio:** Tiburones en el túnel.")

# --- PESTAÑA 4: LOS CONSENTIDOS ---
with tab4:
    st.header("🥂 El Club de los Consentidos")
    st.write("**Amparo, Jime, Diana y Giorgio:** Aquí mandan el buen paladar y el estilo.")
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.subheader("🍴 Gourmet & Vinos")
        st.write("- **Búzios:** Cena de lujo frente al mar.\n- **São Paulo:** La mejor pizza de tu vida.\n- **Minas:** Pão de queijo y café artesanal.")
    with col_g2:
        st.subheader("🛍️ Shopping & Relax")
        st.write("- **Rua Oscar Freire (SP):** Tiendas exclusivas.\n- **Baln. Camboriú:** Caminata por la costanera moderna.\n- **Paraty:** Artesanías con historia.")

# --- PESTAÑA 5: PRESUPUESTO (LOGICA ORIGINAL) ---
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
        nombre_item = col_f1.text_input("¿Qué cotizamos?")
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
            st.dataframe(df_mostrar, use_container_width=True)
            st.metric("TOTAL ESTIMADO", format_money(df_mostrar["USD"].sum()))
    except: st.info("Aún no hay cotizaciones.")
