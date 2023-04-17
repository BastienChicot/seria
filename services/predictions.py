# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 17:42:00 2023

@author: basti
"""

from joblib import load
import pandas as pd
import datetime

df = pd.read_csv("bdd/data/df_all_seasons.csv", sep= ";", index_col = 0)
df.loc[(df["not_lose"] + df["victoire"] == 0), "result"] = "D" 
df.loc[(df["not_lose"] + df["victoire"] == 1), "result"] = "N" 
df.loc[(df["not_lose"] + df["victoire"] == 2), "result"] = "V"

domicile = pd.get_dummies(df["home"], drop_first=True)
saison = pd.get_dummies(df["saison"], drop_first=True)
formation = pd.get_dummies(df["Formation"], drop_first=True)
cluster = pd.get_dummies(df["cluster"], drop_first=True)

domicile = domicile.rename(
    columns = {
        1:"Domicile"
        })

cluster = cluster.rename(
    columns = {
        1:"Cluster1",
        2:"Cluster2",
        3:"Cluster3"
        })

df= pd.concat([df,domicile,saison,formation,cluster],
              axis = 1)

values = pd.read_csv("bdd/data/value_tm_serieA_23.txt", sep=";")
values["value"] = values["value"].str[1:]
values["value"] = values['value'].str.replace('m', '')
values["value"] = values['value'].str.replace(',', '.')
values["value"] = pd.to_numeric(values['value'], errors='coerce').convert_dtypes()

reg=load('model_serieA_cluster.joblib')
reg_test=load('model_serieA.joblib')
mn_logit = load('model_serieA_multinomial.joblib')

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

    x = home[["Sh","Poss","FDA","diff_value","Att","age","SoT",
            "PK","CrdR","top_DM","score_df_mean",
            "Domicile","reste","3-5-2","4-3-3","4-4-2","4-5-1",
            "Cluster1","Cluster2","Cluster3"]]
    
    x = x.iloc[:,~x.columns.duplicated()]

    return(home,x)

def get_predi(domicile, exterieur, h_pk = 0, h_crdr = 0, h_repos = 7, v_pk = 0, v_crdr = 0, v_repos = 7):
    
    home,x = get_df(domicile, exterieur, 1, pk = h_pk, crdr = h_crdr, repos = h_repos)
    exte,b = get_df(exterieur, domicile, 0, pk = v_pk, crdr = v_crdr, repos = v_repos)
    
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
    liste_nom = ["logit","logit avec cluster"]
    
    pred_mn_h = mn_logit.predict(x)
    
    pred_mn_h = pred_mn_h.rename(
        columns = {
            0:"Défaite",
            1:"Nul",
            2:"Victoire"
            })
    
    pred_mn_v = mn_logit.predict(b)

    pred_mn_v = pred_mn_v.rename(
        columns = {
            0:"Défaite",
            1:"Nul",
            2:"Victoire"
            })
    
    for i in range(len(liste_model)):
        
        model = liste_model[i]
        pred_home = model.predict(home)
        pred_exte = model.predict(exte)
        nul = 1 - (pred_home.values + pred_exte.values)
        print(liste_nom[i])
        print(domicile," : ",pred_home.values*100,"        ",exterieur," : ",pred_exte.values*100)
        print("Nul : ",nul*100)
        
    print(domicile)
    print(pred_mn_h)

    print(exterieur)
    print(pred_mn_v)

listePK = [0,1]
listecrdr = [0,1]

for i in listePK :
    for j in listecrdr:
        print("penalty : ",i)
        print("rouge : ",j)
        
        get_predi("Lazio","Juventus",h_pk=i,h_crdr = j,h_repos= 5, v_repos = 6)
        get_predi("Lazio","Juventus",v_pk=i,v_crdr = j,h_repos= 5, v_repos = 6)
                

