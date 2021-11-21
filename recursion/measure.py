import os
import argparse

from utils import get_setup, calls_vs_connectivity


def parse_args():
    parser = argparse.ArgumentParser(description='count calls and solutions to Euler problem')
    parser.add_argument('-n', help="number of nodes", default=3)
    parser.add_argument('-d', help="directory", default="measurements")
    return parser.parse_args()


args = parse_args()
nodes = int(args.n)
folder = args.d
G, E = get_setup(nodes)
df = calls_vs_connectivity(G, E)
filename = os.path.join(folder, f"{nodes}_nodes.csv")
os.makedirs(folder, exist_ok=True)
df.to_csv(filename, index=False)
print(df)