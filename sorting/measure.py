import os
import sys
import argparse
import threading

import numpy as np
import pandas as pd
from tqdm import tqdm

from counter import CountableFloat, Counter
from quicksort2pivot import dualPivotQuickSort
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
    # "Dual Pivot QuickSort": dualPivotQuickSort,
    "Kernigan Richi shellsort": kernigan_richi_shellsort,
    "Knutt shellsort": knutt_shellsort,
    "Tim sort": sorted,
}


args = parse_args()
sys.setrecursionlimit(int(args.r))
threading.stack_size(0x5000000)

stand = np.load(os.path.join("./data", args.i))
n, m = stand.shape
comparisons = {method_name: np.zeros(n) for method_name in methods}
for i in tqdm(range(n)):
    for method_name, method in methods.items():
        cnt = Counter()
        arr = [CountableFloat(x, cnt) for x in stand[i]]
        f = make_callable(method, arr)
        t = threading.Thread(target=f())
        t.start()
        t.join()
        comparisons[method_name][i] = cnt.comparisons
        cnt.reset()


output_filename = f"{args.o}_comparisons.csv"
pd.DataFrame(comparisons).to_csv(os.path.join("./data", output_filename))
print(output_filename)
