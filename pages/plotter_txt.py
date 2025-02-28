import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

st.title('PLOTTER')
c1 = st.container()
c2 = st.container()

upload = c1.file_uploader('Hier .txt/.csv hochladen',type=['txt','csv'])
c11,c12,c13 = c1.columns(3)
c11.selectbox('Trennung zwischen Spalten?',['tab',','])
c12.selectbox('Trennung Dezimalzahlen?',['.',','])
skip = c13.number_input('Wie viele Zeilen skippen?',step=1,min_value=0)

if upload is None:
    st.write('Zuerst muss eine Datei hochgeladen werden!!')
elif upload is not None:
    
    wertetabelle = pd.read_csv(upload,sep='\t',skiprows=skip)
    
    labels = wertetabelle.columns.tolist()
    
    
    x_data = labels[0]
    y_data = labels[1]
    
    c1.write(wertetabelle)
    
    
    
    
    ###############################
    c21,c22,c23 = c2.columns(3)
    text_x_Achse = c21.text_input('Beschriftung der x-Achse?')
    text_y_Achse = c22.text_input('Beschriftung der y-Achse?')
    text_titel = c23.text_input('Titel des Plots?')
    color_input = c21.color_picker('Farbe der Datenpunkte?')
    label_input = c22.text_input('Label für Legende?')
    
    
    
    fig1,ax1 = plt.subplots()
    ax1.scatter(wertetabelle[x_data],wertetabelle[y_data],label=label_input,color = color_input)
    ax1.grid(color='lightgray')
    ax1.set_xlabel(text_x_Achse)
    ax1.set_ylabel(text_y_Achse)
    ax1.set_title(text_titel)
    
    
    
    check_linfit = c23.checkbox('LinFit?')
    if check_linfit==True:
        c3 = st.container()
        c31,c32,c33 = c3.columns(3)
        color_linfit = c31.color_picker('Farbe LinFit?')
        posx_linfit = c32.slider('x-Position LinFit Text?',min_value=0.,max_value=1.,step=0.05,value=0.5)
        posy_linfit = c33.slider('y-Position LinFit Text?',min_value=0.,max_value=1.,step=0.05,value=0.2)
        
        
        x_fit = np.array(wertetabelle[x_data])
        results = linregress(wertetabelle[x_data],wertetabelle[y_data])
        k = results.slope
        k_err = results.stderr
        d = results.intercept
        d_err = results.intercept_stderr
        y_fit = k*x_fit+d
        
        # R² berechnen
        y_mean = np.mean(wertetabelle[y_data])
        ss_tot = np.sum((wertetabelle[y_data] - y_mean) ** 2)  # Gesamtstreuung
        ss_res = np.sum((wertetabelle[y_data] - y_fit) ** 2)   # Reststreuung
        r_squared = 1 - (ss_res / ss_tot)  # R²-Wert
    
        # Chi² berechnen (ohne Fehlerbalken: σ_y = 1)
        chi_squared = np.sum((wertetabelle[y_data] - y_fit) ** 2)
        
        linfit_text = (f'LinFit\n({k:.3}±{k_err:.3})*x+({d:.3}±{d_err:.3})\nR^2={r_squared:.3}\nChi={chi_squared:.3}')
        fig1.text(posx_linfit, posy_linfit, linfit_text, fontsize=8, color="black",backgroundcolor='white')
    
    
    
        
        ax1.plot(x_fit,y_fit,label='LinFit',color=color_linfit)
        
    
    ax1.legend()
    c0 = st.container()
    c0.pyplot(fig1)





