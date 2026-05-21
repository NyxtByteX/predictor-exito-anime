# 🎌 Sistema Inteligente de Recomendación de Anime

¡Bienvenido a mi proyecto final de Machine Learning! 

En este repositorio presento el desarrollo y despliegue de un **Sistema Inteligente de Recomendación de Anime**, construido como parte de mi evaluación académica para ISIL. 

## Sobre el Proyecto:
El objetivo principal de esta aplicación web es interactuar con el usuario para conocer sus preferencias (géneros favoritos, formato de emisión, episodios y expectativa de calificación). Con estos datos, la aplicación hace dos cosas:

1. **Predicción con Machine Learning:** Utiliza un modelo de clasificación entrenado (*Random Forest*) para predecir si esa combinación específica tiene potencial para ser un "Éxito" (alta calificación) en la comunidad.

2. **Sistema de Filtrado:** Busca en una base de datos procesada para devolver recomendaciones reales que calcen perfectamente con los gustos del usuario.

## 🛠️ Tecnologías y Herramientas Utilizadas
Para lograr el flujo completo desde el análisis de datos hasta el despliegue web, utilicé las siguientes librerías:
* **Pandas & NumPy:** Limpieza, preprocesamiento de datos y One-Hot Encoding.
* **Scikit-Learn:** División de datos (`stratify`), entrenamiento de modelos (Random Forest y Regresión Logística) y evaluación de métricas (Accuracy, F1-Score).
* **Joblib:** Exportación e importación de los modelos entrenados (`.pkl`).
* **Streamlit:** Construcción de la interfaz web interactiva y despliegue en la nube.

## 📁 Estructura del Repositorio
* `app.py`: Contiene el código fuente de la interfaz web en Streamlit.
* `requirements.txt`: Lista de dependencias necesarias para que el servidor ejecute la aplicación.
* `anotaciones.txt`: Documentación del prompt utilizado para estructurar el proyecto con IA.
* `/modelos`: Carpeta que almacena los modelos predictivos pre-entrenados, las estructuras de columnas y el dataset limpio.

## 👨‍🎓 Datos del Estudiante
* **Nombre:** Ana Victoria De la Vega Pando
* **Código ISIL:** 76746502
* **Cuaderno de Entrenamiento:** (🔗 https://colab.research.google.com/drive/19GXKxmwQl9fVWnY8g0YBye2kTUh5sA5x?usp=sharing )

---
*Desplegado exitosamente en Streamlit Cloud.*