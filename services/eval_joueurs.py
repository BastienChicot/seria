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

#fichier de base sur lequel je vais joindre les autres

##TIRS
shots = pd.read_csv("bdd/data/dl_fbref/stat_joueur_shots_21_22.txt", sep= ",", index_col = 0)

shots = shots.reset_index()

##PASSES
passes = pd.read_csv("bdd/data/dl_fbref/stat_joueur_pass_21_22.txt", sep= ",", index_col = 0)

passes = passes.reset_index()

##SHOOTING CREATING ACTION
sca = pd.read_csv("bdd/data/dl_fbref/stat_joueur_sca_21_22.txt", sep= ",", index_col = 0)

sca = sca.reset_index()

##DEFENSE
defense = pd.read_csv("bdd/data/dl_fbref/stat_joueur_def_21_22.txt", sep= ",", index_col = 0)

defense = defense.reset_index()

##POSSESSION
poss = pd.read_csv("bdd/data/dl_fbref/stat_joueur_poss_21_22.txt", sep= ",", index_col = 0)

poss = poss.reset_index()

##MISC ATTENTION DOUBLONS DE VARIABLES
misc = pd.read_csv("bdd/data/dl_fbref/stat_joueur_misc_21_22.txt", sep= ",", index_col = 0)

misc = misc.reset_index()

##GARDIENS
goal = pd.read_csv("bdd/data/dl_fbref/stat_goal_stand_21_22.txt", sep= ",", index_col = 0)
                         
goal = goal.reset_index()
goal = goal.loc[goal["-9999"] != "-9999"]

goal_adv = pd.read_csv("bdd/data/dl_fbref/stat_goal_adv_21_22.txt", sep= ",", index_col = 0)
                         
goal_adv = goal_adv.reset_index()

