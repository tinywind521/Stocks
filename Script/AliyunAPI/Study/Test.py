import pandas as pd

VolSMA5=pd.Series(volume).rolling(window=5).mean().dropna()
VolSMA10=pd.Series(volume).rolling(window=10).mean().dropna()