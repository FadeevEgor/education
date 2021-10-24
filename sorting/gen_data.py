import argparse
import operator
from copy import copy
import numpy as np
import os

def parse_args():
    parser = argparse.ArgumentParser(description='Generate matrix to sort')
    parser.add_argument('-N', help='Size of array to sort',  default=10000)
    parser.add_argument('-M', help='Number of steps in each direction', default=100)
    parser.add_argument('-o', help="output filename", default="stand")
    return parser.parse_args()


def bubble_sort_step(array, cmp):
    n = len(array)
    array = copy(array)
    for i in range(n - 1):
        if cmp(array[i], array[i + 1]):
            array[i], array[i + 1] = array[i + 1], array[i]
    return array

def bubble_sort_n_steps(array, cmp, n_steps):
    for i in range(n_steps):
        array = bubble_sort_step(array, cmp)
    return array

args = parse_args()
n = int(args.N)
m = int(args.M)


n_rows = 2 * m + 1
n_cols = n
h = n // m

stand = np.zeros((n_rows, n_cols))
stand[m, :] = np.random.random(n_cols)
for i in range(1, m + 1):
    steps = h
    stand[m + i] = bubble_sort_n_steps(stand[m + i - 1], operator.le, steps)
    stand[m - i] = bubble_sort_n_steps(stand[m - i + 1], operator.ge, steps)

np.save(os.path.join("./data/", args.o), stand)