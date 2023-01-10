# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 21:11:34 2023

@author: basti
"""

### SCRAPING DE FBREF POUR LES DATA PAR TEAM
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
    
saison = "2021-2022"

codes = pd.read_csv("data/code_team.txt", sep = ";")

liste_df = []

for i in tqdm(codes.index):
    url_stat = "https://fbref.com/en/squads/"+str(codes["code_url"][i])+"/"+str(saison)+"/"+str(codes["code"][i])+"-Stats"
    url_shoot = "https://fbref.com/en/squads/"+str(codes["code_url"][i])+"/"+str(saison)+"/matchlogs/all_comps/shooting/"+str(codes["code"][i])+"-Match-Logs-All-Competitions" 
    url_passe = "https://fbref.com/en/squads/"+str(codes["code_url"][i])+"/"+str(saison)+"/matchlogs/all_comps/passing/"+str(codes["code"][i])+"-Match-Logs-All-Competitions" 
    #♦url_def = "https://fbref.com/en/squads/"+str(codes["code_url"][i])+"/"+str(saison)+"/matchlogs/all_comps/defense/"+str(codes["code"][i])+"-Match-Logs-All-Competitions" 
    url_misc = "https://fbref.com/en/squads/"+str(codes["code_url"][i])+"/"+str(saison)+"/matchlogs/all_comps/misc/"+str(codes["code"][i])+"-Match-Logs-All-Competitions" 
    
    ##STAT GENERALES
    r = requests.get(url_stat)
    r_html = r.text
    soup = BeautifulSoup(r_html,'html.parser')

    table=soup.find_all('table', {'id' : 'matchlogs_for'})

    tab_temp = pd.read_html(str(table[0]))[0]
    tab_temp["team"] = codes["code"][i]
    tab_temp["key"] = tab_temp["Date"]+tab_temp["Time"]+tab_temp["Comp"]+tab_temp["Round"]+tab_temp["Venue"]+tab_temp["Result"]+tab_temp["Opponent"]+tab_temp["team"]

    ##STAT TIRS
    r_shoot = requests.get(url_shoot)
    r_html_shoot = r_shoot.text
    soup_shoot = BeautifulSoup(r_html_shoot,'html.parser')

    tab2=soup_shoot.find_all('table', {'id' : 'matchlogs_for'})

    tab_shoot = pd.read_html(str(tab2[0]))[0]
    tab_shoot.columns = tab_shoot.columns.droplevel(0)
    tab_shoot["team"] = codes["code"][i]
    tab_shoot["key"] = tab_shoot["Date"]+tab_shoot["Time"]+tab_shoot["Comp"]+tab_shoot["Round"]+tab_shoot["Venue"]+tab_shoot["Result"]+tab_shoot["Opponent"]+tab_shoot["team"]
    tab_shoot = tab_shoot[["key","Sh","SoT","Dist","FK","PK"]]

    ##STAT PASSES
    r_pass = requests.get(url_passe)
    r_html_pass = r_pass.text
    soup_pass = BeautifulSoup(r_html_pass,'html.parser')

    tab3=soup_pass.find_all('table', {'id' : 'matchlogs_for'})

    tab_pass = pd.read_html(str(tab3[0]))[0]
    tab_pass.columns = tab_pass.columns.droplevel(0)
    tab_pass["team"] = codes["code"][i]
    tab_pass["key"] = tab_pass["Date"]+tab_pass["Time"]+tab_pass["Comp"]+tab_pass["Round"]+tab_pass["Venue"]+tab_pass["Result"]+tab_pass["Opponent"]+tab_pass["team"]
    tab_pass = tab_pass[["key","Att","Cmp%"]]
    ##VERIFIER LA SORTIE DE LA LIGNE CI DESSOUS:
    tab_pass = tab_pass.iloc[:, [0,1,5]]

    ##STAT MISC
    r_misc = requests.get(url_misc)
    r_html_misc = r_misc.text
    soup_misc = BeautifulSoup(r_html_misc,'html.parser')

    tab4=soup_misc.find_all('table', {'id' : 'matchlogs_for'})

    tab_misc = pd.read_html(str(tab4[0]))[0]
    tab_misc.columns = tab_misc.columns.droplevel(0)
    tab_misc["team"] = codes["code"][i]
    tab_misc["key"] = tab_misc["Date"]+tab_misc["Time"]+tab_misc["Comp"]+tab_misc["Round"]+tab_misc["Venue"]+tab_misc["Result"]+tab_misc["Opponent"]+tab_misc["team"]
    tab_misc = tab_misc[["key","CrdY","CrdR","2CrdY","Fls","Off","Int"]]
    
    tab_temp = tab_temp.merge(tab_shoot, how="left",on="key")
    tab_temp = tab_temp.merge(tab_pass, how="left",on="key")
    tab_temp = tab_temp.merge(tab_misc, how="left",on="key")
    
    liste_df.append(tab_temp)



from selenium import webdriver
import time
import os


#DATA MATCH SUR football-data.co.uk
os.getcwd()
driver = webdriver.Chrome()
driver.get("https://www.football-data.co.uk/italym.php")
time.sleep(1)

driver.find_element_by_xpath("/html/body/table[5]/tbody/tr[2]/td[3]/a[2]").click()
    
