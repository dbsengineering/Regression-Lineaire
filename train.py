# coding: utf-8

#########################################################################
#																		#
#							main.py 									#
#																		#
#			Test de régression simple ou multiple 						#
#																		#
#			Auteur : ................. Cavron Jérémy					#
#			Date de création : ....... 13/08/2017						#
#			Date de modification : ... 16/08/2017						#
#																		#
#			Portfolio : www.dbs.bzh/portfolio 							#
#########################################################################

#--- les imports ---
from os import path
from sys import argv
from sys import path as pth
from csv import reader
from numpy import array as arr
from numpy import float as flt
from numpy import dot
from numpy import transpose
from numpy import linalg
from numpy import zeros
from numpy import delete
from numpy import diag
from collections import OrderedDict
from math import sqrt
from scipy.stats import f
pth.insert(0, 'outils')
from matrixop import comatrix

# --- Classe de couleurs ---
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
        self.BOLD = ''
        self.UNDERLINE = ''

# --- Fonction qui retourne le menu d'aide ---
def getAide():
    return """{.WARNING}
    --------------------------------------------\n
    {.UNDERLINE}{.BOLD}Régression linéaire (Simple/Multiple) - Entraînement{.ENDC}{.WARNING}\n
    Copyright (c) Cavron Jérémy, 2017\n\n
    Utilisation : python main.py [file] [option]\n\n
    Options : \n
        e .......... Echantillon
        p .......... Population\n

    Format du fichier csv : 

        | numéro individu | Y | X1 ... Xp |

        Séparation par ","

    --------------------------------------------{.ENDC}""".format(bcolors, 
        bcolors, bcolors, bcolors, bcolors, bcolors)

# Fonction d'extraction du fichier csv. Retourne une liste
def extractioncsv(fichiercsv):
    liste = []
    with open(fichiercsv, 'rb') as fcsv:
        lecteur = reader(fcsv, delimiter=',')
        for ligne  in lecteur:
            liste.append(ligne)
    return liste

# Fonction qui compare 2 valeurs
def compare(val1, val2):
    if val1 < val2:
        return "INF"
    if val1 > val2:
        return "SUP"
    return "EGAL"


