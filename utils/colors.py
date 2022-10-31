def __get_color(rgb: tuple):
    (red, green, blue) = rgb
    return f"\033[38;2;{red};{green};{blue}m"


def colored(*text: str, hex: str = "#a232a8") -> str:
    text = (str(t) for t in text)
    rgb = tuple(int(hex.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
    return f"\033[4m{__get_color(rgb)}{''.join(text)}\033[0m\033[0m"
