import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(page_title="QuickInsight APP", layout="wide")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("QuickInsight APP")
st.markdown("""
            Esta app ayuda a las PyMEs a analizar sus ventas rápidamente usando IA.
            Solo sube tu archivo y pregunta en lenguaje natural.
            """)

with st.expander("Cómo funciona"):
    st.write("""
             1. **Subí tu archivo:** Aceptamos formatos CSV y Excel (.xlsx).
             2. **Analizamos la estructura:** La IA lee los nombres de tus columnas.
             3. **Pregunta lo que quieras:** Ejemplo"¿Cuál fue el producto más vendido en diciembre?"
             4. **Obten resultados:** La app generara el codigo necesario y te dara la respuesta. 
             """)
    
archivo_subido = st.file_uploader("Subi tu archivo", type=["csv", "xlsx"])

if archivo_subido is not None:
    if archivo_subido.name.endswith('.csv'):
        df= pd.read_csv(archivo_subido)
    else:
        df = pd.read_excel(archivo_subido)
        
        st.success("Archivo cargado con éxtito")
        st.subheader("Vista previa del archivo")
        st.write(df.head())
        
        
        