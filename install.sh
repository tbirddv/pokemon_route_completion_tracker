#!/bin/bash

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAIN_PY="$SCRIPT_DIR/main.py"

# Check if main.py exists
if [ ! -f "$MAIN_PY" ]; then
    echo -e "${RED}Error: main.py not found in $SCRIPT_DIR${NC}"
    echo "Please run this script from the project root directory."
    exit 1
fi

# Check if main.py has the shebang
if ! head -n 1 "$MAIN_PY" | grep -q "#!/usr/bin/env python3"; then
    echo -e "${RED}Error: main.py missing proper shebang line${NC}"
    echo "Expected: #!/usr/bin/env python3"
    exit 1
fi

# Determine the appropriate bin directory
if [ -d "$HOME/.local/bin" ]; then
    BIN_DIR="$HOME/.local/bin"
elif [ -d "$HOME/bin" ]; then
    BIN_DIR="$HOME/bin"
else
    echo -e "${YELLOW}Creating $HOME/.local/bin directory...${NC}"
    mkdir -p "$HOME/.local/bin"
    BIN_DIR="$HOME/.local/bin"
fi

SYMLINK_PATH="$BIN_DIR/poketracker"

# Check if symlink already exists
if [ -L "$SYMLINK_PATH" ]; then
    echo -e "${YELLOW}Symlink already exists at $SYMLINK_PATH${NC}"
    read -p "Do you want to replace it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 0
    fi
    rm "$SYMLINK_PATH"
elif [ -f "$SYMLINK_PATH" ]; then
    echo -e "${RED}Error: A file already exists at $SYMLINK_PATH${NC}"
    echo "Please remove it manually and run the installer again."
    exit 1
fi

# Make main.py executable
chmod +x "$MAIN_PY"

# Create symlink to main.py
ln -s "$MAIN_PY" "$SYMLINK_PATH"

echo -e "${GREEN}✓ Successfully created symlink: $SYMLINK_PATH -> $MAIN_PY${NC}"

# Check if the bin directory is in PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo -e "${YELLOW}Warning: $BIN_DIR is not in your PATH.${NC}"
    echo "Add the following line to your shell configuration file (.bashrc, .zshrc, etc.):"
    echo ""
    echo "    export PATH=\"\$PATH:$BIN_DIR\""
    echo ""
    echo "Then restart your terminal or run: source ~/.bashrc"
    echo ""
    echo "Alternatively, you can run the command directly:"
    echo "    $SYMLINK_PATH"
else
    echo -e "${GREEN}✓ $BIN_DIR is already in your PATH${NC}"
    echo ""
    echo "You can now use the command anywhere:"
    echo "    poketracker --help"
fi

echo ""
echo "Installation complete!"