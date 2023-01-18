# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 20:40:48 2023

@author: basti
"""

import pandas as pd
import numpy as np

#IMPORT DU FICHIER
data = pd.read_csv("bdd/data/data_ml.csv", sep= ";", index_col = 0)

data.info()
data = data.rename(columns={"Cmp%":"Cmp"})

import statsmodels.formula.api as smf

df_reg = data.copy()
#df_reg = df_reg.loc[df_reg["team"] == "Milan"]
df_reg=df_reg.dropna()

df_reg.columns
df_reg.info()
a = df_reg.opp_Formation.value_counts()
a = a.reset_index()
a = a.rename(columns={"index":"opp_Formation", "opp_Formation":"n_form"})

df_reg = df_reg.merge(a, how="left", on="opp_Formation")
df_reg = df_reg.loc[df_reg["n_form"] >= 100]

df_reg['Penalty'] = np.where(df_reg['PK']>0, 1, 0)
df_reg['Rouge'] = np.where(df_reg['CrdR']>0, 1, 0)

corr = df_reg.corr()

df_reg = df_reg.loc[df_reg["PK"] < 3]

reg = smf.logit('victoire ~ C(home) + age + Poss + Dist + SoT + diff_value + Int + C(saison) + Sh + C(PK) + C(CrdR) + C(opp_Formation)',
                  data=df_reg).fit()

reg.summary()

##PREDICTIONS ET ERREURS
df_reg['pred']=reg.predict(df_reg)

df_reg["error"]=df_reg["victoire"]-df_reg["pred"]

np.mean(df_reg["error"])
np.std(df_reg["error"])
np.percentile(df_reg["pred"],2.5)
np.percentile(df_reg["pred"],70)

sum(df_reg["victoire"])/len(df_reg)

import matplotlib.pyplot as plt

plt.hist(df_reg["Poss"])
plt.hist(np.log(df_reg["Poss"]))

