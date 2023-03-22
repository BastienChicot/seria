# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 20:40:00 2023

@author: basti
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

opt = ""
opt2 = ""

#IMPORT DU FICHIER
data = pd.read_csv("bdd/data/data_ml_"+str(opt)+"20-21.csv", sep= ";", index_col = 0)
nb_top = pd.read_csv("bdd/data/nb_top_joueurs_20_21"+str(opt2)+".csv",sep=";", index_col = 0)
nb_top_precis = pd.read_csv("bdd/data/nb_top_joueurs_poste_precis.csv",sep=";", index_col = 0)
opp_score = pd.read_csv("bdd/data/score_dis_opp.csv",sep=";", index_col = 0)

nb_top_precis = nb_top_precis.fillna(0)
nb_top_precis = nb_top_precis.rename(
    columns = {
        "DF":"DF2",
        "DM":"DM2",
        "GK":"GK2"
        })
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

# nb_top['Squad'] = nb_top['Squad'].replace('Hellas Verona','Hellas-Verona')
# nb_top['Squad'] = nb_top['Squad'].replace('Saint-Étienne','Saint-Etienne')
# nb_top['Squad'] = nb_top['Squad'].replace('Paris S-G','Paris-Saint-Germain')

data = data.merge(nb_top, how = "left", left_on = "team", right_on = "Squad")
data = data.merge(nb_top_precis, how = "left", left_on = "team", right_on = "Squad")
data = data.merge(opp_score, how = "left", on = "Opponent")
data.to_csv("bdd/data/data_temp_2122.csv", sep= ";")

df_reg = data.copy()
#df_reg = df_reg.loc[df_reg["team"] == "Milan"]
df_reg=df_reg.dropna()

df_reg.columns
df_reg.info()
a = df_reg.opp_Formation.value_counts()
a = a.reset_index()
a = a.rename(columns={"index":"opp_Formation", "opp_Formation":"n_form"})

df_reg = df_reg.merge(a, how="left", on="opp_Formation")
df_reg = df_reg.loc[df_reg["n_form"] >= 80]

b = df_reg.Formation.value_counts()
b = b.reset_index()
b = b.rename(columns={"index":"Formation", "Formation":"n"})

df_reg = df_reg.merge(b, how="left", on="Formation")
df_reg = df_reg.loc[df_reg["n"] >= 80]

corr = df_reg.corr()

df_reg = df_reg.loc[df_reg["PK"] < 3]

df_reg["top_GK"] = 0
df_reg["top_MF"] = 0
df_reg["top_DM"] = 0
df_reg["top_DF"] = 0
df_reg["top_FW"] = 0
df_reg["top_MO"] = 0
df_reg["top_AIL"] = 0
df_reg["top_MIL"] = 0

for i in df_reg.index :
    if df_reg["GK"][i] > 0:
        df_reg["top_GK"][i] = 1
for i in df_reg.index :
    if df_reg["MF"][i] > 0:
        df_reg["top_MF"][i] = 1
for i in df_reg.index :
    if df_reg["DM"][i] > 0:
        df_reg["top_DM"][i] = 1
for i in df_reg.index :
    if df_reg["DF"][i] > 0:
        df_reg["top_DF"][i] = 1
for i in df_reg.index :
    if df_reg["FW"][i] > 0:
        df_reg["top_FW"][i] = 1
for i in df_reg.index :
    if df_reg["MO"][i] > 0:
        df_reg["top_MO"][i] = 1
for i in df_reg.index :
    if df_reg["AIL"][i] > 0:
        df_reg["top_AIL"][i] = 1
for i in df_reg.index :
    if df_reg["MIL"][i] > 0:
        df_reg["top_MIL"][i] = 1

df_reg['nb_def'] = pd.Series(df_reg["Formation"].str[0:1])
df_reg['nb_opp_def'] = pd.Series(df_reg["opp_Formation"].str[0:1])

df_reg['nb_att'] = pd.Series(df_reg["Formation"].str[4:5])
df_reg['nb_opp_att'] = pd.Series(df_reg["opp_Formation"].str[4:5])
df_reg['nb_mil'] = pd.Series(df_reg["Formation"].str[2:3])
df_reg['nb_opp_mil'] = pd.Series(df_reg["opp_Formation"].str[2:3])

df_reg['nb_def'] = pd.to_numeric(df_reg['nb_def'], errors='coerce').convert_dtypes(int)
df_reg['nb_opp_def'] = pd.to_numeric(df_reg['nb_opp_def'], errors='coerce').convert_dtypes(int)
df_reg['nb_att'] = pd.to_numeric(df_reg['nb_att'], errors='coerce').convert_dtypes(int)
df_reg['nb_opp_att'] = pd.to_numeric(df_reg['nb_opp_att'], errors='coerce').convert_dtypes(int)
df_reg['nb_mil'] = pd.to_numeric(df_reg['nb_mil'], errors='coerce').convert_dtypes(int)
df_reg['nb_opp_mil'] = pd.to_numeric(df_reg['nb_opp_mil'], errors='coerce').convert_dtypes(int)

df_reg["diff_avant"] = df_reg["nb_att"] - df_reg["nb_opp_def"]
df_reg["diff_def"] = df_reg["nb_def"] - df_reg["nb_opp_att"]
df_reg["diff_mil"] = df_reg["nb_mil"] - df_reg["nb_opp_mil"]

df_reg["nb_def"] = df_reg["nb_def"].astype("int64")
df_reg["nb_opp_att"] = df_reg["nb_opp_att"].astype("int64")

df_reg["diff_avant"] = df_reg["diff_avant"].astype("int64")
df_reg["diff_def"] = df_reg["diff_def"].astype("int64")
df_reg["diff_mil"] = df_reg["diff_mil"].astype("int64")

df_reg["sup_def"] = 0

for i in df_reg.index :
    if df_reg["diff_def"][i] > 0:
        df_reg["sup_def"][i] = 1

df_reg["diff_def"].value_counts()
df_reg.info()

df_reg['opp_Formation'] = pd.Categorical(df_reg['opp_Formation'])

df_reg.to_csv("bdd/data/df_reg.csv", sep= ";")
 


