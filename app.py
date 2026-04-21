import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests

# 1. Configuración de la página
st.set_page_config(page_title="Misión Brasil 2026", page_icon="🇧🇷", layout="wide")

# --- FUNCIÓN: TASAS DE CAMBIO (API REAL-TIME) ---
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
    .input-container {{ background-color: #1a1c24; padding: 20px; border-radius: 15px; border: 2px solid #009c3b; margin-bottom: 25px; }}
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("<h1>🚀 MISIÓN BRASIL 2026: EL SUEÑO FAMILIAR</h1>", unsafe_allow_html=True)
st.write("---")

# --- SIDEBAR (FINANZAS) ---
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
tab1, tab_map, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️ RUTA 19 DÍAS", "📍 RECORRIDO", "⚽ MATI Y ABUELO", "🎢 BIANCA Y MATI", "🥂 LOS CONSENTIDOS", "💰 PRESUPUESTO"
])

# --- PESTAÑA 1: ITINERARIO COMPLETO ---
with tab1:
    st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/rio.jpg", use_container_width=True)
    
    st.markdown("### 📅 Itinerario Detallado")
    horario_vuelo = st.radio(
        "Para ajustar el inicio, ¿a qué hora aterrizamos en São Paulo?",
        ["Mañana", "Tarde/Noche"], index=0, horizontal=True
    )
    
    # Lógica Narrativa según llegada
    if "Mañana" in horario_vuelo:
        p1 = "⚽ Aterrizaje y visita directa al MUSEO DEL FÚTBOL (Pacaembú). Almuerzo en el estadio y cena italiana en Jardins."
        p2 = "🛍️ Compras en la exclusiva Oscar Freire y visita al Mercado Municipal para probar el famoso sándwich de mortadela."
    else:
        p1 = "🏨 Llegada al hotel, brindis de bienvenida con Caipirinha y descanso total del vuelo internacional."
        p2 = "⚽ Mañana de MUSEO DEL FÚTBOL (Pacaembú). Tarde de compras en Jardins y cena familiar de lujo."

    it_data = [
        {"Fecha": "26 Dic", "Trayecto": "Llegada SP", "Hospedaje": "São Paulo", "Plan": p1},
        {"Fecha": "27 Dic", "Trayecto": "Estancia SP", "Hospedaje": "São Paulo", "Plan": p2},
        {"Fecha": "28 Dic", "Trayecto": "SP -> Balneário", "Hospedaje": "Balneário Camboriú", "Plan": "Viaje al sur (6h). Llegada a la 'Dubai brasileña'. Cena frente al mar en la Avenida Atlântica."},
        {"Fecha": "29 Dic", "Trayecto": "Beto Carrero", "Hospedaje": "Balneário Camboriú", "Plan": "🎢 DÍA 1 PARQUE: Foco en Adrenalina (FireWhip y Big Tower) para Bianca y Mati."},
        {"Fecha": "30 Dic", "Trayecto": "Beto Carrero", "Hospedaje": "Balneário Camboriú", "Plan": "🎢 DÍA 2 PARQUE: Hot Wheels Show, Star Mountain y repetición de las favoritas de los chicos."},
        {"Fecha": "31 Dic", "Trayecto": "Año Nuevo (BC)", "Hospedaje": "Balneário Camboriú", "Plan": "Mañana de playa y noche de 'Reveillón' con el espectáculo de fuegos artificiales más grande del sur."},
        {"Fecha": "01 Ene", "Trayecto": "BC -> Curitiba", "Hospedaje": "Curitiba", "Plan": "Salida calmada 11 AM (3h). Almuerzo en Curitiba y tarde de relax para recargar energías."},
        {"Fecha": "02 Ene", "Trayecto": "Curitiba -> Santos", "Hospedaje": "Santos", "Plan": "🌿 Mañana en el Jardín Botánico de Curitiba. Bajada por la sierra (5h) con vistas increíbles hasta Santos."},
        {"Fecha": "03 Ene", "Trayecto": "Santos -> Paraty", "Hospedaje": "Paraty", "Plan": "⚽ Visita a Vila Belmiro (Santuario de Pelé). Salida por la tarde hacia la magia colonial de Paraty."},
        {"Fecha": "04 Ene", "Trayecto": "Estancia Paraty", "Hospedaje": "Paraty", "Plan": "Caminata histórica por calles de piedra, fotos coloniales y relax en el puerto."},
        {"Fecha": "05 Ene", "Trayecto": "Paraty -> Río", "Hospedaje": "Río de Janeiro", "Plan": "Recorrido por la costa Rio-Santos. Check-in en Copacabana y atardecer en el Arpoador."},
        {"Fecha": "06 Ene", "Trayecto": "Estancia Río", "Hospedaje": "Río de Janeiro", "Plan": "⚽ Tour por el Maracanã y visita al AquaRio (el acuario más grande de Sudamérica)."},
        {"Fecha": "07 Ene", "Trayecto": "Estancia Río", "Hospedaje": "Río de Janeiro", "Plan": "Subida al Cristo Redentor y atardecer inolvidable en el Pan de Azúcar."},
        {"Fecha": "08 Ene", "Trayecto": "Río -> Petrópolis", "Hospedaje": "Petrópolis", "Plan": "🏰 El Eje Imperial: Subida a la sierra (2h). Tour por el Palacio Imperial y cena de vinos de montaña."},
        {"Fecha": "09 Ene", "Trayecto": "Petrópolis -> BH", "Hospedaje": "Belo Horizonte", "Plan": "Viaje hacia Minas (5h). Llegada a BH y primera inmersión en la gastronomía minera."},
        {"Fecha": "10 Ene", "Trayecto": "Estancia BH", "Hospedaje": "Belo Horizonte", "Plan": "⚽ Estadio Mineirão por la mañana y gran banquete en el Mercado Central (Quesos y Dulces)."},
        {"Fecha": "11 Ene", "Trayecto": "Ouro Preto", "Hospedaje": "Belo Horizonte", "Plan": "Día completo en la joya barroca de Ouro Preto. Historia viva e iglesias bañadas en oro."},
        {"Fecha": "12 Ene", "Trayecto": "BH -> São Paulo", "Hospedaje": "São Paulo", "Plan": "Regreso a la base final (8h). Gran cena de despedida familiar en una churrascaría típica."},
        {"Fecha": "13 Ene", "Trayecto": "Vuelo Regreso", "Hospedaje": "---", "Plan": "Últimas compras de tiquis-miquis y traslado al aeropuerto para el vuelo a casa."}
    ]
    st.table(pd.DataFrame(it_data))

