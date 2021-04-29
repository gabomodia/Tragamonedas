# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 12:58:14 2021

@author: Gabriel Modia Pozuelo
"""

import matplotlib.pyplot as plt
import random

EPSILON = 10         #Porcentaje de exploracion
ITERACIONES = 1000   #Cantidad de fichas a jugar
INDICES = [2,6,300]  #Coeficientes de las maquina, habra tantas maquinas como coeficientes haya

#Clase para la máquina tragamonedas
class Bandit:
    def __init__(self, probabilidad):
        self.probabilidad = probabilidad
        self.tiradas = 0
        self.premios = 0
        
    #Estira de la palanca y apunta los resultados
    def pull(self):
        self.tiradas +=1
        resultado = 1 if random.randint(0,self.probabilidad-1)==0 else 0     
        self.premios += resultado
    
    #Devuelve el valor estimado
    def calc_resultado(self):
        if self.premios ==0:
            return float('Inf')
        return self.tiradas/self.premios
    
    #Devuelve la inversa del valor estimado
    def calc_heuristica(self):
        return self.premios/self.tiradas

#Elije la siguiente tragamonedas de la que tirar
def epsilon_greedy(mejor):
    if random.randint(1,100) <= EPSILON:
        return random.randint(0,len(INDICES)-1)
    else:
        return mejor
    
#Aqui guardaremos los resultados para mostrar la gráfica
recompensa_media = []

mis_trag  = [Bandit(INDICES[i]) for i in range(len(INDICES))]

#Realizamos las tiradas siguiendo la estrategia
for i in range(ITERACIONES):
    mejor = 0
    valor = 0.0
    tiradas = 0
    premios = 0
    for j in range(len(INDICES)):
        if mis_trag[j].tiradas >0:
            result = mis_trag[j].calc_heuristica()
        else:
            result=0
        if result > valor:
            mejor = j
            valor = result
        tiradas += mis_trag[j].tiradas
        premios += mis_trag[j].premios
    
    recompensa_media.append(premios/tiradas if premios>0 else 0)
    
    siguiente = epsilon_greedy(mejor)
    mis_trag[siguiente].pull()

#Mostramos las estadísticas
for i in range(len(mis_trag)):
    print('-----------------------')
    print('Valor estimado: ' + str(mis_trag[i].calc_resultado()))
    print('valor real: ' + str(INDICES[i]))
    print('Tiradas: ' + str(mis_trag[i].tiradas))
    print('Premios: ' + str(mis_trag[i].premios))
   

#Mostramos la gráfica y la recompensa final
plt.plot(list(range(ITERACIONES)), recompensa_media)
plt.title('Evolución recompensa media')
plt.xlabel('Tiradas')
plt.ylabel('Recompensa media')
plt.show()
print('Recompensa media final: ' + str(recompensa_media[-1]))