def quicksort(list):
    dual_pivot_sort(list, 0, len(list)-1)

def dual_pivot_sort(list, start, top):
    if top <= start:
        return
    p = start
    q = top
    k = p+1
    h = k
    l = q-1
    if list[p] > list[q]:
        list[p], list[q] = list[q], list[p]
    while k <= l:
        # the last non-check index is l,as l+1 to top - 1 is the part III,
        # where all elements > list[top]
        if list[k] < list[p]:
            list[h], list[k] = list[k], list[h]
            # h is the first element of part II
            h += 1
            # increase h by 1, for pointing to the first element of part II
            k += 1
            # increase k by 1, because we have checked list[k]
        elif list[k] > list[q]:
            # l is the last element of part IV
            list[k], list[l] = list[l], list[k]
            # don't increase k, as we have not check list[l] yet
            l -= 1
            # after swap, we should compare list[k] with list[p] and list[q] again
        else: k += 1
        # no swap, then the current k-th value is in part II, thus we plus 1 to k
    h -= 1 # now,h is the last element of part I
    l += 1 # now, l is the first element of part III
    list[p], list[h] = list[h], list[p]
    list[q], list[l] = list[l], list[q]
    dual_pivot_sort(list, start, h-1)
    dual_pivot_sort(list, h+1, l-1)
    dual_pivot_sort(list, l+1, top)


if __name__ == "__main__":
    from random import randint
    L1 = [randint(-100, 100) for i in range(1000)]
    L2 = L1.copy()
    quicksort(L1)
    L2.sort()
    print(L1)
    print(L2)
    print(L1 == L2)