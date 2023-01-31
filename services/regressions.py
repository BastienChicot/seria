# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 21:13:46 2023

@author: basti
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import statsmodels.formula.api as smf

df_reg = pd.read_csv("bdd/data/df_reg.csv", sep= ";", index_col = 0)

##PREMIERE REGRESSION
reg = smf.logit('victoire ~ C(home) + Poss*C(top_MF) + FDA*C(top_FW) + FDD + age + Dist + SoT + diff_value + C(saison) + C(PK) + C(CrdR) + C(diff_mil) + C(top_GK) + C(top_MF) + C(top_FW) + DF + DM + DM + C(diff_def) + ',
                  data=df_reg).fit()

reg.summary()

##SECONDE REGRESSION
reg_test = smf.logit('victoire ~ C(home) + Poss*score_mf_mean + FDA*C(top_FW) + FDD + age + Dist + SoT + diff_value + C(saison) + C(PK) + C(CrdR) + C(diff_mil) + C(diff_def) + score_df_mean + score_dm_mean + GK',
                  data=df_reg).fit()

reg_test.summary()

##TEST colinéarité
from statsmodels.stats.outliers_influence import variance_inflation_factor
from patsy import dmatrices

df_test = df_reg[["victoire","SoT","CrdR","FDD", "PK","home","age","FDA","Dist","diff_value","Int","saison","Formation","opp_Formation"]]

y, X = dmatrices('victoire ~ C(home) + FDD + FDA + age + Dist + SoT + diff_value + Int + C(saison) + C(PK) + C(CrdR) + C(Formation)*C(opp_Formation, Treatment(reference="4-5-1"))', 
                 df_test, return_type='dataframe')

vif = pd.DataFrame()
vif["VIF Factor"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
vif["features"] = X.columns