# Day 2: Red Nosed Reports

Turns out monday is a lot worse day for these than a sunday,
so I had to solve part two on day 3 actually. And I only have my
naive solutions to show, but here they come.

On day two we had some safe and unsafe reports and we had to check their
validities.

## Part 1:

We have an input like this:
```
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
```

The rows are reports, columns are levels. The report is safe if: 
1. All numbers are either ascending or descending
2. The difference between neighboring numbers has to be 3 at most
And we just have to check how many reports are safe.

This calls for a simple loop:
```python
count: int = 0
for report in text:
    levels: list[int] = [int(x) for x in report.split()]
    if is_safe(levels):
        count += 1

return count
```

So quite literally just iterate over rows, turn each row into a list of numbers
and run the `is_safe()` function on the report. If it is, increment the count.

The fun part is of course the `is_safe()` function:
```python
def is_safe(levels: list[int]) -> bool:
    # sample the first two numbers to see if we are ascending
    descending: bool = levels[0] > levels[1]
    for i in range(1, len(levels)):

        # Check if items are at most 3 apart
        if abs(levels[i] - levels[i - 1]) > 3:
            return False

        # Check that we do differ, early return if so
        if levels[i - 1] == levels[i]:
            return False

        # Check if ascending or descending is continuing
        if descending:
            if levels[i - 1] < levels[i]:
                return False
        else:
            if levels[i - 1] > levels[i]:
                return False

    # If checks pass, return True
    return True
```

Here I sample the first two numbers and find out if the report is ascending or
descending. Then I loop through pairs of numbers, and check whether the
conditions are met. If the report is unsafe, I just return False immediately.

Only even a little little smart thing here is that I check whether the numbers are same before checking ascending/descending, so I avoid one if statement in those
cases.

This runs in 0.0018 seconds and it's a work day so on we go to part 2!


## Part 2

Now we are allowed to remove just one level from the report, and if it's safe
that way, it is considered safe. We need to add tolerance for one error.

I at first tried to make a tolerant version of the `is_safe()` function, but
that idea got lost in the edge cases. The most naive solution is to just try
popping every item of the report and checking whether those are safe or not. If
even one such sublist is safe, then we can add that to the count of valid ones.

```python
count: int = 0
for report in text:
    levels: list[int] = [int(x) for x in report.split()]
    for i in range(len(levels)):
        lev = levels.copy()
        _ = lev.pop(i)
        if is_safe(lev):
            count += 1
            break

return count
```

And that is what I do. It will break out of the inner loop, so when it finds the
first safe sublist, the report is accepted and count incremented.

We get 4541 calls of `is_safe()` with the tolerance added, when in part one we
had only 1000, one for each row in the input. Still this ran in 0.0041s so
nothing to complain in here.

I bet we could somehow count errors in the reports and reduce our complexity
a little, but I have no time for that now.

Oh yes also the memory consumption must be horrendeous because I copy the report
for every sublist just to pop one item from it, but I didn't run out of memory
so, this will do!
