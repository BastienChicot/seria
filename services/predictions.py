# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 17:42:00 2023

@author: basti
"""

from joblib import load
import pandas as pd

df = pd.read_csv("bdd/data/df_all_seasons.csv", sep= ";", index_col = 0)

df = df.loc[df["year"] == "2023"]

reg=load('model_serieA_cluster.joblib')
reg_test=load('model_serieA.joblib')

