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
        return data['rates']['COP'], data['rates']['COP'] / data['rates']['BRL']
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
    .selected-box {{ background-color: #009c3b; padding: 20px; border-radius: 10px; color: white; text-align: center; font-size: 1.5em; font-weight: bold; margin-top: 10px; }}
    .input-container {{ background-color: #1a1c24; padding: 20px; border-radius: 15px; border: 2px solid #009c3b; margin-bottom: 25px; }}
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("<h1>🚀 MISIÓN BRASIL 2026: EL SUEÑO FAMILIAR</h1>", unsafe_allow_html=True)
st.write("---")

# --- SIDEBAR ---
st.sidebar.header("💰 Finanzas en Vivo")
st.sidebar.metric("Dólar (USD)", f"${usd_hoy:,.0f} COP")
st.sidebar.metric("Real (BRL)", f"${brl_hoy:,.0f} COP")
moneda_v = st.sidebar.radio("Ver presupuesto en:", ["COP", "USD", "BRL"])

def format_money(usd_val):
    if moneda_v == "COP": return f"$ {usd_val * usd_hoy:,.0f} COP"
    if moneda_v == "BRL": return f"R$ {(usd_val * usd_hoy)/brl_hoy:,.2f}"
    return f"$ {usd_val:,.2f} USD"

# --- PESTAÑAS ---
tab1, tab_map, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️ RUTA 19 DÍAS", "📍 RECORRIDO", "⚽ MATI Y ABUELO", "🎢 BIANCA Y MATI", "🥂 LOS CONSENTIDOS", "💰 PRESUPUESTO"
])

# --- TAB 1: ITINERARIO NARRATIVO ---
with tab1:
    st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/rio.jpg", use_container_width=True)
    st.markdown("### 📅 Itinerario Detallado (La Experiencia Completa)")
    horario_vuelo = st.radio("¿A qué hora aterrizamos en São Paulo?", ["Mañana", "Tarde/Noche"], horizontal=True)
    
    if "Mañana" in horario_vuelo:
        p1 = "⚽ Aterrizaje y visita al MUSEO DEL FÚTBOL (Pacaembú). Almuerzo en el estadio y cena italiana en Jardins."
        p2 = "🛍️ Compras en Oscar Freire y visita al Mercado Municipal para el famoso sándwich de mortadela."
    else:
        p1 = "🏨 Llegada al hotel, brindis de bienvenida con Caipirinha y descanso total del vuelo."
        p2 = "⚽ Mañana de MUSEO DEL FÚTBOL (Pacaembú). Tarde de compras en Jardins y cena familiar."

    it_data = [
        {"Fecha": "26 Dic", "Trayecto": "Llegada SP", "Hospedaje": "São Paulo", "Plan": p1},
        {"Fecha": "27 Dic", "Trayecto": "Estancia SP", "Hospedaje": "São Paulo", "Plan": p2},
        {"Fecha": "28 Dic", "Trayecto": "SP -> Balneário", "Hospedaje": "Balneário Camboriú", "Plan": "Viaje al sur (6h). Llegada a la 'Dubai brasileña'. Cena frente al mar en la Avenida Atlântica."},
        {"Fecha": "29-30 Dic", "Trayecto": "Beto Carrero", "Hospedaje": "Balneário Camboriú", "Plan": "🎢 2 DÍAS DE PARQUE: FireWhip, Big Tower y el Show de Hot Wheels para los chicos."},
        {"Fecha": "31 Dic", "Trayecto": "Año Nuevo (BC)", "Hospedaje": "Balneário Camboriú", "Plan": "Mañana de playa y noche de 'Reveillón' con fuegos artificiales espectaculares sobre los rascacielos."},
        {"Fecha": "01 Ene", "Trayecto": "BC -> Curitiba", "Hospedaje": "Curitiba", "Plan": "Salida 11 AM (3h). Almuerzo tardío en Curitiba y tarde de relax tras la fiesta de año nuevo."},
        {"Fecha": "02 Ene", "Trayecto": "Curitiba -> Santos", "Hospedaje": "Santos", "Plan": "🌿 Jardín Botánico de Curitiba. Bajada por la sierra hacia Santos para caminar por el jardín de playa más largo del mundo."},
        {"Fecha": "03 Ene", "Trayecto": "Santos -> Paraty", "Hospedaje": "Paraty", "Plan": "⚽ Vila Belmiro (Pele). Ruta escénica hacia Paraty, llegada a la posada colonial y cena tranquila."},
        {"Fecha": "04 Ene", "Trayecto": "Estancia Paraty", "Hospedaje": "Paraty", "Plan": "Centro Histórico: calles de piedra, ventanas de colores y el encanto del puerto antiguo."},
        {"Fecha": "05 Ene", "Trayecto": "Paraty -> Río", "Hospedaje": "Río de Janeiro", "Plan": "Ruta por la Costa Verde. Check-in en Copacabana y primer baño de mar en la Ciudad Maravillosa."},
        {"Fecha": "06 Ene", "Trayecto": "Estancia Río", "Hospedaje": "Río de Janeiro", "Plan": "⚽ Maracanã por la mañana. Tarde de AquaRio para Bianca y Mati. Atardecer en Ipanema."},
        {"Fecha": "07 Ene", "Trayecto": "Estancia Río", "Hospedaje": "Río de Janeiro", "Plan": "Subida al Cristo Redentor (Mañana) y Pan de Azúcar (Atardecer) para la foto familiar definitiva."},
        {"Fecha": "08 Ene", "Trayecto": "Río -> Petrópolis", "Hospedaje": "Petrópolis", "Plan": "🏰 Subida Imperial a la sierra (2h). Tour por el Palacio de Pedro II y cena con clima de montaña."},
        {"Fecha": "09 Ene", "Trayecto": "Petrópolis -> BH", "Hospedaje": "Belo Horizonte", "Plan": "Viaje a Minas (5h). Llegada a BH y cena de 'Comida Mineira' (el mejor queso del mundo)."},
        {"Fecha": "10 Ene", "Trayecto": "Estancia BH", "Hospedaje": "Belo Horizonte", "Plan": "⚽ Estadio Mineirão y banquete en el Mercado Central para comprar dulces y recuerdos."},
        {"Fecha": "11 Ene", "Trayecto": "Ouro Preto", "Hospedaje": "Belo Horizonte", "Plan": "Día completo en la joya barroca. Caminata entre iglesias bañadas en oro y arte colonial."},
        {"Fecha": "12 Ene", "Trayecto": "BH -> São Paulo", "Hospedaje": "São Paulo", "Plan": "Regreso a base final (8h). Gran cena de despedida en una churrascaría tradicional."},
        {"Fecha": "13 Ene", "Trayecto": "Vuelo Regreso", "Hospedaje": "---", "Plan": "Últimas compras y traslado al aeropuerto para volver a casa."}
    ]
    st.table(pd.DataFrame(it_data))

# --- TAB 2: RECORRIDO (MAPA) ---
with tab_map:
    st.header("📍 Trazado Maestro de la Ruta")
    url_mapa = "https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/recorrido_maestro_brasil.png"
    col_map1, col_map2, col_map3 = st.columns([1, 5, 1])
    with col_map2:
        st.image(url_mapa, caption="Circuito oficial SP-Sur-Río-Petrópolis-Minas", width=800)

# --- TAB 3: MATI Y EL ABUELO (FÚTBOL Y RÉCORD) ---
with tab2:
    st.header("🏟️ Templos Sagrados y Récords Mundiales")
    col_f1, col_f2 = st.columns(2)
    with col_f1: 
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/maracana.jpg", caption="Maracanã (Río)")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/santos.jpg", caption="Vila Belmiro (Santos)")
    with col_f2: 
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/pacaembu.jpg", caption="Museo del Fútbol (SP)")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/mineirao.jpg", caption="Mineirão (BH)")
    
    st.write("---")
    st.subheader("🌟 El Orgullo de Santos: Récord Guinness")
    st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/jardines_santos_record.jpg", caption="Jardines de la Orla de Santos: El jardín frontal de playa más largo del mundo (7km).", use_container_width=True)

