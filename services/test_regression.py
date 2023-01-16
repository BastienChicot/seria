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
df_reg.Formation.value_counts()
reg = smf.logit('victoire ~ np.log(opp_att) + np.log(opp_def) + np.log(opp_milieu) + home + np.log(age) + np.log(Poss) + SoT + np.log(Dist) + np.log(Cmp) + np.log(Int) + diff_value + C(Mois)',
                  data=df_reg).fit()

reg.summary()


