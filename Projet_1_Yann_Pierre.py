##Imports
from os import chdir, getcwd, mkdir
import csv
from matplotlib import pyplot as plt
import math
import copy
import datetime

##Convertion du csv en données exploitables
def convert():
    lignes = [] #id des lignes
    id = []
    noise = []
    temp = []
    humidity = []
    lum = []
    co2 = []
    sent_at = []
    res = [id,noise,temp,humidity,lum,co2,sent_at]
    file = open(str(getcwd())+'\\EIVP_KM.csv',"r") #récupère le chemin d'accès
    reader = csv.reader(file, delimiter=';')
    for row in reader :
        lignes.append(row)
    file.close()
    for i in range(1,len(lignes)):
        id.append(int(lignes[i][0]))
        noise.append(float(lignes[i][1]))
        temp.append(float(lignes[i][2]))
        humidity.append(float(lignes[i][3]))
        lum.append(int(lignes[i][4]))
        co2.append(int(lignes[i][5]))
        sent_at.append(datetime.datetime.strptime(lignes[i][6][:-6],'%Y-%m-%d %H:%M:%S'))
    return res

numdata = convert() # Dans tous les cas, on convertis les données dans une liste, c'est une variable globale du script.

##Calcul des intervalles d'indices de lignes et de dates entre deux dates données
def interv(s,e):
    lign = []
    time = []
    for i in range (1335):
        if s<=numdata[6][i]<=e :
            lign.append(i)
            time.append(numdata[6][i])
    return lign,time

##Calcul de l'indice humidex avec la formule de Heinrich Gistav Magnus-Tetens
def humidex(temp,humidity):
    a = 17.27
    b = 237.7
    res = []
    def aux(t,h):
        return (a*t/(b+t+math.log(h)-2))
    for i in range(len(temp)):
        tempr=b*aux(temp[i],humidity[i])/(a-aux(temp[i],humidity[i]))
        res.append(temp[i]+0.5555*(6.11*math.exp(5417.7530*(1/273.16-1/(273.15+tempr)))-10))
    return res

### Fonctions statistiques (utilisables uniquement pour les données du projet, car les fonctions servent à l'extraction de l'intervalle demandé).
##Minimum
def min(var,s,e):
    ind,dates = interv(s,e)
    if var == 'bruit':
        res = numdata[1][0]
        for i in ind:
            if numdata[1][i]<res:
                res=i
        return res
    elif var == 'température':
        res = numdata[2][0]
        for i in ind:
            if numdata[2][i]<res:
                res=i
        return res
    elif var == 'humidité' :
        res = numdata[3][0]
        for i in ind:
            if numdata[3][i]<res:
                res=i
        return res
    elif var == 'luminosité':
        res = numdata[4][0]
        for i in ind:
            if numdata[4][i]<res:
                res=i
        return res
    elif var == 'co2':
        res = numdata[5][0]
        for i in ind:
            if numdata[5][i]<res:
                res=i
        return res
    elif var == 'humidex':
        res = numdata[5][0]
        tempo =humidex([numdata[2][i] for i in ind],[numdata[3][i] for i in ind])
        for i in ind:
            if tempo[i]<res:
                res=i
        return res
    else :
        print("Argument non valide. La variable doit figurer parmis les valeurs suivantes : 'bruit', 'température', 'humidité', 'luminosité', 'co2', 'humidex'. ")

