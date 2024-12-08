from dataclasses import dataclass


@dataclass
class Color:
    red: str = "\033[91m"
    blue: str = "\033[94m"
    green: str = "\033[92m"
    bold: str = "\033[1m"
    under: str = "\033[4m"
    end: str = "\033[0m"

    clear: str = "\033c"


def colorize(text: str, color: str) -> str:
    return f"{color}{text}{Color.end}"


def red(text: str) -> str:
    return colorize(text, Color.red)


def blue(text: str) -> str:
    return colorize(text, Color.blue)


def green(text: str) -> str:
    return colorize(text, Color.green)


def bold(text: str) -> str:
    return colorize(text, Color.bold)


def underline(text: str) -> str:
    return colorize(text, Color.under)


def clear():
    print(Color.clear)
