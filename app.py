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
    .selected-box {{ background-color: #009c3b; padding: 20px; border-radius: 10px; color: white; text-align: center; font-size: 1.5em; font-weight: bold; margin-top: 10px; }}
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
    "🗺️ RUTA 19 DÍAS", "📍 RECORRIDO", "⚽ MATI Y ABUELO", "🎁 BETO CARRERO & MÁS", "🥂 LOS CONSENTIDOS", "💰 PRESUPUESTO"
])

# --- PESTAÑA 1: ITINERARIO ---
with tab1:
    st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/rio.jpg", use_container_width=True)
    st.markdown("### 📅 Detalle del Itinerario")
    horario_vuelo = st.radio("¿A qué hora aterrizamos en São Paulo?", ["Mañana", "Tarde/Noche"], index=0, horizontal=True)
    
    if "Mañana" in horario_vuelo:
        p1 = "⚽ Aterrizaje y visita al MUSEO DEL FÚTBOL (Pacaembú). Almuerzo en el estadio y cena italiana en Jardins."
        p2 = "🛍️ Compras en Oscar Freire y visita al Mercado Municipal."
    else:
        p1 = "🏨 Llegada al hotel, brindis de bienvenida y descanso del vuelo."
        p2 = "⚽ Mañana de MUSEO DEL FÚTBOL. Tarde de compras en Jardins y cena familiar."

    it_data = [
        {"Fecha": "26 Dic", "Trayecto": "Llegada SP", "Hospedaje": "São Paulo", "Plan": p1},
        {"Fecha": "27 Dic", "Trayecto": "Estancia SP", "Hospedaje": "São Paulo", "Plan": p2},
        {"Fecha": "28 Dic", "Trayecto": "SP -> Balneário", "Hospedaje": "Balneário Camboriú", "Plan": "Viaje al sur (6h). Llegada a la 'Dubai brasileña'."},
        {"Fecha": "29-30 Dic", "Trayecto": "Beto Carrero", "Hospedaje": "Balneário Camboriú", "Plan": "🎢 2 DÍAS DE PARQUE: FireWhip, Big Tower y Hot Wheels."},
        {"Fecha": "31 Dic", "Trayecto": "Año Nuevo (BC)", "Hospedaje": "Balneário Camboriú", "Plan": "Reveillón con fuegos artificiales sobre los rascacielos."},
        {"Fecha": "01 Ene", "Trayecto": "BC -> Curitiba", "Hospedaje": "Curitiba", "Plan": "Salida calmada 11 AM (3h). Cena y relax en Curitiba."},
        {"Fecha": "02 Ene", "Trayecto": "Curitiba -> Santos", "Hospedaje": "Santos", "Plan": "🌿 Jardín Botánico y bajada por la sierra hacia Santos (5h)."},
        {"Fecha": "03 Ene", "Trayecto": "Santos -> Paraty", "Hospedaje": "Paraty", "Plan": "⚽ Vila Belmiro. Ruta mágica hacia Paraty."},
        {"Fecha": "04 Ene", "Trayecto": "Estancia Paraty", "Hospedaje": "Paraty", "Plan": "Centro Histórico colonial: calles de piedra y puerto antiguo."},
        {"Fecha": "05 Ene", "Trayecto": "Paraty -> Río", "Hospedaje": "Río de Janeiro", "Plan": "Check-in en Copacabana y primer baño de mar."},
        {"Fecha": "06 Ene", "Trayecto": "Estancia Río", "Hospedaje": "Río de Janeiro", "Plan": "⚽ Maracanã (Mañana) y AquaRio (Tarde)."},
        {"Fecha": "07 Ene", "Trayecto": "Estancia Río", "Hospedaje": "Río de Janeiro", "Plan": "Cristo Redentor y Pan de Azúcar."},
        {"Fecha": "08 Ene", "Trayecto": "Río -> Petrópolis", "Hospedaje": "Petrópolis", "Plan": "🏰 Subida Imperial (2h). Palacio y vinos."},
        {"Fecha": "09 Ene", "Trayecto": "Petrópolis -> BH", "Hospedaje": "Belo Horizonte", "Plan": "Viaje a Minas (5h). Gastronomía mineira."},
        {"Fecha": "10 Ene", "Trayecto": "Estancia BH", "Hospedaje": "Belo Horizonte", "Plan": "⚽ Estadio Mineirão y Mercado Central."},
        {"Fecha": "11 Ene", "Trayecto": "Ouro Preto", "Hospedaje": "Belo Horizonte", "Plan": "Historia barroca e iglesias bañadas en oro."},
        {"Fecha": "12 Ene", "Trayecto": "BH -> São Paulo", "Hospedaje": "São Paulo", "Plan": "Regreso a base y cena de despedida familiar."},
        {"Fecha": "13 Ene", "Trayecto": "Vuelo Regreso", "Hospedaje": "---", "Plan": "Traslado al aeropuerto."}
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
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/maracana.jpg", caption="Maracanã (Río)")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/santos.jpg", caption="Vila Belmiro (Santos)")
    with c2: 
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/pacaembu.jpg", caption="Museo del Fútbol (SP)")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/mineirao.jpg", caption="Mineirão (BH)")

# --- PESTAÑA: BETO CARRERO & MÁS (CON AQUARIO) ---
with tab3:
    st.header("🎢 Beto Carrero World & Aventuras Acuáticas")
    st.markdown("### El Mundo de Bianca y Mati")
    st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/beto_carrero_portal.jpg", use_container_width=True)
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/firewhip_bianca.jpg", caption="FireWhip")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/big_tower_caida.jpg", caption="Big Tower")
    with col_p2:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/hot_wheels_mati.jpg", caption="Hot Wheels Show")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/star_mountain_loop.jpg", caption="Star Mountain")
    
    st.write("---")
    st.subheader("🐠 Río de Janeiro: Aventuras bajo el Mar")
    st.markdown("Visita al **AquaRio**, el acuario marino más grande de Sudamérica.")
    # La foto que ya cargaste:
    st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/aquario_rio.jpg", caption="AquaRio: Túneles de cristal y tiburones.", use_container_width=True)

