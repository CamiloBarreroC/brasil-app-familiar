import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Brasil 2026 - Familia", page_icon="🇧🇷", layout="wide")

# 2. Conexión a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ESTILOS VISUALES ---
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #f0f2f6; border-radius: 5px; }
    .stTabs [aria-selected="true"] { background-color: #009c3b; color: white; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0px 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO PERSONALIZADO ---
st.markdown("<h1 style='text-align: center; color: #002776;'>🇧🇷 ¡Nuestra Gran Aventura en Brasil!</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #009c3b;'>Un viaje inolvidable para Mati, el abuelito y toda la familia</h3>", unsafe_allow_html=True)
st.write("---")

# --- SIDEBAR (Conversor) ---
st.sidebar.header("💰 Configuración de Moneda")
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
        # Foto Arraial do Cabo (Wikimedia)
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Arraial_do_Cabo_02.jpg/800px-Arraial_do_Cabo_02.jpg", 
                 caption="Las playas que nos esperan en Arraial", use_container_width=True)
    with col_txt:
        st.info("**El Plan:** São Paulo ➔ Paraty ➔ Río ➔ Salvador ➔ Belo Horizonte ➔ São Paulo.")
        st.write("Diciembre y Enero son los meses perfectos para disfrutar del sol brasileño.")

with tab2:
    st.header("👟 Templos del Fútbol: Para Mati y el abuelito")
    c1, c2, c3 = st.columns(3)
    with c1:
        # Foto Pacaembu (Wikimedia)
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Est%C3%A1dio_do_Pacaembu_2014.jpg/800px-Est%C3%A1dio_do_Pacaembu_2014.jpg", 
                 caption="Museo del Fútbol (SP)", use_container_width=True)
        st.write("**Para Mati:** Historia interactiva.")
    with c2:
        # Foto Maracanã (Wikimedia)
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Est%C3%A1dio_do_Maracan%C3%A3_-_Rio_de_Janeiro.jpg/800px-Est%C3%A1dio_do_Maracan%C3%A3_-_Rio_de_Janeiro.jpg", 
                 caption="Estadio Maracanã (Río)", use_container_width=True)
        st.write("**Para el abuelito:** El templo de Pelé.")
    with c3:
        # Foto Vila Belmiro (Wikimedia)
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Est%C3%A1dio_Urbano_Caldeira_%28Vila_Belmiro%29_-_Santos_FC.jpg/800px-Est%C3%A1dio_Urbano_Caldeira_%28Vila_Belmiro%29_-_Santos_FC.jpg", 
                 caption="Vila Belmiro (Santos)", use_container_width=True)
        st.write("Donde nació la magia.")

with tab3:
    st.header("📝 Cotizaciones Guardadas")
    
    # 1. LEER DATOS (Visible para la familia)
    try:
        df = conn.read(worksheet="Cotizaciones", ttl=2) # Se actualiza cada 2 segundos
    except:
        df = pd.DataFrame(columns=["Item", "Categoría", "USD", "Detalles"])

    # 2. FORMULARIO PARA GUARDAR NUEVOS PRECIOS
    with st.form("nuevo_registro", clear_on_submit=True):
        st.subheader("Añadir nueva cotización")
        f1, f2, f3 = st.columns(3)
        item_n = f1.text_input("¿Qué servicio es?")
        cat_n = f2.selectbox("Categoría", ["Vuelos", "Hospedaje", "Comida", "Fútbol", "Otros"])
        val_n = f3.number_input("Precio en USD", min_value=0.0)
        det_n = st.text_input("Notas (Opcional)")
        
        if st.form_submit_button("Guardar en el Plan"):
            if item_n:
                # Crear nueva fila y subirla
                new_row = pd.DataFrame([{"Item": item_n, "Categoría": cat_n, "USD": val_n, "Detalles": det_n}])
                updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(worksheet="Cotizaciones", data=updated_df)
                st.success(f"¡Guardado! '{item_n}' aparecerá en la tabla abajo en un momento.")
                st.cache_data.clear() # Limpia la memoria para mostrar el cambio
            else:
                st.error("Por favor escribe el nombre del item.")

    # 3. TABLA DE RESUMEN VISIBLE
    st.write("---")
    st.subheader("💰 Resumen de Gastos")
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        total_usd = df["USD"].sum()
        
        c_t1, c_t2 = st.columns(2)
        c_t1.metric("Total Acumulado (USD)", f"$ {total_usd:,.2f}")
        c_t2.metric(f"Total en {moneda}", format_money(total_usd))
    else:
        st.info("No hay datos guardados aún. ¡Usa el formulario para empezar!")
