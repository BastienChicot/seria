# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 21:35:28 2023

@author: basti
"""

import pandas as pd

##STANDARD
standard = pd.read_csv("bdd/data/dl_fbref/stat_joueur_stand_21_22.txt", sep= ",", index_col = 0)

standard.columns = standard.iloc[0]
                         
standard = standard.reset_index()
standard = standard.loc[standard["-9999"] != "-9999"]

standard.columns
standard = standard.rename(columns = {
    "index":"Player"
    })

#fichier de base sur lequel je vais joindre les autres

##TIRS
shots = pd.read_csv("bdd/data/dl_fbref/stat_joueur_shots_21_22.txt", sep= ",", index_col = 0)

shots = shots.reset_index()

shots.columns

shots = shots[["Sh","SoT","SoT%","-9999","Player"]]
shots = shots.rename(columns = {
    "SoT%":"SoT_pct"
    })

full = pd.merge(standard,shots, how = "left", on = ["-9999","Player"])

##PASSES
passes = pd.read_csv("bdd/data/dl_fbref/stat_joueur_pass_21_22.txt", sep= ",", index_col = 0)

passes = passes.reset_index()

passes.columns

passes = passes[["Cmp","Att","Cmp%","-9999"]]
passes = passes.rename(columns = {
    "Cmp%" : "Cmp_pct"
    })

full = full.merge(passes, how = "left", on = "-9999")

##SHOOTING CREATING ACTION
sca = pd.read_csv("bdd/data/dl_fbref/stat_joueur_sca_21_22.txt", sep= ",", index_col = 0)

sca = sca.reset_index()

sca.columns

sca = sca[["SCA","-9999"]]
full = full.merge(sca, how = "left", on = "-9999")


##DEFENSE
defense = pd.read_csv("bdd/data/dl_fbref/stat_joueur_def_21_22.txt", sep= ",", index_col = 0)

defense = defense.reset_index()

defense.columns

defense = defense[["Tkl","TklW","Tkl%","Blocks","Sh","Pass","Int","Tkl+Int","Clr","Err","-9999"]]

defense = defense.rename(columns = {
    "Tkl%":"Tkl_pct",
    "Sh":"Sh_block"
    })

full = full.merge(defense, how = "left", on = "-9999")


##POSSESSION
poss = pd.read_csv("bdd/data/dl_fbref/stat_joueur_poss_21_22.txt", sep= ",", index_col = 0)

poss = poss.reset_index()

poss.columns

poss = poss[["Touches","Succ%", "Mis","Dis","-9999"]]
poss = poss.rename(columns={
    "Succ%":"Drib_pct"
    })
full = full.merge(poss, how = "left", on = "-9999")

##MISC ATTENTION DOUBLONS DE VARIABLES
misc = pd.read_csv("bdd/data/dl_fbref/stat_joueur_misc_21_22.txt", sep= ",", index_col = 0)

misc = misc.reset_index()

misc.columns

misc = misc[["Fls","Off","Crs","Won%","-9999"]]
misc = misc.rename(columns={
    "Won%":"duels_aeriens_pct"
    })

full = full.merge(misc, how = "left", on = "-9999")

##GARDIENS
goal = pd.read_csv("bdd/data/dl_fbref/stat_goal_stand_21_22.txt", sep= ",", index_col = 0)
                         
goal = goal.reset_index()
goal = goal.loc[goal["-9999"] != "-9999"]

goal_adv = pd.read_csv("bdd/data/dl_fbref/stat_goal_adv_21_22.txt", sep= ",", index_col = 0)
                         
goal_adv = goal_adv.reset_index()

goal.columns
goal_adv.columns

goal = goal[["Save%","CS%","-9999"]]
goal_adv = goal_adv[["Stp%","-9999"]]

goal = goal.merge(goal_adv, how = "left", on = "-9999")
goal = goal.rename(columns={
    "Save%":"Save_pct",
    "CS%":"CS_pct_goal",
    "Stp%":"Stop_pct_goal"
    })

full = full.merge(goal, how = "left", on = "-9999")

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

##XPORT
full.to_csv("bdd/data/table_joueurs.csv",sep=";")

##IMPORT
full = pd.read_csv("bdd/data/table_joueurs.csv",sep=";", index_col = 0)
