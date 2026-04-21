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
        # Valores de respaldo por si falla la API
        return 3950.0, 780.0

usd_hoy, brl_hoy = obtener_tasas()
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ESTILOS MODO OSCURO PRO (COLORES BRASIL) ---
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
st.markdown("<p style='text-align: center; font-size: 1.2em;'>Versión Base 13.0: Eje Imperial y Ruta Optimizada.</p>", unsafe_allow_html=True)
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

# --- PESTAÑA 1: ITINERARIO ---
with tab1:
    st.markdown("### ✈️ Configuración de Llegada (26 Dic)")
    horario_vuelo = st.radio(
        "¿A qué hora aterrizamos en São Paulo?",
        ["Mañana", "Tarde/Noche"], index=0, horizontal=True
    )
    
    # Lógica dinámica para el Museo del Fútbol
    if "Mañana" in horario_vuelo:
        p1, p2 = "⚽ Aterrizaje y MUSEO DEL FÚTBOL (Pacaembú).", "🛍️ Compras en Oscar Freire (Jardins) y Mercado Municipal."
    else:
        p1, p2 = "🏨 Llegada al hotel y descanso del vuelo.", "⚽ Mañana: MUSEO DEL FÚTBOL. Tarde: Compras y Mercado."

    it_data = [
        {"Fecha": "26 Dic", "Trayecto": "Llegada SP", "Hospedaje": "São Paulo", "Plan": p1},
        {"Fecha": "27 Dic", "Trayecto": "Estancia SP", "Hospedaje": "São Paulo", "Plan": p2},
        {"Fecha": "28 Dic", "Trayecto": "SP -> Balneário", "Hospedaje": "Balneário Camboriú", "Plan": "Viaje al sur (6h). Cena en la 'Dubai' brasileña."},
        {"Fecha": "29 Dic", "Trayecto": "BC -> Beto Carrero", "Hospedaje": "Balneário Camboriú", "Plan": "🎢 DÍA 1 PARQUE: Adrenalina pura para Bianca y Mati."},
        {"Fecha": "30 Dic", "Trayecto": "BC -> Beto Carrero", "Hospedaje": "Balneário Camboriú", "Plan": "🎢 DÍA 2 PARQUE: Shows y repetición de favoritas."},
        {"Fecha": "31 Dic", "Trayecto": "Año Nuevo (BC)", "Hospedaje": "Balneário Camboriú", "Plan": "Playa y fuegos artificiales de gala (Reveillón)."},
        {"Fecha": "01 Ene", "Trayecto": "BC -> Curitiba", "Hospedaje": "Curitiba", "Plan": "Salida 11 AM (3h). Relax y cena tranquila en Curitiba."},
        {"Fecha": "02 Ene", "Trayecto": "Curitiba -> Santos", "Hospedaje": "Santos", "Plan": "🌿 Jardín Botánico (Mañana) y bajada a Santos (5h)."},
        {"Fecha": "03 Ene", "Trayecto": "Santos -> Paraty", "Hospedaje": "Paraty", "Plan": "⚽ Vila Belmiro (Mañana) y ruta a Paraty (3.5h)."},
        {"Fecha": "04 Ene", "Trayecto": "Estancia Paraty", "Hospedaje": "Paraty", "Plan": "Centro Histórico y fotos coloniales para las chicas."},
        {"Fecha": "05 Ene", "Trayecto": "Paraty -> Río", "Hospedaje": "Río de Janeiro", "Plan": "Llegada a Copacabana. Atardecer frente al mar."},
        {"Fecha": "06 Ene", "Trayecto": "Estancia Río", "Hospedaje": "Río de Janeiro", "Plan": "⚽ Maracanã y AquaRio para Bianca y Mati."},
        {"Fecha": "07 Ene", "Trayecto": "Estancia Río", "Hospedaje": "Río de Janeiro", "Plan": "Cristo Redentor y Pan de Azúcar."},
        {"Fecha": "08 Ene", "Trayecto": "Río -> Petrópolis", "Hospedaje": "Petrópolis", "Plan": "🏰 Subida a la Ciudad Imperial (2h). Tour de Palacios."},
        {"Fecha": "09 Ene", "Trayecto": "Petrópolis -> BH", "Hospedaje": "Belo Horizonte", "Plan": "Viaje a Minas (5h). Cena de comida minera."},
        {"Fecha": "10 Ene", "Trayecto": "Estancia BH", "Hospedaje": "Belo Horizonte", "Plan": "⚽ Mineirão y Mercado Central."},
        {"Fecha": "11 Ene", "Trayecto": "Ouro Preto", "Hospedaje": "Belo Horizonte", "Plan": "Historia barroca y almuerzo colonial de lujo."},
        {"Fecha": "12 Ene", "Trayecto": "BH -> São Paulo", "Hospedaje": "São Paulo", "Plan": "Regreso a base final y gran cena de despedida."},
        {"Fecha": "13 Ene", "Trayecto": "Vuelo Regreso", "Hospedaje": "---", "Plan": "Traslado al aeropuerto y vuelo a casa."}
    ]
    st.table(pd.DataFrame(it_data))

