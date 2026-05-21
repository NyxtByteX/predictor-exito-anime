import streamlit as st
import pandas as pd
import joblib

# 1. Configuración de la página
st.set_page_config(page_title="Recomendador de Anime", page_icon="🎌", layout="centered")

# 2. Carga de modelos y datos
# Utilizo st.cache_data para que los archivos pesados solo se carguen una vez y la página sea rápida.
@st.cache_data
def cargar_datos():
    modelo = joblib.load('modelos/random_forest.pkl')
    columnas = joblib.load('modelos/columnas.pkl')
    df_limpio = pd.read_csv('modelos/anime_limpio.csv')
    return modelo, columnas, df_limpio

modelo_rf, columnas_modelo, df = cargar_datos()

# 3. REQUISITO DE LA RÚBRICA: Datos del Estudiante en la barra lateral
st.sidebar.markdown("### 🎓 Datos del Estudiante")
st.sidebar.text("Nombre: ANA VICTORIA DE LA VEGA PANDO")
st.sidebar.text("Código ISIL: 76746502")
st.sidebar.markdown("[🔗 https://colab.research.google.com/drive/19GXKxmwQl9fVWnY8g0YBye2kTUh5sA5x?usp=sharing ")

# 4. Interfaz Principal
st.title("🎌 Sistema Inteligente de Recomendación de Anime")
st.write("Dime qué tipo de anime estás buscando, y mi modelo de Machine Learning predecirá si te gustará y te recomendará las mejores opciones.")

# Controles para que el usuario ingrese sus gustos
col1, col2 = st.columns(2)

with col1:
    # Extraigo los tipos únicos del dataset para el menú desplegable
    tipos_disponibles = df['type'].unique().tolist()
    tipo_usuario = st.selectbox("Formato de emisión:", tipos_disponibles)
    
    episodios_usuario = st.number_input("Cantidad de episodios (Aprox):", min_value=1, max_value=1000, value=24)

with col2:
    # Defino una lista de géneros populares para el selector múltiple
    generos_lista = ['Action', 'Adventure', 'Comedy', 'Drama', 'Fantasy', 'Horror', 'Mecha', 'Mystery', 'Romance', 'Sci-Fi', 'Slice of Life', 'Sports', 'Supernatural']
    generos_usuario = st.multiselect("Géneros favoritos (Elige 1 o más):", generos_lista, default=['Action'])
    
    rating_usuario = st.slider("Rating mínimo esperado:", min_value=1.0, max_value=10.0, value=7.5, step=0.1)

# Botón principal
if st.button("🔮 Predecir y Recomendar"):
    
    if len(generos_usuario) == 0:
        st.warning("⚠️ Por favor, selecciona al menos un género.")
    else:
        # 5. PREPARACIÓN DE DATOS PARA EL MODELO
        # Creo un dataframe vacío con una sola fila y las columnas exactas que usé en Colab llenas de ceros.
        input_data = pd.DataFrame(0, index=[0], columns=columnas_modelo)
        
        # Asigno la cantidad de episodios
        input_data['episodes'] = episodios_usuario
        
        # Activo la columna correspondiente al tipo seleccionado (ej. pongo un 1 en 'type_TV')
        columna_tipo = f'type_{tipo_usuario}'
        if columna_tipo in input_data.columns:
            input_data[columna_tipo] = 1
            
        # Activo las columnas de los géneros seleccionados (ej. pongo un 1 en 'Action' y en 'Comedy')
        for genero in generos_usuario:
            if genero in input_data.columns:
                input_data[genero] = 1
                
        # 6. PREDICCIÓN
        # Le paso mis datos procesados al modelo de Random Forest
        prediccion = modelo_rf.predict(input_data)[0]
        
        st.markdown("---")
        if prediccion == 1:
            st.success("✅ **Predicción del Modelo:** ¡Esta combinación tiene un alto potencial de ser un éxito y seguro te encantará!")
        else:
            st.error("❌ **Predicción del Modelo:** Esta combinación no suele tener altas calificaciones. ¡Pero igual te buscaré opciones!")
            
        # 7. FILTRADO DE RECOMENDACIONES USANDO PANDAS
        st.markdown("### 🎬 Mis Recomendaciones para ti:")
        
        # Filtro el dataset original: debe coincidir con el tipo, superar el rating mínimo y contener los géneros buscados.
        recomendaciones = df[
            (df['type'] == tipo_usuario) & 
            (df['rating'] >= rating_usuario)
        ]
        
        # Filtro avanzado: Aseguro que el anime contenga todos los géneros que el usuario eligió
        for genero in generos_usuario:
            recomendaciones = recomendaciones[recomendaciones['genre'].str.contains(genero, na=False)]
            
        # Ordeno por mejor rating y me quedo con los top 5
        recomendaciones = recomendaciones.sort_values(by='rating', ascending=False).head(5)
        
        # 8. MOSTRAR RESULTADOS
        if recomendaciones.empty:
            st.info("No encontré un anime que cumpla exactamente con esos filtros tan estrictos. ¡Prueba bajando el rating o cambiando de género!")
        else:
            for index, row in recomendaciones.iterrows():
                st.write(f"⭐ **{row['name']}** (Rating: {row['rating']}) | Eps: {row['episodes']}")
                st.caption(f"Géneros: {row['genre']}")