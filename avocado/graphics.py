"""
PNG Image Graphics Engine & TrueColor Terminal Renderer v2.0.0
Renders high-definition PNG image assets (assets/avocado_logo.png) with transparent background
and dynamic theme color reaction.
"""
import os
import sys
import subprocess
import struct
import tempfile

def load_bmp_pixels(bmp_path):
    """Parses uncompressed 24-bit / 32-bit BMP file into 2D RGB tuple list."""
    try:
        with open(bmp_path, "rb") as f:
            data = f.read()

        if data[:2] != b'BM':
            return [], 0, 0

        pixel_offset = struct.unpack("<I", data[10:14])[0]
        width, height = struct.unpack("<ii", data[18:26])
        bpp = struct.unpack("<H", data[28:30])[0]

        if bpp not in (24, 32):
            return [], 0, 0

        row_bytes = ((width * bpp + 31) // 32) * 4
        pixels = []

        for y in range(abs(height) - 1, -1, -1):
            row = []
            row_offset = pixel_offset + y * row_bytes
            for x in range(width):
                px_idx = row_offset + x * (bpp // 8)
                if px_idx + 2 < len(data):
                    b_val, g_val, r_val = data[px_idx], data[px_idx+1], data[px_idx+2]
                    row.append((r_val, g_val, b_val))
                else:
                    row.append((0, 0, 0))
            pixels.append(row)

        return pixels, width, abs(height)
    except Exception:
        return [], 0, 0

def render_truecolor_pixel_matrix(image_path, colors=None, width=22):
    """
    Converts PNG image file into transparent 24-bit TrueColor RGB Half-Block (▄) Matrix.
    Masks out black/dark background pixels so terminal background shows through transparently,
    and applies active theme tinting to avocado pixels.
    """
    tmp_fd, tmp_bmp = tempfile.mkstemp(suffix=".bmp", prefix="avocado_term_")
    os.close(tmp_fd)

    try:
        subprocess.run(
            ["sips", "-s", "format", "bmp", image_path, "--resampleWidth", str(width), "--out", tmp_bmp],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
        )
        pixels, w, h = load_bmp_pixels(tmp_bmp)
        if not pixels or h < 2:
            return []

        p_code = colors.get("primary", "\033[38;2;86;180;89m") if colors else "\033[38;2;86;180;89m"
        a_code = colors.get("accent", "\033[38;2;163;209;107m") if colors else "\033[38;2;163;209;107m"
        h_code = colors.get("header", "\033[38;2;244;208;63m") if colors else "\033[38;2;244;208;63m"
        reset = "\033[0m"

        lines = []
        for y in range(0, h - 1, 2):
            line = ""
            top_row = pixels[y]
            bot_row = pixels[y+1]
            for x in range(w):
                tr, tg, tb = top_row[x]
                br, bg, bb = bot_row[x]

                top_bg_dark = (tr + tg + tb) < 35
                bot_bg_dark = (br + bg + bb) < 35

                if top_bg_dark and bot_bg_dark:
                    line += " "
                elif top_bg_dark:
                    if br > 180 and bg > 140:
                        line += f"{h_code}▄{reset}"
                    elif bg > br and bg > bb:
                        line += f"{a_code}▄{reset}"
                    else:
                        line += f"{p_code}▄{reset}"
                elif bot_bg_dark:
                    if tr > 180 and tg > 140:
                        line += f"{h_code}▀{reset}"
                    elif tg > tr and tg > tb:
                        line += f"{a_code}▀{reset}"
                    else:
                        line += f"{p_code}▀{reset}"
                else:
                    line += f"\033[48;2;{tr};{tg};{tb}m\033[38;2;{br};{bg};{bb}m▄{reset}"
            lines.append(line)

        return lines
    except Exception:
        return []
    finally:
        if os.path.exists(tmp_bmp):
            try: os.remove(tmp_bmp)
            except Exception: pass

def get_avocado_graphic(colors=None, width=22):
    """
    Returns an elegant Avocado Teardrop Shape ASCII Graphic that dynamically
    reacts to active theme colors (Avocado, Matrix, Dracula, Ocean, Amber).
    """
    if not colors:
        colors = {
            "primary": "\033[38;2;86;180;89m",
            "accent": "\033[38;2;163;209;107m",
            "header": "\033[38;2;244;208;63m",
            "text": "\033[38;2;230;237;243m",
            "muted": "\033[38;2;110;118;129m",
            "border": "\033[38;2;50;80;50m"
        }

    p = colors.get("primary", "\033[32m")
    a = colors.get("accent", "\033[36m")
    h = colors.get("header", "\033[33m")
    m = colors.get("muted", "\033[90m")
    r = "\033[0m"

    # Symmetrical Teardrop Avocado ASCII Shape
    return [
        f"             {m}. .{r}",
        f"            {p}/{r}   {p}\\{r}",
        f"           {p}/{r} {a}(o){r} {p}\\{r}",
        f"          {p}/{r}     {p}\\{r}",
        f"         {p}/{r}  {a}.---.{r}  {p}\\{r}",
        f"        {p}|{r}  {a}/ {h}(O){a} \\{r}  {p}|{r}",
        f"        {p}|{r} {a}| {h}(###){a} |{r} {p}|{r}",
        f"        {p}|{r}  {a}\\ {h}(O){a} /{r}  {p}|{r}",
        f"         {p}\\{r}  {a}`---'{r}  {p}/{r}",
        f"          {p}\\{r}       {p}/{r}",
        f"           {p}`-----'{r}"
    ]




