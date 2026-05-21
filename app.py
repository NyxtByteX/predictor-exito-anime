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

# Configuro los controles para que el usuario ingrese sus gustos de forma intuitiva
col1, col2 = st.columns(2)

with col1:
    # Sustituyo los tipos crudos del dataset por opciones comerciales y claras para el usuario
    formato_usuario = st.selectbox(
        "¿Qué tipo de formato prefieres?",
        ["Serie de TV / Duración Larga", "Película (Movie)", "Formato Corto (OVA/Special)", "Música / Videoclip"]
    )
    
    # Mapeo internamente la selección del usuario para que mi modelo en formato .pkl la pueda entender sin errores
    if formato_usuario == "Serie de TV / Duración Larga":
        tipo_interno = "TV"
    elif formato_usuario == "Película (Movie)":
        tipo_interno = "Movie"
    elif formato_usuario == "Formato Corto (OVA/Special)":
        tipo_interno = "OVA"
    else:
        tipo_interno = "Music"

    # Implemento la segmentación por duración (Corto/Medio/Largo) para mejorar la experiencia de usuario
    duracion_categoria = st.radio(
        "Preferencia de duración:",
        ["Corto (1 - 12 episodios)", "Medio (13 - 50 episodios)", "Largo (Más de 50 episodios)"]
    )
    
    # Asigno automáticamente una cantidad estimada de episodios según la categoría elegida para alimentar mis variables predictoras
    if duracion_categoria == "Corto (1 - 12 episodios)":
        episodios_usuario = 12
    elif duracion_categoria == "Medio (13 - 50 episodios)":
        episodios_usuario = 24
    else:
        episodios_usuario = 60

with col2:
    # Defino la lista de géneros disponibles para el selector múltiple de la interfaz
    generos_lista = ['Action', 'Adventure', 'Comedy', 'Drama', 'Fantasy', 'Horror', 'Mecha', 'Mystery', 'Romance', 'Sci-Fi', 'Slice of Life', 'Sports', 'Supernatural']
    generos_usuario = st.multiselect("Géneros favoritos (Elige 1 o más):", generos_lista, default=['Action'])
    
    # Configuro el deslizador para establecer la expectativa de nota mínima
    rating_usuario = st.slider("Rating mínimo esperado:", min_value=1.0, max_value=10.0, value=7.5, step=0.1)

# Botón principal para activar mi motor de predicción y filtrado
if st.button("🔮 Predecir y Recomendar"):
    
    if len(generos_usuario) == 0:
        st.warning("⚠️ Por favor, selecciona al menos un género.")
    else:
        # 5. PREPARACIÓN DE DATOS PARA EL MODELO
        # Creo un dataframe vacío con una sola fila y uso las columnas exactas con las que entrené mi modelo, inicializadas en cero
        input_data = pd.DataFrame(0, index=[0], columns=columnas_modelo)
        
        # Asigno la cantidad de episodios derivada de la duración elegida
        input_data['episodes'] = episodios_usuario
        
        # Activo con un 1 la columna del formato correspondiente mapeado internamente (ej. 'type_TV')
        columna_tipo = f'type_{tipo_interno}'
        if columna_tipo in input_data.columns:
            input_data[columna_tipo] = 1
            
        # Activo con un 1 las columnas de los géneros seleccionados por el usuario
        for genero in generos_usuario:
            if genero in input_data.columns:
                input_data[genero] = 1
                
        # 6. PREDICCIÓN
        # Le paso mis datos estructurados al modelo de Random Forest para obtener su veredicto
        prediccion = modelo_rf.predict(input_data)[0]
        
        st.markdown("---")
        if prediccion == 1:
            st.success("✅ **Predicción del Modelo:** ¡Esta combinación tiene un alto potencial de ser un éxito y seguro te encantará!")
        else:
            st.error("❌ **Predicción del Modelo:** Esta combinación no suele tener altas calificaciones. ¡Pero igual te buscaré opciones!")
            
        # 7. FILTRADO DE RECOMENDACIONES USANDO PANDAS
        st.markdown("### 🎬 Mis Recomendaciones para ti:")
        
        # Filtro mi dataset limpio para que coincida con el tipo interno seleccionado y supere el rating mínimo requerido
        recomendaciones = df[
            (df['type'] == tipo_interno) & 
            (df['rating'] >= rating_usuario)
        ]
        
        # Aplico un filtro iterativo para asegurar que los animes resultantes contengan todos los géneros seleccionados
        for genero in generos_usuario:
            recomendaciones = recomendaciones[recomendaciones['genre'].str.contains(genero, na=False)]
            
        # Ordeno los resultados de forma descendente por calificación y selecciono el Top 5
        recomendaciones = recomendaciones.sort_values(by='rating', ascending=False).head(5)
        
        # 8. MOSTRAR RESULTADOS
        if recomendaciones.empty:
            st.info("No encontré un anime que cumpla exactamente con esos filtros tan estrictas. ¡Prueba bajando el rating o cambiando de género!")
        else:
            for index, row in recomendaciones.iterrows():
                st.write(f"⭐ **{row['name']}** (Rating: {row['rating']}) | Eps: {row['episodes']}")
                st.caption(f"Géneros: {row['genre']}")