# --- PESTAÑA: LOS CONSENTIDOS (TEXTO ACTUALIZADO PARA CAMBORIÚ DE DÍA) ---
with tab4:
    st.header("🥂 Los Consentidos: Estilo e Historia")
    st.markdown("### Para Amparo, Jime, Diana y Giorgio")
    
    st.subheader("🏖️ Vida de Playa y Récords")
    st.markdown("Nuestra base en el sur será Balneário Camboriú. Disfrutaremos del mar de día bajo el imponente skyline de la 'Dubai brasileña'.")
    
    # Manteniendo el nombre que ya tienes (playa_camboriu_noche.jpg)
    st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/playa_camboriu_noche.jpg", caption="Balneário Camboriú: La 'Dubai Brasileña' de día.", use_container_width=True)
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/playa_rio_copacabana.jpg", caption="Copacabana, Río.")
    with col_b2:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/jardin_orla_santos.jpg", caption="Orla de Santos (Guinness).")

    st.write("---")
    st.subheader("🏰 Historia y Sabores")
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/museu_imperial_petropolis.jpg", caption="Petrópolis")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/paraty_colonial.jpg", caption="Paraty Colonial")
    with col_h2:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/gastronomia_mineira.jpg", caption="Minas Gerais")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/oscar_freire_shopping.jpg", caption="Shopping SP")
    
    col_h3, col_h4 = st.columns(2)
    with col_h3:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/jardim_botanico_curitiba.jpg", caption="Curitiba")
    with col_h4:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/iglesia_ouro_preto.jpg", caption="Ouro Preto")

# --- PESTAÑA: PRESUPUESTO INTERACTIVO CON RESUMEN ---
with tab5:
    st.header("💰 Simulador de Presupuesto")
    if 'usd_input' not in st.session_state: st.session_state.usd_input = 0.0
    if 'cop_input' not in st.session_state: st.session_state.cop_input = 0.0
    def sync_to_usd(): st.session_state.usd_input = st.session_state.cop_input / usd_hoy
    def sync_to_cop(): st.session_state.cop_input = st.session_state.usd_input * usd_hoy

    st.subheader("➕ Agregar Ítem")
    with st.container():
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        c_r1, c_r2 = st.columns(2)
        nombre_item = c_r1.text_input("¿Qué estamos cotizando?")
        ciudad_item = c_r2.text_input("Ciudad")
        c_r3, c_r4, c_r5 = st.columns(3)
        cat = c_r3.selectbox("Categoría", ["Vuelos", "Carro", "Hospedaje", "Comida", "Parques", "Otros"])
        with c_r4: st.number_input("Precio base (COP)", key="cop_input", on_change=sync_to_usd, step=50000.0)
        with c_r5: st.number_input("Precio base (USD)", key="usd_input", on_change=sync_to_cop, step=10.0)
        c_r6, c_r7 = st.columns([1, 2])
        mult = c_r6.number_input("Cantidad", min_value=1, value=1)
        tot_usd = st.session_state.usd_input * mult
        c_r7.markdown(f"### Total ítem: {format_money(tot_usd)}")
        
        if st.button("🚀 GUARDAR"):
            if nombre_item and st.session_state.usd_input > 0:
                try:
                    df_actual = conn.read(worksheet="Cotizaciones", ttl=0)
                    nueva = pd.DataFrame([{"Item": nombre_item, "Ciudad": ciudad_item, "Categoría": cat, "Precio_Unit_USD": st.session_state.usd_input, "Cantidad": mult, "Total_USD": tot_usd}])
                    conn.update(worksheet="Cotizaciones", data=pd.concat([df_actual, nueva], ignore_index=True))
                    st.success("✅ ¡Guardado!")
                    st.cache_data.clear()
                    st.rerun()
                except: st.error("Error conexión GSheets")
        st.markdown('</div>', unsafe_allow_html=True)

    try:
        df_base = conn.read(worksheet="Cotizaciones", ttl=0)
        if not df_base.empty:
            st.markdown("### 📋 Simulador Interactivo")
            df_check = df_base.copy()
            df_check.insert(0, "Seleccionar", False)
            df_edit = st.data_editor(df_check, column_config={"Seleccionar": st.column_config.CheckboxColumn(required=True)}, disabled=["Item", "Ciudad", "Categoría", "Precio_Unit_USD", "Cantidad", "Total_USD"], hide_index=True, use_container_width=True)
            
            t_sel = df_edit[df_edit["Seleccionar"] == True]["Total_USD"].sum()
            t_gen = df_base["Total_USD"].sum()
            
            st.write("---")
            col_met1, col_met2 = st.columns(2)
            with col_met1: st.markdown(f'<div class="selected-box">🛒 SELECCIONADO<br>{format_money(t_sel)}</div>', unsafe_allow_html=True)
            with col_met2: st.metric("PRESUPUESTO GENERAL TOTAL", format_money(t_gen))
            
            st.write("---")
            st.markdown("### 📊 Resumen por Categoría (Total General)")
            df_resumen = df_base.groupby("Categoría")["Total_USD"].sum().reset_index()
            df_resumen["Suma"] = df_resumen["Total_USD"].apply(format_money)
            st.table(df_resumen[["Categoría", "Suma"]])
    except: st.info("Sin datos guardados.")
