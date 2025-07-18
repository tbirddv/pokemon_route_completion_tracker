# Pokemon Route Completion Tracker

A comprehensive command-line tool for tracking Pokemon completion across different games and areas. Built for completionists who want systematic area-by-area progress tracking with intelligent filtering and companion game support.

Currently supports all games in the North American Version of Generation 1: Pokemon Red, Pokemon Blue and Pokemon Yellow.

## Key Features
- **Area-based completion tracking** - See exactly what you need in each location
- **Smart item filtering** - Only shows encounters you can actually access
- **Version exclusive tracking** - Know which Pokemon to trade for
- **Evolution chain management** - Automatic status updates when catching
- **Progress visualization** - Terminal-friendly progress bars and percentages
- **Companion game support** - Track across multiple versions

## Requirements

- Python 3.10 or higher (developed and tested with Python 3.12)
- Linux/macOS (Works in WSL, standard Windows support not tested)

## Installation

### Option 1: Automated Installation (Recommended)

1. Clone or download this repository
2. Navigate to the project directory
3. Run the installation script:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

This will create a symlink called `poketracker` in your `~/.local/bin` directory (or `~/bin` if it exists) so you can use the command from anywhere.

If `~/.local/bin` is not in your PATH, the installer will provide instructions to add it.

### Option 2: Manual Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Make the main script executable:
   ```bash
   chmod +x main.py
   ```
4. Create a symlink manually:
   ```bash
   ln -s $(pwd)/main.py ~/.local/bin/poketracker
   ```
5. Ensure `~/.local/bin` is in your PATH by adding this to your shell config file (`.bashrc`, `.zshrc`, etc.):
   ```bash
   export PATH="$PATH:$HOME/.local/bin"
   ```

### Option 3: Run Directly

You can also run the program directly without installation:
```bash
python3 main.py [commands]
```

## Usage

After installation, you can use the `poketracker` command from anywhere:

```bash
# Start a new Pokemon Red save
poketracker new Red

# Check current configuration
poketracker config --list

# Mark Pikachu as caught
poketracker catch pikachu

# Get help
poketracker --help
```
### First Time Setup
```bash
# 1. Create a new save
poketracker new Red

# 2. Check what you need in your first area
poketracker area "Route 1"

# 3. As you play, mark Pokemon as caught
poketracker catch Pidgey
```

## Uninstalling

To remove the installed command:
```bash
chmod +x uninstall.sh
./uninstall.sh
```

Or manually remove the symlink:
```bash
rm ~/.local/bin/poketracker
```

## Commands
Unless otherwise noted flags are case-sensitive and positional arguments are not.

### new
Starts a new game. Only one save file can exist for a game at this time.

**Required Arguments:**
- `game_name`: Name of the game to create save data for, omitting the word "Pokemon" (e.g. 'Red', 'Blue', 'Yellow')

**Flags:**
- `-o`, `--overwrite`: Replaces existing save file with new data if it exists

**Examples:**
```bash
# Start a new Pokemon Red save
poketracker new Red

# Start a new Pokemon Blue save, overwriting existing data
poketracker new Blue --overwrite
```

### delete
Delete an existing game save.

**Optional Arguments:**
- `game_name`: Name of game to be deleted, omitting the word "Pokemon" (e.g. 'Red', 'Blue', 'Yellow'). If omitted, deletes the currently tracked game

**Examples:**
```bash
# Delete Pokemon Red save data
poketracker delete Red

# Delete the currently tracked game's save data
poketracker delete
```

### config
Allows viewing and modifying program-wide parameters.

**Defaults:**
- Tracked Game: None
- Companion Game Tracker: False
- Evolution Tracker: False

**Flags:**
- `-l`, `--list`: Prints the current config to standard out
- `-g`, `--game`: Change the currently tracked game
  - **Required arguments:** `game_name` - Name of game to be tracked, omitting the word "Pokemon" (e.g. 'Red', 'Blue', 'Yellow')
- `-c`, `--companion_tracker`: Toggles whether reports display information about other games in the same generation
- `-e`, `--evolution_track`: Toggles whether reports display information about Pokemon that can be obtained by evolving or breeding already caught Pokemon
- `-r`, `--reset`: Full app reset, deletes all save data in the default save folder and resets config to defaults

**Examples:**
```bash
# View current configuration
poketracker config --list

# Set Pokemon Red as the tracked game
poketracker config --game Red

# Toggle companion tracking on/off
poketracker config --companion_tracker

# Enable evolution tracking
poketracker config --evolution_track

# Reset all data and config
poketracker config --reset
```

