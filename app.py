import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Viaje Familiar - Brasil", page_icon="🇧🇷", layout="wide")

# Conexión a Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    st.error("Error de conexión. Revisa los Secrets en Streamlit Cloud.")

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; border-radius: 10px; height: 3.5em; 
        background-color: #009c3b; color: white; font-weight: bold;
    }
    .stButton>button:hover { background-color: #ffdf00; color: #002776; }
    </style>
    """, unsafe_allow_html=True)

# --- TÍTULO PERSONALIZADO ---
st.markdown("<h1 style='text-align: center; color: #002776;'>🇧🇷 ¡Nuestra Gran Aventura en Brasil! 🇧🇷</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #009c3b;'>Un viaje inolvidable para Mati, el abuelito y toda la familia</h3>", unsafe_allow_html=True)
st.write("---")

# --- SIDEBAR: CONFIGURACIÓN ---
st.sidebar.header("⚙️ Configuración")
trm_usd = st.sidebar.number_input("Tasa Dólar (USD -> COP)", value=3950)
trm_brl = st.sidebar.number_input("Tasa Real (BRL -> COP)", value=780)
ver_en = st.sidebar.radio("Ver precios en:", ["COP", "USD", "BRL"])

def formatear(valor_usd):
    if ver_en == "COP": return f"$ {valor_usd * trm_usd:,.0f} COP"
    if ver_en == "BRL": return f"R$ {(valor_usd * trm_usd)/trm_brl:,.2f}"
    return f"$ {valor_usd:,.2f} USD"

# --- PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["🗺️ Itinerario", "⚽ Ruta de Mati y el abuelito", "💰 Cotizador Pro"])

with tab1:
    st.header("Nuestro Recorrido Circular")
    col_img, col_txt = st.columns([2, 1])
    with col_img:
        # Foto de Arraial do Cabo
        st.image("http://googleusercontent.com/image_collection/image_retrieval/9629654463243462635_0", caption="¡Brasil nos espera en familia!", use_container_width=True)
    with col_txt:
        st.subheader("Paradas Principales")
        st.write("📍 **Santos:** La casa de Pelé.")
        st.write("📍 **Paraty:** Historia y barcos.")
        st.write("📍 **Río:** Año Nuevo épico.")
        st.write("📍 **Salvador:** El corazón de Bahía.")
        st.write("📍 **Belo Horizonte:** Comida y estadios.")

with tab2:
    st.header("👟 Los Templos del Fútbol para Mati y el abuelito")
    c1, c2, c3 = st.columns(3)
    with c1:
        # Foto Museo del Fútbol
        st.image("http://googleusercontent.com/image_collection/image_retrieval/18355643073997025256_0", caption="Museo del Fútbol (SP)", use_container_width=True)
        st.write("**Para Mati:** Juegos interactivos.")
        st.write("**Para el abuelito:** La historia de los mundiales.")
    with c2:
        # Foto Maracanã
        st.image("http://googleusercontent.com/image_collection/image_retrieval/17768215703529535617_0", caption="Estadio Maracanã (Río)", use_container_width=True)
        st.write("¡El lugar perfecto para una foto de los dos en el borde de la cancha!")
    with c3:
        # Foto Vila Belmiro
        st.image("http://googleusercontent.com/image_collection/image_retrieval/14102648363937343475_0", caption="Vila Belmiro (Santos)", use_container_width=True)
        st.write("Donde nació la magia de Pelé. Un momento sagrado para compartir.")

with tab3:
    st.header("📝 Registro de Cotizaciones")
    with st.form("nuevo_gasto", clear_on_submit=True):
        f1, f2, f3 = st.columns(3)
        item = f1.text_input("¿Qué cotizaste?")
        cat = f2.selectbox("Categoría", ["Hospedaje", "Transporte", "Fútbol", "Comida", "Otros"])
        precio = f3.number_input("Precio en USD", min_value=0.0)
        if st.form_submit_button("Guardar en el Excel"):
            if item:
                nuevo_dato = pd.DataFrame([{"Item": item, "Categoría": cat, "USD": precio}])
                try:
                    conn.create(data=nuevo_dato, worksheet="Cotizaciones")
                    st.success(f"¡{item} guardado para el presupuesto familiar!")
                    st.cache_data.clear() # Limpia caché para ver el nuevo dato
                except Exception as e: 
                    st.error(f"Error al guardar: {e}")
    
    st.write("---")
    try:
        df = conn.read(worksheet="Cotizaciones", ttl="0s") # Lee sin caché para ver cambios al instante
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            st.metric("Total Proyectado", formatear(df["USD"].sum()))
        else:
            st.info("Registra tu primera cotización para ver el resumen.")
    except: 
        st.info("Asegúrate de que la pestaña 'Cotizaciones' exista en tu Google Sheet.")
