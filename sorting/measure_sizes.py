import sys

import threading
import random

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

methods = {
    "Median of three Quick Sort": quickSortMedian,
    "Dual Pivot QuickSort": dualPivotQuickSort,
    "Kernigan Richi shellsort": kernigan_richi_shellsort,
    "Knutt shellsort": knutt_shellsort,
    "Tim sort": sorted,
}

sys.setrecursionlimit(5000)
threading.stack_size(0x9999999)

N = 11
sizes = [100 * 2 ** i for i in range(N)]

comparisons = {method_name: np.zeros(N) for method_name in methods}
swaps = {method_name: np.zeros(N) for method_name in methods}

for i, size in enumerate(sizes):
    print(size)
    arr = [random.randint(-size, size) for i in range(size)]
    for method_name, method in tqdm(methods.items()):
        cnt = Counter()
        to_sort = [CountableFloat(x, cnt) for x in arr]
        f = make_callable(method, to_sort)
        t = threading.Thread(target=f())
        t.start()
        t.join()
        comparisons[method_name][i] = cnt.comparisons
        swaps[method_name][i] = cnt.swaps

pd.DataFrame(comparisons, index=sizes).to_csv("./data/comparisons.csv")
pd.DataFrame(swaps, index=sizes).to_csv("./data/swaps.csv")
