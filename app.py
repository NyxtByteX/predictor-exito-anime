import streamlit as st
import pandas as pd
import joblib

# 1. Configuración de la página
st.set_page_config(page_title="Recomendador de Anime", page_icon="🎌", layout="centered")

# 2. Carga de modelos y datos
# Utilizo st.cache_data para optimizar el rendimiento y cargar el cerebro de mi app una sola vez
@st.cache_data
def cargar_datos():
    modelo = joblib.load('modelos/random_forest.pkl')
    columnas = joblib.load('modelos/columnas.pkl')
    df_limpio = pd.read_csv('modelos/anime_limpio.csv')
    return modelo, columnas, df_limpio

modelo_rf, columnas_modelo, df = cargar_datos()

# 3. REQUISITO DE LA RÚBRICA: Mis datos de estudiante en la barra lateral
st.sidebar.markdown("### 🎓 Datos del Estudiante")
st.sidebar.text("Nombre: ANA VICTORIA DE LA VEGA PANDO")
st.sidebar.text("Código ISIL: 76746502")
st.sidebar.markdown("[🔗 Ver Cuaderno de Colab (Lector)](https://colab.research.google.com/drive/19GXKmwQl9fVWny8g0YBye2kTUh5sA5x?usp=sharing)")

# 4. Interfaz Principal
st.title("🎌 Sistema Inteligente de Recomendación de Anime")
st.write("Configura tus preferencias generales. Mi modelo predictivo evaluará el potencial de éxito y mi motor de búsqueda filtrará el universo de contenido ideal para ti.")

# Configuro la sección de entradas del usuario dividida en dos columnas coherentes
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### ⚙️ Preferencias de Contenido")
    # Configuro un selector numérico para la cantidad estimada de episodios que el usuario desea ver
    episodios_usuario = st.number_input("Cantidad de episodios aproximados:", min_value=1, max_value=1000, value=24)
    
    # Implemento la gran idea de filtrar por complementos del universo del anime usando checkboxes
    st.write("¿Qué complementos te gustaría que incluya la franquicia?")
    quiere_movies = st.checkbox("🎬 Que tenga Películas (Movies)")
    quiere_ovas = st.checkbox("📀 Que tenga OVAs / Especiales")

with col2:
    st.markdown("#### 🎯 Filtros de Calidad y Estilo")
    # Defino mi lista de géneros limpiando aquellos formatos raros que ensuciaban la interfaz
    generos_lista = ['Action', 'Adventure', 'Comedy', 'Drama', 'Fantasy', 'Horror', 'Mecha', 'Mystery', 'Romance', 'Sci-Fi', 'Slice of Life', 'Sports', 'Supernatural']
    generos_usuario = st.multiselect("Géneros favoritos (Elige 1 o más):", generos_lista, default=['Action'])
    
    # Deslizador para fijar el estándar de calificación esperado por el usuario
    rating_usuario = st.slider("Rating mínimo esperado:", min_value=1.0, max_value=10.0, value=7.5, step=0.1)