##Maximum
def max(var,s,e):
    ind,dates = interv(s,e)
    if var == 'bruit':
        res = numdata[1][0]
        for i in ind:
            if numdata[1][i]>res:
                res=i
        return res
    elif var == 'température':
        res = numdata[2][0]
        for i in ind:
            if numdata[2][i]>res:
                res=i
        return res
    elif var == 'humidité' :
        res = numdata[3][0]
        for i in ind:
            if numdata[3][i]>res:
                res=i
        return res
    elif var == 'luminosité':
        res = numdata[4][0]
        for i in ind:
            if numdata[4][i]>res:
                res=i
        return res
    elif var == 'co2':
        res = numdata[5][0]
        for i in ind:
            if numdata[5][i]>res:
                res=i
        return res
    elif var == 'humidex':
        res = numdata[5][0]
        tempo =humidex([numdata[2][i] for i in ind],[numdata[3][i] for i in ind])
        for i in ind:
            if tempo[i]>res:
                res=i
        return res
    else :
        print("Argument non valide. La variable doit figurer parmis les valeurs suivantes : 'bruit', 'température', 'humidité', 'luminosité', 'co2', 'humidex'. ")

##Moyenne
def mean(var, s,e):
    ind,dates = interv(s,e)
    if var == 'bruit':
        res = 0
        for i in ind:
            res += numdata[1][i]
        return res/len(ind)
    elif var == 'température':
        res = 0
        for i in ind:
            res += numdata[2][i]
        return res/len(ind)
    elif var == 'humidité' :
        res = 0
        for i in ind:
            res += numdata[3][i]
        return res/len(ind)
    elif var == 'luminosité':
        res = 0
        for i in ind:
            res += numdata[4][i]
        return res/len(ind)
    elif var == 'co2':
        res = 0
        for i in ind:
            res += numdata[5][i]
        return res/len(ind)
    elif var == 'humidex':
        res = 0
        tempo = humidex([numdata[2][i] for i in ind],[numdata[3][i] for i in ind])
        for i in ind:
            res += tempo[i]
        return res/len(ind)
    else :
        print("Argument non valide. La variable doit figurer parmis les valeurs suivantes : 'bruit', 'température', 'humidité', 'luminosité', 'co2', 'humidex'. ")

