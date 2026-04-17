import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Brasil 2026 - Familia", page_icon="🇧🇷", layout="wide")

# Conexión a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ESTILOS ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #009c3b; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🇧🇷 Expedición Brasil 2026")
st.write("---")

# --- SIDEBAR: CONVERSOR ---
st.sidebar.header("💰 Configuración Económica")
trm_usd = st.sidebar.number_input("TRM (1 USD -> COP)", value=3950)
trm_brl = st.sidebar.number_input("TRM (1 BRL -> COP)", value=780)
ver_en = st.sidebar.radio("Ver precios en:", ["COP", "USD", "BRL"])

def formatear(valor_usd):
    if ver_en == "COP": return f"$ {valor_usd * trm_usd:,.0f} COP"
    if ver_en == "BRL": return f"R$ {(valor_usd * trm_usd)/trm_brl:,.2f}"
    return f"$ {valor_usd:,.2f} USD"

# --- PESTAÑAS PRINCIPALES ---
tab1, tab2, tab3 = st.tabs(["🗺️ Itinerario", "⚽ Ruta Futbolera", "💰 Cotizador Pro"])

with tab1:
    st.header("Nuestro Recorrido Circular")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.image("https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=1200", caption="Río de Janeiro nos espera para el 31")
    with col2:
        st.write("**Paradas Clave:**")
        st.write("📍 **SP / Santos:** Inicio y Museos.")
        st.write("📍 **Paraty:** 2 días de relax total.")
        st.write("📍 **Río:** 4 días (Reveillon y Maracanã).")
        st.write("📍 **Salvador:** 3 días de cultura y Bahía.")
        st.write("📍 **BH / Minas:** El regreso con mejor comida.")

with tab2:
    st.header("👟 Ruta de los Templos (Para Papá, Hijo y Yo)")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.image("https://images.unsplash.com/photo-1622279457486-62dcc4a4bd13?w=400")
        st.subheader("Museo Pacaembú (SP)")
    with c2:
        st.image("https://images.unsplash.com/photo-1540744158912-d859067c8fc3?w=400")
        st.subheader("Maracanã (Río)")
    with c3:
        st.image("https://images.unsplash.com/photo-1599341457639-968600d80e7d?w=400")
        st.subheader("Vila Belmiro (Santos)")

with tab3:
    st.header("📝 Registro de Cotizaciones")
    
    # Formulario para guardar en Google Sheets
    with st.form("nuevo_gasto"):
        c_item, c_cat, c_val = st.columns(3)
        item = c_item.text_input("¿Qué cotizaste?")
        cat = c_cat.selectbox("Categoría", ["Hospedaje", "Vuelos", "Fútbol", "Comida", "Otros"])
        precio = c_val.number_input("Precio en USD", min_value=0.0)
        btn_guardar = st.form_submit_button("Guardar en el Excel")
        
        if btn_guardar:
            if item:
                # AQUÍ SE ESCRIBE EN EL SHEET (Pestaña 'Cotizaciones')
                nuevo_dato = pd.DataFrame([{"Item": item, "Categoría": cat, "USD": precio}])
                try:
                    conn.create(data=nuevo_dato, worksheet="Cotizaciones")
                    st.success(f"¡{item} guardado!")
                except:
                    st.warning("Guardado local (conecta bien la pestaña 'Cotizaciones' en tu Sheet)")
            else:
                st.error("Ponle un nombre a la cotización")

    st.write("---")
    st.subheader("📊 Resumen de Gastos Acumulados")
    # Intentar leer datos guardados
    try:
        df_existente = conn.read(worksheet="Cotizaciones")
        st.dataframe(df_existente, use_container_width=True)
        total_acumulado = df_existente["USD"].sum()
        st.metric("Presupuesto Total", formatear(total_acumulado))
    except:
        st.info("Aún no hay cotizaciones guardadas en la pestaña 'Cotizaciones'.")
