# Imports
import pandas as pd
import streamlit as st
import os
import utils.verification_utils as vu

st.set_page_config(page_title="Home", layout="wide")

st.title("Statistics Project 1")

# Required libraries
librerias_req = [
    "pandas",
    "streamlit",
    "plotly",
    "scipy",
    "numpy",
    "matplotlib"
]

st.subheader("Required libraries")

# Create a status list for required libraries
for lib in librerias_req:
    if vu.verificar_instalacion(lib):
        st.success(f"✅ **{lib}** is installed")
    else:
        st.error(f"❌ **{lib}** not found")
        st.caption(f"Run: `pip install {lib}` or run the install.bat file to install it")

# Refresh button
if st.button("Check again"):
    st.rerun()

st.subheader("Data upload (required to run the project)")

# File uploader component
archivo_cargado = st.file_uploader("Upload the temperaturas.txt file", type=['txt'])

if archivo_cargado is not None:
    # Read the file and store it in session_state
    df = pd.read_csv(archivo_cargado, sep=r'\s+', encoding='utf-8')
    st.session_state['datos_cargados'] = df
    st.success("File uploaded and stored in memory.")

st.subheader("Download technical report")

# Define the path to your saved PDF file (adjust according to your folder structure)
ruta_pdf = "resources/document.pdf"

# Check if the file exists before showing the download button
if os.path.exists(ruta_pdf):
    # Open the file in binary read mode ('rb')
    with open(ruta_pdf, "rb") as archivo_pdf:
        pdf_bytes = archivo_pdf.read()

    # Streamlit download button
    st.download_button(
        label="📄 Download Technical Report (PDF)",
        data=pdf_bytes,
        file_name="Technical_Report_Statistics.pdf",
        mime="application/pdf",
        help="Click to download the project's official document."
    )
else:
    st.error(f"⚠️ PDF file not found at the specified path: `{ruta_pdf}`. Please verify the file is saved correctly.")