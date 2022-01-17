#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 22:02:08 2021
ANÁLISIS CIFRAS COVID-19 COLOMBIA
Autor: Carlos Armando De Castro (cadecastro.com)
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#Input de región de interés:
print('ANÁLISIS CIFRAS COVID-19 COLOMBIA')
print('Autor: Carlos Armando De Castro - cadecastro.com')
#Importar datos de Datos Abiertos Colombia:
columnas=['Nombre departamento','Edad','Sexo','Ubicación del caso','Estado','Fecha de inicio de síntomas','Fecha de muerte']
covid=pd.read_csv('https://www.datos.gov.co/api/views/gt2j-8ykr/rows.csv',usecols=columnas)
poblacion=pd.read_csv('https://raw.githubusercontent.com/cadecastro/analisis_datos/main/poblacion_deptos_2021.csv')
poblacion=poblacion.set_index('DEPARTAMENTO')
poblacion=poblacion.rename(columns={'POBLACION 2021':'Población'})
#Convertir fechas de muerte a formato adecuado:
covid["Fecha de muerte"] = pd.to_datetime(covid["Fecha de muerte"],dayfirst=True)
covid["Fecha de inicio de síntomas"] = pd.to_datetime(covid["Fecha de inicio de síntomas"],dayfirst=True)
#Corrección datos:
covid['Nombre departamento']=covid['Nombre departamento'].replace(to_replace=['Tolima','Caldas','STA MARTA D.E.'],value=['TOLIMA','CALDAS','SANTA MARTA'])
covid['Sexo']=covid['Sexo'].replace(to_replace=['m'],value=['M'])
#Casos que fallecieron por COVID-19:
muertes=covid[covid['Estado']=='Fallecido']
#RESUMEN REGIONES:
casos_regiones=pd.pivot_table(covid,values='Edad',index='Nombre departamento',aggfunc=np.count_nonzero).fillna(0)
casos_regiones=casos_regiones.rename(columns={'Edad':'Casos'})
muertes_regiones=pd.pivot_table(muertes,values='Edad',index='Nombre departamento',aggfunc=np.count_nonzero).fillna(0)
muertes_regiones=muertes_regiones.rename(columns={'Edad':'Muertes'})
regiones=pd.merge(casos_regiones,muertes_regiones,left_index=True,right_index=True)
regiones=pd.merge(regiones,poblacion,left_index=True,right_index=True)
del casos_regiones,muertes_regiones,poblacion
cfr_reg=regiones['Muertes']/regiones['Casos']*100
cfr_reg=cfr_reg.sort_values(ascending=False)
let_reg=regiones['Muertes']/regiones['Población']*100
let_reg=let_reg.sort_values(ascending=False)
#COLOMBIA:
#Conteo de muertes por fecha de ocurrencia:
fecha_muerte=muertes['Fecha de muerte'].value_counts().fillna(0)
fecha_muerte=fecha_muerte.sort_index()
#Conteo de casos por fecha de inicio de síntomas:
fecha_sint=covid['Fecha de inicio de síntomas'].value_counts().fillna(0)
fecha_sint=fecha_sint.sort_index()
#Muertes por sexo:
sexo_muerte=muertes.groupby(['Sexo'])[['Fecha de muerte']].count().fillna(0)
sexo_muerte=sexo_muerte.sort_values(by=['Fecha de muerte'],ascending=False)
#Muertes por edad:
edades_muerte=muertes.groupby(['Edad'])[['Fecha de muerte']].count().fillna(0)
#Casos por edad:
edades_casos=covid.groupby(['Edad'])[['Edad']].count().fillna(0)
#CFR por edad:
CFR_edad=edades_muerte['Fecha de muerte'].divide(edades_casos['Edad'])
#Estadísticas casos por edad:
stat_edad_casos=covid['Edad'].describe()
stat_edad_muertes=muertes['Edad'].describe()

