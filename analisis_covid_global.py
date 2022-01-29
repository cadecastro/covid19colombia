# -*- coding: utf-8 -*-
"""analisis_covid_global.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1R0iEHfm0vpRsDhDxxhzMK96k2-i2ii1i
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 13:27:22 2021
ANÁLISIS CIFRAS COVID-19 GLOBALES
Autor: Carlos Armando De Castro (cadecastro.com)
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
#MUERTES TOTALES:
#Importar datos de GitHub:
covid_global=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
#Retirar coordenadas:
covid_global=covid_global.drop(labels=['Lat','Long'],axis=1)
#Agrupar por país:
covid_global=covid_global.groupby(['Country/Region']).sum()
covid_global=covid_global.transpose()
#Muertes diarias:
muertes_diarias=covid_global.diff(periods=1,axis=0)
muertes_diarias.index=pd.to_datetime(muertes_diarias.index,dayfirst=False,yearfirst=False)
muertes_diarias['Mundo']=muertes_diarias.sum(axis=1)
pais=str(input('COUNTRY TO ANALYSE: '))
#CASOS CONFIRMADOS:
casos_global=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
#Retirar coordenadas:
casos_global=casos_global.drop(labels=['Lat','Long'],axis=1)
#Agrupar por país:
casos_global=casos_global.groupby(['Country/Region']).sum()
casos_global=casos_global.transpose()
#Casos diarios:
casos_diarias=casos_global.diff(periods=1,axis=0)
casos_diarias.index=pd.to_datetime(casos_diarias.index,dayfirst=False,yearfirst=False)
casos_diarias['Mundo']=casos_diarias.sum(axis=1)
#Salida resultados:
print('Confirmed cases at ',pais,'= ',np.format_float_positional(casos_diarias[pais].sum(),precision=0))
print('Reported deaths at ',pais,'= ',np.format_float_positional(muertes_diarias[pais].sum(),precision=0))
print('Case Fatality Rate at ',pais,'= ',np.format_float_positional(muertes_diarias[pais].sum()/casos_diarias[pais].sum()*100,precision=2),'%')
print('Confirmed cases World = ',np.format_float_positional(casos_diarias['Mundo'].sum(),precision=0))
print('Reported deaths Worldwide = ',np.format_float_positional(muertes_diarias['Mundo'].sum(),precision=0))
print('Case Fatality Rate Worldwide = ',np.format_float_positional(muertes_diarias['Mundo'].sum()/casos_diarias['Mundo'].sum()*100,precision=2),'%')
#POBLACIÓN MUNDIAL:
#Lectura base de datos de la ONU:
pob_mundial=pd.read_csv('https://population.un.org/wpp/Download/Files/1_Indicators%20(Standard)/CSV_FILES/WPP2019_TotalPopulationBySex.csv',
                        usecols=['Location','Variant','Time','PopTotal'])
pob_mundial['PopTotal']=1000*pob_mundial['PopTotal']
pob_mundial=pob_mundial[pob_mundial['Variant']=='Medium'].drop(columns='Variant')
pob2021=pob_mundial[pob_mundial['Time']==2021].drop(columns='Time')
pob2021=pob2021.set_index('Location')

#Comparativo mundial:
comparativo=pd.DataFrame(data=[muertes_diarias['Colombia'].sum()/pob2021['PopTotal']['Colombia'],muertes_diarias['Mexico'].sum()/pob2021['PopTotal']['Mexico'],
                               muertes_diarias['Israel'].sum()/pob2021['PopTotal']['Israel'],muertes_diarias['US'].sum()/pob2021['PopTotal']['United States of America'],
                               muertes_diarias['South Africa'].sum()/pob2021['PopTotal']['South Africa'],muertes_diarias['United Kingdom'].sum()/pob2021['PopTotal']['United Kingdom'],
                               muertes_diarias['Brazil'].sum()/pob2021['PopTotal']['Brazil'],muertes_diarias['India'].sum()/pob2021['PopTotal']['India'],
                               muertes_diarias['Nigeria'].sum()/pob2021['PopTotal']['Nigeria']],
                         index=['Colombia','México','Israel','USA','South Africa','United Kingdom','Brazil','India','Nigeria'])
comparativo=comparativo.rename(columns={0:'Deaths per capita'})
comparativo=comparativo.sort_values(by='Deaths per capita',ascending=False)
print(comparativo)

#Comparativo Latinoamérica:
comparativo_latam=pd.DataFrame(data=[muertes_diarias['Colombia'].sum()/pob2021['PopTotal']['Colombia'],muertes_diarias['Mexico'].sum()/pob2021['PopTotal']['Mexico'],
                               muertes_diarias['Argentina'].sum()/pob2021['PopTotal']['Argentina'],muertes_diarias['Peru'].sum()/pob2021['PopTotal']['Peru'],
                               muertes_diarias['Ecuador'].sum()/pob2021['PopTotal']['Ecuador'],muertes_diarias['Panama'].sum()/pob2021['PopTotal']['Panama'],
                               muertes_diarias['Brazil'].sum()/pob2021['PopTotal']['Brazil'],muertes_diarias['Chile'].sum()/pob2021['PopTotal']['Chile'],
                               muertes_diarias['Uruguay'].sum()/pob2021['PopTotal']['Uruguay'],muertes_diarias['Paraguay'].sum()/pob2021['PopTotal']['Paraguay']],
                         index=['Colombia','México','Argentina','Perú','Ecuador','Panamá','Brasil','Chile','Uruguay','Paraguay'])
comparativo_latam=comparativo_latam.rename(columns={0:'Deaths per capita'})
comparativo_latam=comparativo_latam.sort_values(by='Deaths per capita',ascending=False)
print(comparativo_latam)

#Comparativo Europa:
comparativo_eur=pd.DataFrame(data=[muertes_diarias['United Kingdom'].sum()/pob2021['PopTotal']['United Kingdom'],muertes_diarias['Germany'].sum()/pob2021['PopTotal']['Germany'],
                               muertes_diarias['France'].sum()/pob2021['PopTotal']['France'],muertes_diarias['Italy'].sum()/pob2021['PopTotal']['Italy'],
                               muertes_diarias['Austria'].sum()/pob2021['PopTotal']['Austria'],muertes_diarias['Poland'].sum()/pob2021['PopTotal']['Poland'],
                               muertes_diarias['Sweden'].sum()/pob2021['PopTotal']['Sweden'],muertes_diarias['Spain'].sum()/pob2021['PopTotal']['Spain'],
                               muertes_diarias['Greece'].sum()/pob2021['PopTotal']['Greece'],muertes_diarias['Denmark'].sum()/pob2021['PopTotal']['Denmark'],
                               muertes_diarias['Netherlands'].sum()/pob2021['PopTotal']['Netherlands'],muertes_diarias['Belgium'].sum()/pob2021['PopTotal']['Belgium']],
                         index=['United Kingdom','Germany','France','Italy','Austria','Poland','Sweden','Spain','Greece','Denmark','Netherlands','Belgium'])
comparativo_eur=comparativo_eur.rename(columns={0:'Deaths per capita'})
comparativo_eur=comparativo_eur.sort_values(by='Deaths per capita',ascending=False)
print(comparativo_eur)

#Comparativo países anglos:
comparativo_ang=pd.DataFrame(data=[muertes_diarias['United Kingdom'].sum()/pob2021['PopTotal']['United Kingdom'],muertes_diarias['US'].sum()/pob2021['PopTotal']['United States of America'],
                               muertes_diarias['Ireland'].sum()/pob2021['PopTotal']['Ireland'],muertes_diarias['Australia'].sum()/pob2021['PopTotal']['Australia'],
                               muertes_diarias['New Zealand'].sum()/pob2021['PopTotal']['New Zealand'],muertes_diarias['Canada'].sum()/pob2021['PopTotal']['Canada']],
                         index=['United Kingdom','United States','Ireland','Australia','New Zealand','Canada'])
comparativo_ang=comparativo_ang.rename(columns={0:'Deaths per capita'})
comparativo_ang=comparativo_ang.sort_values(by='Deaths per capita',ascending=False)
print(comparativo_ang)

#GRÁFICAS:
plt.figure(1,figsize=(12,6))
plt.subplot(211)
#plt.bar(casos_diarias.index,casos_diarias['Mundo'],color='blue')
plt.plot(casos_diarias.index,casos_diarias['Mundo'].rolling(window =7).mean(),'b')
plt.title('Daily COVID-19 report Worldwide')
plt.title('cadecastro.com',loc='right')
plt.ylabel('Daily Cases')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(casos_diarias.index[0],casos_diarias.index[len(casos_diarias.index)-1])
plt.legend(['Rolling average 7 days','Daily data'])
plt.subplot(212)
#plt.bar(muertes_diarias.index,muertes_diarias['Mundo'],color='blue')
plt.plot(muertes_diarias.index,muertes_diarias['Mundo'].rolling(window =7).mean(),'r')
plt.ylabel('Daily Deaths')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(muertes_diarias.index[0],muertes_diarias.index[len(muertes_diarias.index)-1])
plt.legend(['Rolling average 7 days','Daily data'])

plt.figure(2,figsize=(12,6))
plt.subplot(211)
#plt.bar(casos_diarias.index,casos_diarias[pais],color='blue')
plt.plot(casos_diarias.index,casos_diarias[pais].rolling(window =7).mean(),'b')
plt.title('Daily COVID-19 report at '+pais)
plt.title('cadecastro.com',loc='right')
plt.ylabel('Daily Cases')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(casos_diarias.index[0],casos_diarias.index[len(casos_diarias.index)-1])
plt.legend(['Rolling average 7 days','Daily data'])
plt.subplot(212)
#plt.bar(muertes_diarias.index,muertes_diarias[pais],color='blue')
plt.plot(muertes_diarias.index,muertes_diarias[pais].rolling(window =7).mean(),'r')
plt.ylabel('Daily Deaths')
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(muertes_diarias.index[0],muertes_diarias.index[len(muertes_diarias.index)-1])
plt.legend(['Rolling average 7 days','Daily data'])

plt.figure(3,figsize=(18,9))
plt.plot(muertes_diarias.index,muertes_diarias['Colombia'].rolling(window =7).mean()/pob2021['PopTotal']['Colombia'],'gold')
plt.plot(muertes_diarias.index,muertes_diarias['Mexico'].rolling(window =7).mean()/pob2021['PopTotal']['Mexico'],'b')
plt.plot(muertes_diarias.index,muertes_diarias['Israel'].rolling(window =7).mean()/pob2021['PopTotal']['Israel'],'r')
plt.plot(muertes_diarias.index,muertes_diarias['US'].rolling(window =7).mean()/pob2021['PopTotal']['United States of America'],'g')
plt.plot(muertes_diarias.index,muertes_diarias['South Africa'].rolling(window =7).mean()/pob2021['PopTotal']['South Africa'],'m')
plt.plot(muertes_diarias.index,muertes_diarias['United Kingdom'].rolling(window =7).mean()/pob2021['PopTotal']['United Kingdom'],'c')
plt.plot(muertes_diarias.index,muertes_diarias['Brazil'].rolling(window =7).mean()/pob2021['PopTotal']['Brazil'],'lime')
plt.plot(muertes_diarias.index,muertes_diarias['India'].rolling(window =7).mean()/pob2021['PopTotal']['India'],'brown')
plt.plot(muertes_diarias.index,muertes_diarias['Canada'].rolling(window =7).mean()/pob2021['PopTotal']['Canada'],'k')
plt.title('Daily COVID-19 Deaths per Capita',size=15)
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Daily Deaths per Capita')
plt.xlabel('Data source: CSSEGISandData/COVID-19 & https://population.un.org/',size=8)
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(muertes_diarias.index[0],muertes_diarias.index[len(muertes_diarias.index)-1])
plt.legend(['Colombia','México','Israel','USA','South Africa','United Kingdom','Brazil','India','Canada'])

plt.figure(4,figsize=(18,9))
plt.plot(muertes_diarias.index,muertes_diarias['Colombia'].rolling(window =7).mean()/pob2021['PopTotal']['Colombia'],'gold')
plt.plot(muertes_diarias.index,muertes_diarias['Mexico'].rolling(window =7).mean()/pob2021['PopTotal']['Mexico'],'b')
plt.plot(muertes_diarias.index,muertes_diarias['Argentina'].rolling(window =7).mean()/pob2021['PopTotal']['Argentina'],'r')
plt.plot(muertes_diarias.index,muertes_diarias['Ecuador'].rolling(window =7).mean()/pob2021['PopTotal']['Ecuador'],'g')
plt.plot(muertes_diarias.index,muertes_diarias['Peru'].rolling(window =7).mean()/pob2021['PopTotal']['Peru'],'m')
plt.plot(muertes_diarias.index,muertes_diarias['Chile'].rolling(window =7).mean()/pob2021['PopTotal']['Chile'],'c')
plt.plot(muertes_diarias.index,muertes_diarias['Brazil'].rolling(window =7).mean()/pob2021['PopTotal']['Brazil'],'lime')
plt.plot(muertes_diarias.index,muertes_diarias['Panama'].rolling(window =7).mean()/pob2021['PopTotal']['Panama'],'brown')
plt.plot(muertes_diarias.index,muertes_diarias['Uruguay'].rolling(window =7).mean()/pob2021['PopTotal']['Uruguay'],'k')
plt.plot(muertes_diarias.index,muertes_diarias['Paraguay'].rolling(window =7).mean()/pob2021['PopTotal']['Paraguay'],'grey')
plt.title('Daily COVID-19 Deaths per Capita Latin America',size=15)
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Daily Deaths per Capita')
plt.xlabel('Data source: CSSEGISandData/COVID-19 & https://population.un.org/',size=8)
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(muertes_diarias.index[0],muertes_diarias.index[len(muertes_diarias.index)-1])
plt.legend(['Colombia','México','Argentina','Ecuador','Perú','Chile','Brasil','Panamá','Uruguay','Paraguay'])

plt.figure(5,figsize=(18,9))
plt.plot(muertes_diarias.index,muertes_diarias['United Kingdom'].rolling(window =7).mean()/pob2021['PopTotal']['United Kingdom'],'gold')
plt.plot(muertes_diarias.index,muertes_diarias['Germany'].rolling(window =7).mean()/pob2021['PopTotal']['Germany'],'b')
plt.plot(muertes_diarias.index,muertes_diarias['France'].rolling(window =7).mean()/pob2021['PopTotal']['France'],'r')
plt.plot(muertes_diarias.index,muertes_diarias['Spain'].rolling(window =7).mean()/pob2021['PopTotal']['Spain'],'g')
plt.plot(muertes_diarias.index,muertes_diarias['Greece'].rolling(window =7).mean()/pob2021['PopTotal']['Greece'],'m')
plt.plot(muertes_diarias.index,muertes_diarias['Denmark'].rolling(window =7).mean()/pob2021['PopTotal']['Denmark'],'c')
plt.plot(muertes_diarias.index,muertes_diarias['Netherlands'].rolling(window =7).mean()/pob2021['PopTotal']['Netherlands'],'lime')
plt.plot(muertes_diarias.index,muertes_diarias['Belgium'].rolling(window =7).mean()/pob2021['PopTotal']['Belgium'],'brown')
plt.plot(muertes_diarias.index,muertes_diarias['Italy'].rolling(window =7).mean()/pob2021['PopTotal']['Italy'],'k')
plt.plot(muertes_diarias.index,muertes_diarias['Poland'].rolling(window =7).mean()/pob2021['PopTotal']['Poland'],'grey')
plt.title('Daily COVID-19 Deaths per Capita Europe',size=15)
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Daily Deaths per Capita')
plt.xlabel('Data source: CSSEGISandData/COVID-19 & https://population.un.org/',size=8)
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(muertes_diarias.index[0],muertes_diarias.index[len(muertes_diarias.index)-1])
plt.legend(['UK','Germany','France','Spain','Greece','Denmark','Netherlands','Belgium','Italy','Poland'])

plt.figure(6,figsize=(18,9))
plt.plot(muertes_diarias.index,muertes_diarias['United Kingdom'].rolling(window =7).mean()/pob2021['PopTotal']['United Kingdom'],'b')
plt.plot(muertes_diarias.index,muertes_diarias['US'].rolling(window =7).mean()/pob2021['PopTotal']['United States of America'],'r')
plt.plot(muertes_diarias.index,muertes_diarias['Ireland'].rolling(window =7).mean()/pob2021['PopTotal']['Ireland'],'lime')
plt.plot(muertes_diarias.index,muertes_diarias['Australia'].rolling(window =7).mean()/pob2021['PopTotal']['Australia'],'c')
plt.plot(muertes_diarias.index,muertes_diarias['New Zealand'].rolling(window =7).mean()/pob2021['PopTotal']['New Zealand'],'m')
plt.plot(muertes_diarias.index,muertes_diarias['Canada'].rolling(window =7).mean()/pob2021['PopTotal']['Canada'],'k')
plt.title('Daily COVID-19 Deaths per Capita Anglo',size=15)
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Daily Deaths per Capita')
plt.xlabel('Data source: CSSEGISandData/COVID-19 & https://population.un.org/',size=8)
plt.grid(True,'both','both')
plt.ylim(0,None)
plt.xlim(muertes_diarias.index[0],muertes_diarias.index[len(muertes_diarias.index)-1])
plt.legend(['United Kingdom','United States','Ireland','Australia','New Zealand','Canada'])

plt.figure(7,figsize=(10,5))
plt.bar(comparativo.index,comparativo['Deaths per capita'],color='blue')
plt.title('Total COVID-19 Deaths per Capita',size=15)
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Total Deaths per Capita')
plt.xlabel('Data source: CSSEGISandData/COVID-19 & https://population.un.org/',size=8)
plt.xticks(rotation=90)
plt.grid(True,'both','both')
plt.ylim(0,None)

plt.figure(8,figsize=(12,6))
plt.bar(comparativo_latam.index,comparativo_latam['Deaths per capita'],color='blue')
plt.title('Deaths per Capita COVID-19 Latin America',size=15)
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Total Deaths per Capita')
plt.xlabel('Data source: CSSEGISandData/COVID-19 & https://population.un.org/',size=8)
plt.xticks(rotation=90)
plt.grid(True,'both','both')
plt.ylim(0,None)

plt.figure(9,figsize=(12,6))
plt.bar(comparativo_eur.index,comparativo_eur['Deaths per capita'],color='blue')
plt.title('Deaths per capita COVID-19 Europe',size=15)
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Total Deaths per Capita')
plt.xlabel('Data source: CSSEGISandData/COVID-19 & https://population.un.org/',size=8)
plt.xticks(rotation=90)
plt.grid(True,'both','both')
plt.ylim(0,None)

plt.figure(10,figsize=(12,6))
plt.bar(comparativo_ang.index,comparativo_ang['Deaths per capita'],color='blue')
plt.title('Deaths per capita COVID-19 Anglo',size=15)
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Total Deaths per Capita')
plt.xlabel('Data source: CSSEGISandData/COVID-19 & https://population.un.org/',size=8)
plt.xticks(rotation=90)
plt.grid(True,'both','both')
plt.ylim(0,None)

mov_global=pd.read_csv('https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv',usecols=['date','country_region','residential_percent_change_from_baseline'])
mov_global['date']=pd.to_datetime(mov_global['date'],yearfirst=True)
mov_medio=pd.pivot_table(data=mov_global,values='residential_percent_change_from_baseline',index='country_region',aggfunc=np.mean)

mov=pd.DataFrame(data=[mov_medio['residential_percent_change_from_baseline']['Colombia'],mov_medio['residential_percent_change_from_baseline']['Mexico'],
                             mov_medio['residential_percent_change_from_baseline']['United States'],mov_medio['residential_percent_change_from_baseline']['United Kingdom'],
                             mov_medio['residential_percent_change_from_baseline']['South Africa'],mov_medio['residential_percent_change_from_baseline']['Israel'],
                             mov_medio['residential_percent_change_from_baseline']['Brazil'],mov_medio['residential_percent_change_from_baseline']['India'],
                             mov_medio['residential_percent_change_from_baseline']['Nigeria']],
                       index=['Colombia','México','USA','United Kingdom','South Africa','Israel','Brazil','India','Nigeria'])
mov=mov.rename(columns={0:'Residential mobility average change'})
mov=mov.sort_values(by='Residential mobility average change',ascending=False)

mov_latam=pd.DataFrame(data=[mov_medio['residential_percent_change_from_baseline']['Colombia'],mov_medio['residential_percent_change_from_baseline']['Mexico'],
                             mov_medio['residential_percent_change_from_baseline']['Argentina'],mov_medio['residential_percent_change_from_baseline']['Peru'],
                             mov_medio['residential_percent_change_from_baseline']['Ecuador'],mov_medio['residential_percent_change_from_baseline']['Panama'],
                             mov_medio['residential_percent_change_from_baseline']['Brazil'],mov_medio['residential_percent_change_from_baseline']['Chile'],
                             mov_medio['residential_percent_change_from_baseline']['Uruguay'],mov_medio['residential_percent_change_from_baseline']['Paraguay']],
                       index=['Colombia','México','Argentina','Perú','Ecuador','Panamá','Brasil','Chile','Uruguay','Paraguay'])
mov_latam=mov_latam.rename(columns={0:'Residential mobility average change'})
mov_latam=mov_latam.sort_values(by='Residential mobility average change',ascending=False)

mov_eur=pd.DataFrame(data=[mov_medio['residential_percent_change_from_baseline']['Poland'],mov_medio['residential_percent_change_from_baseline']['Italy'],
                             mov_medio['residential_percent_change_from_baseline']['United Kingdom'],mov_medio['residential_percent_change_from_baseline']['France'],
                             mov_medio['residential_percent_change_from_baseline']['Greece'],mov_medio['residential_percent_change_from_baseline']['Spain'],
                             mov_medio['residential_percent_change_from_baseline']['Austria'],mov_medio['residential_percent_change_from_baseline']['Germany'],
                             mov_medio['residential_percent_change_from_baseline']['Denmark'],mov_medio['residential_percent_change_from_baseline']['Sweden'],
                           mov_medio['residential_percent_change_from_baseline']['Netherlands'],mov_medio['residential_percent_change_from_baseline']['Belgium']],
                       index=['Poland','Italy','United Kingdom','France','Greece','Spain','Austria','Germany','Denmark','Sweden','Netherlands','Belgium'])
mov_eur=mov_eur.rename(columns={0:'Residential mobility average change'})
mov_eur=mov_eur.sort_values(by='Residential mobility average change',ascending=False)

mov_ang=pd.DataFrame(data=[mov_medio['residential_percent_change_from_baseline']['United States'],mov_medio['residential_percent_change_from_baseline']['Australia'],
                             mov_medio['residential_percent_change_from_baseline']['United Kingdom'],mov_medio['residential_percent_change_from_baseline']['Ireland'],
                             mov_medio['residential_percent_change_from_baseline']['Canada'],mov_medio['residential_percent_change_from_baseline']['New Zealand']],
                       index=['United States','Australia','United Kingdom','Ireland','Canada','New Zealand'])
mov_ang=mov_ang.rename(columns={0:'Residential mobility average change'})
mov_ang=mov_ang.sort_values(by='Residential mobility average change',ascending=False)
print(mov)
print(mov_latam)
print(mov_eur)
print(mov_ang)

comparativo=pd.merge(left=comparativo,right=mov,left_index=True,right_index=True)
print(comparativo)

comparativo_latam=pd.merge(left=comparativo_latam,right=mov_latam,left_index=True,right_index=True)
print(comparativo_latam)

comparativo_eur=pd.merge(left=comparativo_eur,right=mov_eur,left_index=True,right_index=True)
print(comparativo_eur)

comparativo_ang=pd.merge(left=comparativo_ang,right=mov_ang,left_index=True,right_index=True)
print(comparativo_ang)

x=comparativo['Residential mobility average change']
y=comparativo['Deaths per capita']
correlation_matrix = np.corrcoef(x, y)
correlation_xy = correlation_matrix[0,1]
R2 = correlation_xy**2
R2=str(np.format_float_positional(R2,precision=3))
d=np.polyfit(x,y,1)
f= np.poly1d(d)
y1=f(x)
fig, ax = plt.subplots(figsize=(12,6))
plt.plot(x,y,'bo')
plt.plot(x,y1,'r')
plt.title('Deaths per capita COVID-19 vs. Residential mobility average change - R²='+R2,size=12,loc='left')
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Deaths/Population')
plt.xlabel('Residential mobility average change (%)',size=10)
plt.xticks(rotation=90)
plt.grid(True,'both','both')
plt.ylim(0,None)
for index in range(len(x)):
  ax.text(x[index], y[index], comparativo.index[index], size=10)

x=comparativo_latam['Residential mobility average change']
y=comparativo_latam['Deaths per capita']
correlation_matrix = np.corrcoef(x, y)
correlation_xy = correlation_matrix[0,1]
R2 = correlation_xy**2
R2=str(np.format_float_positional(R2,precision=3))
d=np.polyfit(x,y,1)
f= np.poly1d(d)
y1=f(x)
fig, ax = plt.subplots(figsize=(12,6))
plt.plot(x,y,'bo')
plt.plot(x,y1,'r')
plt.title('LATIN AMERICA Deaths per capita vs. Residential mobility change - R²='+R2,size=12,loc='left')
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Deaths/Population')
plt.xlabel('Residential mobility average change (%)',size=10)
plt.xticks(rotation=90)
plt.grid(True,'both','both')
plt.ylim(0,None)
for index in range(len(x)):
  ax.text(x[index], y[index], comparativo_latam.index[index], size=10)

x=comparativo_eur['Residential mobility average change']
y=comparativo_eur['Deaths per capita']
correlation_matrix = np.corrcoef(x, y)
correlation_xy = correlation_matrix[0,1]
R2 = correlation_xy**2
R2=str(np.format_float_positional(R2,precision=3))
d=np.polyfit(x,y,1)
f= np.poly1d(d)
y1=f(x)
fig, ax = plt.subplots(figsize=(12,6))
plt.plot(x,y,'bo')
plt.plot(x,y1,'r')
plt.title('EUROPE Deaths per capita vs. Residential mobility change - R²='+R2,size=12,loc='left')
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Deaths/Population')
plt.xlabel('Residential mobility average change (%)',size=10)
plt.xticks(rotation=90)
plt.grid(True,'both','both')
plt.ylim(0,None)
for index in range(len(x)):
  ax.text(x[index], y[index], comparativo_eur.index[index], size=10)

x=comparativo_ang['Residential mobility average change']
y=comparativo_ang['Deaths per capita']
correlation_matrix = np.corrcoef(x, y)
correlation_xy = correlation_matrix[0,1]
R2 = correlation_xy**2
R2=str(np.format_float_positional(R2,precision=3))
d=np.polyfit(x,y,1)
f= np.poly1d(d)
y1=f(x)
fig, ax = plt.subplots(figsize=(12,6))
plt.plot(x,y,'bo')
plt.plot(x,y1,'r')
plt.title('ANGLO Deaths per capita vs. Residential mobility change - R²='+R2,size=12,loc='left')
plt.title('cadecastro.com',size=10,loc='right')
plt.ylabel('Deaths/Population')
plt.xlabel('Residential mobility average change (%)',size=10)
plt.xticks(rotation=90)
plt.grid(True,'both','both')
plt.ylim(0,None)
for index in range(len(x)):
  ax.text(x[index], y[index], comparativo_ang.index[index], size=10)