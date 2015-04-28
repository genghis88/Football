# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 20:39:56 2015

@author: kumar
"""
import pandas as pd
import collections

df = pd.DataFrame.from_csv('./ned-esp.txt', sep='\t')

print df

playersMap = {1:'Iker Casillas', 2:'Raul Albiol', 3:'Gerard Pique',
4:'Carlos Marchena', 5:'Carlos Puyol', 6:'Andres Iniesta',
7:'David Villa', 8:'Xavi Hernandez', 9:'Fernando Torres',
10:'Cesc Fabregas', 11:'Joan Capdevila', 12:'Victor Valdes',
13:'Juan Mata', 14:'Xabi Alonso', 15:'Sergio Ramos',
16:'Sergio Busquets', 17:'Alvaro Arbeloa', 18:'Pedro Rodriguez',
19:'Fernando Llorente', 20:'Javi Martinez', 21:'David Silva',
22:'Jesus Navas', 23:'Jose Manuel Reina'}

allPlayers = {}

for index, row in df.iterrows():
  if int(row['Passer']) in allPlayers:
    allPlayers.get(int(row['Passer']))[int(row['Rec'])] += 1
  else:
    temp = collections.defaultdict(int)
    temp[int(row['Rec'])] += 1
    allPlayers[int(row['Passer'])] = temp

print allPlayers
print playersMap

def closeness(player,w):
  passesFromPlayer = allPlayers[player]
  totalFrom = 0
  for p in playersMap:
    if p in passesFromPlayer and p != player:
      totalFrom += (1.0 / passesFromPlayer[p])
  
  totalTo = 0
  for p in playersMap:
    if p in allPlayers and p != player:
      passesToPlayer = allPlayers[p]
      if player in passesToPlayer:
        if player in passesToPlayer:
          totalTo += (1.0 / passesToPlayer[player])
        
  return (10 / (w * totalFrom + (1.0 - w) * totalTo))
  
print str(playersMap[1]) + ' ' + str(closeness(1,0.5))