print('-------------------------------------------------------------------')
print('POBLACIÓN EN COLOMBIA: ',np.format_float_positional(regiones['Población'].sum(),precision=0))
print('CASOS EN COLOMBIA: ',np.format_float_positional(regiones['Casos'].sum(),precision=0))
print('MUERTES EN COLOMBIA: ',np.format_float_positional(regiones['Muertes'].sum(),precision=0))
print('MUERTES PER CÁPITA EN COLOMBIA =',np.format_float_positional(regiones['Muertes'].sum()/regiones['Población'].sum()*100,precision=3),'%')
print('LETALIDAD POR CASO EN COLOMBIA =',np.format_float_positional(regiones['Muertes'].sum()/regiones['Casos'].sum()*100,precision=3),'%')
print('-------------------------------------------------------------------')
print('Estadísticas de edad de los casos en COLOMBIA:')
print(stat_edad_casos)
print('Estadísticas de edad de las muertes en COLOMBIA:')
print(stat_edad_muertes)
print('-------------------------------------------------------------------')
print('AVISO: LAS CURVAS DE *CASOS* DEPENDEN DE LAS PRUEBAS Y')
print('POR CAMBIOS EN SU MUESTREO NO SON CONFIABLES')
print('*LA ATENCIÓN DEBE CENTRARSE EN LAS CURVAS DE MUERTES DIARIAS*')

plt.figure(1,figsize=(12,5))
plt.subplot(211)
#plt.bar(fecha_muerte.index[:len(fecha_muerte)-2],fecha_muerte[:len(fecha_muerte)-2],color='blue')
plt.plot(fecha_muerte.index[:len(fecha_muerte)-2],fecha_muerte[:len(fecha_muerte)-2].rolling(window =7).mean(),'r')
plt.title('Cifras diarias COVID-19 en Colombia',loc='left')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(fecha_muerte.index[0],fecha_muerte.index[len(fecha_muerte)-2])
plt.legend(['Media móvil 7 días','Datos'])
plt.ylabel('Muertes diarias')
plt.subplot(212)
#plt.bar(fecha_sint.index[:len(fecha_sint)-7],fecha_sint[:len(fecha_sint)-7],color='blue')
plt.plot(fecha_sint.index[:len(fecha_sint)-7],fecha_sint[:len(fecha_sint)-7].rolling(window =7).mean(),'b')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(fecha_sint.index[0],fecha_sint.index[len(fecha_sint)-7])
plt.legend(['Media móvil 7 días','Datos'])
plt.ylabel('Inicio de síntomas diarios')
plt.xlabel('cadecastro.com')

plt.figure(2,figsize=(12,5))
plt.bar(fecha_muerte.index[len(fecha_muerte)-31:len(fecha_muerte)-2],fecha_muerte[len(fecha_muerte)-31:len(fecha_muerte)-2],color='blue')
plt.plot(fecha_muerte.index[len(fecha_muerte)-31:len(fecha_muerte)-2],fecha_muerte[len(fecha_muerte)-31:len(fecha_muerte)-2].rolling(window=7).mean(),'r')
plt.title('Muertes COVID-19 en Colombia último mes',loc='left')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.ylabel('Muertes diarias')
plt.xlabel('cadecastro.com')

plt.figure(3,figsize=(12,5))
plt.bar(fecha_sint.index[len(fecha_sint)-37:len(fecha_sint)-7],fecha_sint[len(fecha_sint)-37:len(fecha_sint)-7],color='blue')
plt.plot(fecha_sint.index[len(fecha_sint)-37:len(fecha_sint)-7],fecha_sint[len(fecha_sint)-37:len(fecha_sint)-7].rolling(window=7).mean(),'r')
plt.title('Casos por inicio de síntomas en Colombia último mes',loc='left')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.ylabel('Casos diarios')
plt.xlabel('cadecastro.com')

plt.figure(4,figsize=(8,5))
plt.subplot(211)
plt.fill_between(edades_casos.index,edades_casos['Edad'],color='blue')
plt.fill_between(edades_muerte.index,edades_muerte['Fecha de muerte'],color='red')
plt.title('Casos y muertes COVID-19 Colombia por edad',loc='left')
plt.grid(True,'both','both')
plt.legend(['Casos','Muertes'])
plt.xlim(1,114)
plt.ylim(0,None)
plt.subplot(212)
plt.plot(CFR_edad,'b')
plt.ylabel('Muertes/Casos')
plt.xlabel('cadecastro.com')
plt.grid(True,'both','both')
plt.legend(['CFR'])
plt.xlim(1,90)
plt.ylim(0,0.4)

plt.figure(5)
plt.pie(sexo_muerte['Fecha de muerte'],labels=sexo_muerte.index,colors=['red','blue'])
plt.title('Muertes COVID-19 Colombia por género',loc='left')

plt.figure(6,figsize=(12,6))
let_reg.plot.bar(color='blue')
plt.title('Muertes COVID-19 per cápita',loc='left')
plt.title('cadecastro.com',loc='right')
plt.ylabel('Muertes/Habitantes (%)')

