import numpy as np
import random
import bisect
# from collections import Counter
# from tqdm import tqdm

alpha = 0.05
max_iter = 10**8
pr = [4, 3, 2, 1]
s = len(pr) - 1
pr.sort(reverse=True)


class WeightedRandomGenerator(object):
    def __init__(self, weights):
        self.totals = []
        running_total = 0

        for w in weights:
            running_total += w
            self.totals.append(running_total)

    def next(self):
        rnd = random.random() * self.totals[-1]
        return bisect.bisect_right(self.totals, rnd)

    def __call__(self):
        return self.next()


def delta(n, s):
    # alpha_ = lambda s: alpha/s
    return np.sqrt((2./n) * np.log(s + 1/alpha))


gen = WeightedRandomGenerator(pr)
cont = True
n = 0
f = np.zeros(s)
counter = np.zeros(s + 1)
while cont:
    n += 1
    exp = gen()
    counter[exp] += 1
    freq = counter/n
    f = np.zeros(s)
    cont = False
    for i in range(s):
        f[i] = np.sum(freq[:i + 1]) + 2*freq[i + 1]
        temp = True if abs(f[i] - 1) <= delta(n=n, s=s) else False
        cont = cont or temp
    if n % 1000000 == 0:
        print(n)



print("iterations  ", n)
print("p0", end=" ")
for i in range(s):
    symbol = ">" if f[i] > 1 else "="
    print(symbol + " p" + str(i + 1), end=" ")

print("\n\nwhile")
print("pr0", end=" ")
for i in range(s):
    symbol = ">" if pr[i] > pr[i + 1] else "="
    print(symbol + " pr" + str(i + 1), end=" ")

