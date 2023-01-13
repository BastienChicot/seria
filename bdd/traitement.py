# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 20:35:05 2023

@author: basti
"""

import pandas as pd
import numpy as np

#•IMPORT DU FICHIER
data = pd.read_csv("bdd/data/data_2021-2022.csv", sep= ";", index_col = 0)

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

##CREATION DE LA BASE DE ML AVEC MISE EN FORME DES VARIABLES
data_ml = data[["Result","Date","Venue","Poss","age","Formation","SoT","Dist","Cmp%","Int",
                "Fls","value","repos","opp_Formation","opp_value"]]

data_ml['Mois'] = pd.Series(data_ml["Date"].str[5:7])

data_ml['victoire'] = np.where(data_ml['Result']=='W', 1, 0)
data_ml['home'] = np.where(data_ml['Venue']=='Home', 1, 0)
data_ml["diff_value"] = data_ml["value"]-data_ml["opp_value"]
data_ml["nb_def"] = pd.Series(data_ml["Formation"].str[:1])
data_ml["nb_att"] = pd.Series(data_ml["Formation"].str[-1])

data_ml["nb_def"] = pd.to_numeric(data_ml['nb_def'], errors='coerce').convert_dtypes()
data_ml["nb_att"] = pd.to_numeric(data_ml['nb_att'], errors='coerce').convert_dtypes()

data_ml["nb_milieu"] = 10 - (data_ml["nb_def"]+data_ml["nb_att"])
# data_ml.Formation.value_counts()

corr_table = data_ml.corr()

data_ml.columns

data_ml = data_ml[["Result","Venue","Poss","age","Formation","SoT","Dist","Cmp%",
                   "Int","Fls","diff_value","repos","opp_Formation","Mois"]]
#EXPORT
data_ml.to_csv("bdd/data/data_ml.csv",sep=";")
