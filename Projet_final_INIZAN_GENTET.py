##Imports
from os import chdir, getcwd, mkdir
import csv
from matplotlib import pyplot as plt
import math
import copy
import datetime

def humidex(temp,humidity):
    """ Fonction qui prend en argument les listes de température et d'humidité supposées de même taille et renvoie la liste des indices humidex calculés pour chacune des valeurs"""
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
    """fonction impure qui converti les données et les renvoie sous forme de matrice tridimensionnelle"""
    lignes = [] #id des lignes
    ide = [[],[],[],[],[],[],[]] #création de listes vides pour que variable[i] soit la liste des données de variable pour le ième capteur
    noise = [[],[],[],[],[],[],[]]
    temp = [[],[],[],[],[],[],[]]
    humidity = [[],[],[],[],[],[],[]]
    lum = [[],[],[],[],[],[],[]]
    co2 = [[],[],[],[],[],[],[]]
    sent_at = [[],[],[],[],[],[],[]]
    humi = [[],[],[],[],[],[],[]]
    res = [id,noise,temp,humidity,lum,co2,sent_at,humi]
    file = open(str(getcwd())+'\EIVP_KM.csv',"r") #récupère le chemin d'accès
    reader = csv.reader(file, delimiter=';') #création du curseur de lecture
    for row in reader :
        lignes.append(row)   #On récupère le csv sous forme d'une liste de liste telle que lignes[i][j] soit la valeur de la case ij
    file.close()
    for i in range(1,len(lignes)):
        ide[int(lignes[i][1])].append(i)
        noise[int(lignes[i][1])].append(float(lignes[i][2])) # pour chaque valeur, on récupère le numéro de son capteur pour l'injecter dans la bonne liste
        temp[int(lignes[i][1])].append(float(lignes[i][3]))
        humidity[int(lignes[i][1])].append(float(lignes[i][4]))
        lum[int(lignes[i][1])].append(int(lignes[i][5]))
        co2[int(lignes[i][1])].append(int(lignes[i][6]))
        sent_at[int(lignes[i][1])].append(datetime.datetime.strptime(lignes[i][7][:-6],'%Y-%m-%d %H:%M:%S')) #On enlève le fuseau horaire aux dates et on les convertie
    for j in range(1,7): #calcul de l'indice humidex
        for k in range(len(sent_at[j])):
            humi[j].append(humidex(temp[j],humidity[j]))
    return res

numdata = convert() # La matrice numérique des données est une variable globale 

def interv(s,e,c):
    """fonction qui prend en argument un numéro de capteur c et des dates de départ s et de fin e supposées ordonnées pour un intervalle d'écantillonage du capteur c"""
    lign = []
    time = []
    for i in range(len(numdata[var][c])):
        if s<=numdata[6][c][i]<=e :
            lign.append(i)
            time.append(numdata[6][c][i])
    return lign,time



##Implémentation de l'utilisation des dates.
def ask_dates(c):
    """ fonction qui prend en argument un numéro de capteur supposé correcte et qui demande à l'utilisateur un intervalle d'échantillonage et le renvoie s'il est correcte"""
    t0,tmax=numdata[6][c][0],umdata[6][c][-1]
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
    """fonction qui demande à l'utilisateur un numéro de capteur et qui le renvoie s'il est correcte"""
    cap=int(input("Capteur à utiliser :"))
    if cap in [1,2,3,4,5,6]:
        return cap
    else :
        print("Le numéro du capteur est invalide.")
        cap = ask_cap()

def ask_var():
    """fonction qui demande à l'utilisateur un nom de variable et qui renvoie, s'il est correcte, l'indice qui lui est associé dans la table de données numériséé"""
    var=str(input("Variable à utiliser : "))
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
    """fonction qui prend en argument un numéro de variable, un numéro de capteur, une date de début et une date de fin, tous supposés correcte
    et qui renvoie la valeur minimale que prend cette variable sur cet intervalle pour ce capteur"""
    ind,dates = interv(s,e,cap)
    res = numdata[var][0]
    for i in ind:
        if numdata[var][i]<res:
            res=i
    return("Minimum = "+str(res))

def maximum(var,cap,s,e):
     """fonction qui prend en argument un numéro de variable, un numéro de capteur, une date de début et une date de fin, tous supposés correcte
    et qui renvoie la valeur maximale que prend cette variable sur cet intervalle pour ce capteur"""
    ind,dates = interv(s,e,cap)
    res = numdata[var][0]
    for i in ind:
        if numdata[var][i]>res:
            res=i
    return("Maximum = "+str(res))

