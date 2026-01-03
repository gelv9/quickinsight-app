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
        
def generar_codigo_ia(pregunta, columnas):
    system_prompt = f"""
    Eres un analista de datos experto. Tu tarea es generar código Python/Pandas para responder preguntas de negocio.
    REGLAS DE ORO:
    1. Responde ÚNICAMENTE con código funcional.
    2. El DataFrame se llama 'df'. Columnas: {columnas}.
    3. Para resultados de texto o números, genera código que use st.info() o st.success() con una frase breve. 
       Ejemplo: st.success(f"El producto más vendido en diciembre fue: {{valor}}")
    4. Para gráficos, usa Plotly Express (px) y st.plotly_chart(fig).
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": pregunta}
        ],
        temperature=0,
        max_tokens=300
    )
    return response.choices[0].message.content

st.divider()
pregunta_usuario = st.text_input("¿Que te gustaria saber de tus datos?")

if st.button("Generar Insight"):
    if pregunta_usuario and archivo_subido:
        with st.spinner("Generando Insight..."):
            try:
                columnas_lista = df.columns.tolist()
                codigo_ia = generar_codigo_ia(pregunta_usuario, columnas_lista)
                
                codigo_limpio = codigo_ia.replace("```python", "").replace("```", "").strip()
                
                import plotly.express as px
                exec(codigo_limpio)
                
            except Exception as e:
                st.error(f"Error al procesar la pregunta: {e}")            
    else:
        st.warning("Por favor, sube un archivo y escribe una pregunta.")