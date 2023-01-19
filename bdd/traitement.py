# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 20:35:05 2023

@author: basti
"""

import pandas as pd
import numpy as np

#•IMPORT DU FICHIER
data = pd.read_csv("bdd/data/data_2020-2023.csv", sep= ";", index_col = 0)

##CREATION DES ID DE L EQUIPE ADVERSE
data["key"] = data["Date"]+data["team"]+data["Opponent"]+data["Round"]+data["Comp"]

data["opp_key"] = data["Date"]+data["Opponent"]+data["team"]+data["Round"]+data["Comp"]

data["value"] = data["value"].str[1:]
data["value"] = data['value'].str.replace('m', '')
data["value"] = pd.to_numeric(data['value'], errors='coerce').convert_dtypes()

##BASE DE L EQUIPE ADVERSE
opp = data[["Formation","value","key"]]
opp = opp.rename(columns={"Formation":"opp_Formation", "value":"opp_value",
                          "key":"opp_key"})

##INTEGRATION DES DONNEES DE L ADVERSAIRE
data = data.merge(opp, how="left", on=["opp_key"])
data['victoire'] = np.where(data['Result']=='W', 1, 0)
data['not_lose'] = np.where(data['Result']!='L', 1, 0)
corr = data.corr()

##CREATION DE LA BASE DE ML AVEC MISE EN FORME DES VARIABLES
data_ml = data[["not_lose","Result","Date","Venue","Poss","age","Formation","SoT","Dist","Cmp%","Int",
                "Fls","value","repos","opp_Formation","opp_value", "team", "Sh", "PK", "CrdY", "CrdR"]]

data_ml['Mois'] = pd.Series(data_ml["Date"].str[5:7])
data_ml['Mois'] = pd.to_numeric(data_ml['Mois'], errors='coerce').convert_dtypes()

data_ml['victoire'] = np.where(data_ml['Result']=='W', 1, 0)
data_ml['home'] = np.where(data_ml['Venue']=='Home', 1, 0)
data_ml["diff_value"] = data_ml["value"]-data_ml["opp_value"]
data_ml["nb_def"] = pd.Series(data_ml["Formation"].str[:1])
data_ml["nb_att"] = pd.Series(data_ml["Formation"].str[-1])

data_ml["opp_def"] = pd.Series(data_ml["opp_Formation"].str[:1])
data_ml["opp_att"] = pd.Series(data_ml["opp_Formation"].str[-1])

data_ml["nb_def"] = pd.to_numeric(data_ml['nb_def'], errors='coerce').convert_dtypes()
data_ml["nb_att"] = pd.to_numeric(data_ml['nb_att'], errors='coerce').convert_dtypes()

data_ml["opp_def"] = pd.to_numeric(data_ml['opp_def'], errors='coerce').convert_dtypes()
data_ml["opp_att"] = pd.to_numeric(data_ml['opp_att'], errors='coerce').convert_dtypes()


data_ml["nb_milieu"] = 10 - (data_ml["nb_def"]+data_ml["nb_att"])
data_ml["opp_milieu"] = 10 - (data_ml["opp_def"]+data_ml["opp_att"])

data_ml["diff_def"] = data_ml["nb_def"] - data_ml["opp_att"]
data_ml["diff_off"] = data_ml["nb_att"] - data_ml["opp_def"]
data_ml["diff_mil"] = data_ml["nb_milieu"] - data_ml["opp_milieu"]

data_ml["saison"] = "reste"
for i in data_ml.index:
    if 9 <= data_ml["Mois"][i] < 12 :
        data_ml["saison"][i] = "automne"
    else:
        data_ml["saison"][i] = "reste"
    
for i in data_ml.index:
    data_ml["Formation"][i] = str(data_ml["nb_def"][i]) + "-" + str(data_ml["nb_milieu"][i]) + "-" + str(data_ml["nb_att"][i])
    data_ml["opp_Formation"][i] = str(data_ml["opp_def"][i]) + "-" + str(data_ml["opp_milieu"][i]) + "-" + str(data_ml["opp_att"][i])

#data_ml.saison.value_counts()

corr_table = data_ml.corr()

data_ml.columns
# test = data.loc[data["opp_Formation"] == "4-2-3-1"]
# test.Opponent.value_counts()

data_ml = data_ml[["Date","Result","victoire","not_lose","Venue","home","Poss","age","Formation","SoT","Dist","Cmp%",
                   "Int","Fls","diff_value","repos","Mois","opp_Formation","team", "saison",
                   "Sh","PK","CrdY","CrdR"]]
#EXPORT
data_ml.to_csv("bdd/data/data_ml.csv",sep=";")
