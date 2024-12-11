# Day 3: Mull it over

## Part 1:
Today we have some input like this
```
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
```
and we have to find all `mul(a,b)` strings and multiply `a` and `b` together.

Luckily when I was 15 or so I had nothing better to do than to learn regexes, so
this one is easy. Let's start

```
mul\((\d+?),(\d+?)\)
```
is the regex I came up with, it works like this:
- `mul` matches the literal characters _mul_
- `\(` matches a _(_  character. It needs to be escaped with the slash
- `(\d+?)` matches one or more digits, stopping at the first non-digit
    character. The parentheses (unesacped) make it into a capture group, so we
    can retrieve the matched characters later
- `,` matches a literal _,_
- `(\d+?)` is the same as before
- `\)` matches a _)_ sign

This way we can search for all matches of the pattern, and get numbers `a` and
`b` from them. In python you do it like this
```python
pattern: re.Pattern[str] = re.compile(r"mul\((\d+?),(\d+?)\)")
instructions: list[str] = re.findall(pattern, text)
pairs: list[tuple[int, int]] = [(int(a), int(b)) for a, b in instructions]
```
I compile the pattern beforehand to speed things up. Now we can just multiply
all `a` and `b` together and sum those up:
```python
sums: list[int] = [a * b for a, b in pairs]
return sum(sums)
```
Which get's us to the correct result in 0.0008s. But I have many intermediate
variables we could get rid of:
```python
pattern: re.Pattern[str] = re.compile(r"mul\((\d+?),(\d+?)\)")
return sum([int(a) * int(b) for a, b in re.findall(pattern, text)])
```
Which gets us down to 0.0004s. Quite nice. I've heard that regex is slow and
manual parsing is fast, so I wanted to try that as well:
```python
length: int = len(text)

numbers: str = "0123456789"
reading_first_number: bool = False
reading_second_number: bool = False
number1: str = ""
number2: str = ""

count: int = 0

for i in range(4, length - 1):
    buff = text[i - 3 : i + 1]
    if buff == "mul(":
        reading_first_number = True
        continue

    c: str = text[i]
    if reading_first_number:
        if c in numbers:
            number1 += c
            continue
        elif c == ",":
            reading_first_number = False
            reading_second_number = True
            continue
        else:
            reading_first_number = False
            number1 = ""
            continue

    if reading_second_number:
        if c in numbers:
            number2 += c
            continue
        elif c == ")":
            # print(number1, " ", number2)
            reading_second_number = False
            count += int(number1) * int(number2)
            number1 = ""
            number2 = ""
            continue
        else:
            reading_first_number = False
            reading_second_number = False
            number1 = ""
            number2 = ""
            continue

return count
```
Which works but runs on 0.0040s. Ten times slower than the regex implementation.
I have many allocations here, which might be the problem, but without moving to
Rust or C, I felt optimizing this any further would be futile. On to part 2!

## Part 2

Now we have to adhere to `do()` and `don't()` instructions in the input as well.
Inside a do-block we multiply and count, inside a don't-block we don't.

For some reason my brain didn't want to go with the regex-route, so I decided to
use the hand-parser and track whether we are inside a do or not there:

```python
length: int = len(text)

numbers: str = "0123456789"
reading_first_number: bool = False
reading_second_number: bool = False
number1: str = ""
number2: str = ""

in_do: bool = True

count: int = 0

for i in range(4, length - 1):
    if in_do:
        if i > 7 and text[i - 6 : i + 1] == "don't()":
            in_do = False
            continue

        buff = text[i - 3 : i + 1]
        if buff == "mul(":
            reading_first_number = True
            continue

        c: str = text[i]
        if reading_first_number:
            if c in numbers:
                number1 += c
                continue
            elif c == ",":
                reading_first_number = False
                reading_second_number = True
                continue
            else:
                reading_first_number = False
                number1 = ""
                continue

        if reading_second_number:
            if c in numbers:
                number2 += c
                continue
            elif c == ")":
                # print(number1, " ", number2)
                global no_pairs
                no_pairs.append((int(number1), int(number2)))
                reading_second_number = False
                count += int(number1) * int(number2)
                number1 = ""
                number2 = ""
                continue
            else:
                reading_first_number = False
                reading_second_number = False
                number1 = ""
                number2 = ""
                continue
    else:
        if i > 4 and text[i - 3 : i + 1] == "do()":
            in_do = True
            continue

return count
```

It is just a state machine following if we have had a don't or a do last, and
counting numbers in the muls. It's somewhat slow: 0.0044s, but it's still O(n)
so I think we are fine here. I would like to write that regex though...
