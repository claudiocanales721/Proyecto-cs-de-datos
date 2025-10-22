import numpy as np
import pandas as pd
import builtins
import os
import json

with open("data/gamespot.csv", "r", encoding='utf-8') as f:
    df = pd.read_csv(f)

df_limpio = df.rename(columns={'game_name': 'nombre',
                    'score': 'nota',
                    'publish_date': 'publicacion',
                    'game_id': 'id'})

print(df_limpio.columns)

df_limpio = df_limpio.dropna()

df_limpio['publicacion'] = pd.to_datetime(df_limpio['publicacion'], errors= 'coerce')

df_limpio['nota']=pd.to_numeric(df_limpio['nota'])

df_limpio['id']=pd.to_numeric(df_limpio['id'])

print(df_limpio.info())

df_limpio.to_csv('data/gamespot_limpio.csv')