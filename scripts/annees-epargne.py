'''
Ce script permet de calculer le nombre de mois et d'années pendant lesquelles nous devons épargner pour atteindre 
l'indépendance financière, en respectant la règle des 4%, qui stipule que nous devons épargner un montant suffisant
pour n'avoir à retirer que 4% de nos économies tous les ans pour subvenir à nos besoins.
Les résultats sont présentés et expliqués dans notre article : 
http://larevolutionpasteque.com/2018/08/19/combien-dannees-economiser-pour-atteindre-lindependance-financiere/
'''
#***************************** Calcul du nombre d'année d'épargne pour atteindre le montant permettant de soutenir le TRSM *****************************

#importement des librairies nécessaires
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors

#options panda
pd.set_option('display.max_row', 1000)
pd.set_option('display.max_columns', 50)

#initialisation des variables
TRSM = 0.04
rendement = 0.05
resultat = []

#test tous les taux d'épargne
for taux_epargne in range(1,101) :
    #réinitialisation des des variables
    taux_epargne /= 100
    montant_cible = (1-taux_epargne)/((1+TRSM)**(1/12)-1)
    mois = 0
    montant_courant = taux_epargne
    #cherche le mois à partir duquel on a assez épargné :
    while montant_courant < montant_cible :
        montant_courant += taux_epargne*((1+rendement)**(1/12))**mois
        mois += 1
    #ajoute les résultats dans un array avec le bon format
    resultat.append([str(round(taux_epargne*100))+'%',mois])

#aggrégation des résults
resultats_complets = pd.DataFrame(resultat,columns=['Taux d\'épargne','Nombre de mois'])
print(resultats_complets)

#petit graphique couleur pastèque pour la route:
ax = resultats_complets.plot.bar(x='Taux d\'épargne', y='Nombre de mois', color='#e56363', figsize=(20, 7), grid=False, sharex=False)
ax.set_facecolor('xkcd:white')
ax.grid(color='xkcd:light grey')
;
