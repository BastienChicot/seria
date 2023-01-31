# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 21:13:30 2023

@author: basti
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#IMPORT DU FICHIER
data = pd.read_csv("bdd/data/data_ml_21_22.csv", sep= ";", index_col = 0)

df = data.dropna()

mean = df.groupby(["team"]).mean().reset_index()

mean["cmp_pct_mean"] = mean["CMP"]/mean["Att"]*100

mean = mean[["team","Dist","SoT","Fls","Sh","card","CMP"]]
comp = data[["team","Dist","SoT","Fls","Sh","card","CMP","Opponent"]]

mean = mean.rename(columns = {
    "Dist":"mean_dist",
    "SoT":"sot_mean",
    "Fls":"fls_mean",
    "Sh":"sh_mean",
    "card":"card_mean",
    "CMP":"mean_cmp"
    })

comp = comp.merge(mean, how = "left", on = ["team"])

comp["diff_dist"] = comp["Dist"] - comp["mean_dist"]
comp["diff_sot"] = comp["SoT"] - comp["sot_mean"]
comp["diff_fls"] = comp["Fls"] - comp["fls_mean"]
comp["diff_sh"] = comp["Sh"] - comp["sh_mean"]
comp["diff_card"] = comp["card"] - comp["card_mean"]
comp["diff_cmp"] = comp["CMP"] - comp["mean_cmp"]

opp_score = comp.groupby("Opponent").mean().reset_index()

opp_score = opp_score.dropna()
opp_score = opp_score[["Opponent","diff_dist","diff_sot","diff_fls","diff_sh","diff_card","diff_cmp"]]

opp_score["norm_d_dist"] = (opp_score["diff_dist"]-np.mean(opp_score["diff_dist"]))/np.std(opp_score["diff_dist"])
opp_score["norm_d_fls"] = (opp_score["diff_fls"]-np.mean(opp_score["diff_fls"]))/np.std(opp_score["diff_fls"])
opp_score["norm_d_sh"] = (opp_score["diff_sh"]-np.mean(opp_score["diff_sh"]))/np.std(opp_score["diff_sh"])
opp_score["norm_d_cmp"] = (opp_score["diff_cmp"]-np.mean(opp_score["diff_cmp"]))/np.std(opp_score["diff_cmp"])

opp_score["score_dis"]  = opp_score["norm_d_dist"] + opp_score["norm_d_fls"] - opp_score["norm_d_sh"] - opp_score["norm_d_cmp"]

opp_score = opp_score[["Opponent","score_dis"]]

opp_score.to_csv("bdd/data/score_dis_opp.csv",sep=";")