### item
Tracks available items (e.g. HM Surf, Super Rod) for tracking possible encounter types in reports. Modifies settings for currently tracked game only.

**Flags:**
- `-s`, `--surf`: Toggles status of HM Surf
- `-OR`, `--old-rod`: Toggles status of Old Rod
- `-GR`, `--good-rod`: Toggles status of Good Rod
- `-SR`, `--super-rod`: Toggles status of Super Rod

**Examples:**
```bash
# Mark that you have HM Surf
poketracker item --surf

# Mark that you have the Good Rod
poketracker item --good-rod

# Toggle multiple items at once
poketracker item --surf --super-rod
```

### catch
Mark a Pokemon as caught in the currently tracked game.

**Required Arguments:**
- `pokemon_name`: The name of the Pokemon that was caught

**Examples:**
```bash
# Mark Pikachu as caught
poketracker catch pikachu

# Mark Charmander as caught
poketracker catch charmander
```

### evolve
Handles Pokemon evolutions. The command is flexible - you can specify either the Pokemon you're evolving FROM or the Pokemon you're evolving TO, and it will figure out what you meant.

**Required Arguments:**
- `pokemon_name`: The name of a Pokemon in an evolution chain. Can be either the current form or the desired evolved form

**Optional Arguments:**
- `--into`: For handling complex evolutions (like Eevee). Required if the Pokemon has multiple possible evolutions and you need to specify which one

**Examples:**
```bash
# Evolve Charmander into Charmeleon (works either way)
poketracker evolve charmander
# OR
poketracker evolve charmeleon

# Both commands above do the same thing if Charmander is caught and Charmeleon is "Evolvable"

# Handle Eevee's complex evolution (must specify target)
poketracker evolve eevee --into vaporeon
```

### hatch
Mark a Pokemon as caught from hatching. Handled the same as catching but provides different user output text.

**Note:**
Not used in Generation 1 Games

**Required Arguments:**
- `pokemon_name`: The name of the Pokemon that was hatched

**Examples:**
```bash
# Mark a hatched Magikarp
poketracker hatch magikarp
```

### reset-pokemon
Resets a Pokemon's status to uncaught.

**Required Arguments:**
- `pokemon_name`: Name of Pokemon to be reset

**Examples:**
```bash
# Reset Pikachu to uncaught (and Raichu if evolution tracking is enabled)
poketracker reset-pokemon pikachu

# Reset Charizard (and its pre-evolutions if evolution tracking is enabled)
poketracker reset-pokemon charizard
```

### area
Generates a report for a specific location in a game noting caught and uncaught Pokemon available in that area.

If Companion Tracking is enabled, will also display version exclusive Pokemon available in other games of the generation at that location.

If Evolution Tracking is enabled, will display Pokemon that can be caught in that area that you can get via evolving or breeding an already caught Pokemon in a separate list.

The default behavior of this command is a detailed report of all encounters you can see based on items available as tracked in your save game.

**Required Arguments:**
- area_name: Name of area to generate report for. Numbered Routes should include the word 'route' (e.g. `route 1`). Special value `random` or `-r` will randomly select an incomplete area

**Flags:**
- `-S`, `--simple`: Provides an area summary of Pokemon status that does not break down encounters by type. Cannot be used with other flags
- `-i`, `--items-needed`: Generates a report of items needed to complete the area, split into items you have and items you still need based on save data. Cannot be used with other flags
- `-w`, `--walking`: Overrides default behavior to display standard walking encounters (i.e. Tall Grass, Cave). Can be combined with other override flags
- `-f`, `--fishing`: Overrides default behavior to display all fishing encounters (i.e. Super Rod, Good Rod, Old Rod). Can be combined with other override flags
- `-s`, `--surfing`: Overrides default behavior to display all surfing encounters. Can be combined with other override flags
- `-o`, `--other`: Overrides default behavior to display all other encounter types (i.e. Trade, Gift, Headbutt, etc.). Can be combined with other override flags
- `-a`, `--all`: Overrides default behavior to display details of all possible encounters in an area
- `-C`, `--companion-details`: If companion tracking is enabled, toggles whether the companion game section of the report has the same level of detail as the tracked game or is summary only

**Examples:**
```bash
# Default smart report (shows only encounters you can access)
poketracker area "Route 1"

# Simple summary of Route 1
poketracker area "Route 1" --simple

# Detailed report of Viridian Forest showing all encounters
poketracker area "Viridian Forest" --all

# Show all fishing encounters in Route 12
poketracker area "Route 12" --fishing

# Show walking and surfing encounters in Route 19
poketracker area "Route 19" --walking --surfing

# Get a random incomplete area suggestion
poketracker area random

# Check what items you need to complete an area
poketracker area "Cerulean Cave" --items-needed
```

