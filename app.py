import pandas as pd
import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Análisis de Sensores - Mi Ciudad",
    page_icon="✨",
    layout="wide"
)

# Custom CSS for styling
st.markdown(
    """
    <style>
        /* General background and font */
        body {
            background-color: #f6f0e9;
            font-family: 'Times New Roman', serif;
        }

        /* Title styles */
        .title {
            text-align: center;
            color: #a0896b;
            font-size: 3rem;
            margin-bottom: 0.5rem;
        }

        /* Subtitle styles */
        .subtitle {
            text-align: center;
            color: #b3a394;
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }

        /* Tabs background */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #d9cfc2;
            border-radius: 10px;
            padding: 0.5rem;
        }

        .stTabs [data-baseweb="tab"] {
            color: #5c5343;
            font-weight: bold;
        }

        /* Section headers */
        .stContainer h2 {
            text-align: center;
            color: #a0896b;
        }

        /* Buttons and metrics */
        .stButton button {
            background-color: #a0896b;
            color: #fff;
            border-radius: 8px;
        }

        .stMetric {
            background-color: #f2e8dc;
            border-radius: 10px;
            padding: 1rem;
        }

        /* Dataframe styles */
        .stDataFrame {
            border: 1px solid #d9cfc2;
            border-radius: 8px;
            overflow: hidden;
        }

        /* Footer */
        footer {
            text-align: center;
            font-size: 0.9rem;
            color: #a0896b;
            margin-top: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.markdown('<h1 class="title">✨ Análisis de Sensores ✨</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="subtitle">Analiza datos recolectados por sensores ESP32 en tu ciudad</h2>', unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader('Seleccione archivo CSV para analizar', type=['csv'])

if uploaded_file is not None:
    try:
        # Load and process data
        df1 = pd.read_csv(uploaded_file)

        # Renombrar columnas para simplificar
        column_mapping = {
            'temperatura {device="ESP32", name="Sensor 1"}': 'temperatura',
            'humedad {device="ESP32", name="Sensor 1"}': 'humedad'
        }
        df1 = df1.rename(columns=column_mapping)

        df1['Time'] = pd.to_datetime(df1['Time'])
        df1 = df1.set_index('Time')

        # Create tabs for different analyses
        tab1, tab2, tab3 = st.tabs(["📈 Visualización", "📊 Estadísticas", "🔍 Filtros"])

        with tab1:
            st.markdown('<h2>Visualización de Datos</h2>', unsafe_allow_html=True)

            # Variable selector
            variable = st.selectbox(
                "Seleccione variable a visualizar",
                ["temperatura", "humedad", "Ambas variables"]
            )

            # Chart type selector
            chart_type = st.selectbox(
                "Seleccione tipo de gráfico",
                ["Línea", "Área", "Barra"]
            )

            # Create plot based on selection
            if variable == "Ambas variables":
                st.write("### Temperatura")
                if chart_type == "Línea":
                    st.line_chart(df1["temperatura"])
                elif chart_type == "Área":
                    st.area_chart(df1["temperatura"])
                else:
                    st.bar_chart(df1["temperatura"])

                st.write("### Humedad")
                if chart_type == "Línea":
                    st.line_chart(df1["humedad"])
                elif chart_type == "Área":
                    st.area_chart(df1["humedad"])
                else:
                    st.bar_chart(df1["humedad"])
            else:
                if chart_type == "Línea":
                    st.line_chart(df1[variable])
                elif chart_type == "Área":
                    st.area_chart(df1[variable])
                else:
                    st.bar_chart(df1[variable])

        with tab2:
            st.markdown('<h2>Análisis Estadístico</h2>', unsafe_allow_html=True)

            # Variable selector for statistics
            stat_variable = st.radio(
                "Seleccione variable para estadísticas",
                ["temperatura", "humedad"]
            )

            # Statistical summary
            stats_df = df1[stat_variable].describe()
            st.dataframe(stats_df)

        with tab3:
            st.markdown('<h2>Filtros de Datos</h2>', unsafe_allow_html=True)

            # Variable selector for filtering
            filter_variable = st.selectbox(
                "Seleccione variable para filtrar",
                ["temperatura", "humedad"]
            )

            # Minimum value filter
            min_val = st.slider(
                f'Valor mínimo de {filter_variable}',
                float(df1[filter_variable].min()),
                float(df1[filter_variable].max()),
                float(df1[filter_variable].mean()),
                key="min_val"
            )

            filtrado_df_min = df1[df1[filter_variable] > min_val]
            st.write(f"Registros con {filter_variable} superior a {min_val}:")
            st.dataframe(filtrado_df_min)

    except Exception as e:
        st.error(f'Error al procesar el archivo: {str(e)}')
else:
    st.warning('Por favor, cargue un archivo CSV para comenzar el análisis.')

# Footer
st.markdown('<footer>Desarrollado con inspiración en AuraLight ✨</footer>', unsafe_allow_html=True)
