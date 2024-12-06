# AOC 2024 - Day 4: Ceres Search

I don't think day 4 was actually that hard, but boy did I struggle with it...

## Part 1

We have some input like
```
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
```
and we have to find all occurences of XMAS, but they can be reversed,
horizontal, vertical and diagonal.

At first I thought of scanning through the input with a 4x4 kernel. There I can
check for all possible occurences of XMAS like this:

```python
t: list[str] = text # Input
size: int = len(t)

for y in range(2, size - 2):
    for x in range(2, size - 2):
        kernel: list[str] = [
            t[y-2][x-2:x+1],
            t[y-1][x-2:x+1],
            t[y][x-2:x+1]
            t[y+1][x-2:x+1],
        ]

        # CHECK MATCHES
```

A kernel starting at 1,1 would look
like
```
S A M X
M X S X
S A M A
M A S A
```
Where the first row has a reversed `XMAS`!

Now that does kind of work, but there is a problem. Let's look at a kernel
starting at 0,1:
```
M M S X
S A M X
M X S X
S A M A
```
Here we have the same exact `SAMX`. We would have to keep a list of all the
matches we have had, and not count the ones already counted. That can be done
with a set of tuples of tuples containing the start and end coordinates of each
counted match, but I couldn't get that working for some reason. There was either
a problem with converting coordinates from kernel space to input space, or just
a fault in the way I stored the coordinates in the set.

