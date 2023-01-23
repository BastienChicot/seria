# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 20:40:00 2023

@author: basti
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#IMPORT DU FICHIER
data = pd.read_csv("bdd/data/data_ml.csv", sep= ";", index_col = 0)

data = data.dropna()

data.team.value_counts()

data = data.rename( columns = {
    "Cmp%" : "Cmp"})

desc = data.describe()
desc.to_csv("Sorties/base_descript.csv",sep=";")

data["FDD"] = (data["Int"]/(data.Int.quantile([0.75]).values)) - ((data["opp_Sh"]/(data.opp_Sh.quantile([0.75]).values)) + 
                                                (data["Fls"]/(data.Fls.quantile([0.75]).values)) + 
                                                (data["coup_arret"]/(data.coup_arret.quantile([0.75]).values)))

data["FDA"] = ((data["Sh"]/(data.Sh.quantile([0.75]).values)) + 
               (data["opp_fls"]/(data.opp_fls.quantile([0.75]).values)) + 
               (data["Cmp"]/(data.Cmp.quantile([0.75]).values))) - (data["Dist"]/(data.Dist.quantile([0.75]).values)) 

Att = data.groupby("team").mean("FDA").reset_index()
Att = Att[["team","FDA"]].sort_values(by = ["FDA"],ascending=False)
Att.head

Def = data.groupby("team").mean("FDD").reset_index()
Def = Def[["team","FDD"]].sort_values(by = ["FDD"],ascending=True)
Def.head


data.to_csv("bdd/data/data_temp.csv", sep= ";")

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

b = df_reg.Formation.value_counts()
b = b.reset_index()
b = b.rename(columns={"index":"Formation", "Formation":"n"})

df_reg = df_reg.merge(b, how="left", on="Formation")
df_reg = df_reg.loc[df_reg["n"] >= 100]

corr = df_reg.corr()

df_reg = df_reg.loc[df_reg["PK"] < 3]

# test = df_reg.loc[df_reg["Poss"] > 50]
# test = test.loc[test["victoire"] == 1]
# test.groupby(by=["team"]).count()
# test.team.value_counts()

# df_reg['periode'] = pd.Series(df_reg["Date"].str[0:7])
# df_reg['nb_def'] = pd.Series(df_reg["Formation"].str[0:1])
# test = df_reg.groupby(by = ["periode","nb_def"]).count().reset_index()
# test = test[["periode","nb_def","Result"]]

# test.pivot_table(values="Result", index="periode", columns="nb_def").plot()

df_reg['opp_Formation'] = pd.Categorical(df_reg['opp_Formation'])


reg = smf.logit('victoire ~ C(home) + Poss + FDD + FDA + age + Dist + SoT + diff_value + C(saison) + C(PK) + C(CrdR) + C(opp_Formation, Treatment(reference="4-5-1"))',
                  data=df_reg).fit()

reg.summary()
 
##TEST colinéarité
from statsmodels.stats.outliers_influence import variance_inflation_factor
from patsy import dmatrices

df_test = df_reg[["victoire","SoT","CrdR","FDD", "PK","home","age","FDA","Dist","diff_value","Int","saison","Formation","opp_Formation"]]

y, X = dmatrices('victoire ~ C(home) + FDD + FDA + age + Dist + SoT + diff_value + Int + C(saison) + C(PK) + C(CrdR) + C(Formation)*C(opp_Formation, Treatment(reference="4-5-1"))', 
                 df_test, return_type='dataframe')

vif = pd.DataFrame()
vif["VIF Factor"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
vif["features"] = X.columns


