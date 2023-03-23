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

df_reg = pd.read_csv("bdd/data/df_reg_21_22.csv", sep= ";", index_col = 0)
# df_reg["age"] = df_reg["age"].str.replace(',', '.')
# df_reg["age"] = df_reg["age"].astype(float)

corr = df_reg.corr()
corr.to_csv("Sorties/corr.csv", sep= ";")
df_reg.columns

liste_var = ["home","Formation","opp_Formation","saison",
             "PK","CrdR","top_GK","top_MF","top_DM","top_DF",
             "top_FW","diff_avant","diff_def","diff_mil","sup_def",
             "top_MIL","top_AIL","top_MO"]

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
                         + C(PK) + C(CrdR) + C(Formation)*C(top_DM)\
                             + score_df_mean + \
                                 repos ',
                  data=df_reg).fit()

reg_test.summary()

df_20_21 = pd.read_csv("bdd/data/df_reg.csv", sep= ";", index_col = 0)

res = df_20_21[["victoire"]]

df_20_21 = df_20_21[["home","Sh","Poss","score_mf_mean","FDA",
                     "diff_value","Att","age","SoT","saison",
                     "PK","CrdR","Formation","top_DM","score_df_mean","repos" ]]

df_20_21["age"] = df_20_21['age'].str.replace(',', '.')
df_20_21["age"] = df_20_21["age"].astype(float)

df_20_21["y_pred"] = reg_test.predict(df_20_21)

res = res.merge(df_20_21,  left_index=True, right_index=True)
res=res[["victoire","y_pred"]]

res["diff"] = abs(res["y_pred"]-res["victoire"])
res["dif_pred"] = res["victoire"] - res["y_pred"]
res["dif_vic"] = res["y_pred"] - res["victoire"]
res["dif_moy"] = res["victoire"] - np.mean(res["victoire"])

res.describe()
r_car = sum(res["dif_pred"]**2)/sum(res["dif_moy"]**2)

1-r_car

bias = sum(res["dif_vic"])/len(res)

MAE = sum(res["diff"])/len(res)

RMSE = (sum(res["dif_vic"]**2)/len(res))**(1/2)

import seaborn as sns

sns.displot(data=res, x="diff", kind="kde")

res.to_csv("bdd/data/res_20_21.csv")
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


### BOX PLOT
import matplotlib.pyplot as plt

liste_poste = ["score_mo_mean","score_mil_mean","score_ail_mean"]

for poste in liste_poste :
    temp = df_reg.boxplot(by = "opp_Formation", column =[poste])
    plot = temp.get_figure()
    plot.savefig("Sorties/opp_Formation_"+str(poste)+".png")

for poste in liste_poste :  
    temp = df_reg.loc[df_reg[poste]>0]
    x = int(max(temp[poste]) - min(temp[poste])) * 10 
    plt.hist(np.log(temp[poste]), bins = x)
    plt.savefig("Sorties/hist_log_"+str(poste)+".png")
    plt.cla()
