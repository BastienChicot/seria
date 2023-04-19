# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 17:56:55 2023

@author: basti
"""
import pandas as pd

import numpy as np

df = pd.read_csv("bdd/data/df_all_seasons.csv",sep=";", index_col = 0)

df.loc[(df["not_lose"] + df["victoire"] == 0), "result"] = "D" 
df.loc[(df["not_lose"] + df["victoire"] == 1), "result"] = "N" 
df.loc[(df["not_lose"] + df["victoire"] == 2), "result"] = "V"

# clusters = df[["team","Opponent","year","cluster"]]
# df["key"] = ""
# clusters["key"] = ""
# clusters["opp_key"] = ""

# for i in clusters.index :
#     df["key"][i] = df["team"][i]+df["Opponent"][i]+str(df["year"][i])
#     clusters["key"][i] = str(clusters["team"][i])+str(clusters["Opponent"][i])+str(clusters["year"][i])
#     clusters["opp_key"][i] = clusters["Opponent"][i]+clusters["team"][i]+str(clusters["year"][i])

# Opp_tab = clusters[["opp_key","cluster"]]

# Opp_tab = Opp_tab.rename(
#     columns = {
#         "opp_key" : "key",
#         "cluster" : "opp_cluster"
#         })

# clusters = clusters.merge(Opp_tab, on = ["key"], how = "left")
# clusters = clusters.drop_duplicates()

# df = df.merge(Opp_tab, on = ["key"], how = "left")
# df = df.drop_duplicates()

from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.preprocessing import PolynomialFeatures

from sklearn.model_selection import train_test_split
from sklearn.compose import make_column_transformer

data = df.copy()
data = data.dropna()

y = data[["result"]]

X = data[[
    "Poss",
    "age",
    "Formation",
    "SoT",
    "Dist",
    "Int",
    "Fls",
    "diff_value",
    "repos",
    "opp_Formation",
    "saison",
    "PK",
    "CrdY",
    "CrdR",
    "coup_arret",
    "opp_fls",
    "CMP",
    "top_GK",
    "top_MF",
    "top_DF",
    "top_DM",
    "top_FW",
    "cluster",
    "opp_cluster"
    ]]

numeric_data = [
    "Poss",
    "age",
    "SoT",
    "Dist",
    "Int",
    "Fls",
    "diff_value",
    "repos",
    "PK",
    "CrdY",
    "CrdR",
    "coup_arret",
    "opp_fls",
    "CMP"
    ]
object_data = [
    "Formation",
    "opp_Formation",
    "saison",
    "top_GK",
    "top_MF",
    "top_DF",
    "top_DM",
    "top_FW",
    "cluster",
    "opp_cluster"
    ]


for col in data.select_dtypes('float'):
    plt.figure()
    sns.distplot(data[col])

#PIPELINE

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)

numeric_pipeline = make_pipeline(PolynomialFeatures(2),StandardScaler())
object_pipeline = make_pipeline(OneHotEncoder())

preprocessor = make_column_transformer((numeric_pipeline, numeric_data),
                                       (object_pipeline, object_data))


from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier

MLP = make_pipeline(preprocessor, MLPClassifier())
RFR = make_pipeline(preprocessor, RandomForestClassifier(n_estimators=20))
KNN = make_pipeline(preprocessor, KNeighborsClassifier())
SGD = make_pipeline(preprocessor, SGDClassifier())

dict_of_models = {
                  "Neural": MLP,
                  "SGD" : SGD,
                  "KNN":KNN,
                  "RFR":RFR,
                 }

from sklearn.metrics import mean_squared_error, mean_absolute_error

def evaluation (model):
    model.fit(X_train, y_train.values.ravel())
    y_pred = model.predict(X_test)
    # mse = mean_squared_error(y_test, y_pred)
    # mae = mean_absolute_error(y_test.values.ravel(), y_pred)
    # print(mse)
    # print(mae)
    print (model.score(X_test, y_test))
    
for name, model in dict_of_models.items():
    print(name)
    evaluation(model)  


