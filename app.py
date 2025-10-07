import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Vehicles Dashboard", layout="wide")


@st.cache_data
def load_data(path="vehicles_us.csv"):
    df = pd.read_csv(path, low_memory=False)
    return df


def main():
    st.header("Vehicles US — Dashboard")
    st.markdown(
        "Aplicación creada para el Sprint 7: histograma y gráfico de dispersión a partir del dataset `vehicles_us.csv`.\n\n"
        "Desarrollado como ejemplo reproducible."
    )

    # Load data
    try:
        df = load_data("vehicles_us.csv")
    except FileNotFoundError:
        st.error(
            'No se encontró el archivo `vehicles_us.csv`. Asegúrate de colocarlo en la raíz del proyecto.')
        return

    # Sidebar filters
    st.sidebar.header("Filtros")
    if "model_year" in df.columns and df["model_year"].notna().any():
        # Convert safely to numeric if possible
        df["model_year"] = pd.to_numeric(df["model_year"], errors="coerce")
        min_y = int(df['model_year'].dropna().min())
        max_y = int(df['model_year'].dropna().max())
        year_range = st.sidebar.slider(
            "Rango de año", min_value=min_y, max_value=max_y, value=(min_y, max_y))
        df = df[(df['model_year'] >= year_range[0]) &
                (df['model_year'] <= year_range[1])]

    # Select numeric column for histogram & axes for scatter
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if not numeric_cols:
        st.warning(
            "No hay columnas numéricas detectadas para construir gráficos.")
        st.stop()

    col_for_hist = st.sidebar.selectbox(
        "Columna para histograma", options=numeric_cols, index=0)
    x_axis = st.sidebar.selectbox(
        "Eje X para scatter", options=numeric_cols, index=0)
    y_axis = st.sidebar.selectbox(
        "Eje Y para scatter", options=numeric_cols, index=min(1, len(numeric_cols)-1))

    # Buttons / checkboxes
    st.write('---')
    build_hist = st.button("Construir histograma")
    build_scatter = st.button("Construir gráfico de dispersión")

    # Show small table
    if st.checkbox("Mostrar primeras filas del dataset"):
        st.dataframe(df.head(20))

    if build_hist:
        st.write(f"Construyendo histograma para **{col_for_hist}**")
        fig = px.histogram(df, x=col_for_hist, nbins=40,
                           title=f"Histograma de {col_for_hist}")
        st.plotly_chart(fig, use_container_width=True)

    if build_scatter:
        st.write(f"Construyendo scatter: **{x_axis}** vs **{y_axis}**")
        fig2 = px.scatter(df, x=x_axis, y=y_axis,
                          hover_data=df.columns, title=f"{x_axis} vs {y_axis}")
        st.plotly_chart(fig2, use_container_width=True)

    st.write('---')
    st.markdown(
        '**Notas:** Si la aplicación queda "dormida" en Render, recarga la página o ejecuta un "Manual Deploy" desde Render.')


if __name__ == "__main__":
    main()
