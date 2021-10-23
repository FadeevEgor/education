import os
import sys
import argparse
import threading

import numpy as np
import pandas as pd
from tqdm import tqdm

from counter import CountableFloat, Counter
from dualpivot import quicksort as dualPivotQuickSort
from quiksortmedian import quickSortMedian
from shellsort import knutt_shellsort, kernigan_richi_shellsort



def make_callable(method, data):
    def f():
        method(data)
    return f


def parse_args():
    parser = argparse.ArgumentParser(description='Generate matrix to sort')
    parser.add_argument('-i', help="stand filename", default="small_stand.npy")
    parser.add_argument('-o', help="prefix to output", default="")
    parser.add_argument('-r', help="recursion limit", default=1000)
    return parser.parse_args()




methods = {
    "Median of three Quick Sort": quickSortMedian,
    "Dual Pivot QuickSort": dualPivotQuickSort,
    "Kernigan Richi shellsort": kernigan_richi_shellsort,
    "Knutt shellsort": knutt_shellsort,
    "Tim sort": sorted,
}


args = parse_args()
sys.setrecursionlimit(int(args.r))
threading.stack_size(0x9999999)

stand = np.load(os.path.join("./data", args.i))
print(stand.shape)
n, m = stand.shape
comparisons = {method_name: np.zeros(n) for method_name in methods}
swaps = {method_name: np.zeros(n) for method_name in methods}
for i in tqdm(range(n)):
    for method_name, method in methods.items():
        cnt = Counter()
        arr = [CountableFloat(x, cnt) for x in stand[i]]
        f = make_callable(method, arr)
        t = threading.Thread(target=f())
        t.start()
        t.join()
        comparisons[method_name][i] = cnt.comparisons
        swaps[method_name][i] = cnt.swaps
        cnt.reset()


output_filename_1 = f"{args.o}_comparisons.csv"
pd.DataFrame(comparisons).to_csv(os.path.join("./data", output_filename_1))
output_filename_2 = f"{args.o}_swaps.csv"
pd.DataFrame(swaps).to_csv(os.path.join("./data", output_filename_2))
print(output_filename_1, output_filename_2)
