#!/usr/bin/env bash
# Avocado Terminal App One-Line Installer Script
set -e

echo "=================================================="
echo " 🥑 Installing Avocado macOS Terminal App..."
echo "=================================================="

INSTALL_DIR="$HOME/.avocado"
BIN_DIR="/opt/homebrew/bin"

if [ ! -w "$BIN_DIR" ]; then
    BIN_DIR="/usr/local/bin"
fi

if [ ! -w "$BIN_DIR" ]; then
    BIN_DIR="$HOME/.local/bin"
    mkdir -p "$BIN_DIR"
fi

# Clone or update repository
if [ -d "$INSTALL_DIR" ]; then
    echo "Updating existing Avocado installation..."
    cd "$INSTALL_DIR" && git pull --quiet origin main || true
else
    echo "Cloning Avocado repository..."
    git clone --quiet https://github.com/RnR-io/Avacado.git "$INSTALL_DIR"
fi

chmod +x "$INSTALL_DIR/bin/avocado"

# Create global executable symlinks for both avocado and avacado
ln -sf "$INSTALL_DIR/bin/avocado" "$BIN_DIR/avocado"
ln -sf "$INSTALL_DIR/bin/avocado" "$BIN_DIR/avacado"

echo "--------------------------------------------------"
echo "✅ Avocado successfully installed in $BIN_DIR!"
echo ""
echo "To launch Avocado anytime, run:"
echo "   avocado  (or avacado)"
echo "=================================================="
