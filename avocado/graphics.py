"""
Terminal TrueColor Image Graphics Engine & Protocol Detector
Converts PNG/BMP images into true 24-bit RGB TrueColor Half-Block Image Matrix (▄)
or iTerm2 / Kitty / Sixel inline terminal graphics protocols.
"""
import os
import sys
import base64
import subprocess
import struct

def is_iterm2():
    term = os.environ.get("TERM_PROGRAM", "")
    return "iTerm" in term or "WezTerm" in term

def is_kitty():
    term = os.environ.get("TERM", "")
    return "kitty" in term or "ghostty" in term

def render_iterm2_image(image_path, width=20):
    """Renders image using iTerm2 / WezTerm Inline Images Protocol."""
    try:
        with open(image_path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        return f"\033]1337;File=inline=1;width={width}:{data}\007"
    except Exception:
        return ""

def load_bmp_pixels(bmp_path):
    """Parses uncompressed 24-bit / 32-bit BMP file into 2D RGB tuple list."""
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

    for y in range(abs(height) - 1, -1, -1): # BMP rows stored bottom-to-top
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

def render_truecolor_pixel_matrix(image_path, width=22):
    """
    Converts image file to 24-bit TrueColor Half-Block (▄) ANSI matrix.
    Renders 100% native color graphics in macOS Terminal.app, iTerm2, Kitty, Alacritty.
    """
    tmp_bmp = f"/tmp/avocado_term_{width}.bmp"
    try:
        subprocess.run(
            ["sips", "-s", "format", "bmp", image_path, "--resampleWidth", str(width), "--out", tmp_bmp],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
        )
        pixels, w, h = load_bmp_pixels(tmp_bmp)
        if not pixels or h < 2:
            return []

        lines = []
        # Process pairs of rows (top pixel = background, bottom pixel = foreground ▄)
        for y in range(0, h - 1, 2):
            line = ""
            top_row = pixels[y]
            bot_row = pixels[y+1]
            for x in range(w):
                tr, tg, tb = top_row[x]
                br, bg, bb = bot_row[x]
                # If dark/black background, skip or set bg
                line += f"\033[48;2;{tr};{tg};{tb}m\033[38;2;{br};{bg};{bb}m▄\033[0m"
            lines.append(line)

        return lines
    except Exception:
        return []

def get_avocado_graphic(width=22):
    """Returns true-color avocado graphic image lines or fallback."""
    asset_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "avocado_logo.png")
    if os.path.exists(asset_path):
        lines = render_truecolor_pixel_matrix(asset_path, width=width)
        if lines:
            return lines

    # Fallback high-density ASCII
    return [
        "       .------------.",
        "     .'   .------.   '.",
        "    /   .'   @@   '.   \\",
        "   |   /   .----.   \\   |",
        "   |  |   /  (O) \\   |  |",
        "   |  |  |  (###) |  |  |",
        "   |  |   \\  (O) /   |  |",
        "   |   \\   '----'   /   |",
        "    \\   '.        .'   /",
        "     '.   '------'   .'",
        "       '------------'"
    ]
