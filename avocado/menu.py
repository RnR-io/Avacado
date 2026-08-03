"""
Interactive Arrow-Key Menu Selection Engine (Zero Dependencies)
Reads terminal raw keypresses for Up/Down/Left/Right arrow keys and Enter.
"""
import sys
import os
import tty
import termios

def get_keypress():
    """Reads a single keypress or ANSI arrow key sequence from standard input."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == '\x1b': # Escape sequence for arrow keys
            ch2 = sys.stdin.read(1)
            if ch2 == '[':
                ch3 = sys.stdin.read(1)
                if ch3 == 'A': return 'UP'
                if ch3 == 'B': return 'DOWN'
                if ch3 == 'C': return 'RIGHT'
                if ch3 == 'D': return 'LEFT'
            return 'ESC'
        if ch in ('\r', '\n'): return 'ENTER'
        if ch == '\x03': return 'CTRL_C'
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def run_menu(title, options, default_idx=0):
    """
    Renders an interactive menu allowing navigation via Arrow keys and selection via Enter.
    Returns selected index.
    """
    current = default_idx
    num_opts = len(options)

    while True:
        # Clear line and print menu options
        sys.stdout.write("\033[H\033[2J") # Clear screen
        sys.stdout.write(f"\033[1;32m{title}\033[0m\n")
        sys.stdout.write("Use \033[1mUP/DOWN/LEFT/RIGHT\033[0m arrows to navigate | Press \033[1mENTER\033[0m to select\n\n")

        for idx, opt in enumerate(options):
            if idx == current:
                sys.stdout.write(f" \033[1;42;30m ➔ {idx+1}. {opt} \033[0m\n")
            else:
                sys.stdout.write(f"    {idx+1}. {opt}\n")

        sys.stdout.flush()

        key = get_keypress()
        if key in ('UP', 'LEFT'):
            current = (current - 1) % num_opts
        elif key in ('DOWN', 'RIGHT'):
            current = (current + 1) % num_opts
        elif key == 'ENTER':
            return current
        elif key in ('q', 'Q', 'ESC', 'CTRL_C'):
            return num_opts - 1 # Quit option
        elif key.isdigit():
            val = int(key) - 1
            if 0 <= val < num_opts:
                return val
