'''
Le but de ce script est de mettre en évidence les bénéfices liés à la diversification. A partir d'une liste d'entreprises
(dans notre cas, 50 entreprises du S&P500 prises au hasard), nous constitutons des portefeuilles avec [2..50] instruments,
et observons leur performance (rendement et volatilité). Les résultats sont ensuite consolidés afin de déterminer quel
est le nombre d'instruments optimal.
Les résultats sont présentés et expliqués dans notre article :
http://larevolutionpasteque.com/2018/07/26/diversification-la-cle-de-voute-de-tout-portefeuile/
'''

#importation des modules
import quandl
quandl.ApiConfig.api_key = 'YOURKEY'
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import random

#options panda
pd.set_option('display.max_row', 1000)
pd.set_option('display.max_columns', 50)

#lire une sélection de tickers, et télécharger la data avec quandl
selected = ["AET","AFL","AKAM","GOOG","ANSS","AIV","ADSK","BSX","AVGO","CHRW","CPB",
            "CB","CHD","CI","CLX","CME","DHI","EMR","EXPD","FBHS","GPC","HOG","HSY",
            "HOLX","IR","K","L","MPC","MRK","KORS","MU","MSFT","MCO","NKTR","NKE","PNC",
            "PX","SNPS","TMK","TSS","TSCO","USB","VTR","WAT","WMB","AAP","BK","DUK","FE","HAL"]
data = quandl.get_table('WIKI/PRICES', ticker = selected,
                        qopts = { 'columns': ['date', 'ticker', 'adj_close'] },
                        date = { 'gte': '2017-06-30', 'lte': '2018-06-30' }, paginate=True)

#réorganisation de la donnée
clean = data.set_index('date')
table = clean.pivot(columns='ticker')
df = pd.DataFrame(columns=['Returns', 'Volatility', 'Number of Assets'])

#initialisation des listes de résultat
port_returns = []
port_volatility = []
port_nb_assets = []

#simulations
for y in range(1000):

    #boucles avec tous les nombres d'actifs (selon la liste entrée au-dessus), et calcul des volatilités
    for i in range(len(selected)-1):
        #poids des actifs (égal pour chacun)
        weights = np.array([1/(i+2)] * (i+2))
        #calcul des statistiques
        returns_daily = table.loc[:,table.columns.to_series().sample(i+2)].pct_change()
        returns_annual = returns_daily.mean() * 250
        returns = np.dot(weights, returns_annual)
        cov_daily = returns_daily.cov()
        cov_annual = cov_daily * 250
        volatility = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))

        #sauvegarde des résultats
        port_returns.append(returns)
        port_volatility.append(volatility)
        port_nb_assets.append(i+2)

#aggrégation des résultats
results = {'Rendement': port_returns,
            'Risque': port_volatility,
            'Nombre d\'Actifs' : port_nb_assets}
df = pd.DataFrame(results)

#trouver les valeurs médianes pour chaque nombre d'actif (afin d'éliminer les valeurs incohérentes ou extrêmes)
df = df.groupby('Nombre d\'Actifs', as_index=False)[['Risque', 'Rendement']].median()

#impression des résultats
print(df)

#préparation du graphique
plt.style.use('seaborn-dark')
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["#da2525","#1dc942"])
ax = df.plot.scatter(x='Nombre d\'Actifs', y='Risque', c='Rendement',
                cmap=cmap, figsize=(15, 7), grid=True, sharex=False)
ax.set_facecolor('xkcd:white')
ax.grid(color='xkcd:light grey')
ax.set_ylim(bottom=0.08, top=0.175)
;
