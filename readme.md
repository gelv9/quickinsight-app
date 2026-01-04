# 📊 QuickInsight Pro: Consultor de IA para PyMEs

**QuickInsight Pro** es una herramienta de análisis de datos impulsada por Inteligencia Artificial (GPT-4) diseñada para que dueños de pequeñas y medianas empresas puedan obtener respuestas de negocio y gráficos profesionales sin necesidad de saber programación o SQL.

---

## 🚀 Funcionalidades Clave

* **Interfaz Inteligente:** Procesamiento de lenguaje natural para convertir preguntas simples en código funcional de Python/Pandas.
* **Visualización con Plotly:** Generación de gráficos interactivos (barras, líneas, torta) que facilitan la interpretación de tendencias.
* **Persistencia de Estado:** Uso de `st.session_state` para asegurar que los resultados y gráficos no desaparezcan al interactuar con la app o descargar archivos.
* **Reportes de Insights:** Sistema de descarga de conclusiones en formato `.txt` para facilitar el archivo y la toma de decisiones.
* **Diseño Profesional:** Estructura en columnas (Controles vs. Resultados) con modo oscuro nativo y branding personalizado.

---

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.13.3
* **Interfaz:** [Streamlit](https://streamlit.io/)
* **Cerebro de IA:** OpenAI API (Modelo **GPT-4**)
* **Análisis de Datos:** Pandas
* **Gráficos:** Plotly Express

---

##  Instalación y Configuración

Sigue estos pasos para ejecutar el proyecto en un entorno local:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/tu-usuario/quickinsight-app.git](https://github.com/tu-usuario/quickinsight-app.git)
cd quickinsight-app

2. Configurar el Entorno Virtual
Bash

python -m venv .venv
# Activar en Windows:
.venv\Scripts\activate
# Activar en Mac/Linux:
source .venv/bin/activate

3. Instalar Dependencias
Bash

pip install -r requirements.txt

4. Configuración de Secretos

Crea un archivo en .streamlit/secrets.toml con tu clave de OpenAI:
Ini, TOML

OPENAI_API_KEY = "tu_clave_aqui"

Análisis de Factibilidad Económica

El proyecto ha sido optimizado para ser rentable bajo un modelo de pago por uso:

    Costo por consulta: Basado en un promedio de 500 tokens de entrada y 500 de salida.

    Costo estimado: $0.0075 USD por cada análisis completo realizado.

    Eficiencia: El uso de max_tokens=500 previene respuestas innecesariamente largas, garantizando un control total sobre el presupuesto de la API.

Autor

    Gabriel Elvaz - Estudiante de Data Science en Coderhouse.

    Proyecto: Entrega Final - Curso de Prompt Engineering.

2026 QuickInsight Pro - Herramientas de IA aplicadas a negocios.
