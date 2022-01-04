#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 18:39:14 2021
ANÁLISIS CIFRAS COVID-19 BOGOTÁ
Autor: Carlos Armando De Castro (cadecastro.com)
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
datos=pd.read_csv('https://datosabiertos.bogota.gov.co/dataset/44eacdb7-a535-45ed-be03-16dbbea6f6da/resource/b64ba3c4-9e41-41b8-b3fd-2da21d627558/download/osb_enftransm-covid-19_03012022.csv',sep=',')
datos['FECHA_DE_INICIO_DE_SINTOMAS']=pd.to_datetime(datos['FECHA_DE_INICIO_DE_SINTOMAS'],yearfirst=True)
FIS_bog=datos['FECHA_DE_INICIO_DE_SINTOMAS'].value_counts()
FIS_bog=FIS_bog.sort_index()
activos=datos.groupby('ESTADO').count()
activos=activos.drop(['Recuperado','Fallecido','Fallecido (No aplica No causa Directa)'])
activos=activos.sort_values('CASO',ascending=False)
localidades=pd.pivot_table(datos,values='CASO',index='FECHA_DE_INICIO_DE_SINTOMAS',columns='LOCALIDAD_ASIS',aggfunc=np.count_nonzero)
total_act=activos['CASO'].sum()
asint=activos['CASO'].sum()-activos['FECHA_DE_INICIO_DE_SINTOMAS'].sum()
leve=activos['CASO']['Leve']-asint
moderado=activos['CASO']['Moderado']
grave=activos['CASO']['Grave']
estados1=['Asintomático','Síntomas leves','Moderado','Grave']
estados2=np.array([asint,leve,moderado,grave])
activos=pd.DataFrame(estados2,estados1)
print('Casos activos en Bogotá: ',total_act)
print('Casos asintomáticos: ',np.format_float_positional(asint,precision=0),' Porcentaje: ',np.format_float_positional(asint/total_act*100,precision=2),'%')
print('Casos con síntomas leves: ',leve,' Porcentaje: ',np.format_float_positional(leve/total_act*100,precision=2),' %')
print('Casos con síntomas moderados: ',moderado,' Porcentaje: ',np.format_float_positional(moderado/total_act*100,precision=2),' %')
print('Casos con síntomas graves: ',grave,' Porcentaje: ',np.format_float_positional(grave/total_act*100,precision=2),' %')
plt.figure(1,figsize=(12,5))
plt.bar(FIS_bog.index,FIS_bog,color='blue')
plt.plot(FIS_bog.index,FIS_bog.rolling(window=7).mean(),'r')
plt.title('Casos por fecha inicio síntomas COVID-19 en Bogotá',loc='left')
plt.title('cadecastro.com',loc='right')
plt.ylabel('Casos diarios')
plt.legend(['Media móvil semanal','Casos diarios'])
plt.ylim(0,None)
localidad=str(input('Localidad: '))
plt.figure(2,figsize=(12,5))
plt.bar(localidades.index,localidades[localidad],color='blue')
plt.plot(localidades.index,localidades[localidad].rolling(window=7).mean(),'r')
plt.title('Casos por fecha inicio síntomas COVID-19 en '+localidad,loc='left')
plt.title('cadecastro.com',loc='right')
plt.ylabel('Casos diarios')
plt.legend(['Media móvil semanal','Casos diarios'])
plt.ylim(0,None)
plt.figure(3)
plt.bar(activos.index,activos[0],color='blue')
plt.title('Casos activos COVID-19 Bogotá',loc='left')
plt.title('cadecastro.com',loc='right')
plt.figure(4,figsize=(12,5))
plt.plot(localidades.index,localidades['Sin dato'],'r')
plt.plot(localidades.index,localidades['Suba'],'b')
plt.plot(localidades.index,localidades['Kennedy'],'y')
plt.plot(localidades.index,localidades['Santa Fe'],'c')
plt.plot(localidades.index,localidades['Chapinero'],'m')
plt.plot(localidades.index,localidades['Usaquén'],'g')
plt.legend(['Sin dato','Suba','Kennedy','Santa Fe','Chapinero','Usaquén'])
plt.title('Casos COVID-19 localidades Bogotá',loc='left')
plt.xlabel('cadecastro.com')
plt.ylabel('Inicios de síntomas')
plt.ylim(0,None)
plt.grid(True,'both','both')
plt.figure(5,figsize=(12,5))
plt.bar(localidades.index,localidades['Sin dato'],color='blue')
plt.plot(localidades.index,localidades['Sin dato'].rolling(window=7).mean(),'r')
plt.title('Casos COVID-19 localidad Sin dato',loc='left')
plt.title('cadecastro.com',loc='right')
plt.ylabel('Inicios de síntomas')
plt.ylim(0,None)
plt.grid(True,'both','both')
plt.legend(['Media móvil semanal','Casos diarios'])