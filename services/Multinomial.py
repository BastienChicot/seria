"""
Created on Fri Mar 31 17:11:12 2023

@author: basti
"""
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import statsmodels.api as st
from statsmodels.discrete.conditional_models import ConditionalLogit

df = pd.read_csv("bdd/data/df_all_seasons.csv",sep=";")

df.loc[(df["not_lose"] + df["victoire"] == 0), "result"] = "D" 
df.loc[(df["not_lose"] + df["victoire"] == 1), "result"] = "N" 
df.loc[(df["not_lose"] + df["victoire"] == 2), "result"] = "V" 

y = df.result

x = df[["home","Sh","Poss","FDA","diff_value","Att","age","SoT","saison",
        "PK","CrdR","Formation","top_DM","cluster","score_df_mean"]]

home = pd.get_dummies(x["home"], drop_first=True)
saison = pd.get_dummies(x["saison"], drop_first=True)
formation = pd.get_dummies(x["Formation"], drop_first=True)
cluster = pd.get_dummies(x["cluster"], drop_first=True)

x.drop(["home","saison","Formation","cluster"], axis = 1,
           inplace = True)

x = pd.concat([x,home,saison,formation,cluster],
              axis = 1)

# x = np.array(x, dtype = float)
# y = np.array(y)

mdl = st.MNLogit(y, x)
mdl_fit = mdl.fit()

mdl_fit.summary()

mdl_margeff = mdl_fit.get_margeff()
 
mdl_margeff.summary()

from joblib import dump

dump(mdl_fit, 'model_serieA_multinomial.joblib')
