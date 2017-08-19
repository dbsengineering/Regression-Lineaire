# coding: utf-8

#########################################################################
#                                                                       #
#                           prediction.py                               #
#                                                                       #
#           Test de régression simple ou multiple                       #
#           Prédiction                                                  #
#                                                                       #
#           Auteur : ................. Cavron Jérémy                    #
#           Date de création : ....... 17/08/2017                       #
#           Date de modification : ... 19/08/2017                       #
#                                                                       #
#           Portfolio : www.dbs.bzh/portfolio                           #
#########################################################################

#--- les imports ---
from os import path
from sys import argv
from sys import path as pth
import re
from collections import OrderedDict


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
    {.UNDERLINE}{.BOLD}Régression linéaire (Simple/Multiple) - Prédiction{.ENDC}{.WARNING}\n
    Copyright (c) Cavron Jérémy, 2017\n\n
    Utilisation : python prediction.py\n\n
    --------------------------------------------{.ENDC}""".format(bcolors, 
        bcolors, bcolors, bcolors, bcolors, bcolors)

# Fonction d'extraction du fichier des coefficients
def extractionCoef(fichierCoef):
    liste = []
    param = 0
    f=open(fichierCoef, "r")
    while 1:
        data=f.readline()
        if not data:
            break
        ligne = data.split(",")
        liste.append(ligne)
    return liste

def numbereval(x):
    if re.match(r"^[+-]?[0-9]+[lL]?$", x):
        if x!="" and x[-1] in "lL":
            return long(x[:-1])
        else:
            return int(x)
    elif re.match(r"^[+-]?(([0-9]+[eE][+-]?[0-9]+)|([0-9]+\.[0-9]*([eE][+-]?[0-9]+)?)|(\.[0-9]+([eE][+-]?[0-9]+)?))$", x):
        return float(x)
    else:
        return "False" #Return False en caractères brutes car problème avec le chiffre 0

# Procédure de traitement des données
def traitement(fichier):
    yt = extractionCoef(fichier) # Extraction de la liste des valeurs estmées
    lstNb = []
    i = 1
    while(len(lstNb) != len(yt)-1):
        x = numbereval(raw_input("Entrez " + str(yt[i][0]) + " : \n").strip())
        if x != "False":
            lstNb.append(float(x))
            i +=1
    predic = float(yt[0][1].replace("\n", ""))
    for i in range(1,len(yt)):
        coef = float(yt[i][1].replace("\n", ""))
        predic += coef*lstNb[i-1]
    print bcolors.OKGREEN + "Estimation de : " + str(yt[0][0]) + " : " + str(predic) + bcolors.ENDC

# Procédure principale
def main():
    print """{.OKGREEN}Régression linéaire - Prédiction{.ENDC}""".format(bcolors,bcolors)
    fichier = "pred.prd"
    if (path.exists(fichier)):
        traitement(fichier)
    else:
        print ("{.FAIL}Erreur ! Le fichier de prédicton n'existe pas à cet emplacement. \n Veuillez faire l'entraînement (train.py).{.ENDC}".format(
            bcolors, bcolors))

#--- Lancement de la procédure principale ---
if __name__ == '__main__':
    #teste si le bon nombre d'arguments est rentré
    if (len(argv) < 2):
        main()
    else:
        print(getAide())