plt.figure(7,figsize=(12,6))
cfr_reg.plot.bar(color='blue')
plt.title('Tasa de letalidad por caso',loc='left')
plt.title('cadecastro.com',loc='right')
plt.ylabel('Muertes/Casos (%)')

plt.figure(8,figsize=(12,5))
plt.subplot(121)
covid['Edad'].plot.hist(color='blue')
plt.title('Histograma casos COVID-19',loc='left')
plt.xlabel('Edad')
plt.subplot(122)
muertes['Edad'].plot.hist(color='red')
plt.title('Histograma muertes COVID-19',loc='left')
plt.xlabel('Edad - cadecastro.com')
plt.xlabel('cadecastro.com')

#Muertes per cápita en regiones de interés:
mpc=pd.pivot_table(data=muertes,values='Edad',index='Fecha de muerte',columns='Nombre departamento',aggfunc=np.count_nonzero).fillna(0)
mpc=mpc[['AMAZONAS','ANTIOQUIA','BARRANQUILLA','BOGOTA','VALLE']]
mpc['AMAZONAS']=mpc['AMAZONAS']/regiones['Población']['AMAZONAS']
mpc['ANTIOQUIA']=mpc['ANTIOQUIA']/regiones['Población']['ANTIOQUIA']
mpc['BARRANQUILLA']=mpc['BARRANQUILLA']/regiones['Población']['BARRANQUILLA']
mpc['BOGOTA']=mpc['BOGOTA']/regiones['Población']['BOGOTA']
mpc['VALLE']=mpc['VALLE']/regiones['Población']['VALLE']

plt.figure(9,figsize=(12,6))
plt.title('Muertes per cápita - media móvil 7 días')
plt.title('cadecastro.com',loc='right')
plt.ylabel('Muertes diarias / Habitantes')
plt.plot(mpc.index[:len(mpc.index)-2],mpc['BOGOTA'][:len(mpc.index)-2].rolling(window=7).mean(),'b')
plt.plot(mpc.index[:len(mpc.index)-2],mpc['BARRANQUILLA'][:len(mpc.index)-2].rolling(window=7).mean(),'r')
plt.plot(mpc.index[:len(mpc.index)-2],mpc['VALLE'][:len(mpc.index)-2].rolling(window=7).mean(),'m')
plt.plot(mpc.index[:len(mpc.index)-2],mpc['ANTIOQUIA'][:len(mpc.index)-2].rolling(window=7).mean(),'g')
plt.plot(mpc.index[:len(mpc.index)-2],mpc['AMAZONAS'][:len(mpc.index)-2].rolling(window=7).mean(),'c')
plt.legend(['Bogotá','Barranquilla','Valle','Antioquia','Amazonas'])
plt.grid(True,which='both',axis='both')
plt.ylim(0,None)
plt.xlim(mpc.index[0],mpc.index[len(mpc.index)-2])

#REGIÓN A ANALIZAR:
depto=str(input('Departamento o distrito a analizar (todo en mayúsculas):'))
#Casos y muertes:
casos_dep=covid[covid['Nombre departamento']==depto]
muertes_dep=casos_dep[casos_dep['Estado']=='Fallecido']
#Conteo de casos por fecha de inicio de síntomas:
fecha_sint_dep=casos_dep['Fecha de inicio de síntomas'].value_counts().fillna(0)
fecha_sint_dep=fecha_sint_dep.sort_index()
#Conteo por fecha de ocurrencia:
fecha_muerte_dep=muertes_dep['Fecha de muerte'].value_counts().fillna(0)
fecha_muerte_dep=fecha_muerte_dep.sort_index()
#Muertes por edad:
edades_muerte_dep=muertes_dep.groupby(['Edad'])[['Fecha de muerte']].count().fillna(0)
#Casos por edad:
edades_casos_dep=casos_dep.groupby(['Edad'])[['Edad']].count().fillna(0)
#CFR por edad:
CFR_dep=edades_muerte_dep['Fecha de muerte'].divide(edades_casos_dep['Edad'])
#Estadísticas casos por edad:
stat_edad_casos_dep=casos_dep['Edad'].describe()
stat_edad_muertes_dep=muertes_dep['Edad'].describe()

