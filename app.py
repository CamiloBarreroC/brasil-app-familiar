import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Brasil 2026 - Familia", page_icon="🇧🇷", layout="wide")

# 2. Conexión a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ESTILOS VISUALES ---
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #f0f2f6; border-radius: 5px; padding: 10px; }
    .stTabs [aria-selected="true"] { background-color: #009c3b; color: white; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0px 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO FAMILIAR ---
st.markdown("<h1 style='text-align: center; color: #002776;'>🇧🇷 ¡Nuestra Gran Aventura en Brasil!</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #009c3b;'>Un viaje para Mati, el abuelito y toda la familia</h3>", unsafe_allow_html=True)
st.write("---")

# --- SIDEBAR (Conversor) ---
st.sidebar.header("💰 Configuración")
trm_usd = st.sidebar.number_input("TRM Dólar (USD -> COP)", value=3950)
trm_brl = st.sidebar.number_input("TRM Real (BRL -> COP)", value=780)
moneda = st.sidebar.radio("Ver precios en:", ["COP", "USD", "BRL"])

def format_money(usd_val):
    if moneda == "COP": return f"$ {usd_val * trm_usd:,.0f} COP"
    if moneda == "BRL": return f"R$ {(usd_val * trm_usd)/trm_brl:,.2f}"
    return f"$ {usd_val:,.2f} USD"

# --- PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["🗺️ Itinerario", "⚽ Ruta de Mati y el abuelito", "💰 Cotizaciones y Gastos"])

with tab1:
    st.header("Recorrido Circular")
    col_img, col_txt = st.columns([2, 1])
    with col_img:
        # Imagen de Arraial do Cabo (Link estable)
        st.image("https://images.unsplash.com/photo-1544918818-830a34596d0c?auto=format&fit=crop&w=1000", caption="Las playas que nos esperan")
    with col_txt:
        st.info("**Plan General:** São Paulo ➔ Paraty ➔ Río ➔ Salvador ➔ Belo Horizonte ➔ São Paulo.")
        st.write("Diciembre es época de verano y sol total.")

with tab2:
    st.header("👟 Templos del Fútbol")
    c1, c2, c3 = st.columns(3)
    # Imágenes de Estadios con links optimizados
    with c1:
        st.image("https://images.unsplash.com/photo-1622279457486-62dcc4a4bd13?auto=format&fit=crop&w=400", caption="Museo Pacaembú (SP)")
        st.write("**Para Mati:** Interactividad pura.")
    with c2:
        st.image("https://images.unsplash.com/photo-1540744158912-d859067c8fc3?auto=format&fit=crop&w=400", caption="Estadio Maracanã (Río)")
        st.write("**Para el abuelito:** La magia del 10.")
    with c3:
        st.image("https://images.unsplash.com/photo-1599341457639-968600d80e7d?auto=format&fit=crop&w=400", caption="Vila Belmiro (Santos)")
        st.write("Donde Pelé se hizo leyenda.")

with tab3:
    st.header("📝 Gestión de Gastos")
    
    # 1. LEER DATOS EXISTENTES (Visible en la App)
    try:
        data = conn.read(worksheet="Cotizaciones", ttl=5) # Actualiza cada 5 seg
        df = pd.DataFrame(data)
    except:
        df = pd.DataFrame(columns=["Item", "Categoría", "USD", "Detalles"])

    # 2. FORMULARIO PARA GUARDAR
    with st.form("nuevo_registro"):
        st.subheader("Añadir nueva cotización")
        f1, f2, f3 = st.columns(3)
        item_n = f1.text_input("¿Qué servicio es?")
        cat_n = f2.selectbox("Categoría", ["Vuelos", "Hospedaje", "Comida", "Fútbol", "Otros"])
        val_n = f3.number_input("Precio en USD", min_value=0.0)
        det_n = st.text_input("Notas adicionales")
        
        if st.form_submit_button("Guardar en el Plan"):
            if item_n:
                # Crear nueva fila
                new_row = pd.DataFrame([{"Item": item_n, "Categoría": cat_n, "USD": val_n, "Detalles": det_n}])
                # Concatenar y subir
                updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(worksheet="Cotizaciones", data=updated_df)
                st.success(f"¡{item_n} guardado! Refresca en un momento para ver.")
                st.cache_data.clear() # Limpiar memoria para ver el dato nuevo
            else:
                st.error("Ponle un nombre al item.")

    # 3. MOSTRAR TABLA DE RESULTADOS (Visible para todos)
    st.write("---")
    st.subheader("💰 Resumen Actual del Viaje")
    if not df.empty:
        # Mostramos la tabla formateada
        st.dataframe(df, use_container_width=True)
        total_usd = df["USD"].sum()
        
        c_tot1, c_tot2 = st.columns(2)
        c_tot1.metric("Total Acumulado (USD)", f"$ {total_usd:,.2f}")
        c_tot2.metric(f"Total en {moneda}", format_money(total_usd))
    else:
        st.info("Aún no hay cotizaciones guardadas. ¡Usa el formulario de arriba!")
