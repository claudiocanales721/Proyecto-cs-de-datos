import numpy as np
import pandas as pd



df = pd.read_csv("proyecto\data\IMBD.csv")
df['year']=df['year']
print(f"{df['year'].max()}")