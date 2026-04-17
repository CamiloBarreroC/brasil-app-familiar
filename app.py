import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("🇧🇷 Conexión Brasil 2026")

# Crear conexión con Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

st.success("¡App lista para conectarse!")
