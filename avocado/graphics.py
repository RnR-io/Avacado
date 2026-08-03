"""
Transparent Theme-Adaptive Graphics Engine v1.8.0
Renders high-density detailed Avocado Art matching active themes (Avocado, Matrix, Dracula, Ocean, Amber)
with transparent background and responsive terminal height/width scaling.
"""
import os
import sys

def get_theme_colored_avocado(colors, mode="normal"):
    """
    Renders high-density detailed Avocado graphic tinting foreground pixels 
    with active theme colors and using transparent backgrounds.
    """
    p = colors["primary"]
    a = colors["accent"]
    h = colors["header"]
    r = "\033[0m"

    if mode == "compact":
        return [
            f"{a}      .------------.{r}",
            f"{a}    .'   .------.   '.{r}",
            f"{a}   /   .'   {h}@@{a}   '.   \\{r}",
            f"{a}  |   /   .----.   \\   |{r}",
            f"{a}  |  |   /  {p}(O){a} \\   |  |{r}",
            f"{a}  |  |  |  {p}(###){a}  |  |  |{r}",
            f"{a}  |  |   \\  {p}(O){a} /   |  |{r}",
            f"{a}  |   \\   '----'   /   |{r}",
            f"{a}   \\   '.        .'   /{r}",
            f"{a}    '.   '------'   .'{r}",
            f"{a}      '------------'{r}"
        ]

    # Ultra-detailed matching CRT reference image
    return [
        f"{a}          .------------------.{r}",
        f"{a}        .'                    '.{r}",
        f"{a}       /     ..-------------..  \\{r}",
        f"{a}      |    .'   .---------.   '. |{r}",
        f"{a}      |   /   .'   {h}.---.{a}   '.   \\|{r}",
        f"{a}      |  |   /    /     \\    \\   |{r}",
        f"{a}      |  |  |    |   {p}O{a}   |    |  |{r}",
        f"{a}      |  |  |    |  {p}(O){a}  |    |  |{r}",
        f"{a}      |  |   \\    \\     /    /   |{r}",
        f"{a}      |   \\   '.   {h}'---'{a}   .'   /{r}",
        f"{a}      |    '.   '---------'   .'{r}",
        f"{a}       \\     ''-------------''{r}",
        f"{a}        '.                    .'{r}",
        f"{a}          '------------------'{r}"
    ]
