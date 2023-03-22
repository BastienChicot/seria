# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 21:11:34 2023

@author: basti
"""
# annee = "2021"
###RECUP VALUES SUR TRANSFERMARKT == 1 fois par an
import pandas as pd
import re
from selenium import webdriver
import time
import os

os.chdir("bdd")
def recup_values(annee):
    driver = webdriver.Chrome()
    
    
    driver.get("https://www.transfermarkt.fr/serie-a/startseite/wettbewerb/IT1/plus/?saison_id=2020")
    time.sleep(20)
    print("Va cliquer sur accepter les cookies blaireau !")
    ####ALLEZ CLIQUER SUR VALIDER LES COOKIES AVANT DE LANCER LA SUITE
    output_lst = []    
    
    for tbody in driver.find_elements_by_xpath('//*[@id="yw1"]/table'):
        tds = tbody.find_elements_by_tag_name('tr')
        output_lst = [td.text for td in tds]
        
    list_df=[]
    for elt in range(0,len(output_lst)):
        output_lst[elt] = re.sub(' +', ' ',output_lst[elt])
        temp=output_lst[elt].split(' ')
        tempdf=pd.DataFrame(temp)
        tempdf=tempdf.transpose()
        list_df.append(tempdf)
        
    final=pd.concat(list_df)
    final.columns = final.iloc[0]
    final = final.reset_index()
    
    final.drop([0], axis=0, inplace=True)
    final.drop([1], axis=0, inplace=True)
    
    final.to_csv("data/value_tm_serieA_20.txt",sep = ";")
    
    print("Tu peux aller modifier le fichier sur bloc note morray !")

##ALLER MODIFIER LE FICHIER A LA MAIN AVANT DE L UTILISER A CAUSE DES CLUB AVEC DES NOMS A RALLONGE

### SCRAPING DE FBREF POUR LES DATA PAR TEAM
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import datetime
import os
import time

def data_fbref(saison):
    
    os.chdir("bdd")
    
    liste_saison = ["2020-2021"]
    
    codes = pd.read_csv("data/code_seriea.txt", sep = ";")
    values = pd.read_csv("data/value_tm_20.txt", sep=";")
    liste_df = []

    for saison in liste_saison:
        for i in tqdm(codes.index):
            try:
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
                
                time.sleep(3)
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
                time.sleep(3)
            
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
                time.sleep(3)
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
                time.sleep(3)
                
                tab_temp = tab_temp.merge(tab_shoot, how="left",on="key")
                tab_temp = tab_temp.merge(tab_pass, how="left",on="key")
                tab_temp = tab_temp.merge(tab_misc, how="left",on="key")
                
                # tm_data = values.loc[values["team"] == tab_temp["team"][0]]
                tm_data = values[["team","age","value"]]    
                
                tab_temp = tab_temp.merge(tm_data, how="left",on="team")
                
                tab_temp["repos"] = 10
                
                for j in range(1,len(tab_temp)):
                    tab_temp["repos"][j] = abs((datetime.strptime(tab_temp["Date"][j], "%Y-%m-%d") - datetime.strptime(tab_temp["Date"][j-1], "%Y-%m-%d")).days)
                    
                tab_temp = tab_temp[tab_temp['Result'].notna()]
                
                liste_df.append(tab_temp)
                time.sleep(10)
                
            except:
                print(codes["code"][i])
                

    data=pd.concat(liste_df)
    
    # data["team"].unique()
    
    data.to_csv("data/data_"+str(saison)+".csv",sep=";")

##MERGE all

data21 = pd.read_csv("data/data_2020-2021.csv",sep=";",index_col = 0)
data22 = pd.read_csv("data/data_2021-2022.csv",sep=";",index_col = 0 )
data23 = pd.read_csv("data/data_2022-2023.csv",sep=";", index_col = 0)

datas = [data21,data22,data23]
table = pd.concat(datas)

table.to_csv("data/data_2020-2023.csv", sep= ";")
#DATA MATCH SUR football-data.co.uk
# os.getcwd()
# driver = webdriver.Chrome()
# driver.get("https://www.football-data.co.uk/italym.php")
# time.sleep(1)

# driver.find_element_by_xpath("/html/body/table[5]/tbody/tr[2]/td[3]/a[2]").click()
    
