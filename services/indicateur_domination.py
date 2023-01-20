# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 20:40:00 2023

@author: basti
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#IMPORT DU FICHIER
data = pd.read_csv("bdd/data/data_ml.csv", sep= ";", index_col = 0)

data = data.dropna()

data.team.value_counts()

desc = data.describe()
desc.to_csv("Sorties/base_descript.csv",sep=";")

data["FDD"] = (data["Int"]/(data.Int.quantile([0.75]).values)) - ((data["opp_Sh"]/(data.opp_Sh.quantile([0.75]).values)) + 
                                                (data["Fls"]/(data.Fls.quantile([0.75]).values)) + 
                                                (data["coup_arret"]/(data.coup_arret.quantile([0.75]).values)))

data["FDA"] = ((data["Sh"]/(data.Sh.quantile([0.75]).values)) + 
               (data["opp_fls"]/(data.opp_fls.quantile([0.75]).values)) + 
               (data["Poss"]/(data.Poss.quantile([0.75]).values))) - (data["Dist"]/(data.Dist.quantile([0.75]).values)) 

Att = data.groupby("team").mean("FDA").reset_index()
Att = Att[["team","FDA"]].sort_values(by = ["FDA"],ascending=False)
Att.head

Def = data.groupby("team").mean("FDD").reset_index()
Def = Def[["team","FDD"]].sort_values(by = ["FDD"],ascending=True)
Def.head


data.to_csv("bdd/data/data_temp.csv", sep= ";")
 