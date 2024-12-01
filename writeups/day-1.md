# AOC 2024 - day 1: Historian hysteria

First day of AOC 2024 started with a historian who had left only their notes
behind and even those in disarray. Maybe the elves are running a startup:
someone with all the knowledge disappears, leaving absolutely no documentation
behind and it becomes the juniors problem. Anyway, to the solutions

## Part 1

We have an input with two columns of numbers:
```
3   4
4   3
2   5
1   3
3   9
3   3
```

We need to pair the numbers together based on their sorted positions, count
their difference and sum those differences up. Quite simple:

```python
list_1: list[int] = []
list_2: list[int] = []

for line in text:
    parts: list[str] = line.split(" ")
    a: int = int(parts[0])
    b: int = int(parts[-1])

    list_1.append(a)
    list_2.append(b)

list_1.sort()
list_2.sort()

comb: list[tuple[int, int]] = list(zip(list_1, list_2))

total = 0
for pair in comb:
    total += max(pair) - min(pair)

return total
```

I could have used a CsvReader here, but I found it easier to just split on
spaces and get the first and last items. then I just construct two lists from
the numbers. When I have the lists, I just sort them and zip them into pairs.
For those I can count the difference and sum them up.

Now this is just the very first naive solution, but it manages the whole actual
input in just 0.0012s.

As is the purpose of naive solutions, I figured out an optimisation while
writing this: we can skip constructing the lists entirely, just sum up the
columns and return their difference.

```python
sum_1: int = 0
sum_2: int = 0

for line in text:
    parts: list[str] = line.split(" ")
    sum_1 += int(parts[0])
    sum_2 += int(parts[-1])

return abs(sum_2 - sum_1)
```

Which churns through the input data in 0.0004s. I can't think a faster solution
right now, since any SIMD-capable libraries would add too much overhead, so on
to the second part!

## Part 2

We continue with the exact same input as always, but now we need to find out how
many times the values on the left side appear on the right side and multiply
each value by the number.

My naive solution is to construct a list from the values on the left, and
a dict from the values on the right, counting their occurences. Then I can loop
through the first column and add the value multiplied by it's occurences on the
right side to a total:

```python
    list_1: list[int] = []
    list_2: dict[int, int] = {}

    for line in text:
        parts: list[str] = line.split(" ")
        a: int = int(parts[0])
        b: int = int(parts[-1])

        list_1.append(a)

        if b in list_2:
            list_2[b] += 1
        else:
            list_2[b] = 1

    total: int = 0
    for x in list_1:
        if x in list_2:
            total += x * list_2[x]

    return total
```

Once again nothing fancy. At first I thought of using a set for the first list,
but I need to count all of the occurences from it, so that doesn't work. (But if
you look at the next line, you might get some ideas!)

Surely all of this hashing kills the performance already? No: 0.0007 seconds,
part 2 completed. Easy.

Well let's try to add a dict counting occurences on the first column as well,
just because why not.

```python
list_1: dict[int, int] = {}
list_2: dict[int, int] = {}

for line in text:
    parts: list[str] = line.split(" ")
    a: int = int(parts[0])
    b: int = int(parts[-1])

    if a in list_1:
        list_1[a] += 1
    else:
        list_1[a] = 1

    if b in list_2:
        list_2[b] += 1
    else:
        list_2[b] = 1

total: int = 0
for x in list_1:
    if x in list_2:
        total += x * list_1[x] * list_2[x]

return total
```

So exactly the same but we construct two dicts and sum just a little less in the
second loop. This slows us to 0.0008 seconds because hashing is often slower
than looping through a single layer.

## Summary

All in all this was a very easy warm-up with nothing crazy. Let's see if we actually need to start optimizing tomorrow!
