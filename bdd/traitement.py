# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 20:35:05 2023

@author: basti
"""

import pandas as pd
import re

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
                "Fls","value","opp_Formation","opp_value"]]

data_ml['Mois'] = pd.Series(data_ml["Date"].str[5:7])
# data_ml.Formation.value_counts()

#EXPORT
data_ml.to_csv("bdd/data/data_ml.csv",sep=";")
