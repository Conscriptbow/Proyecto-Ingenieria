import datetime
import time
import streamlit as st
import plotly_express as px
import pandas as pd
from PIL import Image
import sqlite3
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
conn = sqlite3.connect('data.db')
c = conn.cursor()

#DISEÑO
def design():
    #TITULO    
    st.set_option('deprecation.showfileUploaderEncoding',False)
    title_container = st.container()
    col1, col3 = st.columns([15, 5])
    with title_container:
        with col1:
                st.image('https://seeklogo.com/images/C/cecytem-logo-57EA94498B-seeklogo.com.png', width=150)
        with col3:
                st.image('https://www.paratodomexico.com/imagenes/estados-de-mexico/mexico/escudo_estado_mexico.png', width=150)
    st.markdown("<h1 style='text-align: center;'>Colegio de Estudios Científicos y Tecnológicos del Estado de México</h1>", unsafe_allow_html=True)
    #st.video('https://www.youtube.com/watch?v=8K_9mlscRfg&ab_channel=VIDEOSDEIMPACTO')

#BARRA AJUSTES Y LECTURA ARCHIVO
def lectura_archivo():
    st.subheader("INSERTAR ARCHIVO:")
    # CARGA DE ARCHIVOS
    archivo_cargado = st.file_uploader(label="Sube aqui tus archivos CSV o Excel.",
                         type=['csv','xlsx'])
    global datos
    # si el archivo cargado no es ninguno
    if archivo_cargado is not None:
        print(archivo_cargado)
        try:
            datos = pd.read_csv(archivo_cargado)   
        except Exception as e:
            st.subheader("TABLA CECYTEM: ")
            print(e)
            datos = pd.read_excel(archivo_cargado)
            my_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1)

    global cols_num
    try:
        st.write(datos)# tipos de datos del df, seleccion de columns
        menu = ["Turno Matutino", "Turno Vespertino"]
        semestre = st.sidebar.multiselect("Seleccione el semestre: ", options=datos["Semestre"].unique())
        carrera = st.sidebar.multiselect("Seleccione la carrera: ", options=datos["Carrera"].unique())
        grupo = st.sidebar.multiselect("Seleccione el grupo: ", options=datos["Grupo"].unique())
        asignatura = st.sidebar.multiselect("Seleccione la asignatura: ", options=datos["Asignatura"].unique())
        datos_selection = datos.query("Grupo==@grupo and Semestre==@semestre and Carrera == @carrera and Asignatura == @asignatura")
        #Indice aprobación todo los datos
        Aprobacion()
        #DATOS RESUMIDOS
        prueba1 = datos.describe()
        st.subheader("DATOS RESUMIDOS: ")
        prueba = prueba1.iloc[[1,3,4,5,6,7],[3,4,5,7]]
        prueba
        #Promedio por grupo, materia...
        st.subheader("PROMEDIOS: ")
        ndf = datos.pivot_table(index = ['Grupo', 'Carrera'],columns=['Asignatura', 'Semestre'],aggfunc={'P1':np.average,'P2':np.average})
        ndf
        try:
            st.subheader("TABLA CON DATOS FILTRADOS: ")
            st.dataframe(datos_selection)
            choice =st.selectbox("Seleccione el turno: ", menu)
            if choice == "Turno Matutino":
                cols_num = list(datos.select_dtypes(['float','int','object']).columns)
                a=100
                frames = []
                for i in range(0,6):
                    if a == 104:
                        a=200
                    elif a == 204:
                        a=300
                    elif a == 304:
                        a=400
                    elif a == 404:
                        a=500
                    elif a==504:
                        a=600
                    for j in range(0,4):
                        a = a + 1
                        grupoMatutino = datos.loc[datos['Grupo'] == a]
                        frames.append(grupoMatutino)
                df = pd.concat(frames, sort=False)
                st.subheader("TABLA TURNO MATUTINO: ")
                st.dataframe(df)
                grafico()
            elif choice == "Turno Vespertino":
                a=104
                frames2 = []
                for i in range(0,6):
                    if a == 108:
                        a=204
                    elif a == 208:
                        a=304
                    elif a == 308:
                        a=404
                    elif a == 408:
                        a=504
                    elif a==508:
                        a=604
                    for j in range(0,4):
                        a = a + 1
                        grupoTarde = datos.loc[datos['Grupo'] == a]
                        frames2.append(grupoTarde)
                dc = pd.concat(frames2, sort = False)
                st.subheader("TABLA TURNO VESPERTINO: ")
                st.dataframe(dc)
                grafico()
        except Exception as e:
            print(e)
            st.write("No has seleccionado el turno")
    except Exception as e:
        print(e)
        st.write("Porfavor suba su archivo a la aplicación")

#BD BASA EN DISCO
    #CREAR TABLA BD
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')
    #AGREGAR USER Y PASSWORD
def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()
    #LOGIN
def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data
    #CAMBIAR PASSWORD
def change_password(password,username):
    c.execute('UPDATE userstable SET password =? WHERE username =?',(password,username))
    conn.commit()
    #VER TODOS LOS USUARIOS
def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

