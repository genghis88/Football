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

#print allPlayers
#print playersMap

def pagerank(prob,players,pageRank):
  for player in players:
    if player in playersMap:
      #calculate pagerank of player
      total = 0
      for p in playersMap:
        if p in allPlayers and p != player:
          numerator = 0
          denominator = 0
          passesToPlayer = allPlayers[p]
          if player in passesToPlayer:
            numerator = passesToPlayer[player]
            for a in passesToPlayer:
              if a in playersMap:
                denominator += passesToPlayer[a]
            total += numerator * 1.0/denominator * pageRank[p]
      pageRank[player] = total
  return pageRank

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
        totalTo += (1.0 / passesToPlayer[player])
        
  return (10 / (w * totalFrom + (1.0 - w) * totalTo))
  
for player in allPlayers:
  if player in playersMap:
    print str(playersMap[player]) + ' ' + str(closeness(player,0.5))
    
pageRank = {}
for a in allPlayers:
  if a in playersMap:
    pageRank[a] = 1
    
prob = 0.5
for i in range(1,11):
  pageRank = pagerank(prob,allPlayers,pageRank)
  
print pageRank

for p in pageRank:
  print playersMap[p] + ' ' + str(pageRank[p])
  

passStrings = []
passString = []
for index, row in df.iterrows():
  if int(row['Passer']) > 0:
    if len(passString) == 0:
      passString.append(int(row['Passer']))
    if int(row['Rec']) > 0:
      passString.append(int(row['Rec']))
    else:
      passStrings.append(passString)
      passString = []
      
print passStrings

def mapTemp(passString):
  betweenCounts = {}
  for i in range(len(passString)):
    for j in range(i+2,len(passString)):
      if passString[j] == passString[i]:
        break
      for k in range(i+1,j-1):
        if passString[k] in betweenCounts:
          betweenCounts[passString[k]][str(passString[i])+'-'+str(passString[j])] += 1
        else:
          tempDict = collections.defaultdict(int)
          tempDict[str(passString[i])+'-'+str(passString[j])] = 1
          betweenCounts[passString[k]] = tempDict
  return betweenCounts

#print mapTemp(passStrings[0])
finalBetweenCounts = {}
for passString in passStrings:
  betweenCounts = mapTemp(passString)
  for player in betweenCounts:
    if player in finalBetweenCounts:
      for key in betweenCounts[player]:
        finalBetweenCounts[player][key] += betweenCounts[player][key]
    else:
      tempDict = betweenCounts[player]
      finalBetweenCounts[player] = tempDict
      
#print finalBetweenCounts

def betweenness(player):
  numerator = 0
  denominator = 0
  betweenValue = 0
  if player in finalBetweenCounts:
    betweenCounts = finalBetweenCounts[player]
    for path in betweenCounts:
      numerator = betweenCounts[path]
      for p in finalBetweenCounts:
        tempBetweenCounts = finalBetweenCounts[p]
        denominator += tempBetweenCounts[path]
      betweenValue += (numerator * 1.0) / denominator
  return betweenValue
  
for player in finalBetweenCounts:
  print playersMap[player] + ' ' + str(betweenness(player))