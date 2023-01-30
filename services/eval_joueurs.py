# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 21:35:28 2023

@author: basti
"""

import pandas as pd
import numpy as np

##STANDARD
standard = pd.read_csv("bdd/data/dl_fbref/stat_joueur_stand_21_22.txt", sep= ",", index_col = 0)

standard.columns = standard.iloc[0]
                         
standard = standard.reset_index()
standard = standard.loc[standard["-9999"] != "-9999"]

standard.columns
standard = standard.rename(columns = {
    "index":"Player"
    })

standard["key"] = standard["Player"] + standard["Pos"] + standard["Squad"]
#fichier de base sur lequel je vais joindre les autres

##TIRS
shots = pd.read_csv("bdd/data/dl_fbref/stat_joueur_shots_21_22.txt", sep= ",", index_col = 0)

shots = shots.reset_index()
shots["key"] = shots["Player"] + shots["Pos"] + shots["Squad"]

shots.columns

shots = shots[["Sh","SoT","SoT%","key"]]
shots = shots.rename(columns = {
    "SoT%":"SoT_pct"
    })

full = pd.merge(standard,shots, how = "inner", on = ["key"])

##PASSES
passes = pd.read_csv("bdd/data/dl_fbref/stat_joueur_pass_21_22.txt", sep= ",", index_col = 0)

passes = passes.reset_index()
passes["key"] = passes["Player"] + passes["Pos"] + passes["Squad"]

passes.columns

passes = passes[["Cmp","Att","Cmp%","key"]]
passes = passes.rename(columns = {
    "Cmp%" : "Cmp_pct"
    })

full = full.merge(passes, how = "left", on = "key")

##SHOOTING CREATING ACTION
sca = pd.read_csv("bdd/data/dl_fbref/stat_joueur_sca_21_22.txt", sep= ",", index_col = 0)

sca = sca.reset_index()
sca["key"] = sca["Player"] + sca["Pos"] + sca["Squad"]

sca.columns

sca = sca[["SCA","key"]]
full = full.merge(sca, how = "left", on = "key")


##DEFENSE
defense = pd.read_csv("bdd/data/dl_fbref/stat_joueur_def_21_22.txt", sep= ",", index_col = 0)

defense = defense.reset_index()
defense["key"] = defense["Player"] + defense["Pos"] + defense["Squad"]

defense.columns

defense = defense[["Tkl","TklW","Tkl%","Blocks","Sh","Pass","Int","Tkl+Int","Clr","Err","key"]]

defense = defense.rename(columns = {
    "Tkl%":"Tkl_pct",
    "Sh":"Sh_block"
    })

full = full.merge(defense, how = "left", on = "key")


##POSSESSION
poss = pd.read_csv("bdd/data/dl_fbref/stat_joueur_poss_21_22.txt", sep= ",", index_col = 0)

poss = poss.reset_index()
poss["key"] = poss["Player"] + poss["Pos"] + poss["Squad"]

poss.columns

poss = poss[["Touches","Succ%", "Mis","Dis","key"]]
poss = poss.rename(columns={
    "Succ%":"Drib_pct"
    })
full = full.merge(poss, how = "left", on = "key")

##MISC ATTENTION DOUBLONS DE VARIABLES
misc = pd.read_csv("bdd/data/dl_fbref/stat_joueur_misc_21_22.txt", sep= ",", index_col = 0)

misc = misc.reset_index()
misc["key"] = misc["Player"] + misc["Pos"] + misc["Squad"]

misc.columns

misc = misc[["Fls","Off","Crs","Won%","key"]]
misc = misc.rename(columns={
    "Won%":"duels_aeriens_pct"
    })

full = full.merge(misc, how = "left", on = "key")

##GARDIENS
goal = pd.read_csv("bdd/data/dl_fbref/stat_goal_stand_21_22.txt", sep= ",", index_col = 0)
                         
goal = goal.reset_index()
goal = goal.loc[goal["-9999"] != "-9999"]
goal["key"] = goal["Player"] + goal["Pos"] + goal["Squad"]

goal_adv = pd.read_csv("bdd/data/dl_fbref/stat_goal_adv_21_22.txt", sep= ",", index_col = 0)
                         
goal_adv = goal_adv.reset_index()
goal_adv["key"] = goal_adv["Player"] + goal_adv["Pos"] + goal_adv["Squad"]

goal.columns
goal_adv.columns

goal = goal[["Save%","CS%","key"]]
goal_adv = goal_adv[["Stp%","key"]]

goal = goal.merge(goal_adv, how = "left", on = "key")
goal = goal.rename(columns={
    "Save%":"Save_pct",
    "CS%":"CS_pct_goal",
    "Stp%":"Stop_pct_goal"
    })

full = full.merge(goal, how = "left", on = "key")

##DEDOUBLONNEMENT

full = full.drop_duplicates()

##REGROUPER LES POSTES

full['Squad'] = full['Squad'].replace('Inter','Internazionale')
full['Squad'] = full['Squad'].replace('Hellas Verona','Hellas-Verona')

full.Pos.value_counts()

full['Pos'] = full['Pos'].replace('MFFW','Milieu')
full['Pos'] = full['Pos'].replace('FWMF','Milieu')
full['Pos'] = full['Pos'].replace('DFMF','Milieu')
full['Pos'] = full['Pos'].replace('MFDF','Milieu')
full['Pos'] = full['Pos'].replace('FWDF','FW')
full['Pos'] = full['Pos'].replace('DFFW','Milieu')

full.Pos.value_counts()

dm = pd.read_csv("bdd/data/dl_fbref/milieu_def.txt", sep= ",")
dm["DM"]=1

full = full.merge(dm, how = "left", left_on=("Player"), right_on=("PLAYER"))
full.DM.value_counts()
full.loc[full.DM == 1, 'Pos'] = "DM"

full['Pos'] = full['Pos'].replace('Milieu','MF')

##VERIF FICHIER
lignes = full.groupby("Squad").count().reset_index()

test = full.groupby("Squad").sum().reset_index()
test = test[["Squad", "MP","Min","90s"]]
test["n"] = test["90s"]/11

team = pd.read_csv("bdd/data/data_2021-2022.csv", sep= ";", index_col = 0)
nb_match = team.groupby("team").count().reset_index()
nb_match = nb_match[["team","Date"]]

test = test.merge(nb_match, how = "left", left_on = "Squad", right_on = "team")

##CALCUL DES INDICATEURS
##Milieux
full.columns

mf = full.loc[full["Pos"] == "MF"]
mf = mf.loc[mf["90s"] >= 15]

mf["Drib_pct_rel"] = mf["Drib_pct"] / mf["90s"]
mf["Touches_rel"] = mf["Touches"] / mf["90s"]
mf["Cmp_pct_rel"] = mf["Cmp_pct"] / mf["90s"]
mf["Ast_rel"] = mf["Ast"] / mf["90s"]
mf["Gls_rel"] = mf["Gls"] / mf["90s"]
mf["SCA_rel"] = mf["SCA"] / mf["90s"]
mf["Fls_rel"] = mf["Fls"] / mf["90s"]
mf["Off_rel"] = mf["Off"] / mf["90s"]
mf["CrdY_rel"] = mf["CrdY"] / mf["90s"]

mf["score"] = ((mf["Drib_pct_rel"]/(mf.Drib_pct_rel.quantile([0.8]).values)) + 
               (mf["Touches_rel"]/(mf.Touches_rel.quantile([0.8]).values)) + 
               (mf["Cmp_pct_rel"]/(mf.Cmp_pct_rel.quantile([0.8]).values)) +
               (mf["Ast_rel"]/(mf.Ast_rel.quantile([0.8]).values)) +
               (mf["Gls_rel"]/(mf.Gls_rel.quantile([0.8]).values)) +
               (mf["SCA_rel"]/(mf.SCA_rel.quantile([0.8]).values)) 
               ) - (mf["Fls_rel"]/(mf.Fls_rel.quantile([0.8]).values) +
                    mf["Off_rel"]/(mf.Off_rel.quantile([0.8]).values) + 
                    mf["CrdY_rel"]/(mf.CrdY_rel.quantile([0.8]).values)
                    )
                    
mf = mf[["Player","score","key"]].sort_values(by = ["score"],ascending=False)
mf.head

##Défenseurs
df = full.loc[full["Pos"] == "DF"]
df = df.loc[df["90s"] >= 15]

df["Tkl_pct_rel"] = df["Tkl_pct"] / df["90s"]
df["Int_rel"] = df["Int"] / df["90s"]
df["Blocks_rel"] = df["Blocks"] / df["90s"]
df["Cmp_pct_rel"] = df["Cmp_pct"] / df["90s"]
df["Sh_block_rel"] = df["Sh_block"] / df["90s"]
df["duels_aeriens_pct_rel"] = df["duels_aeriens_pct"] / df["90s"]
df["Fls_rel"] = df["Fls"] / df["90s"]
df["CrdY_rel"] = df["CrdY"] / df["90s"]
df["CrdR_rel"] = df["CrdR"] / df["90s"]
df["Err_rel"] = df["Err"] / df["90s"]

df["score"] = ((df["Tkl_pct_rel"]/(df.Tkl_pct_rel.quantile([0.8]).values)) + 
               (df["Int_rel"]/(df.Int_rel.quantile([0.8]).values)) + 
               (df["Blocks_rel"]/(df.Blocks_rel.quantile([0.8]).values)) +
               (df["Cmp_pct_rel"]/(df.Cmp_pct_rel.quantile([0.8]).values)) +
               (df["Sh_block_rel"]/(df.Sh_block_rel.quantile([0.8]).values)) +
               (df["duels_aeriens_pct_rel"]/(df.duels_aeriens_pct_rel.quantile([0.8]).values)) 
               ) - (df["Fls_rel"]/(df.Fls_rel.quantile([0.8]).values) +
                    df["CrdR_rel"]/(df.CrdR_rel.quantile([0.8]).values) + 
                    df["Err_rel"]/(df.Err_rel.quantile([0.8]).values) + 
                    df["CrdY_rel"]/(df.CrdY_rel.quantile([0.8]).values)
                    )
                    
df = df[["Player","score","key"]].sort_values(by = ["score"],ascending=False)
df.head

##Attaquants
fw = full.loc[full["Pos"] == "FW"]
fw = fw.loc[fw["90s"] >= 15]

fw["Gls_rel"] = fw["Gls"] / fw["90s"]
fw["Drib_pct_rel"] = fw["Drib_pct"] / fw["90s"]
fw["SCA_rel"] = fw["SCA"] / fw["90s"]
fw["Cmp_pct_rel"] = fw["Cmp_pct"] / fw["90s"]
fw["SoT_rel"] = fw["SoT"] / fw["90s"]
fw["Ast_rel"] = fw["Ast"] / fw["90s"]
fw["Off_rel"] = fw["Off"] / fw["90s"]
fw["Fls_rel"] = fw["Fls"] / fw["90s"]

fw["score"] = ((fw["Gls_rel"]/(fw.Gls_rel.quantile([0.8]).values)) + 
               (fw["Drib_pct_rel"]/(fw.Drib_pct_rel.quantile([0.8]).values)) + 
               (fw["SCA_rel"]/(fw.SCA_rel.quantile([0.8]).values)) +
               (fw["Cmp_pct_rel"]/(fw.Cmp_pct_rel.quantile([0.8]).values)) +
               (fw["SoT_rel"]/(fw.SoT_rel.quantile([0.8]).values)) +
               (fw["Ast_rel"]/(fw.Ast_rel.quantile([0.8]).values)) 
               ) - (fw["Fls_rel"]/(fw.Fls_rel.quantile([0.8]).values) +
                    fw["Off_rel"]/(fw.Off_rel.quantile([0.8]).values) 
                    )
                    
fw = fw[["Player","score","key"]].sort_values(by = ["score"],ascending=False)
fw.head

##Milieux def
dm = full.loc[full["Pos"] == "DM"]
dm = dm.loc[dm["90s"] >= 15]

dm["Int_rel"] = dm["Int"] / dm["90s"]
dm["Blocks_rel"] = dm["Blocks"] / dm["90s"]
dm["Cmp_pct_rel"] = dm["Cmp_pct"] / dm["90s"]
dm["Touches_rel"] = dm["Touches"] / dm["90s"]
dm["Tkl_pct_rel"] = dm["Tkl_pct"] / dm["90s"]
dm["Fls_rel"] = dm["Fls"] / dm["90s"]
dm["CrdY_rel"] = dm["CrdY"] / dm["90s"]

dm["score"] = ((dm["Tkl_pct_rel"]/(dm.Tkl_pct_rel.quantile([0.8]).values)) + 
               (dm["Int_rel"]/(dm.Int_rel.quantile([0.8]).values)) + 
               (dm["Blocks_rel"]/(dm.Blocks_rel.quantile([0.8]).values)) +
               (dm["Touches_rel"]/(dm.Touches_rel.quantile([0.8]).values)) +
               (dm["Cmp_pct_rel"]/(dm.Cmp_pct_rel.quantile([0.8]).values))
               ) - (dm["Fls_rel"]/(dm.Fls_rel.quantile([0.8]).values) +
                    dm["CrdY_rel"]/(dm.CrdY_rel.quantile([0.8]).values)
                    )
                    
dm = dm[["Player","score","key"]].sort_values(by = ["score"],ascending=False)
dm.head

##Gardiens
gk = full.loc[full["Pos"] == "GK"]
gk = gk.loc[gk["90s"] >= 15]

gk["CS_pct_goal_rel"] = gk["CS_pct_goal"] / gk["90s"]
gk["Save_pct_rel"] = gk["Save_pct"] / gk["90s"]
gk["Stop_pct_goal_rel"] = gk["Stop_pct_goal"] / gk["90s"]
gk["Cmp_pct_rel"] = gk["Cmp_pct"] / gk["90s"]
gk["Fls_rel"] = gk["Fls"] / gk["90s"]
gk["CrdY_rel"] = gk["CrdY"] / gk["90s"]
gk["CrdR_rel"] = gk["CrdR"] / gk["90s"]
gk["Err_rel"] = gk["Err"] / gk["90s"]

gk["score"] = ((gk["CS_pct_goal_rel"]/(gk.CS_pct_goal_rel.quantile([0.8]).values)) + 
               (gk["Save_pct_rel"]/(gk.Save_pct_rel.quantile([0.8]).values)) + 
               (gk["Cmp_pct_rel"]/(gk.Cmp_pct_rel.quantile([0.8]).values)) +
               (gk["Stop_pct_goal_rel"]/(gk.Stop_pct_goal_rel.quantile([0.8]).values)
                )) - (gk["Fls_rel"]/(gk.Fls_rel.quantile([0.8]).values) +
                    gk["Err_rel"]/(gk.Err_rel.quantile([0.8]).values) + 
                    gk["CrdY_rel"]/(gk.CrdY_rel.quantile([0.8]).values)
                    )
                    
gk = gk[["Player","score","key"]].sort_values(by = ["score"],ascending=False)
gk.head

##JOUEURS AU DESSUS DU LOT
borne_mf = mf.score.quantile([0.8]).values[0]

for i in mf.index:
    if mf["score"][i] >= borne_mf :
        mf["top"][i] = 1
    else:
        mf["top"][i] = 0

borne_fw = fw.score.quantile([0.8]).values[0]
fw["top"] = 0

for i in fw.index:
    if fw["score"][i] >= borne_fw :
        fw["top"][i] = 1
    else:
        fw["top"][i] = 0

borne_df = df.score.quantile([0.8]).values[0]
df["top"] = 0

for i in df.index:
    if df["score"][i] >= borne_df :
        df["top"][i] = 1
    else:
        df["top"][i] = 0

borne_dm = dm.score.quantile([0.8]).values[0]
dm["top"] = 0

for i in dm.index:
    if dm["score"][i] >= borne_dm :
        dm["top"][i] = 1
    else:
        dm["top"][i] = 0

borne_gk = gk.score.quantile([0.8]).values[0]
gk["top"] = 0

for i in gk.index:
    if gk["score"][i] >= borne_gk :
        gk["top"][i] = 1
    else:
        gk["top"][i] = 0
        
top_player = mf.append(df)
top_player = top_player.append(dm)
top_player = top_player.append(fw)
top_player = top_player.append(gk)

ekip = full[["key","Squad", "Pos"]]

top_player = top_player.merge(ekip, how = "left", on = "key")

nb_top = top_player.groupby(["Squad","Pos"]).sum(["top"]).reset_index()

table = pd.pivot_table(nb_top, values='top', index=['Squad'],
                    columns=['Pos'], aggfunc=np.sum)

table = table.fillna(0)
##XPORT
full.to_csv("bdd/data/table_joueurs.csv",sep=";")

table.to_csv("bdd/data/nb_top_joueurs.csv",sep=";")
##IMPORT
full = pd.read_csv("bdd/data/table_joueurs.csv",sep=";", index_col = 0)

