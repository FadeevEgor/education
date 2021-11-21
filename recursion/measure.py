import pandas as pd

from utils import get_setup, calls_vs_connectivity

dfs = []
for i in range(3, 5):
    G, E = get_setup(i)
    dfs.append(calls_vs_connectivity(G, E))

df = pd.concat(dfs, ignore_index=True)
df.to_csv("measurements_3_8.csv", index=False)