# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 17:11:12 2023

@author: basti
"""
import pandas as pd

from sklearn.cluster import KMeans
from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


from statsmodels.discrete.conditional_models import ConditionalLogit

##CREATION BASE
df21 = pd.read_csv("bdd/data/df_reg.csv", sep= ";", index_col = 0)
df22 = pd.read_csv("bdd/data/df_reg_21_22.csv", sep= ";", index_col = 0)
df23 = pd.read_csv("bdd/data/df_reg_22_23.csv", sep= ";", index_col = 0)

df21 = df21[["victoire","not_lose","home","Poss","age","Formation","SoT","Dist","Cmp",
             "Int","Fls","diff_value","repos","Mois","opp_Formation","team","saison",
             "Sh","PK","CrdY","CrdR","opp_Sh","coup_arret","opp_fls","Opponent","CMP",
             "Att","FDA","FDD",'score_df_mean', 'score_mf_mean', 'score_fw_mean', 
             'score_dm_mean','score_gk_mean','top_GK','top_MF', 'top_DM', 
             'top_DF', 'top_FW']]
df22 = df22[["victoire","not_lose","home","Poss","age","Formation","SoT","Dist","Cmp",
             "Int","Fls","diff_value","repos","Mois","opp_Formation","team","saison",
             "Sh","PK","CrdY","CrdR","opp_Sh","coup_arret","opp_fls","Opponent","CMP",
             "Att","FDA","FDD",'score_df_mean', 'score_mf_mean', 'score_fw_mean', 
             'score_dm_mean','score_gk_mean','top_GK','top_MF', 'top_DM', 
             'top_DF', 'top_FW']]
df23 = df23[["victoire","not_lose","home","Poss","age","Formation","SoT","Dist","Cmp",
             "Int","Fls","diff_value","repos","Mois","opp_Formation","team","saison",
             "Sh","PK","CrdY","CrdR","opp_Sh","coup_arret","opp_fls","Opponent","CMP",
             "Att","FDA","FDD",'score_df_mean', 'score_mf_mean', 'score_fw_mean', 
             'score_dm_mean','score_gk_mean','top_GK','top_MF', 'top_DM', 
             'top_DF', 'top_FW']]

df = pd.concat([df21,df22,df23])

df = df.dropna()

moy = df.groupby(["team","Formation"]).mean().reset_index()

apparition = df.groupby("team").count().reset_index()
apparition = apparition[["team","victoire"]]
apparition = apparition.rename(columns={
    "victoire":"count"
    })

df = df.merge(apparition, how = "left")
df = df.loc[df["count"] >= 50]
##CONDITIONAL LOGIT

g = df["team"]
x = df["diff_value"]
y = df["victoire"]

formule = 'victoire ~ diff_value + Poss + C(top_DM) - 1 '

m = ConditionalLogit(endog=y, exog=x, groups=g)
model = ConditionalLogit.from_formula(formule, df,groups=df['team'])

r = m.fit()
test = model.fit()

r.summary()
test.summary()

##CLUSTERING
group = moy.copy()
group = group[['team','Formation','Poss','SoT','Dist','Fls','diff_value','CrdY',"CrdR","PK",
               "coup_arret","top_DM"]]
group = group.set_index(['team','Formation'])

x = group.values #returns a numpy array
#min_max_scaler = preprocessing.MinMaxScaler()
#x_scaled = min_max_scaler.fit_transform(x)
#d_scaled = pd.DataFrame(x_scaled)
 
#Choix du nombre de cluster
inertie = []
K_range = range(1, 20)
for k in K_range:
    model = KMeans(n_clusters=k).fit(x)
    inertie.append(model.inertia_)
    
plt.plot(K_range, inertie)
    
kmeans = KMeans(n_clusters=4, random_state=0).fit(x)
kmeans.labels_
group['cluster'] = kmeans.labels_
group.loc[group.cluster == 2].count()

group = group.reset_index()
sns.swarmplot(group.cluster,group.cluster)
