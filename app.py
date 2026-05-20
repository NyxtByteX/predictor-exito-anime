import streamlit as st
import pandas as pd
import joblib

# Configuración de la página (Requisito 10)
st.set_page_config(page_title="Predicción de Anime", layout="centered")

st.title("🔮 Predicción de Éxito de un Anime")
st.markdown("**(Alumno: ANA VICTORIA DE LA VEGA PANDO - Código ISIL: 76746502)**")
st.markdown("[🔗 Enlace a mi Google Colab (Solo lectura) - HAZ CLIC AQUÍ](PON_AQUI_TU_LINK_DE_COLAB)")
st.write("---")
st.write("Ingresa los 3 datos principales de un anime para predecir si será Altamente Calificado (Rating mayor a 7.0).")

# Cargar el modelo y columnas
try:
    modelo = joblib.load('modelos/modelo_anime.pkl')
    columnas = joblib.load('modelos/columnas_x.pkl')
except FileNotFoundError:
    st.error("Error: No se encontraron los archivos del modelo. Revisa la carpeta 'modelos'.")
    st.stop()

# 1. Inputs de la interfaz
tipo = st.selectbox("Formato de Emisión (Type)", ['TV', 'Movie', 'OVA', 'Special', 'ONA', 'Music'])
episodios = st.number_input("Cantidad de Episodios", min_value=1, value=12, step=1)
miembros = st.number_input("Popularidad (Cantidad de miembros)", min_value=1, value=10000, step=100)

if st.button("Hacer Predicción 🚀"):
    # 2. Crear un dataframe con el dato ingresado
    input_data = pd.DataFrame({'episodes': [episodios], 'members': [miembros]})
    
    # Manejar el tipo (One Hot Encoding manual basado en las columnas de entrenamiento)
    for col in columnas:
        if col.startswith('type_'):
            tipo_col = col.replace('type_', '')
            input_data[col] = 1 if tipo == tipo_col else 0
            
    # Asegurar el orden correcto de las columnas
    input_data = input_data[columnas]
    
    # 3. Predecir
    prediccion = modelo.predict(input_data)[0]
    
    if prediccion == 1:
        st.success("🎉 ¡Predicción: El anime será **ALTAMENTE CALIFICADO** (Rating >= 7.0)!")
    else:
        st.warning("📉 Predicción: El anime tendrá una calificación **promedio/baja** (Rating < 7.0).")