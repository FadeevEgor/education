from random import sample
def swap(data, i, j):
    data[i], data[j] = data[j], data[i]
    try:
        data[i].counter.being_swapped()
    except AttributeError:
        pass

def dualPivotQuicksort(data, left, right, div):
    len = right - left
    if len < 27:
        for i in range(left+1, right+1):
            for j in range(i, left, -1):
                if data[j] >= data[j - 1]:
                    break
                swap(data, j-1, j)
        return

    third = len // div

    # "medians"
    m1 = left + third
    m2 = right - third
    # m1, m2 = sample(range(left + 1, right - 1), 2)


    if m1 <= left:
        m1 = left + 1

    if m2 >= right:
        m2 = right - 1

    if data[m1] < data[m2]:
        swap(data, m1, left)
        swap(data, m2, right)
    else:
        swap(data, m1, right)
        swap(data, m2, left)
    # pivots
    pivot1 = data[left]
    pivot2 = data[right]

    # pointers
    less = left + 1
    great = right - 1

    # sorting
    k = less
    # for k in range(less, great+1):
    while k <= great:
        if data[k] < pivot1:
            swap(data, k, less)
            less += 1

        elif data[k] > pivot2:
            while k < great and data[great] > pivot2:
                great -= 1

            swap(data, k, great)
            great -= 1

            if data[k] < pivot1:
                swap(data, k, less)
                less += 1
        k += 1

    # swaps
    dist = great - less
    if dist < 13:
        div += 1

    swap(data, less-1, left)
    swap(data, great+1, right)

    # subarrays
    dualPivotQuicksort(data, left, less - 2, div)
    dualPivotQuicksort(data, great + 2, right, div)

    # equal elements
    if (dist > (len - 13)) and (pivot1 != pivot2):
        k = less
        # for k in range(less, great + 1):
        while k <= great:
            if data[k] == pivot1:
                swap(data, k, less)
                less += 1
            elif data[k] == pivot2:
                swap(data, k, great)
                great -= 1
                if data[k] == pivot1:
                    swap(data, k, less)
                    less += 1
            k += 1
    # subarray
    if pivot1 < pivot2:
        dualPivotQuicksort(data, less, great, div)


def sort_rec(data, fromIndex, toIndex):
    dualPivotQuicksort(data, fromIndex, toIndex - 1, 3)


def quicksort(data):
    sort_rec(data, 0, len(data))


if __name__ == "__main__":
    from random import randint
    L1 = [randint(-10000, 10000) for i in range(10000)]
    L2 = L1.copy()
    quicksort(L1)
    L2.sort()
    print(L1)
    print(L2)
    print(L1 == L2)
