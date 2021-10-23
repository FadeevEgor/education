import operator


class Counter:
    def __init__(self):
        self.comparisons = 0
        self.swaps = 0

    def being_compared(self):
        self.comparisons += 1

    def being_swapped(self):
        self.swaps += 1

    def reset(self):
        self.comparisons = 0
        self.swaps = 0


class CountableFloat:
    def __init__(self, value, counter):
        self.value = value
        self.counter : Counter = counter

    def __le__(self, other):
        self.counter.being_compared()
        return operator.le(self.value, other.value)

    def __lt__(self, other):
        self.counter.being_compared()
        return operator.lt(self.value, other.value)

    def __ge__(self, other):
        self.counter.being_compared()
        return operator.ge(self.value, other.value)

    def __gt__(self, other):
        self.counter.being_compared()
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