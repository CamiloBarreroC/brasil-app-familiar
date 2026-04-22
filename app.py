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
    .stTabs [data-baseweb="tab"] {{ color: #ffffff !important; font-weight: bold; }}
    .stTabs [aria-selected="true"] {{ background-color: #009c3b !important; color: white !important; border-radius: 7px; }}
    .stTable, [data-testid="stTable"] {{ background-color: #1a1c24; color: white !important; border-radius: 10px; }}
    [data-testid="stTable"] td, [data-testid="stTable"] th {{ color: white !important; border-bottom: 1px solid #31333f; }}
    section[data-testid="stSidebar"] {{ background-color: #000b1a; }}
    .stButton>button {{ background-color: #009c3b; color: white; border-radius: 10px; border: none; font-weight: bold; width: 100%; height: 3em; }}
    .input-container {{ background-color: #1a1c24; padding: 20px; border-radius: 15px; border: 2px solid #009c3b; margin-bottom: 25px; }}
    .selected-box {{ background-color: #009c3b; padding: 20px; border-radius: 10px; color: white; text-align: center; font-size: 1.5em; font-weight: bold; margin-top: 10px; }}
    .metric-card {{ background-color: #1a1c24; border: 1px solid #31333f; padding: 15px; border-radius: 10px; text-align: center; }}
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
moneda_v = st.sidebar.radio("Ver totales en:", ["COP", "USD"])

def format_money(val, moneda="USD"):
    if moneda == "COP": return f"$ {val:,.0f} COP"
    return f"$ {val:,.2f} USD"

# --- PESTAÑAS ---
tab1, tab_map, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️ RUTA 19 DÍAS", "📍 RECORRIDO", "⚽ MATI Y ABUELO", "🎁 AVENTURAS B&M", "🥂 LOS CONSENTIDOS", "💰 PRESUPUESTO"
])

# (ESTAS PESTAÑAS NO SE TOCARON)
with tab1:
    st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/rio.jpg", use_container_width=True)
    st.markdown("### 📅 Detalle del Itinerario")
    # ... (Resto del código de itinerario se mantiene igual)
    it_data = [{"Fecha": "26 Dic", "Trayecto": "Llegada SP", "Hospedaje": "São Paulo", "Plan": "Llegada al hotel y relax."}] # Simplificado para el ejemplo
    st.table(pd.DataFrame(it_data))

with tab_map:
    st.header("📍 Trazado Maestro de la Ruta")
    st.image("https://raw.githubusercontent.com/CamiloBarreroC/brasil-app-familiar/main/img/recorrido_maestro_brasil.png", width=800)

with tab2:
    st.header("🏟️ Ruta de los Templos Sagrados")
    # ... (Imágenes de estadios se mantienen igual)

with tab3:
    st.header("🎢 Beto Carrero World & AquaRio")
    # ... (Aventuras se mantienen igual)

with tab4:
    st.header("🥂 Estilo e Historia")
    # ... (Consentidos se mantienen igual)


# --- PESTAÑA 5: PRESUPUESTO (AQUÍ ESTÁN LOS CAMBIOS) ---
with tab5:
    st.header("💰 Simulador de Presupuesto Familiar")
    
    # 1. Selector de Personas
    col_p1, col_p2 = st.columns([1, 2])
    with col_p1:
        num_personas = st.number_input("Número de personas:", min_value=1, value=8, step=1)
    with col_p2:
        st.info(f"💡 Los cálculos individuales se dividen entre **{num_personas}** personas.")

    # 2. Formulario para agregar ítem
    if 'usd_input' not in st.session_state: st.session_state.usd_input = 0.0
    if 'cop_input' not in st.session_state: st.session_state.cop_input = 0.0
    def sync_to_usd(): st.session_state.usd_input = st.session_state.cop_input / usd_hoy
    def sync_to_cop(): st.session_state.cop_input = st.session_state.usd_input * usd_hoy

    st.subheader("➕ Agregar Nueva Cotización")
    with st.container():
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        c_r1, c_r2 = st.columns(2)
        nombre_item = c_r1.text_input("¿Qué estamos cotizando? (Ej: Tiquetes, Hotel...)")
        ciudad_item = c_r2.text_input("Ciudad / Lugar")
        
        c_r3, c_r4, c_r5 = st.columns(3)
        cat = c_r3.selectbox("Categoría", ["Vuelos", "Carro", "Hospedaje", "Comida", "Parques", "Otros"])
        with c_r4: st.number_input("Precio base (COP)", key="cop_input", on_change=sync_to_usd, step=100000.0)
        with c_r5: st.number_input("Precio base (USD)", key="usd_input", on_change=sync_to_cop, step=10.0)
        
        mult = st.number_input("Cantidad de este ítem (Ej: 1 grupo, 8 tiquetes...)", min_value=1, value=1)
        tot_item_usd = st.session_state.usd_input * mult
        
        if st.button("🚀 GUARDAR EN EXCEL"):
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
                    st.success("✅ ¡Guardado!")
                    st.cache_data.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al guardar: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. Visualización de la Tabla con cálculos individuales
    try:
        df_base = conn.read(worksheet="Cotizaciones", ttl=0)
        # Limpiar columnas viejas/vacías si existen
        valid_cols = ["Item", "Ciudad", "Categoría", "Precio_Unit_USD", "Cantidad", "Total_USD"]
        df_base = df_base[valid_cols].dropna(how='all')

        if not df_base.empty:
            # --- CÁLCULOS MÁGICOS ---
            df_base["Total_COP"] = df_base["Total_USD"] * usd_hoy
            df_base["Individual_USD"] = df_base["Total_USD"] / num_personas
            df_base["Individual_COP"] = df_base["Total_COP"] / num_personas
            
            st.markdown("### 📊 Desglose de Gastos (Grupo vs Individual)")
            
            df_check = df_base.copy()
            df_check.insert(0, "Seleccionar", False)
            
            df_edit = st.data_editor(
                df_check,
                column_config={
                    "Seleccionar": st.column_config.CheckboxColumn("✅"),
                    "Total_USD": st.column_config.NumberColumn("Total (USD)", format="$ %.2f"),
                    "Total_COP": st.column_config.NumberColumn("Total (COP)", format="$ %,.0f"),
                    "Individual_USD": st.column_config.NumberColumn("Por Persona (USD)", format="$ %.2f"),
                    "Individual_COP": st.column_config.NumberColumn("Por Persona (COP)", format="$ %,.0f"),
                },
                disabled=df_base.columns,
                hide_index=True,
                use_container_width=True
            )
            
            # --- RESUMEN DE TOTALES ---
            t_sel_usd = df_edit[df_edit["Seleccionar"] == True]["Total_USD"].sum()
            t_gen_usd = df_base["Total_USD"].sum()
            
            st.write("---")
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f'<div class="metric-card">💰 TOTAL GENERAL<br><span style="font-size:20px; font-weight:bold; color:#ffdf00;">{format_money(t_gen_usd * (usd_hoy if moneda_v=="COP" else 1), moneda_v)}</span></div>', unsafe_allow_html=True)
            with m2:
                st.markdown(f'<div class="metric-card">👤 POR PERSONA (8)<br><span style="font-size:20px; font-weight:bold; color:#009c3b;">{format_money((t_gen_usd/num_personas) * (usd_hoy if moneda_v=="COP" else 1), moneda_v)}</span></div>', unsafe_allow_html=True)
            with m3:
                st.markdown(f'<div class="selected-box">🛒 SELECCIONADO<br>{format_money(t_sel_usd * (usd_hoy if moneda_v=="COP" else 1), moneda_v)}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.info("Agrega tu primera cotización para ver la tabla de presupuesto.")
