import streamlit as st
import pandas as pd
import numpy as np
import json
from streamlit_lottie import st_lottie

st.set_page_config(page_title = "JN style", page_icon = ":chart", layout = "centered")
st.title("JN Style")

st.subheader("Vístete con nosotros y lleva tu estilo a otro nivel")

st.image("./Foto.png")

st.markdown("En JN Style nos apasiona el estilo y la elegancia. Somos una marca comprometida en ofrecerte las últimas tendencias en moda con un toque personal y único. Nuestra marca nace de la fusión de visiones creativas y el amor por la moda, creando una experiencia de compra en línea que destaca por su calidad, diseño y autenticidad.")

st.write("**JN Style**")

with st.expander("Sostenibilidad"):
    st.markdown("""JN Style garantiza que todos los pasos que da para satisfacer a sus clientes se realizan del modo más sostenible posible.""")
    st.markdown("""
            * Más de la mitad de los productos son ecológicos. \n
            * El grupo ha reducido en una tercera parte sus emisiones de CO2 (desde 2010). \n
            * Asimismo, ha reducido al máximo los embalajes y optimizado sus rutas de transporte""")

uploaded_file = st.file_uploader(".data/Sample-Superstore.csv", type = ["csv"])
if uploaded_file is not None:
    dataset = pd.read_csv(uploaded_file, parse_dates = ["Order Date"])
    dataset["Order Date Year"] = dataset["Order Date"].dt.strftime('%Y')
    
    if st.button("ver datos"):
        st.markdown("<h3 style='text-align: center; color:red;'>DataFrame (2013 - 2016)</h3>", unsafe_allow_html=True)
        st.dataframe(dataset)
        pivot_table = pd.pivot_table(dataset, values = "Sales", index = "Order Date Year",  columns = "Region", aggfunc = np.sum).copy()
        st.markdown("<p style='text-align: center;'>Ventas totales por Estado (2013 - 2016)</p>", unsafe_allow_html=True)
        st.line_chart(pivot_table)
        st.balloons()
        st.snow()
        with open("data/animation.json") as source:
            animation = json.load(source)
        st_lottie(animation, height=100, width=100)