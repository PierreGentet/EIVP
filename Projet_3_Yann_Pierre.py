##Imports
from os import chdir, getcwd, mkdir
import csv
from matplotlib import pyplot as plt
import math
import copy
import datetime

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

##Convertion du csv en données exploitables
def convert():
    lignes = [] #id des lignes
    id = [[],[],[],[],[],[],[]]
    noise = [[],[],[],[],[],[],[]]
    temp = [[],[],[],[],[],[],[]]
    humidity = [[],[],[],[],[],[],[]]
    lum = [[],[],[],[],[],[],[]]
    co2 = [[],[],[],[],[],[],[]]
    sent_at = [[],[],[],[],[],[],[]]
    humi = [[],[],[],[],[],[],[]]
    res = [id,noise,temp,humidity,lum,co2,sent_at,humi]
    file = open('C:\Users\pierre.gentet\Desktop\COURS\ALGO\EIVP_projet_1\\EIVP_KM.csv',"r") #récupère le chemin d'accès
    reader = csv.reader(file, delimiter=';')
    for row in reader :
        lignes.append(row)
    file.close()
    for i in range(1,len(lignes)):
        id[int(lignes[i][1])].append(i)
        noise[int(lignes[i][1])].append(float(lignes[i][2]))
        temp[int(lignes[i][1])].append(float(lignes[i][3]))
        humidity[int(lignes[i][1])].append(float(lignes[i][4]))
        lum[int(lignes[i][1])].append(int(lignes[i][5]))
        co2[int(lignes[i][1])].append(int(lignes[i][6]))
        sent_at[int(lignes[i][1])].append(datetime.datetime.strptime(lignes[i][7][:-6],'%Y-%m-%d %H:%M:%S'))
    for j in range(1,7):
        for k in range(len(sent_at[j])):
            humi[j].append(humidex(temp[j],humidity[j]))
    return res

numdata = convert()

def interv(s,e,c):
    lign = []
    time = []
    for i in range(len(numdata[c])):
        if s<=numdata[6][c][i]<=e :
            lign.append(i)
            time.append(numdata[6][c])
    return lign,time


t0,tmax,t06,tmax6 = numdata[6][1][0],numdata[6][1][-1],numdata[6][6][0],numdata[6][6][-1]

##Implémentation de l'utilisation des dates.
def ask_dates(c):
        if c == 6 :
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
            if not t06<=start<=end<=tmax6: # Vérification de la validité de l'intervalle.
                print("Intervalle non valide")
                start,end = ask_dates()
            else :
                return start,end
        else :
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
                start,end = ask_dates(c)

            else:
                return start,end

def ask_cap():
    cap=input("Capteur à utiliser :")
    if cap not in [1,2,3,4,5,6]:
        print("Le numéro du capteur est invalide.")
        cap = ask_cap()
    else :
        return cap

def ask_var():
    var=input("Variable à utiliser : ")
    if var == 'bruit':
        return 1
    elif var == 'température':
        return 2
    elif var == 'humidité' :
        return 3
    elif var == 'luminosité':
        return 4
    elif var == 'co2':
        return 5
    elif var == 'humidex':
        return 6

def minimum(var,cap,s,e):
    ind,dates = interv(s,e,cap)
    res = numdata[var][0]
    for i in ind:
        if numdata[var][i]<res:
            res=i
    return("Minimum = "+str(res))

def maximum(var,cap,s,e):
    ind,dates = interv(s,e,cap)
    res = numdata[var][0]
    for i in ind:
        if numdata[var][i]>res:
            res=i
    return("Maximum = "+str(res))

def moyenne(var,cap,s,e):
    ind,dates = interv(s,e,cap)
    res = 0
    for i in ind:
        res += numdata[var][i]
    return("Moyenne = "+str(res/len(numdata[var][i])))