# --- TAB 4: BIANCA Y MATI ---
with tab3:
    st.header("🎢 Bianca y Mati: Adrenalina")
    st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/beto_carrero_portal.jpg", use_container_width=True)
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/firewhip_bianca.jpg", caption="FireWhip")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/big_tower_caida.jpg", caption="Big Tower")
    with col_p2:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/hot_wheels_mati.jpg", caption="Hot Wheels Show")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/star_mountain_loop.jpg", caption="Star Mountain")

# --- TAB 5: LOS CONSENTIDOS (PLAYAS Y LUJO) ---
with tab4:
    st.header("🥂 Los Consentidos: Playas, Estilo e Historia")
    st.markdown("### Para Amparo, Jime, Diana y Giorgio")
    
    st.subheader("🏖️ El Paraíso frente al Mar")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/playa_rio_copacabana.jpg", caption="Copacabana, Río: La playa más famosa del mundo.")
    with col_b2:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/playa_camboriu_noche.jpg", caption="Balneário Camboriú: Nuestra base para el Año Nuevo.")

    st.write("---")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/museu_imperial_petropolis.jpg", caption="🏰 Petrópolis Imperial")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/gastronomia_mineira.jpg", caption="☕ Sabores de Minas")
    with col_c2:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/jardim_botanico_curitiba.jpg", caption="🌿 Curitiba")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/oscar_freire_shopping.jpg", caption="🛍️ Compras en SP")