def moyenne(var,cap,s,e):
     """fonction qui prend en argument un numéro de variable, un numéro de capteur, une date de début et une date de fin, tous supposés correcte
    et qui renvoie la moyenne des valeurs que prend cette variable sur cet intervalle pour ce capteur"""
    ind,dates = interv(s,e,cap)
    res = 0
    for i in ind:
        res += numdata[var][i]
    return("Moyenne = "+str(res/len(numdata[var][i])))

def mediane(var,cap,s,e):
     """fonction qui prend en argument un numéro de variable, un numéro de capteur, une date de début et une date de fin, tous supposés correcte
    et qui renvoie la valeur médiane pour cette variable sur cet intervalle pour ce capteur"""
    ind,dates = interv(s,e,cap)
    L=copy.deepcopy([numdata[var][cap][i] for i in ind])
    L.sort()
    n=len(L)
    if n%2==0 :
        return (L[n//2]+L[n//2+1])/2
    else :
        return L[n//2+1]

def pvariance(var,cap,s,e):
     """fonction qui prend en argument un numéro de variable, un numéro de capteur, une date de début et une date de fin, tous supposés correcte
    et qui renvoie la valeur de la variance pour cette variable sur cet intervalle pour ce capteur"""
    ind,dates = interv(s,e,cap)
    tempo=0
    l=[numdata[var][cap][j] for j in ind]
    for i in l :
        tempo += i**2
    return (tempo/len(l)-moyenne(var,cap,s,e))


##Affichages des données statistiques d'une variable.
def displayStats():
    """fonction qui affiche les valeurs statistique pour les données demandées par l'utilisateur via les fonctions d'interface précédentes"""
    var = ask_var()
    cap = ask_cap()
    s,e=ask_dates(cap) #A chaque fois, on utilise la fonction ask_dates pour limiter les calculs à un intervalle.
    m=minimum(var,cap,s,e)
    M=maximum(var,cap,s,e)
    av=moyenne(var,cap,s,e)
    med=mediane(var,cap,s,e)
    var=pvariance(var,cap,s,e)
    print("min = "+str(m)+', max = '+str(M)+", moyenne = "+str(av)+", médiane = "+str(med)+", variance = "+str(var)+", écart-type = "+str(math.sqrt(var))+'.')
    return(m,M,av,med,var,math.sqrt(var)) #on renvoie quand même les valeurs au cas où on voudrait les utiliser dans une autre fonction

def display():
    """fonction qui affiche le graphe des données demandées par l'utilisateur via les fonctions d'interface précédentes"""
    var = ask_var()
    cap = ask_cap()
    s,e=ask_dates(cap)
    ind,dates=interv(s,e,cap)
    plt.xlabel("t")
    plt.ylabel(var)
    plt.title("Courbe de "+noms[var]+" en fonction du temps du "+str(s)+" au "+str(e))
    plt.scatter(dates,[numdata[var][cap][k] for k in ind], label="capteur "+str(cap))
    plt.legend(loc='upperleft')
    plt.show()

def effacer():
    """fonction impure qui 'nettoie' l'interface de pyplot"""
    plt.draw()

def covariance(var1,cap1,var2,cap2,s,e):
    """fonction qui prend en argument deux numéros de variable, deux numéros de capteur, une date de début et une date de fin, tous supposés correcte
    et qui renvoie la valeur de la covariance pour ces variables sur cet intervalle pour ces capteur"""
    tempo = 0
    ind,dates = interv(s,e,cap1)
    for i in ind :
        tempo += numdata[var1][cap1][i]*numdata[var2][cap2][i]
    return (tempo/len(ind)-moyenne(var1,cap1,s,e)*moyenne(var2,cap2,s,e))

noms = ["","bruit","température","humidité","luminosité","co2","","humidex"] # création d'une liste qui permet de récupérer une chaine de caractère à partir du numéro de variable

def correlation():
    """fonction qui affiche le graphe et renvoie le coefficient de corrélation linéaire entre deux variables fournies par l'utilisateur via l'interface codé par les fonction précédentes"""
    print("Premières valeurs :")
    var1=ask_var()
    cap1=ask_cap()
    print("Deuxièmes valeurs :")
    var2=ask_var()
    cap2=ask_cap()
    s,e=ask_dates(cap1)
    ind,dates=interv(s,e,cap1)
    plt.draw()
    plt.xlabel(noms[var1]+"fourni(e) par le capteur"+cap1)
    plt.ylabel(noms[var2]+"fourni(e) par le capteur"+cap2)
    plt.title(noms[var2]+" fonction de "+noms[var1])
    plt.scatter([numdata[var1][cap1][i] for i in ind],[numdata[var2][cap2][j] for j in ind],'+')
    cor = covariance(var1,cap1,var2,cap2,s,e)/(math.sqrt(pvariance(var1,cap1,s,e))*math.sqrt(pvariance(var2,cap2,s,e)))
    return "le coefficient de correlation linéaire entre "+noms[var1]+" et "+noms[var2]+" est de "+str(cor)+"."

    
def anomalie():
    """fonction qui renvoie la liste de valeurs considérées comme des anomalies et affiche le graphe de la valeur choisie en entourant en rouge les outliers."""
    var = ask_var()
    cap = ask_cap()
    numdata1=numdata.copy() #on effectue une copie de la liste "originale" numdata pour lui retirer les valeurs anormales
    anomalies=[] #création de liste vide pour y mettre les anomalies
    moment_anomalies=[] #création de liste vide pour y mettre le moment des anomalies
    i=1 #initialisation de i à 1 pour commencer à analyser la deuxième donnée, 
    # on considère la première correcte
    a=1 #le compteur "a" compte le nombre de valeur correcte
    b=0 #le compteur "b" évite le décalage entres anomalie et moment_de_l'anomalie
    if var in [1,2,3,5,6]:
        ecart_relatif=input("Ecart relatif entre 2 valeurs pour considérer que la valeur est anormale (en pourcentage):")
        while i < int(len(numdata[var][cap])):
            if (abs(numdata[var][cap][i] - numdata[var][cap][i-1])/(numdata[var][cap][i-1]+0.0001))> float(ecart_relatif): 
                #on vérifie que l'écart relatif entre 2 valeurs consécutives est inférieur à l'écart relatif
                print("anomalie trouvée à :", numdata[6][cap][i+b] ) #on affiche le moment des anomalies
                anomalies.append(numdata[var][cap][i]) #on  affecte la valeur de chaque anomalie 
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
    print ("données anormales", anomalies)
    print ("moment où ces données sont anormales", moment_anomalies)
    s,e=ask_dates(cap)
    ind,dates=interv(s,e,cap)
    plt.xlabel("t")
    plt.ylabel(noms[var])
    plt.title("Courbe de "+ noms[var] + "en fonction du temps du "+str(s)+" au "+str(e))
    plt.scatter(dates,numdata[var][cap], color='k',s=3.,label="capteur "+str(cap))
    plt.scatter(moment_anomalies,anomalies, edgecolors='r',
            facecolors='none', s =5.)
    plt.legend(loc='upperleft')
    plt.show()
    
def calculate_median(l):
    L = sorted(copy.deepcopy(l))
    n = len(L)
    if n < 1:
        return None
    if n % 2 == 0 :
        return ( L[(n-1)/2] + L[(n+1)/2] ) / 2.0
    else:
        return L[(n-1)/2]
    
def horaires():
    bruitm=[(numdata[1][1][i]+numdata[1][2][i]+numdata[1][3][i]+numdata[1][4][i]+numdata[1][5][i]+numdata[1][6][i])/6 for i in range(len(numdata[1][1]))]
    lumm=[(numdata[4][1][i]+numdata[4][2][i]+numdata[4][3][i]+numdata[4][4][i]+numdata[4][5][i]+numdata[4][6][i])/6 for i in range(len(numdata[4][1]))]
    co2m=[(numdata[5][1][i]+numdata[5][2][i]+numdata[5][3][i]+numdata[5][4][i]+numdata[5][5][i]+numdata[5][6][i])/6 for i in range(len(numdata[1][1]))]
    medbruit=calculate_median(bruitm)
    medlum=calculate_median(lumm)
    medco2=calculate_median(co2m)
    for i in range(len(bruitm)-2):
        if bruitm[i]<bruitm[i+2] and bruitm[i+2]>medbruit and lumm[i]<lumm[i+2] and lumm[i+2]>medlum and co2m[i]<co2m[i+2] and co2m[i+2]>medco2 :
            print("début de journée à environ " + str(numdata[6][1][i+2])
        elif bruitm[i]>bruitm[i+2] and bruitm[i+2]<medbruit and lumm[i]>lumm[i+2] and lumm[i+2]<medlum and co2m[i]>co2m[i+2] and co2m[i+2]<medco2 :
            print("fin de journée à environ " + str(numdata[6][1][i+2])
        else :
            print("pas d'horaires détectés")
                