### pokemon-report
Generates a report for a specific Pokemon. Default behavior is to report status only.

**Required Arguments:**
- `pokemon_name`: Name of Pokemon to generate report for (e.g. pikachu)

**Flags:**
- `-l`, `--location`: Toggles additional information on where requested Pokemon can be found in the current game. If companion tracking is enabled, also displays locations in companion games

**Examples:**
```bash
# Check Pikachu's catch status
poketracker pokemon-report pikachu

# Get detailed location info for Dratini
poketracker pokemon-report dratini --location
```

### completion
Generates a report on the overall completion of the Pokedex for the currently tracked game. Default behavior is to display counts of Pokemon by status and percentage completion.

**Flags:**
- `-d`, `--detailed`: Causes report to also include lists of all Pokemon by status
- `-a`, `--areas`: Generate an area-by-area completion report with progress bars and percentages

**Examples:**
```bash
# Show completion summary
poketracker completion

# Show detailed completion with Pokemon lists
poketracker completion --detailed

# Show completion progress by area
poketracker completion --areas

# Show detailed area-by-area completion
poketracker completion --areas --detailed
```

### exclusives
Shows which version exclusives from companion games are still needed for the tracked game.

**Examples:**
```bash
# Show remaining version exclusives you need
poketracker exclusives
```

## Example Output

### Simple Area Report
```bash
Randomly selected area: Pokemon Tower

--- Simple Area Report for: Pokemon Tower in Pokemon Red ---

Caught:
  None

Uncaught Pokemon:
  Cubone, Gastly, Haunter
No Pokemon not found in this game can be caught in this area in companion games.

[░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 0.00% Complete.
```

### Pokemon Report
```bash
--- Basic Report for: #16 Pidgey in Pokemon Red ---

Status:
Caught

Locations Pidgey is found in the current game:

  Route 1, Route 12, Route 13, Route 14, Route 15, Route 2, Route 21, Route 24, Route 25, Route 3, Route 5, Route 6, Route 7, Route 8

Locations Pidgey is found in other games in this generation:
  Blue: Route 1, Route 2, Route 3, Route 5, Route 6, Route 7, Route 8, Route 12, Route 13, Route 14, Route 15, Route 21, Route 24, Route 25
  Yellow: Route 1, Route 2, Route 5, Route 6, Route 7, Route 8, Route 11, Route 12, Route 13, Route 21, Route 24, Route 25, Viridian Forest
```
## Example Workflows

### Basic Completion Workflow
```bash
# Start in a new area
poketracker area "Safari Zone"
# Output shows: Walking encounters you can access

# Catch Pokemon as you find them
poketracker catch "Nidoran♂"
poketracker catch Exeggcute

# Check progress with visual feedback
poketracker area "Safari Zone" -S
# Output: [████████░░] 80.5% Complete

# See overall progress
poketracker completion
```

### Version Exclusive Workflow
```bash
# See what version exclusives you still need
poketracker exclusives

# Check where to find them in other games  
poketracker pokemon-report <pokemon> --locations
```

### Smart Item Management
```bash
# Before getting Super Rod - shows basic encounters
poketracker area "Route 6" 

# After getting Super Rod - now shows Super Rod encounters as well
poketracker item --super-rod
poketracker area "Route 6"
```

## Data Structure
The tracker uses CSV files for encounter data:
- Generation 1:
    - local_gen_1.csv - Pokemon with game specific locations and evolution chains
    - kanto_gen_1.csv - Area Encounters by game version

Save Data Location
- Config: `~/.pokemon_tracker/config.json`
- Game Saves: `~/.pokemon_tracker/saves/<Game>/save.json`
- Automatic Backups: `~/.pokemon_tracker/.backups/<Game>/save_backup.json`

## Troubleshooting
Common Issues
- **No game currently being tracked**: Run `poketracker config --game <GameName>`
- **Pokemon not found**: Check spelling and that correct game is loaded
- **Area not found**: Use exact names, include "Route" for numbered routes. Run `poketracker completion --areas` for a list of area names
- **Save Corruption**: Should be handled when attempting to load. Backups can be accessed in the `.backups` directory

Getting Help
- Use `poketracker --help` for command overview
- Use `poketracker <command> --help` for specific command details

## Future Features

Future features may include (in no particular order):
- A GUI rather than CLI
- Support for other generations of pokemon games
- Search individual Pokemon to determine where it can be caught in all regions

## Contributions

This project is primarily for personal use, but suggestions and bug reports are welcome via Github issues.