# --- PESTAÑA: RECORRIDO ---
with tab_map:
    st.header("📍 Trazado Maestro de la Ruta")
    url_mapa = "https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/recorrido_maestro_brasil.png"
    col_map1, col_map2, col_map3 = st.columns([1, 5, 1])
    with col_map2:
        st.image(url_mapa, caption="Circuito oficial SP-Sur-Río-Petrópolis-Minas", width=800)

# --- PESTAÑA: MATI Y EL ABUELO ---
with tab2:
    st.header("🏟️ Ruta de los Templos Sagrados")
    c1, c2 = st.columns(2)
    with c1: 
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/maracana.jpg", caption="Maracanã")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/santos.jpg", caption="Vila Belmiro")
    with c2: 
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/pacaembu.jpg", caption="Museo del Fútbol")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/mineirao.jpg", caption="Mineirão")

# --- PESTAÑA: BIANCA Y MATI ---
with tab3:
    st.header("🎢 Bianca y Mati: Adrenalina")
    st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/beto_carrero_portal.jpg", use_container_width=True)
    st.write("---")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/firewhip_bianca.jpg", caption="FireWhip")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/big_tower_caida.jpg", caption="Big Tower")
    with col_p2:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/hot_wheels_mati.jpg", caption="Hot Wheels Show")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/star_mountain_loop.jpg", caption="Star Mountain")

# --- PESTAÑA: LOS CONSENTIDOS (CON NOMBRES) ---
with tab4:
    st.header("🥂 Los Consentidos: Estilo e Historia")
    st.markdown("### Para Amparo, Jime, Diana y Giorgio")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/museu_imperial_petropolis.jpg", caption="🏰 Petrópolis")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/gastronomia_mineira.jpg", caption="☕ Minas Gerais")
    with col_c2:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/jardim_botanico_curitiba.jpg", caption="🌿 Curitiba")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/oscar_freire_shopping.jpg", caption="🛍️ São Paulo")
    st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/iglesia_ouro_preto.jpg", caption="⛪ Ouro Preto", use_container_width=True)

# --- PESTAÑA: PRESUPUESTO ---
with tab5:
    st.header("💰 Gestión de Presupuesto")
    if 'usd_input' not in st.session_state: st.session_state.usd_input = 0.0
    if 'cop_input' not in st.session_state: st.session_state.cop_input = 0.0
    def sync_to_usd(): st.session_state.usd_input = st.session_state.cop_input / usd_hoy
    def sync_to_cop(): st.session_state.cop_input = st.session_state.usd_input * usd_hoy

    st.subheader("➕ Agregar Ítem")
    with st.container():
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        c_row1_1, c_row1_2 = st.columns(2)
        nombre_item = c_row1_1.text_input("¿Qué estamos cotizando?")
        ciudad_item = c_row1_2.text_input("Ciudad (Opcional)")
        c_row2_1, c_row2_2, c_row2_3 = st.columns(3)
        categoria = c_row2_1.selectbox("Categoría", ["Vuelos", "Carro", "Hospedaje", "Comida", "Parques", "Otros"])
        with c_row2_2: st.number_input("Precio base (COP)", key="cop_input", on_change=sync_to_usd)
        with c_row2_3: st.number_input("Precio base (USD)", key="usd_input", on_change=sync_to_cop)
        c_row3_1, c_row3_2 = st.columns([1, 2])
        multiplicador = c_row3_1.number_input("Cantidad", min_value=1, value=1)
        total_usd_item = st.session_state.usd_input * multiplicador
        c_row3_2.markdown(f"### Total ítem: {format_money(total_usd_item)}")
        if st.button("🚀 GUARDAR EN PRESUPUESTO"):
            if nombre_item and st.session_state.usd_input > 0:
                try:
                    df_actual = conn.read(worksheet="Cotizaciones", ttl=0)
                    nueva_fila = pd.DataFrame([{"Item": nombre_item, "Ciudad": ciudad_item, "Categoría": categoria, "Precio_Unit_USD": st.session_state.usd_input, "Cantidad": multiplicador, "Total_USD": total_usd_item}])
                    conn.update(worksheet="Cotizaciones", data=pd.concat([df_actual, nueva_fila], ignore_index=True))
                    st.success("✅ ¡Guardado!")
                    st.cache_data.clear()
                    st.rerun()
                except: st.error("Error de conexión.")
        st.markdown('</div>', unsafe_allow_html=True)
    try:
        df_mostrar = conn.read(worksheet="Cotizaciones", ttl=0)
        if not df_mostrar.empty:
            st.dataframe(df_mostrar, use_container_width=True)
            st.metric("TOTAL ESTIMADO DEL VIAJE", format_money(df_mostrar["Total_USD"].sum()))
    except: st.info("Sin datos.")
