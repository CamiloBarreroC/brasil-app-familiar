import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Brasil 2026 - Familia", page_icon="🇧🇷", layout="wide")

# 2. Conexión a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ESTILOS VISUALES (ALTO CONTRASTE) ---
st.markdown("""
    <style>
    /* Fondo general */
    .main { background-color: #f0f4f8; }
    
    /* Configuración de las pestañas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #002776; /* Azul oscuro para que resalten las letras */
        padding: 10px 10px 0px 10px;
        border-radius: 10px 10px 0 0;
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #ffffff !important; /* Letras blancas siempre */
        font-weight: bold;
        font-size: 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #009c3b !important; /* Verde cuando está seleccionada */
        border-radius: 5px;
        border-bottom: 4px solid #ffdf00; /* Línea amarilla abajo */
    }
    
    /* Tarjetas de información */
    .info-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("<h1 style='text-align: center; color: #002776;'>🇧🇷 Plan de Viaje: Brasil 2026</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #009c3b;'>Para Mati y el abuelito</h3>", unsafe_allow_html=True)
st.write("---")

# --- SIDEBAR ---
st.sidebar.header("💰 Conversor")
trm_usd = st.sidebar.number_input("Dólar (USD -> COP)", value=3950)
trm_brl = st.sidebar.number_input("Real (BRL -> COP)", value=780)
moneda = st.sidebar.radio("Ver precios en:", ["COP", "USD", "BRL"])

def format_money(usd_val):
    if moneda == "COP": return f"$ {usd_val * trm_usd:,.0f} COP"
    if moneda == "BRL": return f"R$ {(usd_val * trm_usd)/trm_brl:,.2f}"
    return f"$ {usd_val:,.2f} USD"

# --- PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["🗺️ ITINERARIO DETALLADO", "⚽ MATI Y EL ABUELITO", "💰 COTIZACIONES"])

with tab1:
    st.header("Cronograma de la Gran Ruta")
    
    # Imagen de portada (La que funcionó antes)
    st.image("https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=1000", caption="Río de Janeiro - El corazón del viaje")
    
    # Itinerario organizado en tabla
    data_itinerario = {
        "Días": ["1 - 2", "3", "4 - 6", "7 - 8", "9 - 12", "13 - 17"],
        "Destino": ["São Paulo / Santos", "Paraty", "Río de Janeiro", "Arraial do Cabo", "Salvador de Bahía", "Regreso (Chapada / BH / SP)"],
        "Actividad Principal": ["Museos y casa de Pelé", "Paseo en barco y centro histórico", "Reveillon (Año Nuevo) y Maracanã", "Playas de agua turquesa", "Cultura, música y playas del norte", "Naturaleza, cuevas y comida minera"]
    }
    df_it = pd.DataFrame(data_itinerario)
    st.table(df_it)

with tab2:
    st.header("Ruta Futbolera para Mati y el abuelito")
    c1, c2, c3 = st.columns(3)
    
    # Usando links de Unsplash que suelen ser más compatibles
    with c1:
        st.image("https://images.unsplash.com/photo-1540744158912-d859067c8fc3?w=400", caption="Maracanã (Río)")
        st.write("**Para el abuelito:** La magia del 10.")
    with c2:
        st.image("https://images.unsplash.com/photo-1622279457486-62dcc4a4bd13?w=400", caption="Museo del Fútbol (SP)")
        st.write("**Para Mati:** Juegos interactivos.")
    with c3:
        st.image("https://images.unsplash.com/photo-1599341457639-968600d80e7d?w=400", caption="Vila Belmiro (Santos)")
        st.write("**Santos:** La casa de Pelé.")

with tab3:
    st.header("Gestión de Presupuesto")
    
    # Leer datos del Google Sheet
    try:
        df_gastos = conn.read(worksheet="Cotizaciones", ttl=0)
    except:
        df_gastos = pd.DataFrame(columns=["Item", "Categoría", "USD", "Notas"])

    # Formulario para guardar
    with st.form("nuevo_gasto", clear_on_submit=True):
        f1, f2, f3 = st.columns(3)
        item = f1.text_input("¿Qué servicio es?")
        cat = f2.selectbox("Categoría", ["Vuelos", "Hospedaje", "Comida", "Fútbol", "Otros"])
        precio = f3.number_input("Precio en USD", min_value=0.0)
        detalles = st.text_input("Notas adicionales")
        
        if st.form_submit_button("Guardar en el Plan"):
            if item:
                new_row = pd.DataFrame([{"Item": item, "Categoría": cat, "USD": precio, "Notas": detalles}])
                updated_df = pd.concat([df_gastos, new_row], ignore_index=True)
                conn.update(worksheet="Cotizaciones", data=updated_df)
                st.success(f"¡{item} guardado!")
                st.cache_data.clear()
            else:
                st.error("Ponle un nombre.")

    # Mostrar la tabla de lo que se ha guardado
    st.write("---")
    st.subheader("💰 Resumen de Gastos Acumulados")
    if not df_gastos.empty:
        st.dataframe(df_gastos, use_container_width=True)
        total = df_gastos["USD"].sum()
        st.metric("Total Proyectado", format_money(total))
    else:
        st.info("No hay cotizaciones guardadas todavía.")