That idea did seem error
prone, so instead of continuing with the solution, I realized I could separate
the scanning of lines and rows from scanning diagonals. If I just scan each line
first, then each column, and then use the kernel idea just for diagonals, that
should work? Probably, but I never implemented that: I didn't like the idea of
three separate passes, when I realized I could just construct strings from all
the lines, columns and diagonals, and just count `XMAS` and `SAMX` occurences on
all of those? (I know it's still three passes really...)

Joining the lines together is trivial, and technically unnecessary since the
input was a string of lines separated by `\n`s in the beginning. They have been
lost se we need to add them back with `"\n".join(t)`.

Columns require a little more work when I don't have the data in `np.arange`
which could be transformed easily. Here's how I do it:
```python
cols: str = ""
for x in range(size):
    for y in range(size):
        cols += t[y][x]

    cols += "\n"
```

And then the diagonals are the tricky part. Let's first plot the indexes of
a 4x4 grid:
```
0,0 0,1 0,2 0,3
1,0 1,1 1,2 1,3
2,0 2,1 2,2 2,3
3,0 3,1 3,2 3,3
```
The diagonals would then be
```
0,0
1,0 0,1
2,0 1,1 0,2
3,0 2,1 1,2 0,3
3,1 2,2 1,3
3,2 2,3
3,3
```

If we have the normal text in variable `rows` as a list of lines and column-wise
in `cols`, we can construct the diagonals with
```python
diag_1 = "" # From left-top to right-bottom
diag_2 = "" # From right-bottom to left-top

for i in range(n+1):
    for j in range(i):
        diag_1 += rows[i-j-1][j]
        diag_2 += cols[i-j-1][j]

    diag_1 += "\n"
    diag_2 += "\n"

for i in range(n,0,-1):
    for j in range(i-1):
        diag_1 += rows[n-j-1][j+1+(n-i)]
        diag_2 += cols[n-j-1][j+1+(n-i)]

    diag_1 += "\n"
    diag_2 += "\n"
```

And then the answer should be
```python
rows_str.count("XMAS") +
rows_str.count("MASX") +
cols_str.count("XMAS") +
cols_str.count("MASX") +
diag_1.count("XMAS") +
diag_1.count("MASX") +
diag_2.count("XMAS") +
diag_2.count("MASX")
```

Or so I think, but it is not. Counting also `M̀ASX` should effectively include
all four diagonals. Something is wrong, and I just couldn't get what it was, so
I turned to visualization!

First let's define some control sequences:
```python
class CC:
    RED: str = "\033[91m"
    BLUE: str = "\033[94m"
    GREEN: str = "\033[92m"
    BOLD: str = "\033[1m"
    UNDER: str = "\033[4m"
    END: str = "\033[0m"

    CLEAR: str = "\033c"
```
and a function that can draw the given input nicely on the screen, using these
colors:
```python
def print_text(
    text: list[str],
    red: list[tuple[int, int]],
    blue: list[tuple[int, int]],
    green: list[tuple[int, int]],
    bold: list[tuple[int, int]],
    curr: tuple[int, int],
):
    height: int = len(text)
    width: int = len(text[0])

    for y in range(height - 1):
        for x in range(width):
            if (y, x) in bold:
                print(CC.BOLD, end="")

            if (y, x) == curr:
                print(CC.UNDER, end="")

            if (y, x) in red:
                print(CC.RED, end="")

            if (y, x) in blue:
                print(CC.BLUE, end="")

            if (y, x) in green:
                print(CC.GREEN, end="")


            print(text[y][x], end=" ")
            print(CC.END, end="")

        print()
```

Now my idea is to scan through the input, marking every X as red. Let's start
with that!

```python
size: int = len(t)

red: list[tuple[int,int]] = []
blue: list[tuple[int,int]] = []
green: list[tuple[int,int]] = []
bold: list[tuple[int,int]] = []

print_text(t, red, blue, green, bold, (0,0))

for y in range(size - 1):
    for x in range(size - 1):
        print(CC.CLEAR)

        if t[y][x] == "X":
            red.append((y,x))

        print_text(t, red, blue, green, bold, (y,x))

        if t[y][x] == "X":
            time.sleep(0.5)
        else:
            time.sleep(0.1)
```
This very nicely scans through the grid and marks all the x'es.

Now I want to find all the possible lines containing XMAS from the X'es. They
can be found from this coordinate-grid

```
(y-3,x-3) (y-3,x-2) (y-3,x-1) (y-3, x ) (y-3,x+1) (y-3,x+2) (y-3,x+3)
(y-2,x-3) (y-2,x-2) (y-2,x-1) (y-2, x ) (y-2,x+1) (y-2,x+2) (y-2,x+3)
(y-1,x-3) (y-1,x-2) (y-1,x-1) (y-1, x ) (y-1,x+1) (y-1,x+2) (y-1,x+3)
( y ,x-3) ( y ,x-2) ( y ,x-1) ( y , x ) ( y ,x+1) ( y ,x+2) ( y ,x+3)
(y+1,x-3) (y+1,x-2) (y+1,x-1) (y+1, x ) (y+1,x+1) (y+1,x+2) (y+1,x+3)
(y+2,x-3) (y+2,x-2) (y+2,x-1) (y+2, x ) (y+2,x+1) (y+2,x+2) (y+2,x+3)
(y+3,x-3) (y+3,x-2) (y+3,x-1) (y+3, x ) (y+3,x+1) (y+3,x+2) (y+3,x+3)
```

Let's mark up the lines with blue! In the loop where I found the x'es we can
have:
```python
for y in range(size):
    for x in range(size):
        blue = [] # Reset the blues 
        print(CC.CLEAR)
        if t[y][x] == "X":
            red.append((y,x))

            blue.extend(((y - 1, x), (y - 2, x), (y - 3, x)))
            blue.extend(((y - 1, x + 1), (y - 2, x + 2), (y - 3, x + 3)))
            blue.extend(((y, x + 1), (y, x + 2), (y, x + 3)))
            blue.extend(((y + 1, x + 1), (y + 2, x + 2), (y + 3, x + 3)))
            blue.extend(((y + 1, x), (y + 2, x), (y + 3, x)))
            blue.extend(((y + 1, x - 1), (y + 2, x - 2), (y + 3, x - 3)))
            blue.extend(((y, x - 1), (y, x - 2), (y, x - 3)))
            blue.extend(((y - 1, x - 1), (y - 2, x - 2), (y - 3, x - 3)))
```

Ok then because we actually need the characters as well, not just the positions,
I wrote a function that returns me the lines stemming from y,x
```python
def get_lines(t: list[str], y: int, x: int, size: int) -> list[str]:
    res: list[str] = []

    if y >= 3:
        res.append(t[y][x] + t[y - 1][x] + t[y - 2][x] + t[y - 3][x])
    else:
        res.append("")

    if y >= 3 and x < size - 3:
        res.append(t[y][x] + t[y - 1][x + 1] + t[y - 2][x + 2] + t[y - 3][x + 3])
    else:
        res.append("")

    if x < size - 3:
        res.append(t[y][x] + t[y][x + 1] + t[y][x + 2] + t[y][x + 3])
    else:
        res.append("")

    if y < size - 3 and x < size - 3:
        res.append(t[y][x] + t[y + 1][x + 1] + t[y + 2][x + 2] + t[y + 3][x + 3])
    else:
        res.append("")

    if y < size - 3:
        res.append(t[y][x] + t[y + 1][x] + t[y + 2][x] + t[y + 3][x])
    else:
        res.append("")

    if y < size - 3 and x >= 3:
        res.append(t[y][x] + t[y + 1][x - 1] + t[y + 2][x - 2] + t[y + 3][x - 3])
    else:
        res.append("")

    if x >= 3:
        res.append(t[y][x] + t[y][x - 1] + t[y][x - 2] + t[y][x - 3])
    else:
        res.append("")

    if y >= 3 and x >= 3:
        res.append(t[y][x] + t[y - 1][x - 1] + t[y - 2][x - 2] + t[y - 3][x - 3])
    else:
        res.append("")

    return res
```
Not convoluted at all. I also check here wether the line is even possible, or
does it cross the boundaries of the input.

Now we can check the lines with this
```python
    ...

    lines: list[str] = get_lines(t, y, x, size)
    for line in lines:
        if line == "XMAS":
            count += 1

    ...
```

But I also want to mark them persistently, and I'm also a huge fan of repeating
my own code, the final result is this:
```python
def p1_naive(t: list[str]) -> int:
    height: int = len(t)
    width: int = len(t[0])

    count: int = 0

    red: list[tuple[int, int]] = []
    blue: list[tuple[int, int]] = []
    green: list[tuple[int, int]] = []
    bold: list[tuple[int, int]] = []

    print_text(t, red, blue, green, bold, (0, 0))

    for y in range(height - 1):
        for x in range(width):
            blue = []
            print(CC.CLEAR)
            if t[y][x] == "X":
                red.append((y, x))

                blue.extend(((y - 1, x), (y - 2, x), (y - 3, x)))
                blue.extend(((y - 1, x + 1), (y - 2, x + 2), (y - 3, x + 3)))
                blue.extend(((y, x + 1), (y, x + 2), (y, x + 3)))
                blue.extend(((y + 1, x + 1), (y + 2, x + 2), (y + 3, x + 3)))
                blue.extend(((y + 1, x), (y + 2, x), (y + 3, x)))
                blue.extend(((y + 1, x - 1), (y + 2, x - 2), (y + 3, x - 3)))
                blue.extend(((y, x - 1), (y, x - 2), (y, x - 3)))
                blue.extend(((y - 1, x - 1), (y - 2, x - 2), (y - 3, x - 3)))

                idx = [
                    (((y - 1, x), (y - 2, x), (y - 3, x))),
                    (((y - 1, x + 1), (y - 2, x + 2), (y - 3, x + 3))),
                    (((y, x + 1), (y, x + 2), (y, x + 3))),
                    (((y + 1, x + 1), (y + 2, x + 2), (y + 3, x + 3))),
                    (((y + 1, x), (y + 2, x), (y + 3, x))),
                    (((y + 1, x - 1), (y + 2, x - 2), (y + 3, x - 3))),
                    (((y, x - 1), (y, x - 2), (y, x - 3))),
                    (((y - 1, x - 1), (y - 2, x - 2), (y - 3, x - 3))),
                ]

                lines: list[str] = get_lines(t, y, x, width)
                for i, line in enumerate(lines):
                    if line == "XMAS":
                        count += 1
                        bold.extend(idx[i])
                        green.extend(idx[i])

            print_text(t, red, blue, green, bold, (y, x))

            if t[y][x] == "X":
                time.sleep(0.5)
            else:
                time.sleep(0.1)

    return count
```

All this leads up to this beautiful little animation:
![Cursors scanning the input text, marking every X with red, flashing rows,
columns and diagonals from the x'es as blue and marking found XMASes as green](aoc2024d4p1.gif "Day 4 Part 1 - visualized")

Which does result in the correct answer with both the example data and the real
input! And if we skip all the printing and waiting, it only takes 0.011s. Nice!
In the end the visualization part was fun, and it did help me see when mistakes
where happening, and it got me to the right answer. It did take maybe an hour or
so but we are not doing AOC to save time, but to learn!

Now I bet this code could and most definitely should be cleaned up, but I'm just
going to move on to part two.

## Part 2

So it turns out we actually don't give a damn about `XMAS` strings, we need to
find `MAS` strings that are shaped like an X. Let's forget about the X-shaped
requirement because it makes the problem way too easy, and think about `MAS`
strings that overlap in any way. Remember to read the problem...

One possibility is
```
M A S
A . .
S . .
```
where there is no central A or any other symbol, so my fancy visualization
approach doesn't work. However here it's not possible for the same row or column
to be counted twice, if we move with 3x3 kernels. Trust me, it can't happen. So
we go back to kernels!

As earlier, the kernels can be found like this
```python
height: int = len(t)
width: int = len(t[0])

count: int = 0

for y in range(1, height - 2):
    for x in range(1, width - 1):
        kernel: list[str] = [
                t[y-1][x-1:x+2],
                t[y][x-1:x+2],
                t[y+1][x-1:x+2]
        ]

        for kern in KERNELS:
            if kernel_matches(kernel, kern):
                count += 1
```

But what are `KERNELS` and `kernel_matches()`? Glad you asked! KERNELS is a list
of lists of strings, each containing a sample kernel with overlapping
`MAS`-strings in a unique way. There are 16 such kernels, and they look like
this:
```python
KERNELS: list[list[str]] = [
["M.S",
".A.",
"M.S,"],

["M.M",
".A.",
"S.S"],

["S.S",
".A.",
"M.M"],

["S.M",
".A.",
"S.M"],

[".M.",
"MAS",
".S."],

[".S.",
"SAM",
".M."],

[".M.",
"SAM",
".S."],

[".S.",
"MAS",
".M."],

["MAS",
"A..",
"S.."],

["..M",
"..A",
"MAS"],

["MAS",
"..A",
"..M"],

["S..",
"A..",
"MAS"],

["SAM",
"A..",
"M.."],

["..S",
"..A",
"SAM"],

["SAM",
"..A",
"..S"],

["M..",
"A..",
"SAM"],
]
```

Beautiful, aren't they. You can check, there are no other options. I think. The
dot's represent characters I don't care about. With these, I can just check the
current kernel against all of these, and increment the count by one everytime
one matches. The matching can be done with:
```python
def kernel_matches(a: list[str], b: list[str]) -> bool:
    size: int = len(a)
    for y in range(size):
        for x in range(size):
            if a[y][x] == "." or b[y][x] == ".":
                continue
            elif a[y][x] != b[y][x]:
                return False

    return True
```
And if we now run the original function with the example input, everything works
and the answer is correct! Put the full input on! What do you mean the answer is
too high? 

Remember when I forgot about the X-requirement? Turns out 12 of my 16 kernels do
not map out an X-MAS-pattern, but just random overlapping MASes. Se let's
comment out a few and try just with these ones:
```python
KERNELS: list[list[str]] = [
    ["M.S",
    ".A.",
    "M.S,"],

    ["M.M",
    ".A.",
    "S.S"],

    ["S.S",
    ".A.",
    "M.M"],

    ["S.M",
    ".A.",
    "S.M"]
]
```

Now we get the correct result! If you look closely, all the kernels do have
a central A and there are only two possible lines stemming from them, so with
the original visualization based solution this would have a) worked, b) been
probably faster than the 0.0406s we got now...

But we did get there! I leave all further improvements as an excercise to you and go practise my reading comprehension.
