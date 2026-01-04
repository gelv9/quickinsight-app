import streamlit as st
import pandas as pd
from openai import OpenAI
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(page_title="QuickInsight APP", layout="wide")

# 2. Inicialización del estado de la sesión (Memoria de la App)
if "codigo_guardado" not in st.session_state:
    st.session_state.codigo_guardado = None
if "insight_guardado" not in st.session_state:
    st.session_state.insight_guardado = None

# 3. Cliente OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 4. Estilos y Branding
def aplicar_estilos_custom():
    st.markdown("""
        <style>
        .main { background-color: #0e1117; }
        
        .custom-header {
            background-color: #1f2630;
            padding: 20px;
            border-radius: 15px;
            border: 1px solid #464e5f;
            margin-bottom: 25px;
            text-align: center;
        }
        
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #0e1117;
            color: #6c757d;
            text-align: center;
            padding: 10px;
            font-size: 12px;
            border-top: 1px solid #464e5f;
            z-index: 999;
        }

        .main .block-container { padding-bottom: 70px; }
        </style>
        
        <div class="custom-header">
            <h1 style="color: #00d4ff; margin: 0;">📊 QuickInsight Pro</h1>
            <p style="color: #a3a8b4; font-size: 18px; margin: 5px 0 0 0;">
                Consultor de Inteligencia Artificial para PyMEs
            </p>
        </div>

        <div class="footer">
            QuickInsight App v2.0 | Proyecto Final Coderhouse | Gabriel Elvaz © 2026
        </div>
    """, unsafe_allow_html=True)

aplicar_estilos_custom()

# 5. Función para generar código con la IA
def generar_codigo_ia(pregunta, columnas):
    system_prompt = f"""
    Eres un Senior Data Scientist. Tu salida debe ser ÚNICAMENTE código de Python.
    Contexto: El DataFrame se llama 'df' y tiene estas columnas: {columnas}.
    
    INSTRUCCIONES DE SALIDA:
    1. Si el usuario pide un análisis, usa st.metric() o st.write() para mostrarlo.
    2. IMPORTANTE: Siempre guarda el resultado textual o la conclusión final en una variable llamada 'respuesta_ia'.
       Ejemplo: respuesta_ia = f"El producto más vendido fue {{valor}}"
    3. Si es un gráfico, usa Plotly Express (px) y st.plotly_chart(fig).
    4. No incluyas ```python ni explicaciones.
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": pregunta}],
        temperature=0,
        max_tokens=500 
    )
    return response.choices[0].message.content

# 6. Diseño de Interfaz (Columnas)
col_l, col_r = st.columns([1, 2], gap="large")

with col_l:
    st.subheader("🛠️ Panel de Control")
    st.markdown("Analiza tus ventas rápidamente usando IA.")
    
    with st.expander("ℹ️ Cómo funciona"):
        st.write("""
        1. **Sube tu archivo:** CSV o Excel (.xlsx).
        2. **IA Analiza:** Lee tus columnas automáticamente.
        3. **Pregunta:** En lenguaje natural.
        4. **Resultados:** Obtén insights y gráficos al instante.
        """)
    
    archivo_subido = st.file_uploader("1. Sube tu archivo", type=["csv", "xlsx"])
    
    st.divider()
    
    pregunta_usuario = st.text_input("2. ¿Qué quieres saber?", placeholder="Ej: ¿Cuál es el producto más vendido?")
    
    boton_ejecutar = st.button("Generar Insight", use_container_width=True)
    
    # Botón opcional para limpiar resultados
    if st.session_state.codigo_guardado:
        if st.button("Limpiar Resultados", type="secondary", use_container_width=True):
            st.session_state.codigo_guardado = None
            st.session_state.insight_guardado = None
            st.rerun()

with col_r:
    st.subheader("💡 Insights y Visualizaciones")
    
    if archivo_subido is not None:
        # Carga del DataFrame
        if archivo_subido.name.endswith('.csv'):
            df = pd.read_csv(archivo_subido)
        else:
            df = pd.read_excel(archivo_subido)

        # ACCIÓN: Generar nuevo insight si se presiona el botón
        if boton_ejecutar:
            if pregunta_usuario:
                with st.spinner("La IA está analizando tus datos..."):
                    try:
                        columnas_lista = df.columns.tolist()
                        codigo_ia = generar_codigo_ia(pregunta_usuario, columnas_lista)
                        
                        # Limpiamos y guardamos el código en el estado de sesión
                        st.session_state.codigo_guardado = codigo_ia.replace("```python", "").replace("```", "").strip()
                        
                        # Definimos el scope y ejecutamos para capturar el insight inicial
                        scope_local = {"df": df, "st": st, "px": px, "pd": pd, "respuesta_ia": ""}
                        exec(st.session_state.codigo_guardado, {}, scope_local)
                        
                        # Guardamos el insight textual en el estado de sesión
                        st.session_state.insight_guardado = scope_local.get("respuesta_ia", "Análisis visual generado.")
                        
                    except Exception as e:
                        st.error(f"Error técnico al procesar el código de IA: {e}")
            else:
                st.warning("⚠️ Por favor, escribe una pregunta en el panel izquierdo.")

        # RENDERIZADO: Mostrar resultados persistentes si existen en la memoria
        if st.session_state.codigo_guardado:
            # Si no acabamos de presionar el botón (es un rerun por descarga), volvemos a ejecutar el código guardado
            if not boton_ejecutar:
                try:
                    scope_local = {"df": df, "st": st, "px": px, "pd": pd, "respuesta_ia": ""}
                    exec(st.session_state.codigo_guardado, {}, scope_local)
                except Exception as e:
                    st.error(f"Error al recargar visualización: {e}")

            # Sección de descarga persistente
            st.divider()
            reporte_texto = f"REPORTE DE INSIGHTS - QuickInsight App\n"
            reporte_texto += f"Pregunta: {pregunta_usuario if pregunta_usuario else 'Consulta previa'}\n"
            reporte_texto += f"Resultado: {st.session_state.insight_guardado}\n"
            reporte_texto += f"---\n"
            
            st.download_button(
                label="📥 Descargar Reporte de Insight (TXT)",
                data=reporte_texto,
                file_name="insight_ventas.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        elif not boton_ejecutar:
            # Estado inicial cuando se sube el archivo por primera vez
            st.success("✅ Archivo cargado correctamente.")
            st.write("Vista previa de los primeros 10 registros:")
            st.dataframe(df.head(10), use_container_width=True)
            st.info("Escribe una pregunta y presiona el botón para generar el análisis.")
            
    else:
        st.info("Comienza subiendo un archivo de ventas en el panel lateral.")

st.write("---")
st.caption("Desarrollado por Gabriel Elvaz para Coderhouse | QuickInsight App v2.0")