def mediane(var,cap,s,e):
    ind,dates = interv(s,e,cap)
    L=copy.deepcopy([numdata[var][cap][i] for i in ind])
    L.sort()
    n=len(L)
    if n%2==0 :
        return (L[n//2]+L[n//2+1])/2
    else :
        return L[n//2+1]

def pvariance(var,cap,s,e):
    ind,dates = interv(s,e,cap)
    tempo=0
    l=[numdata[var][cap][j] for j in ind]
    for i in l :
        tempo += i**2
    return (tempo/len(l)-moyenne(var,cap,s,e))


##Affichages des données statistiques d'une variable.
def displayStats():
    var = ask_var()
    cap = ask_cap()
    s,e=ask_dates(cap) #A chaque fois, on utilise la fonction ask_dates pour limiter les calculs à un intervalle.
    m=minimum(var,cap,s,e)
    M=maximum(var,cap,s,e)
    av=moyenne(var,cap,s,e)
    med=mediane(var,cap,s,e)
    var=pvariance(var,cap,s,e)
    print("min = "+str(m)+', max = '+str(M)+", moyenne = "+str(av)+", médiane = "+str(med)+", variance = "+str(var)+", écart-type = "+str(math.sqrt(var))+'.')
    return(m,M,av,med,var,math.sqrt(var))

def display():
    var = ask_var()
    cap = ask_cap()
    s,e=ask_dates(cap)
    ind,dates=interv(s,e,cap)
    plt.xlabel("t")
    plt.ylabel(var)
    plt.title("Courbe de l indice humidex en fonction du temps du "+str(s)+" au "+str(e))
    plt.plot(dates,numdata[var][cap], label="capteur "+str(cap))
    plt.show()

def effacer():
    plt.draw()

def covariance(var1,cap1,var2,cap2,s,e):
    tempo = 0
    for i in ind :
        tempo += numdata[var1][cap1][i]*numdata[var2][cap2][i]
    return (tempo/len(ind)-moyenne(var1,cap1,s,e)*moyenne(var2,cap2,s,e))

noms = ["","bruit","température","humidité","luminosité","co2","humidex"]

def correlation():
    print("Premières valeurs :")
    var1=ask_var()
    cap1=ask_cap()
    print("Deuxièmes valeurs :")
    var2=ask_var()
    cap2=ask_cap()
    s,e=ask_dates(cap1)
    ind,dates=interv(s,e,cap1)
    plt.draw()
    plt.xlabel(noms[var1])
    plt.ylabel(noms[var2])
    plt.title("Correlation entre "+noms[var1]+" et "+noms[var2]+".")
    plt.plot([numdata[var1][cap1][i] for i in ind],[numdata[var2][cap2][j] for j in ind],'+')
    cor = covariance(var1,cap1,var2,cap2,s,e)/(math.sqrt(pvariance(var1,cap1,s,e))*math.sqrt(pvariance(var2,cap2,s,e)))
    return "le coefficient de correlation linéaire entre "+noms[var1]+" et "+noms[var2]+" est de "+str(cor)+"."
def nom_var(c):
    if c == 1:
        return 'bruit'
    elif c == 2:
        return 'température'
    elif c == 3 :
        return 'humidité'
    elif c == 4:
        return 'luminosité'
    elif c == 5:
        return 'co2'
    elif c == 7:
        return 'indice humidex'
    
def anomalie():
    var = ask_var()
    cap = ask_cap()
    s,e=ask_dates(cap)
    ind,dates=interv(s,e,cap)
    numdata1=numdata.copy()
    anomalies=[] #création de liste vide pour y mettre les anomalies
    moment_anomalies=[] #création de liste vide pour y mettre le moment des anomalies
    i=1 #initialisation de i à 1 pour commencer à analyser la deuxième donnée, 
    # on considère la première correcte
    a=1 #le compteur a compte le nombre de valeur correcte
    b=0
    if var in [1,2,3,5,6]:
        ecart_relatif=input("Ecart relatif entre 2 valeurs pour considérer que la valeur est anormale (en pourcentage):")
        while i < int(len(numdata[var][cap])):
            if (abs(numdata[var][cap][i] - numdata[var][cap][i-1])/(numdata[var][cap][i-1]+0.0001))> float(ecart_relatif): 
                #on vérifie que l'écart relatif entre 2 valeurs consécutives est inférieur à l'écart relatif
                print("anomalie trouvée à :", numdata[6][cap][i+b] ) #on affiche le moment des anomalies
                anomalies.append(numdata[var][cap][i]) #on  affecte la valeurs de chaque anomalie 
                #dans la liste "anomalies"
                moment_anomalies.append(numdata[6][cap][i+b])
                del numdata1[var][cap][i] #on supprime les valeurs des anomalies dans les données
                i=i+1
                b=b+1
            else:
                i=i+1
                a=a+1
        if a==len(numdata1[var][cap]):
            print("aucune anomalie")     
    else:
        while i < int(len(numdata[var][cap])-1):
            mx = max([numdata[var][cap][i-1],numdata[var][cap][i+1]])
            mn = min([numdata[var][cap][i-1],numdata[var][cap][i+1]])
            if  (mn-35)<=numdata[var][cap][i]<=(mx+35):
                i=i+1
                a=a+1
            else :
                print("anomalie trouvée à :", numdata[6][cap][i+b] ) #on affiche le moment des anomalies
                anomalies.append(numdata[var][cap][i]) #on  affecte la valeurs de chaque anomalie 
                #dans la liste "anomalies"
                moment_anomalies.append(numdata[6][cap][i+b])
                del numdata1[var][cap][i] #on supprime les valeurs des anomalies dans les données
                i=i+1
                b=b+1
        if a==len(numdata1[var][cap]):
            print("aucune anomalie")
    print ("données correctes", numdata1[var][cap])
    print ("données annormales", anomalies)
    print ("moment où ces données sont annormales", moment_anomalies)
    plt.xlabel("t")
    plt.ylabel(noms[var])
    plt.title("Courbe de "+ str(nom_var(var)) + "en fonction du temps du "+str(s)+" au "+str(e))
    plt.scatter(dates,numdata[var][cap], color='k',s=3.,label="capteur "+str(cap))
    plt.scatter(moment_anomalies,anomalies, edgecolors='r',
            facecolors='none', s =5.)
    plt.legend(loc='upperleft')
    plt.show()

