import streamlit as st
import pandas as pd
import plotly.express as px

# Leer el archivo CSV en un DataFrame
# Asegúrate de que el archivo esté en el directorio correcto
car_data = pd.read_csv('vehicles_us.csv')

# Encabezado de la aplicación
st.header('Análisis de Anuncios de Venta de Coches')

# Checkbox para histograma (desafío extra)
build_histogram = st.checkbox('Construir un histograma de odómetro')

if build_histogram:
    st.write(
        'Creación de un histograma para el conjunto de datos de anuncios de venta de coches')
    # Crear histograma con Plotly Express
    fig_hist = px.histogram(car_data, x='odometer')
    # Mostrar el gráfico interactivo
    st.plotly_chart(fig_hist, use_container_width=True)

# Checkbox para gráfico de dispersión
build_scatter = st.checkbox(
    'Construir un gráfico de dispersión (odómetro vs precio)')

if build_scatter:
    st.write('Creación de un gráfico de dispersión para odómetro vs precio')
    # Crear gráfico de dispersión con Plotly Express (ajusta columnas si es necesario)
    # 'color' es opcional para más detalle
    fig_scatter = px.scatter(car_data, x='odometer',
                             y='price', color='condition')
    # Mostrar el gráfico interactivo
    st.plotly_chart(fig_scatter, use_container_width=True)
