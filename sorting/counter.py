import operator


class Counter:
    def __init__(self):
        self.comparisons = 0
        self.assignments = 0

    def __call__(self):
        self.comparisons += 1
        self.assignments += 1

    def reset(self):
        self.comparisons = 0
        self.assignments = 0


class CountableFloat:
    def __init__(self, value, counter):
        self.value = value
        self.counter = counter

    def __le__(self, other):
        self.counter()
        return operator.le(self.value, other.value)

    def __lt__(self, other):
        self.counter()
        return operator.lt(self.value, other.value)

    def __ge__(self, other):
        self.counter()
        return operator.ge(self.value, other.value)

    def __gt__(self, other):
        self.counter()
        return operator.gt(self.value, other.value)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)

if __name__ == "__main__":
    arr = list(range(1000, 0, -1))
    counter = Counter()
    arr = [CountableFloat(x, counter) for x in arr]
    print(arr)
    arr.sort()
    print(counter.comparisons)