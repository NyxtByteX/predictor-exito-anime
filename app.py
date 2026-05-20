import streamlit as st
import pandas as pd
import joblib

modelo = joblib.load("modelos/modelo_randomforest.pkl")

st.set_page_config(page_title="Anime Popularity Predictor")

st.title("🎌 Anime Popularity Predictor")

st.write("Anita Victoria de la Vega")
st.write("Código ISIL: 76746502")

st.markdown("[Ver Google Colab](https://colab.research.google.com/drive/16v2MH2GRI56DD0CFavKbGtO3e8Ylw-qg?usp=sharing)")

st.image("https://cdn.myanimelist.net/images/anime/10/47347.jpg")

tipo = st.selectbox(
    "Tipo de anime",
    ["TV", "Movie", "OVA", "Special", "ONA", "Music"]
)

tipos = {
    "Movie": 0,
    "Music": 1,
    "ONA": 2,
    "OVA": 3,
    "Special": 4,
    "TV": 5
}

type_num = tipos[tipo]

episodes = st.slider("Cantidad de episodios", 1, 300, 12)

if st.button("Predecir"):

    datos = pd.DataFrame(
        [[type_num, episodes]],
        columns=['type', 'episodes']
    )

    pred = modelo.predict(datos)

    if pred[0] == 1:
        st.success("✅ Anime probablemente popular")
    else:
        st.error("❌ Anime probablemente no popular")