#INGRESO A LA PLATAFORMA
def seguridad():
    design()
    st.sidebar.image('https://www.pinclipart.com/picdir/big/564-5647199_transparent-home-icon-clipart-circle-transparent-home-icon.png',width=100)
    menu = ["Acceder", "SignUp", "Cerrar Sesión"]
    choice = st.sidebar.selectbox("MENU", menu)
    if choice == "Cerrar Sesión":
        st.info("Has cerrado sesión")
    elif choice == "Acceder":
        username = st.sidebar.text_input("Nombre de usuario")
        password = st.sidebar.text_input("Contraseña", type = 'password')
        if st.sidebar.checkbox("Acceder"):
            create_usertable()
            result = login_user(username,password)
            if result:
                st.success("Te has logeado como: {}".format(username))                          
                lectura_archivo()
            else:
                st.warning("Incorrect Username/Password")
        elif st.sidebar.checkbox("¿Olvido su contraseña?"):
            st.subheader("Cambiar password")      
            user = st.text_input("Username") #INGRESAR USUARIO EL CUAL NOS VA SERVIR COMO REFERENCIA
            new_pass = st.text_input("Password", type='password') #INGRESAR LA NUEVA CONTRASEÑA z 
            if st.checkbox("Change"):
                change_password(new_pass,user) #FUNCION PARA CAMBIAR CONTRASEÑA
                st.success("Se cambio su contraseña")
    elif choice == "SignUp":
        st.subheader("Crear nueva cuenta")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user, new_password)
            st.success("New account")
            st.info("Puede ingresar")

def grafico():
    st.subheader("Gráfico de barras:")
    st.subheader("Gráfico: ")
    try:
            x_val = st.selectbox('Seleccione x: ', options = ['P1', 'P2', 'P3', 'FIN'])
            y_val = st.selectbox('Seleccione y: ', options = ['Carrera', 'Semestre','Grupo'])
            plot = px.box(data_frame=datos, x=x_val,y=y_val,width=600, height=400)
            st.plotly_chart(plot)
    except Exception as e:
        print(e)

def Aprobacion():
    indiceAproP1 = datos.loc[datos['P1'] >= 6]
    porcentajeP1 = (len(indiceAproP1)*100)/len(datos)
    indiceReproP1 = datos.loc[datos['P1']<=5]
    porcentajeReP1 = (len(indiceReproP1)*100)/len(datos)
    st.subheader("PORCENTAJE DE APROBACIÓN DE P1: " + str(round(porcentajeP1, 2)) 
                + "% Y PORCENTAJE DE REPROBACIÓN DE P1: " + str(round(porcentajeReP1, 2)) + "%")
    #P2
    indiceAproP2 = datos.loc[datos['P2'] >= 6]
    porcentajeP2 = (len(indiceAproP2)*100)/len(datos)
    indiceReproP2 = datos.loc[datos['P2']<=5]
    porcentajeReP2 = (len(indiceReproP2)*100)/len(datos)
    st.subheader("PORCENTAJE DE APROBACIÓN DE P2: " + str(round(porcentajeP2, 2)) 
                + "% Y EL PORCENTAJE DE REPROBACIÓN DE P2: " + str(round(porcentajeReP2, 2)) + "%")

    a=100
    frames = []
    for i in range(0,6):
        if a == 104:
            a=200
        elif a == 204:
            a=300
        elif a == 304:
            a=400
        elif a == 404:
            a=500
        elif a==504:
            a=600
        for j in range(0,4):
            a = a + 1
            grupoMatutino = datos.loc[datos['Grupo'] == a]
            frames.append(grupoMatutino)
            
    a=104
    frames2 = []
    for i in range(0,6):
        if a == 108:
            a=204
        elif a == 208:
            a=304
        elif a == 308:
             a=404
        elif a == 408:
            a=504
        elif a==508:
            a=604
        for j in range(0,4):
            a = a + 1
            grupoTarde = datos.loc[datos['Grupo'] == a]
            frames2.append(grupoTarde)
    

    indiceMañana = []
    for i in range(0, len(frames)):
        primerGrupo=frames[i].loc[frames[i]['P1']>=6]
        if primerGrupo.empty:
            continue
        porcentaje = (len(primerGrupo)*100)/len(frames[i])
        indiceMañana.append(porcentaje)

    mañana=pd.DataFrame(data=indiceMañana)
    mañana.rename(columns={0:'APROBACIÓN (%)'}, inplace=True)

    pruebasm = []

    for i in range(0, len(frames)):
        if frames[i].empty:
            continue
        pruebas = frames[i]['Grupo'].unique()
        pruebasm.append(pruebas)

    for i in range (0, len(mañana)):
        mañana.rename(index={i:int(pruebasm[i])}, inplace=True)

    mañana

    indiceTarde = []
    for i in range(0, len(frames2)):
        segundoGrupo=frames2[i].loc[frames2[i]['P1']>=6]
        if segundoGrupo.empty:
            continue
        porcentaje = (len(segundoGrupo)*100)/len(frames2[i])
        indiceTarde.append(porcentaje)

    tarde=pd.DataFrame(data=indiceTarde)
    tarde.rename(columns={0:'APROBACIÓN (%)'}, inplace=True)

    pruebast = []
    for i in range(0, len(frames2)):
        if frames2[i].empty:
            continue
        pruebas = frames2[i]['Grupo'].unique()
        pruebast.append(pruebas)

    for i in range (0, len(tarde)):
        tarde.rename(index={i:int(pruebast[i])}, inplace=True)
    tarde
#FUNCION PRINCIPAL        
seguridad()