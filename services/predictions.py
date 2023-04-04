# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 17:42:00 2023

@author: basti
"""

from joblib import load
import pandas as pd
import datetime

df = pd.read_csv("bdd/data/df_all_seasons.csv", sep= ";", index_col = 0)
values = pd.read_csv("bdd/data/value_tm_serieA_23.txt", sep=";")
values["value"] = values["value"].str[1:]
values["value"] = values['value'].str.replace('m', '')
values["value"] = values['value'].str.replace(',', '.')
values["value"] = pd.to_numeric(values['value'], errors='coerce').convert_dtypes()

reg=load('model_serieA_cluster.joblib')
reg_test=load('model_serieA.joblib')

def get_df(team, opp, dom, pk = 0, crdr = 0, repos = 7):

    today = datetime.date.today()

    an = today.strftime("%Y")
    mois = today.strftime("%m")
        
    ##RECUP LIGNE EKIP
    home = df[(df["team"] == team) & (df["year"] == int(an))]
    temp = home.groupby(["team","Formation"]).count().reset_index()
    temp = temp.loc[temp["victoire"] == max(temp["victoire"])]
    home_form = temp["Formation"].values[0]
    
    ##DIFFERENCE DE VALEUR
    home_v =values[values["team"] == team]
    exte_v =values[values["team"] == opp]
    diff_v = float(home_v["value"])-float(exte_v["value"])
    
    ##SAISON
    if int(mois) < 9 or int(mois) == 12:
        sais = "reste"
    else:
        sais = "automne"
    
    if (str(opp) in home["Opponent"].unique()) and (home_form in home["Formation"].unique()):
        home = home[(home["Opponent"] == str(opp)) & (home["Formation"] == home_form)]
        home = home.groupby(["team","Formation"]).mean().reset_index()
        
    elif (str(opp) in home["Opponent"].unique()) and not (home_form in home["Formation"].unique()):
        home = home[home["Opponent"] == str(opp)]
        home = home.groupby(["team","Formation"]).mean().reset_index()
        home["Formation"] = home_form
        
    elif not (str(opp) in home["Opponent"].unique()) and (home_form in home["Formation"].unique()):
        home = home[home["Formation"] == home_form]
        home = home.groupby(["team","Formation"]).mean().reset_index()
        home["Opponent"] = str(opp)
        home["diff_value"] = diff_v
     
    else:
        home = home.groupby(["team","Formation"]).mean().reset_index()
        home["Opponent"] = str(opp)
        home["diff_value"] = diff_v
        home["Formation"] = home_form
        
    home["saison"] = sais
    home["repos"] = repos
    home["PK"] = pk
    home["CrdR"] = crdr
    home["home"] = dom
    home["Mois"] = mois

    return(home)

def get_predi(domicile, exterieur, h_pk = 0, h_crdr = 0, h_repos = 7, v_pk = 0, v_crdr = 0, v_repos = 7):
    
    home = get_df(domicile, exterieur, 1, pk = h_pk, crdr = h_crdr, repos = h_repos)
    exte = get_df(exterieur, domicile, 0, pk = v_pk, crdr = v_crdr, repos = v_repos)
    
    # df_h_1 = home[["home","Sh","Poss","score_mf_mean","FDA",
    #                  "diff_value","Att","age","SoT","saison",
    #                  "PK","CrdR","Formation","top_DM","score_df_mean","repos" ]]
    # df_v_1 = exte[["home","Sh","Poss","score_mf_mean","FDA",
    #                  "diff_value","Att","age","SoT","saison",
    #                  "PK","CrdR","Formation","top_DM","score_df_mean","repos" ]]
    # df_h_2 = home[["home","Sh","Poss","FDA","diff_value","Att","age","SoT",
    #                "saison","PK","CrdR","Formation","top_DM","cluster",
    #                "score_df_mean"
    #     ]]
    # df_v_2 = exte[["home","Sh","Poss","FDA","diff_value","Att","age","SoT",
    #                "saison","PK","CrdR","Formation","top_DM","cluster",
    #                "score_df_mean"
    #     ]]

    liste_model = [reg_test,reg]
    
    for model in liste_model:
        
        pred_home = model.predict(home)
        pred_exte = model.predict(exte)
        nul = 1 - (pred_home.values + pred_exte.values)
        print(domicile," : ",pred_home.values*100,"        ",exterieur," : ",pred_exte.values*100)
        print("Nul : ",nul*100)
        
test = get_predi("Milan", "Internazionale")

