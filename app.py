import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Misión Brasil 2026", page_icon="🇧🇷", layout="wide")

# 2. Conexión a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ESTILOS VISUALES MEJORADOS ---
st.markdown("""
    <style>
    /* Fondo general */
    .main { background-color: #f4f7f6; }
    
    /* Configuración de las pestañas (Tabs) para que se vean SIEMPRE */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #002776; /* Azul oscuro de fondo */
        padding: 10px 10px 0px 10px;
        border-radius: 10px 10px 0 0;
        gap: 15px;
    }
    
    /* Texto de las pestañas NO seleccionadas */
    .stTabs [data-baseweb="tab"] {
        color: #ffffff !important; 
        font-weight: bold;
        font-size: 16px;
        opacity: 0.7; /* Un poco transparentes si no están activas */
    }
    
    /* Texto de la pestaña SELECCIONADA */
    .stTabs [aria-selected="true"] {
        background-color: #009c3b !important; /* Verde Brasil */
        color: #ffffff !important;
        opacity: 1 !important;
        border-radius: 5px 5px 0 0;
    }
    
    /* Mejorar visibilidad de las tablas */
    .stTable {
        background-color: white;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("<h1 style='text-align: center; color: #002776;'>🚀 Misión Brasil 2026: Nuestra Aventura Inolvidable</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #009c3b; margin-bottom: 0;'>Para Mati y el abuelito</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>Un plan para toda la familia con unos detallitos para Mati y el abuelito</p>", unsafe_allow_html=True)
st.write("---")

# --- SIDEBAR ---
st.sidebar.header("💰 Conversor de Moneda")
trm_usd = st.sidebar.number_input("Dólar (USD -> COP)", value=3950)
trm_brl = st.sidebar.number_input("Real (BRL -> COP)", value=780)
moneda = st.sidebar.radio("Ver precios en:", ["COP", "USD", "BRL"])

def format_money(usd_val):
    if moneda == "COP": return f"$ {usd_val * trm_usd:,.0f} COP"
    if moneda == "BRL": return f"R$ {(usd_val * trm_usd)/trm_brl:,.2f}"
    return f"$ {usd_val:,.2f} USD"

# --- PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["🗺️ ITINERARIO POR DÍAS", "⚽ MATI Y EL ABUELITO", "💰 COTIZACIONES"])

with tab1:
    # Imagen de portada (sin el caption que pediste quitar)
    st.image("https://images.unsplash.com/photo-1483729558449-99ef09a8c325?q=80&w=1200")
    
    st.header("📅 Cronograma del Viaje")
    
    # Itinerario con fechas exactas
    itinerario_data = {
        "Fecha": [
            "26 - 27 de Dic", 
            "28 de Dic", 
            "29 - 31 de Dic", 
            "01 - 02 de Ene", 
            "03 - 06 de Ene", 
            "07 - 11 de Ene"
        ],
        "Destino": [
            "São Paulo / Santos", 
            "Paraty", 
            "Río de Janeiro", 
            "Arraial do Cabo", 
            "Salvador de Bahía", 
            "Regreso (Chapada / BH / SP)"
        ],
        "Lo que haremos": [
            "Llegada, Museos y visita a la casa de Pelé.",
            "Pueblo colonial, barquitos y descanso.",
            "Año Nuevo en la playa y visita al Maracanã.",
            "Caribe brasileño: aguas cristalinas y sol.",
            "Cultura, música, comida bahiana y playas del norte.",
            "Naturaleza en la Chapada, comida en Minas y vuelta a SP."
        ]
    }
    df_it = pd.DataFrame(itinerario_data)
    st.table(df_it)

with tab2:
    st.header("👟 Ruta de los Templos: ¡Para los más futboleros!")
    st.write("Esta sección es especial para que Mati y el abuelito disfruten de los estadios más icónicos del mundo.")
    
    c1, c2, c3 = st.columns(3)
    
    # Intentando links alternativos para que carguen sí o sí
    with c1:
        st.image("https://images.unsplash.com/photo-1540744158912-d859067c8fc3?auto=format&fit=crop&q=60&w=500", caption="Estadio Maracanã (Río)")
        st.write("**Para el abuelito:** Ver la inmensidad del Maracanã.")
    with c2:
        st.image("https://images.unsplash.com/photo-1574629810360-7efbbe195018?auto=format&fit=crop&q=60&w=500", caption="Museo del Fútbol (SP)")
        st.write("**Para Mati:** Juegos e historia del fútbol.")
    with c3:
        st.image("https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&q=60&w=500", caption="Vila Belmiro (Santos)")
        st.write("**Santos:** Donde nació la magia de Pelé.")

with tab3:
    st.header("📝 Cotizaciones y Presupuesto")
    
    # Leer datos del Google Sheet
    try:
        df_gastos = conn.read(worksheet="Cotizaciones", ttl=0)
    except:
        df_gastos = pd.DataFrame(columns=["Item", "Categoría", "USD", "Notas"])

    # Formulario para guardar
    with st.form("nuevo_gasto", clear_on_submit=True):
        f1, f2, f3 = st.columns(3)
        item = f1.text_input("¿Qué estamos cotizando?")
        cat = f2.selectbox("Categoría", ["Vuelos", "Hospedaje", "Comida", "Fútbol", "Otros"])
        precio = f3.number_input("Precio en USD", min_value=0.0)
        detalles = f1.text_input("Notas adicionales")
        
        if st.form_submit_button("Guardar en el Plan"):
            if item:
                new_row = pd.DataFrame([{"Item": item, "Categoría": cat, "USD": precio, "Notas": detalles}])
                updated_df = pd.concat([df_gastos, new_row], ignore_index=True)
                conn.update(worksheet="Cotizaciones", data=updated_df)
                st.success(f"¡{item} guardado con éxito!")
                st.cache_data.clear()
            else:
                st.error("Por favor, ponle un nombre a la cotización.")

    st.write("---")
    st.subheader("💰 Resumen de Gastos")
    if not df_gastos.empty:
        st.dataframe(df_gastos, use_container_width=True)
        total = df_gastos["USD"].sum()
        st.metric("Total Estimado", format_money(total))
    else:
        st.info("Aún no hemos guardado cotizaciones. ¡Empecemos!")
