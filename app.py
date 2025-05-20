import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Sensores - Mi Ciudad",
    page_icon="✨",
    layout="wide"
)

# Estilo CSS personalizado
st.markdown("""
    <style>
    body {
        background-color: #FAF2E9;
        font-family: 'Times New Roman', serif;
    }
    .stApp {
        background-color: #FAF2E9;
    }
    .titulo {
        color: #B2A898;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .subtitulo {
        color: #B2A898;
        text-align: center;
        font-size: 1.5rem;
        margin-bottom: 2rem;
    }
    .contenedor {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    }
    .grafico {
        border-radius: 15px;
        padding: 15px;
        background-color: #ffffff;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background-color: #B2A898;
        color: white;
        border-radius: 10px;
        font-size: 16px;
        padding: 8px 20px;
    }
    .stButton>button:hover {
        background-color: #9C8F85;
    }
    </style>
""", unsafe_allow_html=True)

# Títulos
st.markdown('<h1 class="titulo">✨ Análisis de Sensores en Mi Ciudad ✨</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="subtitulo">Temperatura y Humedad recolectados por sensores ESP32</h2>', unsafe_allow_html=True)

# Cargador de archivo
uploaded_file = st.file_uploader('Sube un archivo CSV con los datos:', type=['csv'])

if uploaded_file is not None:
    try:
        # Carga y procesamiento de datos
        df1 = pd.read_csv(uploaded_file)

        # Renombrar columnas para simplificar
        column_mapping = {
            'temperatura {device="ESP32", name="Sensor 1"}': 'temperatura',
            'humedad {device="ESP32", name="Sensor 1"}': 'humedad'
        }
        df1 = df1.rename(columns=column_mapping)
        df1['Time'] = pd.to_datetime(df1['Time'])
        df1 = df1.set_index('Time')

        # Contenedor principal
        with st.container():
            # Tabs para organización
            tab1, tab2, tab3 = st.tabs(["📊 Gráficos", "📋 Estadísticas", "🔍 Filtros"])

            with tab1:
                st.markdown('<div class="contenedor"><h3 style="text-align: center;">📈 Gráficos de Variables</h3></div>', unsafe_allow_html=True)
                variable = st.selectbox("Selecciona la variable a visualizar:", ["temperatura", "humedad"])
                tipo_grafico = st.selectbox("Selecciona el tipo de gráfico:", ["Línea", "Área", "Barra"])

                # Generar gráficos con Plotly
                if tipo_grafico == "Línea":
                    fig = px.line(df1, y=variable, title=f'{variable.capitalize()} a lo largo del tiempo', markers=True)
                elif tipo_grafico == "Área":
                    fig = px.area(df1, y=variable, title=f'{variable.capitalize()} a lo largo del tiempo')
                else:
                    fig = px.bar(df1, y=variable, title=f'{variable.capitalize()} a lo largo del tiempo')

                fig.update_layout(
                    title_font=dict(size=20, color='#B2A898'),
                    paper_bgcolor="#FAF2E9",
                    plot_bgcolor="#FAF2E9",
                    font=dict(color='#B2A898', size=14),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor="#EAEAEA"),
                )
                st.plotly_chart(fig, use_container_width=True)

            with tab2:
                st.markdown('<div class="contenedor"><h3 style="text-align: center;">📋 Estadísticas Descriptivas</h3></div>', unsafe_allow_html=True)
                variable_stats = st.radio("Selecciona la variable:", ["temperatura", "humedad"])
                stats_df = df1[variable_stats].describe()
                st.dataframe(stats_df.style.set_properties(**{'background-color': '#FAF2E9', 'color': '#B2A898'}))

            with tab3:
                st.markdown('<div class="contenedor"><h3 style="text-align: center;">🔍 Filtros de Datos</h3></div>', unsafe_allow_html=True)
                variable_filtro = st.selectbox("Selecciona la variable para filtrar:", ["temperatura", "humedad"])
                min_val = st.slider(f'Valor mínimo de {variable_filtro}:', float(df1[variable_filtro].min()), float(df1[variable_filtro].max()), float(df1[variable_filtro].mean()))
                max_val = st.slider(f'Valor máximo de {variable_filtro}:', float(df1[variable_filtro].min()), float(df1[variable_filtro].max()), float(df1[variable_filtro].mean()))

                df_filtrado = df1[(df1[variable_filtro] >= min_val) & (df1[variable_filtro] <= max_val)]
                st.dataframe(df_filtrado.style.set_properties(**{'background-color': '#FAF2E9', 'color': '#B2A898'}))

    except Exception as e:
        st.error(f'Error procesando el archivo: {str(e)}')
else:
    st.warning('Por favor sube un archivo CSV para empezar el análisis.')