# --- PESTAÑA: RECORRIDO (MAPA) ---
with tab_map:
    st.header("📍 Trazado Maestro de la Ruta")
    url_mapa = "https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/recorrido_maestro_brasil.png"
    st.image(url_mapa, caption="Ruta Oficial: SP -> Sur -> Santos -> Paraty -> Río -> Petrópolis -> Minas -> SP", use_container_width=True)

# --- PESTAÑA 2: MATI Y EL ABUELO ---
with tab2:
    st.header("🏟️ Ruta de los Templos Sagrados")
    c1, c2 = st.columns(2)
    with c1: 
        st.markdown("**Maracanã (Río)**")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/maracana.jpg", use_container_width=True)
        st.markdown("**Vila Belmiro (Santos)**")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/santos.jpg", use_container_width=True)
    with c2: 
        st.markdown("**Museo del Fútbol - Pacaembú (SP)**")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/pacaembu.jpg", use_container_width=True)
        st.markdown("**Mineirão (Belo Horizonte)**")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/mineirao.jpg", use_container_width=True)

# --- PESTAÑA 3: BIANCA Y MATI ---
with tab3:
    st.header("🎢 Gritos y Adrenalina")
    st.image("https://images.unsplash.com/photo-1513889959013-c2845acb46ad?q=80&w=800", caption="Beto Carrero World: 2 Días de Diversión")
    st.markdown("- **FireWhip:** La montaña rusa más extrema.\n- **AquaRio:** El acuario más grande de Sudamérica.\n- **Hot Wheels:** El show que Mati no se puede perder.")

# --- PESTAÑA 4: LOS CONSENTIDOS ---
with tab4:
    st.header("🥂 El Club de los Consentidos")
    st.image("https://images.unsplash.com/photo-1590424765651-f2305886617c?q=80&w=600", caption="Momentos para disfrutar")
    st.markdown("""
    - **Petrópolis:** Elegancia imperial, palacios y clima de montaña.
    - **Curitiba:** El Jardín Botánico más lindo de Brasil.
    - **Minas Gerais:** La mejor hospitalidad y los mejores quesos del mundo.
    - **São Paulo:** Shopping de lujo en Oscar Freire.
    """)

# --- PESTAÑA 5: PRESUPUESTO ---
with tab5:
    st.header("💰 Gestión de Gastos")
    if 'usd_input' not in st.session_state: st.session_state.usd_input = 0.0
    if 'cop_input' not in st.session_state: st.session_state.cop_input = 0.0
    def sync_to_usd(): st.session_state.usd_input = st.session_state.cop_input / usd_hoy
    def sync_to_cop(): st.session_state.cop_input = st.session_state.usd_input * usd_hoy

    with st.container():
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        nombre_item = col1.text_input("¿Qué estamos cotizando?")
        categoria = col2.selectbox("Categoría", ["Vuelos", "Carro", "Hospedaje", "Comida", "Parques"])
        cp1, cp2, cp3 = st.columns(3)
        with cp1: st.number_input("Pesos (COP)", min_value=0.0, key="cop_input", on_change=sync_to_usd, step=50000.0)
        with cp2: st.number_input("Dólares (USD)", min_value=0.0, key="usd_input", on_change=sync_to_cop, step=10.0)
        with cp3: st.metric("Ref. Reales", f"R$ {(st.session_state.usd_input * usd_hoy) / brl_hoy:,.2f}")
        
        if st.button("🚀 GUARDAR COTIZACIÓN"):
            if nombre_item and st.session_state.usd_input > 0:
                try: df_actual = conn.read(worksheet="Cotizaciones", ttl=0)
                except: df_actual = pd.DataFrame(columns=["Item", "Categoría", "USD"])
                nueva_fila = pd.DataFrame([{"Item": nombre_item, "Categoría": categoria, "USD": st.session_state.usd_input}])
                conn.update(worksheet="Cotizaciones", data=pd.concat([df_actual, nueva_fila], ignore_index=True))
                st.success("✅ ¡Cotización guardada!")
                st.cache_data.clear()
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    try:
        df_mostrar = conn.read(worksheet="Cotizaciones", ttl=0)
        if not df_mostrar.empty:
            st.dataframe(df_mostrar, use_container_width=True)
            st.metric("TOTAL ESTIMADO DEL VIAJE", format_money(df_mostrar["USD"].sum()))
    except: st.info("Aún no hay datos en la hoja de cálculo.")