# Procédure de traitement des données
def traitement(inputFile, option):
    moyPred = 0.5
    liste = arr(extractioncsv(inputFile)) # Extraction de la liste
    lstHead = arr(liste[0]) # Création de l'en-tête
    n = len(liste)-1 # nombre d'individus
    p = len(lstHead)-2 # nombre de paramètres

    collect = OrderedDict() # Mettre le dictionnaire par ordre
    param = 0

    # Création d'une collection de listes
    for i in lstHead:
        collect[i]=liste[1:,[param]]
        param += 1
    
    Y = collect[lstHead[1]].astype(flt) # matrice des variables réelles à expliquer

    X = zeros([n, p+1]) # Création de la matrice des paramètres explicatif

    # Initialisation de la première colonne de la matrice des paramètres à 1
    for i in range(n):
        X[i][0] = 1

    # Initialisation du reste de la matrice des paramètres avec les données collectées
    s = 1
    for j in range(2,p+2,1):
        lstTemp = collect[lstHead[j]].astype(flt)
        for k in range(n):
            X[k][s] = lstTemp[k]
        s +=1

    # Matrice transposée
    Xt = transpose(X)

    # Multiplication des matrices X et Xt
    XtX = dot(Xt,X)

    # Déterminant de la matrice
    detX = linalg.det(XtX)

    # test si le déterminant != 0
    if detX != 0:
        # Estimation des paramètres

        # Multiplication de Xt et Y
        XtY = dot(Xt,Y)
        #invXtX = linalg.inv(XtX) #Inverse de la matrice
        #comXtX = invXtX/(1/detX) 
        comXtX = comatrix(XtX,detX) # Comatrice
        coef = 1/detX*(dot(comXtX,XtY)) # Paramètres du modèle

        X = delete(X, 0, 1) #Suppression de la colonne des 1

        #Calcul valeurs estimées
        yt = zeros([n, 1]) #Estimation observée

        for i in range(n):
            m = 1
            nb = 0
            yt[i][0] = coef[0]
            while(m < coef.size):
                yt[i][0] += coef[m]*X[i][nb]
                m += 1
                nb +=1


        #Somme des carrés des écarts résiduels
        SCEr = 0
        for i in range(n):
            SCEr += abs(Y[i][0]-yt[i][0])**2

        #Variance des Ecarts residuels
        MTemp = (1/detX)*comXtX

        d = diag(MTemp) #Récupération des valeurs en diagonale

        # Ecarts-types res
        ecartCoef = zeros([coef.size,1])
        for i in range(ecartCoef.size):
            ecartCoef[i][0] = sqrt((SCEr/(n-p-1)*d[i]))

        #Somme des carrés des écarts du modèle
        SCEm = 0
        for i in range(n):
            SCEm += (yt[i][0]-Y.mean())**2

        # Somme des carrés des écarts total
        SCEt = SCEm + SCEr

        #Les carrés moyens
        CMm = SCEm/p
        CMr = SCEr/(n-p-1)
        CMt = SCEt/(n-1)

        #Coefficient de détermination R^2
        R2 = SCEm/SCEt

        print "----------------------------------"
        for i in range(coef.size):
            print "coef."+str(i)+" : ", coef[i][0], "; Ecart-Type"+str(i)+" : ", ecartCoef[i][0]
        print "----------------------------------"

        print "----------------------------------"
        print "SCEm : ",SCEm, "; ddl : ", p, "; CMm : ", CMm
        print "SCEr : ",SCEr, "; ddl : ", n-p-1, "; CMr : ", CMr
        print "SCEt : ",SCEt, "; ddl : ", n-1, "; CMt : ", CMt
        print "----------------------------------"

        choixCoul = {'INF': bcolors.FAIL, 'SUP': bcolors.OKGREEN, 'EGAL': bcolors.WARNING}
        choixMess = {'INF': "est petit. La corrélation est faible !", 'SUP': """est bon. La corrélation 
        est fiable. A vérifier.""", 'EGAL': "est égal. La corrélation est juste !"}

        couleur = choixCoul.get(compare(R2,moyPred))
        message = choixMess.get(compare(R2,moyPred))

        print "----------------------------------"
        print couleur
        print  "R2 : " + str(R2)
        print "Le coefficient de détermination " + message + bcolors.ENDC
        print "----------------------------------"

        if compare(R2,moyPred) != "INF":
            print "Test au seuil de signification Fisher à 95% sur le modèle complet : "
            borneSup = f.isf(0.05, p, (n-p-1))
            tSeuil = CMm/CMr
            print "H0 : tous les coefficients sont nuls"
            if(tSeuil > borneSup):
                print bcolors.OKGREEN + "Seuil : " , tSeuil, " > borne supérieur : ", borneSup
                print "Au moins un coefficient != 0. On rejette H0. On garde le modèle."
                print "Création du fichier des prédictions." + bcolors.ENDC

                #Création du fichier des coefficients pour la prédiction
                fichier = open("pred.prd", "w")
                for i in range(coef.size):
                    fichier.write(lstHead[i+1] + "," + str(coef[i][0])+"\n")
                fichier.close()
            else:
                print bcolors.FAIL + "Seuil : " , tSeuil, " < borne supérieur : ", borneSup
                print "Au moins un coefficient = 0. On rejette le modèle." + bcolors.ENDC
        else:
            print """{.FAIL}Traitement arrêté !{.ENDC}""".format(bcolors, bcolors) # On arrête le traitement
    else:
        print """{.FAIL}Erreur ! Déterminant = 0. 
        Matrice non inversible. Vous avez des données
        non indispensables. Veuillez éléminer les colonnes
        non indispensables{.ENDC}""".format(bcolors, bcolors)
    

# Procédure principale
def main(**kwargs):
    print """{.OKGREEN}Régression linéaire - Entraînement{.ENDC}""".format(bcolors,bcolors)
    inputFile=kwargs.get('inputFile', None)
    option=kwargs.get('option', None)
    if (path.exists(inputFile)):
        if (option == "e" or option == "p"):
            traitement(inputFile, option)
        else:
            print ("{.FAIL}Erreur ! L'option est invalide.{.ENDC}".format(bcolors, bcolors))
            print (getAide())
    else:
        print ("{.FAIL}Erreur ! Le fichier n'existe pas à cet emplacement.{.ENDC}".format(
            bcolors, bcolors))

#--- Lancement de la procédure principale ---
if __name__ == '__main__':
    #teste si le bon nombre d'arguments est rentré
    if (len(argv) == 3):
        main(inputFile = argv[1], option= argv[2])
    else:
        print(getAide())
