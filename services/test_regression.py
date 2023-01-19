# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 20:40:48 2023

@author: basti
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

# test = df_reg.loc[df_reg["Poss"] > 50]
# test = test.loc[test["victoire"] == 1]
# test.groupby(by=["team"]).count()
# test.team.value_counts()

df_reg['periode'] = pd.Series(df_reg["Date"].str[0:7])
df_reg['nb_def'] = pd.Series(df_reg["Formation"].str[0:1])
test = df_reg.groupby(by = ["periode","nb_def"]).count().reset_index()
test = test[["periode","nb_def","Result"]]

test.pivot_table(values="Result", index="periode", columns="nb_def").plot()

reg = smf.logit('not_lose ~ C(home) + age + Poss + Dist + SoT + diff_value + Int + C(saison) + Sh + C(PK) + C(CrdR) + C(opp_Formation)',
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

##PLOT POUR LES NP LOG
plt.hist(df_reg["Poss"])
plt.hist(np.log(df_reg["Poss"]))

