import pandas as pd
import streamlit as st
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Datos de Sensores",
    page_icon="📊",
    layout="wide"
)

# Estilos personalizados
st.markdown(
    """
    <style>
        body {
            background-color: #FAF2E9;
            font-family: 'Times New Roman', serif;
        }
        h1, h2, h3 {
            color: #B2A898;
            text-align: center;
        }
        .stTabs [role="tab"] {
            background-color: #B2A898;
            color: white;
            border-radius: 10px;
            padding: 10px;
        }
        .stTabs [role="tab"]:hover {
            background-color: #8B8175;
            color: white;
        }
        .stTabs [role="tab"][aria-selected="true"] {
            background-color: #FAF2E9;
            color: #B2A898;
            font-weight: bold;
        }
        .block-container {
            border-radius: 15px;
            padding: 2rem;
        }
        .stButton button {
            background-color: #B2A898;
            color: white;
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Título
st.title("📊 Análisis de Datos de Sensores")
st.markdown(
    """
    Esta aplicación permite cargar y analizar datos de sensores de temperatura y humedad 
    recolectados en diferentes ubicaciones.
    """
)

# Subida de archivos
uploaded_file = st.file_uploader("Seleccione un archivo CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Lectura del archivo
        df = pd.read_csv(uploaded_file)

        # Renombrar columnas (si es necesario)
        column_mapping = {
            'temperatura {device="ESP32", name="Sensor 1"}': 'temperatura',
            'humedad {device="ESP32", name="Sensor 1"}': 'humedad'
        }
        df = df.rename(columns=column_mapping)

        # Convertir la columna de tiempo a datetime
        if 'Time' in df.columns:
            df['Time'] = pd.to_datetime(df['Time'])
            df = df.set_index('Time')

        # Tabs para la organización de la información
        tab1, tab2, tab3 = st.tabs(["📈 Visualización", "📊 Estadísticas", "🔍 Filtros"])

        # Tab de visualización
        with tab1:
            st.header("Visualización de Datos")
            variable = st.selectbox(
                "Seleccione una variable para visualizar",
                ["temperatura", "humedad"]
            )
            chart_type = st.selectbox(
                "Seleccione el tipo de gráfico",
                ["Línea", "Área"]
            )

            if chart_type == "Línea":
                st.line_chart(df[variable])
            elif chart_type == "Área":
                st.area_chart(df[variable])

            # Mostrar datos crudos
            if st.checkbox("Mostrar datos crudos"):
                st.write(df)

        # Tab de estadísticas
        with tab2:
            st.header("Análisis Estadístico")
            variable = st.radio(
                "Seleccione una variable para estadísticas",
                ["temperatura", "humedad"]
            )

            stats = df[variable].describe()
            st.dataframe(stats)

            st.metric("Promedio", f"{stats['mean']:.2f}")
            st.metric("Máximo", f"{stats['max']:.2f}")
            st.metric("Mínimo", f"{stats['min']:.2f}")

        # Tab de filtros
        with tab3:
            st.header("Filtros de Datos")
            variable = st.selectbox(
                "Seleccione una variable para filtrar",
                ["temperatura", "humedad"]
            )

            col1, col2 = st.columns(2)

            with col1:
                min_val = st.slider(
                    f"Valor mínimo de {variable}",
                    float(df[variable].min()),
                    float(df[variable].max()),
                    float(df[variable].mean())
                )
                filtrado_min = df[df[variable] > min_val]
                st.dataframe(filtrado_min)

            with col2:
                max_val = st.slider(
                    f"Valor máximo de {variable}",
                    float(df[variable].min()),
                    float(df[variable].max()),
                    float(df[variable].mean())
                )
                filtrado_max = df[df[variable] < max_val]
                st.dataframe(filtrado_max)

            # Descargar datos filtrados
            if st.button("Descargar datos filtrados"):
                csv = filtrado_min.to_csv().encode('utf-8')
                st.download_button(
                    label="Descargar CSV",
                    data=csv,
                    file_name="datos_filtrados.csv",
                    mime="text/csv"
                )

    except Exception as e:
        st.error(f"Error al procesar el archivo: {str(e)}")
else:
    st.warning("Por favor, cargue un archivo CSV para comenzar el análisis.")
