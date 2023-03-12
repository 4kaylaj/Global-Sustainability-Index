#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 08:14:08 2023

@author: kayla
"""

import pandas as pd
import jenkspy

#Read in CSV to a df
df_env = pd.read_csv("Environmental.csv")

#%%
#Calculate energy production percentages

df_env["perc_coal"] = df_env["Coal"]/df_env["Energy Production"]

df_env['perc_natgas'] = df_env["Natural Gas"]/df_env["Energy Production"]

df_env['perc_petroleum'] = df_env["Petroleum"]/df_env["Energy Production"]

df_env['perc_nuclear'] =  df_env["Nuclear"]/df_env["Energy Production"]

df_env['perc_renew'] = df_env['Renewables and Other']/df_env["Energy Production"]

#Sum energy percents

df_env["perc_carbon"] = df_env["perc_coal"] + df_env["perc_natgas"] + df_env['perc_petroleum']

df_env["perc_nocarbon"] = df_env['perc_nuclear'] + df_env['perc_renew']

#%%
#Setting up an empty df for quantiles
q_envdf = pd.DataFrame()

#Giving points for high outcome
def envquant_1 (name,column):
    q_envdf[name]=pd.qcut(df_env[column], 4, labels=[1,2,3,4])
   
#Giving points for low outcome
def envquant_2 (name,column):
    q_envdf[name]=pd.qcut(df_env[column], 4, labels=[4,3,2,1])
#%%
#Calculate quantiles
envquant_1("RISE Energy Efficiency", "RISE Energy Efficiency")

envquant_1("RISE Renewable Energy", "RISE Renewable Energy")

envquant_2("perc_carbon", "perc_carbon")

envquant_1("perc_nocarbon", "perc_nocarbon")

envquant_1("Carbon Offsets-Project Count", "Carbon Offests Projects")

envquant_1("Ecosytem Vitality", "Ecosystem Vitality")

envquant_1("Waste Management", "Waste Management")

envquant_1("Climate Change", "Climate Change")

#%%
q_envdf["Environmental Index Score"] = q_envdf.sum( axis = 1)

q_envdf["Country"] = df_env["Variable"]

#%%
#Read in CSV to a df
df_soc = pd.read_csv("Social.csv")

#%%
#Setting up an empty df for quantiles
q_socdf = pd.DataFrame()

#Giving points for high outcome
def socquant_1 (name,column):
    q_socdf[name]=pd.qcut(df_soc[column], 4, labels=[1,2,3,4])
   
#Giving points for low outcome
def socquant_2 (name,column):
    q_socdf[name]=pd.qcut(df_soc[column], 4, labels=[4,3,2,1])
    
#%%
#Calculate quantiles
socquant_1("Universal Health Coverage", "Universal Health Coverage")

socquant_2("Unemployment", "Unemployment")

socquant_1("Quality of Water Services", "Quality of Water Services")

socquant_2("Poverty", "Poverty")

socquant_1("Population", "Population")

socquant_1("Mean Years of Schooling", "Mean Years of Schooling")

socquant_1("Life Expectancy", "Life Expectancy")

#Write code to run this as a quantile (5 bins)
socquant_2("Global Rights Index", "Global Rights Index")

socquant_1("Expected Years of Schooling", "Expected Years of Schooling")

socquant_2("Air Quality", "Air Quality")

socquant_1("Age Demographic", "Age Demographic")

#Check scoring
socquant_1("Global Peace Index", "Global Peace Index")
#%%
q_socdf["Social Index Score"] = q_socdf.sum( axis = 1)

q_socdf["Country"] = df_soc["Variable"]

#%%
#Read in CSV to a df
df_econ = pd.read_csv("Economic.csv")

#%%
#Setting up an empty df for quantiles
q_econdf = pd.DataFrame()

#Giving points for high outcome
def econquant_1 (name,column):
    q_econdf[name]=pd.qcut(df_econ[column], 4, labels=[1,2,3,4])
   
#Giving points for low outcome
def econquant_2 (name,column):
    q_econdf[name]=pd.qcut(df_econ[column], 4, labels=[4,3,2,1])
    
#%%

econquant_1("Trade Openness", "Trade Openness")

econquant_1("Sovereign Credit Ratings", "Sovereign Credit Ratings")

econquant_1("Population Growth", "Population Growth")

econquant_1("Net Trade", "Net Trade")

econquant_1("Labor Force", "Labor Force")

econquant_1("Innovative Capability", "Innovative Capability")

econquant_1("Infrastrcuture", "Infrastrcuture")

econquant_2("Inflation", "Inflation")

econquant_2("Government Debt", "Government Debt ")

econquant_1("GDP Per Capita","GDP Per Capita")

econquant_1("FDI", "FDI")

econquant_1("Financail System Depth", "Financial System Depth")

econquant_2("Electricity Prices", "Electricity Prices")

econquant_1("Corruption", "Corruption")

econquant_2("Corporate Tax", "Corporate Tax")

#Natural breaks because bin error with quantile function
breaks=jenkspy.jenks_breaks(df_econ["Access to Electricity"], n_classes=4)
q_econdf["Access to Electricity"]=pd.cut(df_econ["Access to Electricity"], 
                                           bins = breaks,
                                           labels=[1,2,3,4],
                                           include_lowest=True)                                       
#%%
q_econdf["Economic Index Score"] = q_econdf.sum( axis = 1)

q_econdf["Country"] = df_econ["Variable"]

#%%
#Add sub-indices together

#Create empt df
df_index = pd.DataFrame()

def indexquant_1 (name,column):
    df_index[name]=pd.qcut(df_index[column], 4, labels=[1,2,3,4])

#Need to fix math in this part
df_index["Environmental Index Score"] = ((q_envdf["Environmental Index Score"]/32)*(1/3))


df_index["Social Index Score"] = ((q_socdf["Social Index Score"]/48)*(1/3))


df_index["Economic Index Score"] = ((q_econdf["Economic Index Score"]/64)*(1/3))


df_index["Sustainability Index Score"] = df_index.sum( axis = 1)

#How to make score out of 100?
df_index["Sustainability Index Score"] = (df_index["Sustainability Index Score"]*100)

indexquant_1("Sustainability Index Q", "Sustainability Index Score")

indexquant_1("Environmental Index Q", "Environmental Index Score")

df_index["Environmental Index Score"] = (df_index["Environmental Index Score"]*100)

indexquant_1("Social Index Q", "Social Index Score")

df_index["Social Index Score"] = (df_index["Social Index Score"]*100)

indexquant_1("Economic Index Q", "Economic Index Score")

df_index["Economic Index Score"] = (df_index["Economic Index Score"]*100)

#%%
#Convert quantiles to grade
df_index["Sustainability Grade"]=df_index["Sustainability Index Q"].astype(str)
df_index.loc[df_index["Sustainability Grade"]=="4", "Sustainability Grade"]="A"
df_index.loc[df_index["Sustainability Grade"]=="3", "Sustainability Grade"]="B"
df_index.loc[df_index["Sustainability Grade"]=="2", "Sustainability Grade"]="C"
df_index.loc[df_index["Sustainability Grade"]=="1", "Sustainability Grade"]="D"

df_index["Environmental Grade"]=df_index["Environmental Index Q"].astype(str)
df_index.loc[df_index["Environmental Grade"]=="4", "Environmental Grade"]="A"
df_index.loc[df_index["Environmental Grade"]=="3", "Environmental Grade"]="B"
df_index.loc[df_index["Environmental Grade"]=="2", "Environmental Grade"]="C"
df_index.loc[df_index["Environmental Grade"]=="1", "Environmental Grade"]="D"

df_index["Social Grade"]=df_index["Social Index Q"].astype(str)
df_index.loc[df_index["Social Grade"]=="4", "Social Grade"]="A"
df_index.loc[df_index["Social Grade"]=="3", "Social Grade"]="B"
df_index.loc[df_index["Social Grade"]=="2", "Social Grade"]="C"
df_index.loc[df_index["Social Grade"]=="1", "Social Grade"]="D"

df_index["Economic Grade"]=df_index["Economic Index Q"].astype(str)
df_index.loc[df_index["Economic Grade"]=="4", "Economic Grade"]="A"
df_index.loc[df_index["Economic Grade"]=="3", "Economic Grade"]="B"
df_index.loc[df_index["Economic Grade"]=="2", "Economic Grade"]="C"
df_index.loc[df_index["Economic Grade"]=="1", "Economic Grade"]="D"

df_index["Country"] = df_econ["Variable"]

df_index.to_csv("IndexResult.csv")
#%%








