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
# a = df_reg.couple_Formation.value_counts()
# a = a.reset_index()
# a = a.rename(columns={"index":"couple_Formation", "couple_Formation":"n_form"})

# df_reg = df_reg.merge(a, how="left", on="couple_Formation")
# df_reg = df_reg.loc[df_reg["n_form"] >= 30]

reg = smf.logit('victoire ~ home + age + Poss + SoT + Dist + Int + diff_value + C(saison) + Sh + PK + CrdR + C(opp_Formation)',
                  data=df_reg).fit()

reg.summary()


