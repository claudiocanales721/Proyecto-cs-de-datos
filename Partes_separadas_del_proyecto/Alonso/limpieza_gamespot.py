import numpy as np
import pandas as pd
import builtins
import os
import json

with open('data/gamespot_reseñas.json', mode="r", encoding='utf-8') as d:
    data=json.load(d)


df=pd.read_json(data)

print(df.head())