#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Find the poketracker command
POKETRACKER_PATH=$(which poketracker 2>/dev/null || echo "")

if [ -z "$POKETRACKER_PATH" ]; then
    # Check common locations
    for dir in "$HOME/.local/bin" "$HOME/bin"; do
        if [ -f "$dir/poketracker" ]; then
            POKETRACKER_PATH="$dir/poketracker"
            break
        fi
    done
fi

if [ -z "$POKETRACKER_PATH" ]; then
    echo -e "${YELLOW}poketracker command not found.${NC}"
    echo "It may have already been uninstalled."
    exit 0
fi

echo -e "${YELLOW}Found poketracker at: $POKETRACKER_PATH${NC}"

# Show what it links to if it's a symlink
if [ -L "$POKETRACKER_PATH" ]; then
    TARGET=$(readlink "$POKETRACKER_PATH")
    echo -e "${YELLOW}Links to: $TARGET${NC}"
fi

read -p "Do you want to remove it? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm "$POKETRACKER_PATH"
    echo -e "${GREEN}✓ Successfully removed poketracker${NC}"
else
    echo "Uninstall cancelled."
fi