print('-------------------------------------------------------------------')
print('POBLACIÓN EN '+depto+': ',np.format_float_positional(regiones['Población'][depto].sum(),precision=0))
print('CASOS EN '+depto+': ',np.format_float_positional(regiones['Casos'][depto].sum(),precision=0))
print('MUERTES EN '+depto+': ',np.format_float_positional(regiones['Muertes'][depto].sum(),precision=0))
print('MUERTES PER CÁPITA EN '+depto+' =',np.format_float_positional(regiones['Muertes'][depto].sum()/regiones['Población'][depto].sum()*100,precision=3),'%')
print('LETALIDAD POR CASO EN '+depto+' =',np.format_float_positional(regiones['Muertes'][depto].sum()/regiones['Casos'][depto].sum()*100,precision=3),'%')
print('-------------------------------------------------------------------')
print('Estadísticas de edad de los casos en ',depto)
print(stat_edad_casos_dep)
print('Estadísticas de edad de las muertes en ',depto)
print(stat_edad_muertes_dep)
print('-------------------------------------------------------------------')
print('AVISO: LAS CURVAS DE *CASOS* DEPENDEN DE LAS PRUEBAS Y')
print('POR CAMBIOS EN SU MUESTREO NO SON CONFIABLES')
print('*LA ATENCIÓN DEBE CENTRARSE EN LAS CURVAS DE MUERTES DIARIAS*')

plt.figure(10,figsize=(12,5))
plt.subplot(211)
#plt.bar(fecha_muerte_dep.index[:len(fecha_muerte_dep)-2],fecha_muerte_dep[:len(fecha_muerte_dep)-2],color='blue')
plt.plot(fecha_muerte_dep[:len(fecha_muerte_dep)-2].rolling(window =7).mean(),'r')
plt.title('Cifras diarias COVID-19 '+depto,loc='left')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(fecha_muerte_dep.index[0],fecha_muerte_dep.index[len(fecha_muerte_dep)-2])
plt.legend(['Media móvil 7 días','Datos'])
plt.ylabel('Muertes diarias')
plt.subplot(212)
#plt.bar(fecha_sint_dep.index[:len(fecha_sint_dep)-7],fecha_sint_dep[:len(fecha_sint_dep)-7],color='blue')
plt.plot(fecha_sint_dep.index[:len(fecha_sint_dep)-7],fecha_sint_dep[:len(fecha_sint_dep)-7].rolling(window =7).mean(),'b')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(fecha_sint_dep.index[0],fecha_sint_dep.index[len(fecha_sint_dep)-7])
plt.legend(['Media móvil 7 días','Datos'])
plt.ylabel('Inicio síntomas diarios')
plt.xlabel('cadecastro.com')

plt.figure(11,figsize=(12,5))
plt.bar(fecha_muerte_dep.index[len(fecha_muerte_dep)-31:len(fecha_muerte_dep)-1],fecha_muerte_dep[len(fecha_muerte_dep)-31:len(fecha_muerte_dep)-1],color='blue')
plt.plot(fecha_muerte_dep.index[len(fecha_muerte_dep)-31:len(fecha_muerte_dep)-1],fecha_muerte_dep[len(fecha_muerte_dep)-31:len(fecha_muerte_dep)-1].rolling(window=7).mean(),'r')
plt.title('Muertes COVID-19 en '+depto+' último mes',loc='left')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.ylabel('Muertes diarias')
plt.xlabel('cadecastro.com')

plt.figure(12,figsize=(12,5))
plt.bar(fecha_sint_dep.index[len(fecha_sint_dep)-37:len(fecha_sint_dep)-7],fecha_sint_dep[len(fecha_sint_dep)-37:len(fecha_sint_dep)-7],color='blue')
plt.plot(fecha_sint_dep.index[len(fecha_sint_dep)-37:len(fecha_sint_dep)-7],fecha_sint_dep[len(fecha_sint_dep)-37:len(fecha_sint_dep)-7].rolling(window=7).mean(),'r')
plt.title('Casos por inicio de síntomas en '+depto+' último mes',loc='left')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.ylabel('Casos diarios')
plt.xlabel('cadecastro.com')

plt.figure(13,figsize=(8,5))
plt.subplot(211)
plt.fill_between(edades_casos_dep.index,edades_casos_dep['Edad'],color='blue')
plt.fill_between(edades_muerte_dep.index,edades_muerte_dep['Fecha de muerte'],color='red')
plt.title('Casos y muertes COVID-19 por edad '+depto,loc='left')
plt.grid(True,'both','both')
plt.legend(['Casos','Muertes'])
plt.xlim(1,114)
plt.ylim(0,None)
plt.subplot(212)
plt.plot(CFR_dep,'b')
plt.ylabel('Muertes/Casos')
plt.xlabel('cadecastro.com')
plt.grid(True,'both','both')
plt.legend(['CFR'])
plt.xlim(1,90)
plt.ylim(0,0.4)
