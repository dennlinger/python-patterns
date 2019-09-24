"""
An in-depth comparison of performance of dictionary insertion across several Python data structures.
This file compares the test runs I have evaluated on this, as well as a minimal implementation of
both a static insertion scenario, and a repeated function call to larger values.
"""

import timeit
import numpy as np
import string

# Classic try-except construct. By far the slowest, but at least with proper error handling.
force = """\
d = {}
for el in test:
    try:
        d[el] += 1
    except KeyError:
        d[el] = 0
"""

# Two-pass solution that first creates a dict with all encountered values as keys, and then
# a second pass during which the values are actually counted.
sample = """\
d = {el:0 for el in test}
for val in test:
    d[val] += 1
"""

# Available Counter data structure is by far the most convenient to use, and also offers
# nice downstream functions, such as .most_common()
count = """\
d = Counter(test)
"""

# This works on the regular dict() structure, and utilizes .get() to return a default element.
# Against all expectations this turns out to be a very good all-rounder solution,
# and offers way faster performance than default dicts.
getter = """\
d = {}
for val in test:
    temp = d.get(val, 0)
    temp += 1
    d[val] = temp
"""

# Essentially the same construct as in getter, but with marginally improved speed due to the
# inline code representation. I honestly know too little about the internals, and would
# well blame the performance difference on some multi-line string handling of timeit...
getter_v2 = """\
d = {}
for val in test:
    d[val] = d.get(val, 0) + 1
"""

# defaultdict implementation. Very similar to the two above, but with slighty more concise
# notation. Another reason as to why this is not a preferred solution is that the
# above solutions can be easily pickled, while defaultdict, similar to Counter,
# requires an additional conversion.
default = """\
d =  defaultdict(lambda: 0)
for val in test:
    d[val] += 1
"""


def generate_inserts(n):
    return ["".join(np.random.choice(list(string.ascii_letters), 4)) for _ in range(n)]


def generate_single_insert():
    return "".join(np.random.choice(list(string.ascii_letters), 1))


# Further evaluation, but with values created on the fly.
# With the runtimes for a single iteration, variance is now becoming very close to what
# could be statistically insignificant, but overall a similar trend can be observed.

live_force = """\
d = {}
for _ in range(10000):
    el = generate_single_insert()
    try:
        d[el] += 1
    except KeyError:
        d[el] = 0
"""

live_sample = """\
test = [generate_single_insert() for _ in range(10000)]
d = {el:0 for el in test}
for val in test:
    d[val] += 1
"""

live_count = """\
test = [generate_single_insert() for _ in range(10000)]
d = Counter(test)
"""

live_getter = """\
d = {}
for _ in range(10000):
    val = generate_single_insert()
    temp = d.get(val, 0)
    temp += 1
    d[val] = temp
"""

live_getter_v2 = """\
d = {}
for _ in range(10000):
    val = generate_single_insert()
    d[val] = d.get(val, 0) + 1
"""

live_default = """\
d =  defaultdict(lambda: 0)
for _ in range(10000):
    val = generate_single_insert()
    d[val] += 1
"""


if __name__ == "__main__":
    test = generate_inserts(10000)

    number = 100

    t1 = timeit.timeit(force, setup="from __main__ import test", number=number)
    print("Time for forced insertion: {:.6f} s".format(t1/number))

    t2 = timeit.timeit(sample, setup="from __main__ import test", number=number)
    print("Time for sample-first insertion: {:.6f} s".format(t2/number))

    t3 = timeit.timeit(count, setup="from __main__ import test; from collections import Counter", number=number)
    print("Time for Counter: {:.6f} s".format(t3/number))

    t4 = timeit.timeit(getter, setup="from __main__ import test", number=number)
    print("Time for getter v1: {:.6f} s".format(t4/number))

    t5 = timeit.timeit(getter_v2, setup="from __main__ import test", number=number)
    print("Time for getter v2: {:.6f} s".format(t5/number))

    t6 = timeit.timeit(default, setup="from __main__ import test; from collections import defaultdict", number=number)
    print("Time for default dict: {:.6f} s".format(t6/number))

    number = 50

    tt1 = timeit.timeit(live_force, setup="from __main__ import generate_single_insert", number=number)
    print("Time for live forced insertion: {:.6f} s".format(tt1/number))

    tt2 = timeit.timeit(live_sample, setup="from __main__ import generate_single_insert", number=number)
    print("Time for live sample-first insertion: {:.6f} s".format(tt2/number))

    tt3 = timeit.timeit(live_count, setup="from __main__ import generate_single_insert; from collections import Counter", number=number)
    print("Time for live Counter: {:.6f} s".format(tt3/number))

    tt4 = timeit.timeit(live_getter, setup="from __main__ import generate_single_insert", number=number)
    print("Time for live getter v1: {:.6f} s".format(tt4/number))

    tt5 = timeit.timeit(live_getter_v2, setup="from __main__ import generate_single_insert", number=number)
    print("Time for live getter v2: {:.6f} s".format(tt5/number))

    tt6 = timeit.timeit(live_default, setup="from __main__ import generate_single_insert; from collections import defaultdict", number=number)
    print("Time for live default dict: {:.6f} s".format(tt6/number))
