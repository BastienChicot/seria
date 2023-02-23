# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 21:13:46 2023

@author: basti
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import statsmodels.api as sm
import statsmodels.formula.api as smf

from scipy.stats import chi2_contingency

df_reg = pd.read_csv("bdd/data/df_reg.csv", sep= ";", index_col = 0)

corr = df_reg.corr()
corr.to_csv("Sorties/corr.csv", sep= ";")
df_reg.columns

liste_var = ["home","Formation","opp_Formation","saison",
             "PK","CrdR","top_GK","top_MF","top_DM","top_DF",
             "top_FW","diff_avant","diff_def","diff_mil","sup_def"]

liste_result = []

for i in liste_var:
    for j in liste_var:
        if i == j:
            pass
        else:
            cross_temp = pd.crosstab(index=df_reg[i],columns=df_reg[j])
            ChiSqResult = chi2_contingency(cross_temp)
            result = pd.DataFrame([[i,j,ChiSqResult[1]]], columns = ["i","j","chi2"])
            liste_result.append(result)
            
table_resultat = pd.concat(liste_result)
View = table_resultat.loc[table_resultat["chi2"] < 0.01]

table_resultat.to_csv("Sorties/chisquare.csv", sep= ";")
##PREMIERE REGRESSION
# reg = smf.logit('victoire ~ C(home) + Poss*C(top_MF) + FDA*C(top_FW) + FDD + age + Dist + SoT + diff_value + C(saison) + C(PK) + C(CrdR) + C(diff_mil) + C(top_GK) + C(top_MF) + C(top_FW) + DF + DM + DM + C(diff_def) + ',
#                   data=df_reg).fit()

# reg.summary()

##SECONDE REGRESSION
reg_test = smf.logit('victoire ~ C(home)*Sh + Poss*score_mf_mean + FDA + \
                     diff_value + Att + age + SoT + C(saison) + \
                         + C(PK) + C(CrdR) + C(Formation)*C(top_FW)\
                             + score_df_mean + \
                                 repos ',
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
vif
