"""
Based on a suggestion by Domso, who argued that O-notation is sometimes silly.
Specifically, whether sets are actually a viable alternative to a (theoretically more
inefficient) "direct solution". For his reference, see:
https://quick-bench.com/q/IWu6r5eNUkkUfVjxSZ04gp4V3PQ
"""

from timeit import timeit

if __name__ == "__main__":
    # Follow creation of lists from Domso's script.
    list1 = []
    list2 = []
    for i in range(10000):
        list1.append(i * 2)
        list2.append(i * 4)
        list1.append(i * 6)
        list2.append(i * 3)

    number = 1000

    appr1 = timeit("res = set(list1).intersection(set(list2))", "from __main__ import list1, list2", number=number)
    print(f"Set intersection took {appr1/number:.6f} s per iteration")

    stmt = """ 
intersection = []
# supposedly more efficient according to docs than sorted(list1)
list1.sort()
list2.sort()
idx1 = 0
idx2 = 0
while idx1 < len(list1) and idx2 < len(list2):
    if list1[idx1] == list2[idx2]:
        intersection.append(list1[idx1])
        idx1 += 1
        idx2 += 1
    elif list1[idx1] < list2[idx2]:
        idx1 += 1
    else:
        idx2 += 1
    """
    appr2 = timeit(stmt, "from __main__ import list1, list2", number=number)
    print(f"Sorted lists took {appr2/number:.6f} s per iteration")