##Mediane
def median(var,s,e):
    ind,dates = interv(s,e)
    if var == 'bruit':
        L=copy.deepcopy([numdata[1][i] for i in ind])
        L.sort()
        n=len(L)
        if n%2==0 :
            return (L[n//2]+L[n//2+1])/2
        else :
            return L[n//2+1]
    elif var == 'température':
        L=copy.deepcopy([numdata[2][i] for i in ind])
        L.sort(key=lambda x: x)
        n=len(L)
        if n%2==0 :
            return (L[n//2]+L[n//2+1])/2
        else :
            return L[n//2+1]
    elif var == 'humidité' :
        L=copy.deepcopy([numdata[3][i] for i in ind])
        L.sort()
        n=len(L)
        if n%2==0 :
            return (L[n//2]+L[n//2+1])/2
        else :
            return L[n//2+1]
    elif var == 'luminosité':
        L=copy.deepcopy([numdata[4][i] for i in ind])
        L.sort()
        n=len(L)
        if n%2==0 :
            return (L[n//2]+L[n//2+1])/2
        else :
            return L[n//2+1]
    elif var == 'co2':
        L=copy.deepcopy([numdata[5][i] for i in ind])
        L.sort()
        n=len(L)
        if n%2==0 :
            return (L[n//2]+L[n//2+1])/2
        else :
            return L[n//2+1]
    elif var == 'humidex':
        tempo = humidex([numdata[2][i] for i in ind],[numdata[3][i] for i in ind])
        L=copy.deepcopy(tempo)
        L.sort()
        n=len(L)
        if n%2==0 :
            return (L[n//2]+L[n//2+1])/2
        else :
            return L[n//2+1]
    else :
        print("Argument non valide. La variable doit figurer parmis les valeurs suivantes : 'bruit', 'température', 'humidité', 'luminosité', 'co2', 'humidex'. ")

##Variance
def pvariance(var,s,e):
    ind,dates = interv(s,e)
    if var == 'bruit':
        tempo=0
        l=numdata[1][ind[0]:ind[len(ind)-1]]
        for i in l :
            tempo += i**2
        return tempo/len(l)-mean(var,s,e)
    elif var == 'température':
        tempo=0
        l=numdata[2][ind[0]:ind[len(ind)-1]]
        for i in l :
            tempo += i**2
        return tempo/len(l)-mean(var,s,e)
    elif var == 'humidité' :
        tempo=0
        l=numdata[3][ind[0]:ind[len(ind)-1]]
        for i in l :
            tempo += i**2
        return tempo/len(l)-mean(var,s,e)
    elif var == 'luminosité':
        tempo=0
        l=numdata[4][ind[0]:ind[len(ind)-1]]
        for i in l :
            tempo += i**2
        return tempo/len(l)-mean(var,s,e)
    elif var == 'co2':
        tempo=0
        l=numdata[5][ind[0]:ind[len(ind)-1]]
        for i in l :
            tempo += i**2
        return tempo/len(l)-mean(var,s,e)
    elif var == 'humidex':
        hu = humidex([numdata[2][i] for i in ind],[numdata[3][i] for i in ind])
        tempo=0
        for i in hu :
            tempo += i**2
        return tempo/len(hu)-mean(var,s,e)
    else :
        print("Argument non valide. La variable doit figurer parmis les valeurs suivantes : 'bruit', 'température', 'humidité', 'luminosité', 'co2', 'humidex'. ")

t0,tmax = numdata[6][0],numdata[6][1334] # On fixe l'intervalle de validité des calculs.

##Implémentation de l'utilisation des dates.
def ask_dates():
    start=input("Date de début d'échantillonage (format AAAA-MM-JJ HH:MM:SS) : ")
    while type(start)!= datetime.datetime:
        try :
            datetime.datetime.strptime(start,'%Y-%m-%d %H:%M:%S')
        except ValueError:
            start=input("Erreur, date de début d'échantillonage(format AAAA-MM-JJ HH:MM:SS) : ")
    end=input("Date de fin d'échantillonage (format AAAA-MM-JJ HH:MM:SS) : ")
    while type(end)!= datetime.datetime:
        try :
            datetime.datetime.strptime(end,'%Y-%m-%d %H:%M:%S')
        except ValueError:
            end=input("Erreur, date de début (format AAAA-MM-JJ HH:MM:SS) : ")
    if not t0<=start<=end<=tmax: # Vérification de la validité de l'intervalle.
        print("Intervalle non valide")
        start,end = ask_dates()
    else:
        return start,end

##Affichages des données statistiques d'une variable.
def displayStats(var):
    s,e=ask_dates() #A chaque fois, on utilise la fonction ask_dates pour limiter les calculs à un intervalle.
    m=min(var,s,e)
    M=max(var,s,e)
    av=mean(var,s,e)
    med=median(var,s,e)
    var=pvariance(var,s,e)
    print("min = "+str(m)+', max = '+str(M)+", moyenne = "+str(av)+", médiane = "+str(med)+", variance = "+str(var)+", écart-type = "+str(math.sqrt(var))+'.')
    return(m,M,av,med,var,math.sqrt(var))

##Affichage de la courbe d'une variable, on pourrait la modifier pour pouvoir afficher plusieurs courbes avec un seul appel.
def display(var):
    s,e = ask_dates()
    ind,dates=interv(s,e)
    plt.draw
    if var == 'bruit':
        plt.xlabel("t")
        plt.ylabel("Bruit en dB")
        plt.title("Courbe du bruit en fonction du temps du "+str(s)+" au "+str(e))
        plt.plot(dates,[numdata[1][i] for i in ind], label="capteur 1")
        plt.plot(dates,[numdata[1][i+1335] for i in ind], label="capteur 2")
        plt.plot(dates,[numdata[1][i+2682] for i in ind], label="capteur 3")
        plt.plot(dates,[numdata[1][i+4028] for i in ind], label="capteur 4")
        plt.plot(dates,[numdata[1][i+5372] for i in ind], label="capteur 5")
        plt.legend()
        plt.show()
    elif var == 'température':
        plt.xlabel("t")
        plt.ylabel("Temperature en degre celcius")
        plt.title("Courbe de la temperature en fonction du temps du "+str(s)+" au "+str(e))
        plt.plot(dates,[numdata[2][i] for i in ind], label="capteur 1")
        plt.plot(dates,[numdata[2][i+1335] for i in ind], label="capteur 2")
        plt.plot(dates,[numdata[2][i+2682] for i in ind], label="capteur 3")
        plt.plot(dates,[numdata[2][i+4028] for i in ind], label="capteur 4")
        plt.plot(dates,[numdata[2][i+5372] for i in ind], label="capteur 5")
        plt.legend()
        plt.show()
    elif var == 'humidité' :
        plt.xlabel("t")
        plt.ylabel("Taux d'humidite")
        plt.title("Courbe du taux d humidite en fonction du temps du "+str(s)+" au "+str(e))
        plt.plot(dates,[numdata[3][i] for i in ind], label="capteur 1")
        plt.plot(dates,[numdata[3][i+1335] for i in ind], label="capteur 2")
        plt.plot(dates,[numdata[3][i+2682] for i in ind], label="capteur 3")
        plt.plot(dates,[numdata[3][i+4028] for i in ind], label="capteur 4")
        plt.plot(dates,[numdata[3][i+5372] for i in ind], label="capteur 5")
        plt.legend()
        plt.show()
    elif var == 'luminosité':
        plt.xlabel("t")
        plt.ylabel("Luminosite en lux")
        plt.title("Courbe de la luminosite en fonction du temps du "+str(s)+" au "+str(e))
        plt.plot(dates,[numdata[4][i] for i in ind], label="capteur 1")
        plt.plot(dates,[numdata[4][i+1335] for i in ind], label="capteur 2")
        plt.plot(dates,[numdata[4][i+2682] for i in ind], label="capteur 3")
        plt.plot(dates,[numdata[4][i+4028] for i in ind], label="capteur 4")
        plt.plot(dates,[numdata[4][i+5372] for i in ind], label="capteur 5")
        plt.legend()
        plt.show()
    elif var == 'co2':
        plt.xlabel("t")
        plt.ylabel("Taux de CO2 en ppm")
        plt.title("Courbe du taux de CO2 en fonction du temps du "+str(s)+" au "+str(e))
        plt.plot(dates,[numdata[5][i] for i in ind], label="capteur 1")
        plt.plot(dates,[numdata[5][i+1335] for i in ind], label="capteur 2")
        plt.plot(dates,[numdata[5][i+2682] for i in ind], label="capteur 3")
        plt.plot(dates,[numdata[5][i+4028] for i in ind], label="capteur 4")
        plt.plot(dates,[numdata[5][i+5372] for i in ind], label="capteur 5")
        plt.legend()
        plt.show()
    elif var == 'humidex':
        plt.xlabel("t")
        plt.ylabel("Indice humidex")
        plt.title("Courbe de l indice humidex en fonction du temps du "+str(s)+" au "+str(e))
        plt.plot(dates,humidex([numdata[2][i] for i in ind],[numdata[3][i] for i in ind]), label="capteur 1")
        plt.plot(dates,humidex([numdata[2][i+1335] for i in ind],[numdata[3][i+1335] for i in ind]), label="capteur 2")
        plt.plot(dates,humidex([numdata[2][i+2682] for i in ind],[numdata[3][i+2682] for i in ind]), label="capteur 3")
        plt.plot(dates,humidex([numdata[2][i+4028] for i in ind],[numdata[3][i+4028] for i in ind]), label="capteur 4")
        plt.plot(dates,humidex([numdata[2][i+5372] for i in ind],[numdata[3][i+5372] for i in ind]), label="capteur 5")
        plt.legend()
        plt.show()
    else :
        print("Argument non valide. La variable doit figurer parmis les valeurs suivantes : 'bruit', 'température', 'humidité', 'luminosité', 'co2', 'humidex'. ")






