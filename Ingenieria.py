import datetime
import time
import streamlit as st
import plotly_express as px
import pandas as pd
from PIL import Image

#DISEÑO
def design():
    st.set_option('deprecation.showfileUploaderEncoding',False)
#Titulo y sub
# Images
#img = Image.open(r'C:\Users\josma\Documents\CarpetaVisualStudio\cecytem.jpg')
#st.image(img, width=200)
#header_pic = Image.open(r'C:\Users\josma\Documents\CarpetaVisualStudio\cecytem.jpg')
#st.image(header_pic, use_column_width=False)
#st.markdown("<h3 style='text-align: center; color: white;'>Plantel Tequixquiac</h1>", unsafe_allow_html=True)
    title_container = st.container()
    col1, col3 = st.columns([15, 5])
    image = Image.open(r'C:\Users\josma\Documents\CarpetaVisualStudio\cecytem.jpg')
    logmx = Image.open(r'C:\Users\josma\Documents\CarpetaVisualStudio\mx2.jpg')
    with title_container:
        with col1:
                st.image(image, width=150)
        with col3:
                st.image(logmx, width=150)
    st.markdown("<h1 style='text-align: center; color: white;'>Colegio de Estudios Científicos y Tecnológicos del Estado de México</h1>", unsafe_allow_html=True)

#USUARIO Y CONTRASEÑA
def autorizacion():
    usuario = st.text_input("Usuario:", "")
    password = st.text_input("Contrasena:")
    while True:
        if usuario == "yo" and password == "contra":
            
            break
        

#BARRA AJUSTES Y LECTURA ARCHIVO
def lectura_archivo():
    st.sidebar.subheader("AJUSTES")
    # CARGA DE ARCHIVOS
    archivo_cargado = st.sidebar.file_uploader(label="Sube aqui tus archivos CSV o Excel.",
                         type=['csv','xlsx'])
    global datos
    # si el archivo cargado no es ninguno
    if archivo_cargado is not None:
        print(archivo_cargado)
        try:
            datos = pd.read_csv(archivo_cargado)
        except Exception as e:
            print(e)
            datos = pd.read_excel(archivo_cargado)
    global cols_num
    try:
        st.write(datos)# tipos de datos del df, seleccion de columns
        cols_num = list(datos.select_dtypes(['float','int']).columns)
        cols_numNoNumericas = list(datos.select_dtypes(['object']).columns)
    except Exception as e:
        print(e)
        st.write("Porfavor suba su archivo a la aplicaión")

#FUNCION PRINCIPAL        
design()
lectura_archivo()