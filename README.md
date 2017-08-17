# Régression Linéaire simple et multiple

Script python de régression linéaire simple et multiple à partir d'un fichier .csv

## Commencer

La régression se passe en 2 temps :

-  "entraînement" (train.py) : permet de générer un modèle, et d'en déduire si celui-ci est correct pour la prédiction.

-  "prédiction" (prediction.py) : permet de prédire une valeur à expliquer.

### Prérequis

Pour commencer vous devez au préalable installer Numpy et scipy.
Ensuite vous devez avoir votre fichier de données .csv au même format que les exemples donnés et au même endroit que les fichiers de script.

```
|Colonne numérotation | Y | X1 ...|.... Xp |

Y : Variables à expliquées
X : Variables explicatives
```

### Tests

Testez sur les 2 exemples mis à disposition ici. Un exemple pour la régression simple (cigarette.csv) et un exemple pour la régression multiple (resistanceMat.csv).

1 - La commande pour l'entraînement est : python train.py resistanceMat.csv e

Un fichier est généré (pred.prd). Ce fichier contient les coefficients pour la prédiction (seulement si les tests ce sont bien déroulés).

2 - La commande pour la prédiction est : python prediction.py

Vous devez saisir les chiffres qu'on vous demande. Par exemple pour le fichier (resistanceMat.csv) :
```
Entrez EpaisseurX1 :
3.5
Entrez DensiteX2 :
3.9
>>>>> Estimation de : ResistanceY : 30.2665950099
```

## Auteur

* **Jérémy Cavron** - GitHub : [DBSEngineering](https://github.com/dbsengineering).

Voir aussi [portfolio](http://www.dbs.bzh/portfolio).