# Botón principal para ejecutar toda la lógica de mi proyecto
if st.button("🔮 Predecir y Recomendar"):
    
    if len(generos_usuario) == 0:
        st.warning("⚠️ Por favor, selecciona al menos un género.")
    else:
        # 5. PREPARACIÓN DE DATOS PARA MI MODELOpredictivo
        # Para que mi modelo .pkl no sufra por la falta de la columna 'type', determino un tipo principal por defecto (TV)
        # y mapeo las variables de forma transparente para mantener la compatibilidad del 100%
        tipo_defecto = "Movie" if (quiere_movies and not quiere_ovas) else "TV"
        
        # Creo la estructura con las columnas exactas llenas de ceros
        input_data = pd.DataFrame(0, index=[0], columns=columnas_modelo)
        input_data['episodes'] = episodios_usuario
        
        columna_tipo = f'type_{tipo_defecto}'
        if columna_tipo in input_data.columns:
            input_data[columna_tipo] = 1
            
        for genero in generos_usuario:
            if genero in input_data.columns:
                input_data[genero] = 1
                
        # 6. PREDICCIÓN CON MACHINE LEARNING
        # Consulto a mi modelo entrenado de Random Forest si esta combinación de géneros y episodios es un "Éxito"
        prediccion = modelo_rf.predict(input_data)[0]
        
        st.markdown("---")
        if prediccion == 1:
            st.success("✅ **Predicción del Modelo:** ¡Esta configuración de géneros y estructura tiene alta probabilidad de ser un Éxito rotundo!")
        else:
            st.error("❌ **Predicción del Modelo:** Estadísticamente, esta combinación suele tener menor puntuación, ¡pero mi motor te buscará joyas ocultas!")
            
        # 7. SISTEMA AVANZADO DE RECOMENDACIÓN Y FILTRADO (Lógica de Negocio Coherente)
        st.markdown("### 🎬 Universos de Anime Recomendados:")
        
        # Filtro inicial basado en el rating mínimo esperado por el usuario
        recomendaciones = df[df['rating'] >= rating_usuario]
        
        # Filtro estricto para asegurar que contenga todos los géneros que seleccioné
        for genero in generos_usuario:
            recomendaciones = recomendaciones[recomendaciones['genre'].str.contains(genero, na=False)]
            
        # Ordeno por los mejores calificados de mi base de datos
        recomendaciones = recomendaciones.sort_values(by='rating', ascending=False)
        
        # Filtro dinámico: Si el usuario activó películas u OVAs, busco que existan esos formatos con el mismo nombre en la base de datos
        lista_final = []
        vistos = set()
        
        for index, row in recomendaciones.iterrows():
            nombre_base = row['name'].split(':')[0].split('2nd')[0].strip() # Limpio el nombre para agrupar franquicias
            
            if nombre_base in vistos:
                continue
                
            # Busco en mi dataframe si esta franquicia cuenta con películas o con OVAs disponibles
            franquicia = df[df['name'].str.contains(nombre_base, na=False, case=False)]
            tiene_m = "Movie" in franquicia['type'].values
            tiene_o = "OVA" in franquicia['type'].values or "Special" in franquicia['type'].values
            
            # Aplico la lógica de negocio basada en las casillas marcadas por el usuario
            cumple_m = True if not quiere_movies else tiene_m
            cumple_o = True if not quiere_ovas else tiene_o
            
            if cumple_m and cumple_o and len(lista_final) < 5:
                vistos.add(nombre_base)
                
                # Extraigo las notas específicas de sus formatos complementarios para mostrarlos al costado
                rating_tv = franquicia[franquicia['type'] == 'TV']['rating'].max()
                rating_movie = franquicia[franquicia['type'] == 'Movie']['rating'].max()
                rating_ova = franquicia[franquicia['type'] == 'OVA']['rating'].max()
                
                lista_final.append({
                    'name': nombre_base,
                    'rating_gral': row['rating'],
                    'generos': row['genre'],
                    'tv': rating_tv,
                    'movie': rating_movie,
                    'ova': rating_ova
                })

        # 8. PRESENTACIÓN DE RESULTADOS EN FORMATO DE STREAMING REAL
        if not lista_final:
            st.info("No encontré universos de anime que cumplan con todos los filtros cruzados. ¡Prueba flexibilizar el rating o desmarcar algún complemento!")
        else:
            for anime in lista_final:
                st.markdown(f"🏆 **{anime['name']}** — *Rating General: ⭐ {anime['rating_gral']}*")
                
                # Genero las etiquetas de formato dinámicas y sus respectivos ratings al costado
                detalles = []
                if pd.notna(anime['tv']): detalles.append(f"📺 Serie TV: ⭐ {anime['tv']:.2f}")
                if pd.notna(anime['movie']): detalles.append(f"🎬 Película: ⭐ {anime['movie']:.2f}")
                if pd.notna(anime['ova']): detalles.append(f"📀 OVA/Especial: ⭐ {anime['ova']:.2f}")
                
                st.write(" | ".join(detalles))
                st.caption(f"📂 Géneros asociados: {anime['generos']}")
                st.markdown("---")