# --- TAB 6: PRESUPUESTO INTERACTIVO ---
with tab5:
    st.header("💰 Simulador de Presupuesto")
    # ... (Mantenemos la lógica de presupuesto del código anterior)
    if 'usd_input' not in st.session_state: st.session_state.usd_input = 0.0
    if 'cop_input' not in st.session_state: st.session_state.cop_input = 0.0
    def sync_to_usd(): st.session_state.usd_input = st.session_state.cop_input / usd_hoy
    def sync_to_cop(): st.session_state.cop_input = st.session_state.usd_input * usd_hoy

    with st.container():
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        n_item = c1.text_input("Ítem")
        c_item = c2.text_input("Ciudad")
        c3, c4, c5 = st.columns(3)
        cat = c3.selectbox("Categoría", ["Vuelos", "Carro", "Hospedaje", "Comida", "Parques", "Otros"])
        with c4: st.number_input("Precio base (COP)", key="cop_input", on_change=sync_to_usd)
        with c5: st.number_input("Precio base (USD)", key="usd_input", on_change=sync_to_cop)
        c6, c7 = st.columns([1, 2])
        mult = c6.number_input("Cantidad", min_value=1, value=1)
        tot_usd = st.session_state.usd_input * mult
        c7.markdown(f"### Total ítem: {format_money(tot_usd)}")
        if st.button("🚀 GUARDAR"):
            if n_item and st.session_state.usd_input > 0:
                try:
                    df = conn.read(worksheet="Cotizaciones", ttl=0)
                    nueva = pd.DataFrame([{"Item": n_item, "Ciudad": c_item, "Categoría": cat, "Precio_Unit_USD": st.session_state.usd_input, "Cantidad": mult, "Total_USD": tot_usd}])
                    conn.update(worksheet="Cotizaciones", data=pd.concat([df, nueva], ignore_index=True))
                    st.success("¡Guardado!")
                    st.cache_data.clear()
                    st.rerun()
                except: st.error("Error conexión")
        st.markdown('</div>', unsafe_allow_html=True)

    try:
        df_base = conn.read(worksheet="Cotizaciones", ttl=0)
        if not df_base.empty:
            df_check = df_base.copy()
            df_check.insert(0, "Seleccionar", False)
            df_edit = st.data_editor(df_check, column_config={"Seleccionar": st.column_config.CheckboxColumn(required=True)}, disabled=["Item", "Ciudad", "Categoría", "Precio_Unit_USD", "Cantidad", "Total_USD"], hide_index=True, use_container_width=True)
            t_sel = df_edit[df_edit["Seleccionar"] == True]["Total_USD"].sum()
            t_gen = df_base["Total_USD"].sum()
            st.write("---")
            col_m1, col_m2 = st.columns(2)
            with col_m1: st.markdown(f'<div class="selected-box">🛒 SELECCIONADO: {format_money(t_sel)}</div>', unsafe_allow_html=True)
            with col_m2: st.metric("PRESUPUESTO TOTAL", format_money(t_gen))
    except: st.info("Sin datos")
