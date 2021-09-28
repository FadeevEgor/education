import argparse
import pandas as pd
import os
from random import randint, choices

def parse_args():
    parser = argparse.ArgumentParser(description='translate text into int32 array of unicode points')
    parser.add_argument('-l', help='language',  required=True)
    parser.add_argument('-N', help='text length', default=10 ** 8)
    parser.add_argument('-M', help='maximum pattern length', default=10 ** 7)
    return parser.parse_args()
     



def random_substring(string, length=None):
    n = len(string)
    if length is None:
        length = randint(0, n // 2)
    
    max_index = n - length
    index = randint(0, max_index)
    return string[index : index+length]
    

def random_string(symbols, length):
    return choices(population=symbols, k=length)

args = parse_args()
directory = os.path.join("data", args.l)
filepath = os.path.join(directory, f"ted_{args.l}.txt")

unicode_codes = []

with open(filepath, encoding="utf-8") as f:
    for line in f:
        unicode_codes.extend([ord(symbol) for symbol in line])
        if len(unicode_codes) > int(args.N):
            break

symbols = sorted(list(set(unicode_codes)))
symbols_new_codes = {old:new for new, old in enumerate(symbols)}
unicode_codes = [symbols_new_codes[code] for code in unicode_codes]
symbols = sorted(list(set(unicode_codes)))
 
symbols = list(set(unicode_codes))
pattern_length = 10
while pattern_length <= int(args.M):
    with open(os.path.join(directory, f"patterns_{pattern_length}.txt"), "w") as f:
        for i in range(50):
            pattern = random_substring(unicode_codes, pattern_length)
            f.write(" ".join([str(code) for code in pattern]) + "\n")
            # pattern = random_string(symbols, pattern_length)
            # f.write(" ".join([str(code) for code in pattern]) + "\n")
    pattern_length *= 10
    
    


unicode_codes = pd.DataFrame({"codes": unicode_codes})
unicode_codes.to_csv(os.path.join(directory, "text.csv"), header=False, index=False)