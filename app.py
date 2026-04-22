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

# Conexión a Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"Error de configuración: {e}")

# --- ESTILOS MODO OSCURO PRO ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; }}
    h1, h2, h3 {{ color: #ffdf00 !important; text-align: center; font-family: 'Arial Black', sans-serif; }}
    p, span, label, .stMarkdown {{ color: #ffffff !important; }}
    .stTabs [data-baseweb="tab-list"] {{ background-color: #1a1c24; border-radius: 10px; padding: 5px; gap: 10px; }}
    .stTabs [data-baseweb="tab"] {{ color: #ffffff !important; font-weight: bold; font-size: 1.1em; }}
    .stTabs [aria-selected="true"] {{ background-color: #009c3b !important; color: white !important; border-radius: 7px; }}
    .stTable, [data-testid="stTable"] {{ background-color: #1a1c24; color: white !important; border-radius: 10px; }}
    [data-testid="stTable"] td, [data-testid="stTable"] th {{ color: white !important; border-bottom: 1px solid #31333f; font-size: 1.05em; }}
    section[data-testid="stSidebar"] {{ background-color: #000b1a; }}
    .stButton>button {{ background-color: #009c3b; color: white; border-radius: 10px; border: none; font-weight: bold; width: 100%; height: 3em; font-size: 1.1em; transition: 0.3s; }}
    .stButton>button:hover {{ background-color: #ffdf00; color: #000b1a; }}
    .input-container {{ background-color: #1a1c24; padding: 25px; border-radius: 15px; border: 2px solid #009c3b; margin-bottom: 25px; box-shadow: 0px 4px 15px rgba(0, 156, 59, 0.2); }}
    .selected-box {{ background-color: #009c3b; padding: 20px; border-radius: 10px; color: white; text-align: center; font-size: 1.5em; font-weight: bold; margin-top: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.5); }}
    .metric-card {{ background-color: #1a1c24; border: 1px solid #31333f; padding: 15px; border-radius: 10px; text-align: center; box-shadow: 0px 4px 10px rgba(0,0,0,0.5); }}
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("<h1>🚀 MISIÓN BRASIL 2026: EL SUEÑO DE LA FAMILIA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2em; color: #aaaaaa !important;'>19 Días • 5 Ciudades • 8 Corazones • 1 Aventura Inolvidable</p>", unsafe_allow_html=True)
st.write("---")

# --- SIDEBAR (FINANZAS) ---
st.sidebar.header("💰 Radar Financiero")
st.sidebar.markdown("Mantén el control del presupuesto en tiempo real con las tasas de hoy.")
st.sidebar.metric("💵 Dólar (USD)", f"${usd_hoy:,.0f} COP")
st.sidebar.metric("🏖️ Real Brasileño (BRL)", f"${brl_hoy:,.0f} COP")
st.sidebar.write("---")
moneda_v = st.sidebar.radio("Ver presupuesto maestro en:", ["COP", "USD"])

def format_money(val, moneda="USD"):
    if moneda == "COP": return f"$ {val:,.0f} COP"
    return f"$ {val:,.2f} USD"

# --- PESTAÑAS ---
tab1, tab_map, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️ GRAN ITINERARIO", "📍 EL MAPA", "⚽ PASIÓN Y GLORIA", "🎢 AVENTURAS B&M", "🥂 LOS CONSENTIDOS", "💰 PRESUPUESTO"
])

# --- PESTAÑA 1: ITINERARIO DETALLADO ---
with tab1:
    st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/rio.jpg", use_container_width=True, caption="Río de Janeiro nos espera con los brazos abiertos.")
    st.markdown("### 📅 La Ruta de Nuestra Vida")
    st.markdown("Cada día está diseñado para mezclar la **adrenalina** que buscan los más jóvenes, la **pasión por el fútbol** para los hinchas de la casa, y el **descanso y lujo** que todos merecemos.")
    
    horario_vuelo = st.radio("⏳ Simular llegada a São Paulo:", ["Vuelo de Mañana", "Vuelo de Tarde/Noche"], index=0, horizontal=True)
    
    if "Mañana" in horario_vuelo:
        p1 = "🛬 Aterrizaje triunfal. Directo al corazón del fútbol: MUSEO DEL FÚTBOL (Pacaembú). Terminamos con una cena italiana de lujo en Jardins."
        p2 = "🛍️ Día de ciudad: Compras exclusivas en Oscar Freire y un festín de sabores en el famoso Mercado Municipal de São Paulo."
    else:
        p1 = "🛬 Llegada al hotel. Brindis de bienvenida, asignación de habitaciones y descanso profundo para recargar baterías."
        p2 = "⚽ Mañana de inmersión en el MUSEO DEL FÚTBOL. Tarde de compras por Jardins y nuestra primera gran cena familiar brasileña."

    it_data = [
        {"Día": "1 (26 Dic)", "Destino": "São Paulo 🏙️", "La Experiencia": p1},
        {"Día": "2 (27 Dic)", "Destino": "São Paulo 🏙️", "La Experiencia": p2},
        {"Día": "3 (28 Dic)", "Destino": "Camboriú 🏖️", "La Experiencia": "🚗 Roadtrip al sur (6h). Atravesamos paisajes hasta llegar a la espectacular 'Dubai brasileña'. Noche de playa."},
        {"Día": "4 y 5 (29-30 Dic)", "Destino": "Beto Carrero 🎢", "La Experiencia": "🔥 2 DÍAS DE LOCURA: Gritos en la FireWhip, vértigo en la Big Tower y el show de Hot Wheels para Mati y Bianca."},
        {"Día": "6 (31 Dic)", "Destino": "Camboriú 🎆", "La Experiencia": "🥂 REVEILLÓN: Despedimos el año en la playa, todos de blanco, viendo los fuegos artificiales iluminar los rascacielos."},
        {"Día": "7 (01 Ene)", "Destino": "Curitiba 🌿", "La Experiencia": "Recuperación de año nuevo. Viaje corto (3h) hacia la capital ecológica. Tarde de paz en el Jardín Botánico de cristal."},
        {"Día": "8 (02 Ene)", "Destino": "Santos ⚓", "La Experiencia": "Descenso panorámico por la sierra del mar hacia la costa. Caminata por los jardines de playa más grandes del mundo."},
        {"Día": "9 (03 Ene)", "Destino": "Paraty ⛵", "La Experiencia": "⚽ Mañana sagrada en Vila Belmiro (La casa de Pelé y Neymar). Tarde de ruta escénica hacia la mágica Paraty."},
        {"Día": "10 (04 Ene)", "Destino": "Paraty ⛵", "La Experiencia": "Viaje en el tiempo. Caminamos por calles de piedra colonial, degustamos cachaça y paseamos en barco por aguas esmeralda."},
        {"Día": "11 (05 Ene)", "Destino": "Río de Janeiro 🏝️", "La Experiencia": "Recorremos la legendaria Costa Verde hasta hacer nuestra entrada triunfal a Copacabana. ¡Caipirinhas frente al mar!"},
        {"Día": "12 (06 Ene)", "Destino": "Río de Janeiro 🏝️", "La Experiencia": "⚽ Peregrinación al MARACANÃ en la mañana. En la tarde, inmersión total con tiburones en el espectacular AquaRio."},
        {"Día": "13 (07 Ene)", "Destino": "Río de Janeiro 🏝️", "La Experiencia": "Día de postales: Subida al Cristo Redentor para abrazar la ciudad y atardecer en el teleférico del Pan de Azúcar."},
        {"Día": "14 (08 Ene)", "Destino": "Petrópolis 👑", "La Experiencia": "Subida a la sierra imperial (2h). Cambiamos la playa por castillos, el Palacio de Cristal y una cata de vinos de altura."},
        {"Día": "15 (09 Ene)", "Destino": "Belo Horizonte 🧀", "La Experiencia": "Viaje al corazón gastronómico de Brasil. Llegada a Minas Gerais para probar el mejor 'Pão de Queijo' del mundo."},
        {"Día": "16 (10 Ene)", "Destino": "Belo Horizonte 🧀", "La Experiencia": "⚽ Visita al imponente estadio Mineirão. Tarde de perdernos entre olores y sabores en el Mercado Central."},
        {"Día": "17 (11 Ene)", "Destino": "Ouro Preto ⛪", "La Experiencia": "Excursión a las montañas de oro. Iglesias barrocas esculpidas por el Aleijadinho y calles llenas de misticismo."},
        {"Día": "18 (12 Ene)", "Destino": "São Paulo 🏙️", "La Experiencia": "Regreso al punto de partida. Últimas compras, empacar recuerdos y una cena nostálgica de despedida familiar."},
        {"Día": "19 (13 Ene)", "Destino": "El Regreso ✈️", "La Experiencia": "Traslado al aeropuerto. Volvemos a casa con el corazón lleno y la promesa de que esta aventura quedará para la historia."}
    ]
    st.table(pd.DataFrame(it_data))

# --- PESTAÑA: RECORRIDO ---
with tab_map:
    st.header("📍 El Mapa del Tesoro")
    st.markdown("Más de **2.500 kilómetros** de costa, montañas, metrópolis y selva. Esta es la ruta exacta que conquistaremos juntos.")
    url_mapa = "https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/recorrido_maestro_brasil.png"
    col_map1, col_map2, col_map3 = st.columns([1, 5, 1])
    with col_map2:
        st.image(url_mapa, caption="Circuito SP -> Sur -> Río -> Minas -> SP", width=800)

# --- PESTAÑA: MATI Y EL ABUELO ---
with tab2:
    st.header("🏟️ Para Mati y el Abuelo: La Tierra del Jogo Bonito")
    st.markdown("Brasil no se entiende sin una pelota. Hemos diseñado paradas estratégicas en los **santuarios más sagrados** del fútbol mundial. Prepárense para pisar la misma grama donde jugaron Pelé, Ronaldo y Ronaldinho.")
    
    c1, c2 = st.columns(2)
    with c1: 
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/maracana.jpg", caption="El mítico Maracanã (Río de Janeiro). El templo máximo.")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/santos.jpg", caption="Vila Belmiro (Santos). Donde nació la leyenda de Pelé y Neymar.")
    with c2: 
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/pacaembu.jpg", caption="Museo del Fútbol (São Paulo). Historia interactiva en el Pacaembú.")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/mineirao.jpg", caption="Mineirão (Belo Horizonte). El coloso de Minas Gerais.")

# --- PESTAÑA: AVENTURAS B&M ---
with tab3:
    st.header("🎢 Zona Extrema: El Territorio de Bianca y Mati")
    st.markdown("### 🎡 Beto Carrero World: El parque más grande de Latinoamérica")
    st.markdown("Dos días completos de pura adrenalina. Montañas rusas invertidas, caídas libres y espectáculos de primer nivel. **¡Prohibido aburrirse!**")
    st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/beto_carrero_portal.jpg", use_container_width=True)
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/firewhip_bianca.jpg", caption="FireWhip: Montaña rusa invertida a 100km/h.")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/big_tower_caida.jpg", caption="Big Tower: 100 metros de caída libre. ¿Se atreven?")
    with col_p2:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/hot_wheels_mati.jpg", caption="Hot Wheels Epic Show: Derrapes y fuego en vivo.")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/star_mountain_loop.jpg", caption="Star Mountain: Doble loop para marear hasta a los más fuertes.")
    
    st.write("---")
    st.subheader("🦈 Río de Janeiro: Misterios del Océano")
    st.markdown("En el corazón del puerto de Río, caminaremos bajo el agua en el **AquaRio**, rodeados de tiburones, mantarrayas y miles de peces tropicales.")
    st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/aquario_rio.jpg", caption="AquaRio: El mayor acuario marino de Sudamérica.", use_container_width=True)

# --- PESTAÑA: LOS CONSENTIDOS ---
with tab4:
    st.header("🥂 Los Consentidos: Amaro, Jime, Diana y Giorgio")
    st.subheader("🌴 El Lujo y Relax que se Merecen")
    st.markdown("Mientras los más jóvenes gastan energía, nuestros consentidos disfrutarán del paraíso a su propio ritmo. Nuestra base de Año Nuevo será **Balneário Camboriú**, conocida como la 'Dubai Brasileña', el lugar perfecto para caminar frente al mar y brindar por la vida sin afanes.")
    
    st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/playa_camboriu_noche.jpg", caption="El imponente skyline de Balneário Camboriú.", use_container_width=True)
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/playa_rio_copacabana.jpg", caption="Las icónicas olas de piedra en Copacabana para una tarde de cócteles.")
    with col_b2:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/jardin_orla_santos.jpg", caption="La Orla de Santos, récord Guinness al jardín de playa más grande del mundo.")

    st.write("---")
    st.subheader("🍷 Historia, Oro y Buena Mesa")
    st.markdown("Un recorrido pensado para el deleite absoluto. Visitaremos los palacios de cristal de la familia real en **Petrópolis**, sentiremos la mística del oro en **Ouro Preto**, y por supuesto, todo estará acompañado de un excelente vino y la inigualable gastronomía de Minas Gerais.")
    
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/museu_imperial_petropolis.jpg", caption="Palacio Imperial en Petrópolis.")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/paraty_colonial.jpg", caption="El encanto detenido en el tiempo de Paraty.")
    with col_h2:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/gastronomia_mineira.jpg", caption="El auténtico Pão de Queijo y los manjares de Minas Gerais.")
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/oscar_freire_shopping.jpg", caption="Tarde de vitrinas exclusivas en São Paulo.")
    
    col_h3, col_h4 = st.columns(2)
    with col_h3:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/jardim_botanico_curitiba.jpg", caption="La joya de cristal: Jardín Botánico de Curitiba.")
    with col_h4:
        st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/iglesia_ouro_preto.jpg", caption="Reliquias doradas en Ouro Preto.")

# --- PESTAÑA 5: PRESUPUESTO (INTACTA Y FUNCIONAL) ---
with tab5:
    st.header("💰 Simulador del Tesoro Familiar")
    
    col_p1, col_p2 = st.columns([1, 2])
    with col_p1:
        num_personas = st.number_input("Número de pasajeros en la misión:", min_value=1, value=8, step=1)
    with col_p2:
        st.info(f"💡 El sistema dividirá los costos totales automáticamente entre **{num_personas}** personas.")

    if 'usd_input' not in st.session_state: st.session_state.usd_input = 0.0
    if 'cop_input' not in st.session_state: st.session_state.cop_input = 0.0
    def sync_to_usd(): st.session_state.usd_input = st.session_state.cop_input / usd_hoy
    def sync_to_cop(): st.session_state.cop_input = st.session_state.usd_input * usd_hoy

    st.subheader("➕ Sumar Nueva Inversión al Viaje")
    with st.container():
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        c_r1, c_r2 = st.columns(2)
        nombre_item = c_r1.text_input("¿Qué estamos cotizando? (Ej: Tiquetes LATAM, Airbnb Copacabana...)")
        ciudad_item = c_r2.text_input("Destino / Ciudad")
        
        c_r3, c_r4, c_r5 = st.columns(3)
        cat = c_r3.selectbox("Categoría", ["Vuelos", "Carro", "Hospedaje", "Comida", "Parques", "Otros"])
        with c_r4: st.number_input("Precio base (COP)", key="cop_input", on_change=sync_to_usd, step=100000.0)
        with c_r5: st.number_input("Precio base (USD)", key="usd_input", on_change=sync_to_cop, step=10.0)
        
        mult = st.number_input("Cantidad de este ítem (Ej: 1 camioneta, 8 tiquetes...)", min_value=1, value=1)
        tot_item_usd = st.session_state.usd_input * mult
        
        if st.button("🚀 GUARDAR EN LA BASE DE DATOS"):
            if nombre_item and st.session_state.usd_input > 0:
                try:
                    df_actual = conn.read(worksheet="Cotizaciones", ttl=0)
                    nueva = pd.DataFrame([{
                        "Item": nombre_item, 
                        "Ciudad": ciudad_item, 
                        "Categoría": cat, 
                        "Precio_Unit_USD": st.session_state.usd_input, 
                        "Cantidad": mult, 
                        "Total_USD": tot_item_usd
                    }])
                    conn.update(worksheet="Cotizaciones", data=pd.concat([df_actual, nueva], ignore_index=True))
                    st.success("✅ ¡Inversión registrada con éxito!")
                    st.cache_data.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al guardar. Revisa la conexión: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    try:
        df_base = conn.read(worksheet="Cotizaciones", ttl=0)
        valid_cols = ["Item", "Ciudad", "Categoría", "Precio_Unit_USD", "Cantidad", "Total_USD"]
        df_base = df_base[valid_cols].dropna(how='all')

        if not df_base.empty:
            df_base["Total_COP"] = df_base["Total_USD"] * usd_hoy
            df_base["Individual_USD"] = df_base["Total_USD"] / num_personas
            df_base["Individual_COP"] = df_base["Total_COP"] / num_personas
            
            st.markdown("### 📊 Desglose Transparente (Grupo vs Individual)")
            
            df_check = df_base.copy()
            df_check.insert(0, "Seleccionar", False)
            
            df_edit = st.data_editor(
                df_check,
                column_config={
                    "Seleccionar": st.column_config.CheckboxColumn("✅"),
                    "Item": st.column_config.TextColumn("Descripción", width="medium"),
                    "Precio_Unit_USD": st.column_config.NumberColumn("Precio Unit. (USD)", format="$ %.2f"),
                    "Total_USD": st.column_config.NumberColumn("Total Grupo (USD)", format="$ %.2f"),
                    "Total_COP": st.column_config.NumberColumn("Total Grupo (COP)", format="$ %,.0f"),
                    "Individual_USD": st.column_config.NumberColumn("Por Persona (USD)", format="$ %.2f"),
                    "Individual_COP": st.column_config.NumberColumn("Por Persona (COP)", format="$ %,.0f"),
                },
                disabled=df_base.columns,
                hide_index=True,
                use_container_width=True
            )
            
            t_sel_usd = df_edit[df_edit["Seleccionar"] == True]["Total_USD"].sum()
            t_gen_usd = df_base["Total_USD"].sum()
            
            st.write("---")
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f'<div class="metric-card">💰 GRAN TOTAL FAMILIAR<br><span style="font-size:22px; font-weight:bold; color:#ffdf00;">{format_money(t_gen_usd * (usd_hoy if moneda_v=="COP" else 1), moneda_v)}</span></div>', unsafe_allow_html=True)
            with m2:
                st.markdown(f'<div class="metric-card">👤 CUOTA POR PERSONA<br><span style="font-size:22px; font-weight:bold; color:#009c3b;">{format_money((t_gen_usd/num_personas) * (usd_hoy if moneda_v=="COP" else 1), moneda_v)}</span></div>', unsafe_allow_html=True)
            with m3:
                st.markdown(f'<div class="selected-box">🛒 SELECCIONADO<br>{format_money(t_sel_usd * (usd_hoy if moneda_v=="COP" else 1), moneda_v)}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.info("Añade la primera inversión para activar el panel financiero.")
