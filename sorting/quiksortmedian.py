from random import sample

def quickSortMedian(L, ascending = True):
    quicksorthelp(L, 0, len(L), ascending)


def quicksorthelp(L, low, high, ascending = True):
    result = 0
    if low < high:
        pivot_location, result = Partition(L, low, high, ascending)
        result += quicksorthelp(L, low, pivot_location, ascending)
        result += quicksorthelp(L, pivot_location + 1, high, ascending)
    return result


def median_of_three(L, low, high):

    if high - low > 2:
        i, j, k = sample(range(low, high), 3)
        a, b, c = L[i], L[j], L[k]
        if a <= b <= c:
            return b, j
        if c <= b <= a:
            return b, j
        if a <= c <= b:
            return c, k
        if b <= c <= a:
            return c, k
        return a, i

    return L[low], low

def Partition(L, low, high, ascending = True):
    # print('Quicksort, Parameter L:')
    # print(L)
    result = 0
    pivot, pidx = median_of_three(L, low, high)
    L[low], L[pidx] = L[pidx], L[low]
    i = low + 1
    for j in range(low+1, high, 1):
        result += 1
        if (ascending and L[j] < pivot) or (not ascending and L[j] > pivot):
            L[i], L[j] = L[j], L[i]
            i += 1
    L[low], L[i-1] = L[i-1], L[low]
    return i - 1, result

if __name__ == "__main__":
    from random import randint
    L = [randint(-10, 10) for i in range(10)]
    print(L)
    quickSortMedian(L)
    print(L)