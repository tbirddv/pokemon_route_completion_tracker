#!/usr/bin/env bash

# Bash completion for poketracker CLI.
_poketracker_match_list() {
    local cur cur_lc quote value candidate
    cur="$1"
    quote=""

    if [[ "$cur" == \"* || "$cur" == \'* ]]; then
        quote="${cur:0:1}"
        cur="${cur:1}"
    fi

    cur_lc="${cur,,}"
    shift
    COMPREPLY=()

    for value in "$@"; do
        [[ -z "$value" ]] && continue
        if [[ "${value,,}" == "$cur_lc"* ]]; then
            if [[ -n "$quote" ]]; then
                candidate="$quote$value$quote"
            else
                candidate="${value// /\\ }"
            fi
            COMPREPLY+=("$candidate")
        fi
    done
}

_poketracker_project_root() {
    local exe resolved
    exe="$(command -v poketracker 2>/dev/null || true)"
    [[ -z "$exe" ]] && return 1

    resolved="$(readlink -f "$exe" 2>/dev/null || true)"
    [[ -z "$resolved" ]] && resolved="$exe"
    dirname "$resolved"
}

_poketracker_games() {
    echo "Red"
    echo "Blue"
    echo "Yellow"
}

_poketracker_pokemon_names() {
    local root csv
    root="$(_poketracker_project_root)" || return 0
    csv="$root/Data/Pokemon/local_gen_1.csv"
    [[ -f "$csv" ]] || return 0

    awk -F',' 'NR > 1 {print $1}' "$csv"
}

_poketracker_area_names() {
    local root csv
    root="$(_poketracker_project_root)" || return 0
    csv="$root/Data/Locations/kanto_gen_1.csv"
    [[ -f "$csv" ]] || return 0

    awk -F',' 'NR > 1 {print $1}' "$csv"
}

_poketracker_tracked_save_pokemon_names() {
    local mode
    mode="$1"

    python3 - "$mode" <<'PY'
import json
import pathlib
import sys

mode = sys.argv[1]
home = pathlib.Path.home()
config_path = home / ".pokemon_tracker" / "config.json"

try:
    config = json.loads(config_path.read_text(encoding="utf-8"))
except Exception:
    sys.exit(0)

tracked_game = config.get("tracked_game")
if not tracked_game:
    sys.exit(0)

save_path = home / ".pokemon_tracker" / "saves" / tracked_game / "save.json"
if not save_path.exists():
    sys.exit(0)

try:
    save_data = json.loads(save_path.read_text(encoding="utf-8"))
except Exception:
    sys.exit(0)

for pokemon in save_data.get("pokemon", []):
    name = pokemon.get("name")
    status = pokemon.get("status", "")
    if not name:
        continue

    status_norm = str(status).strip().lower()

    if mode == "not_caught" and status_norm == "caught":
        continue
    if mode == "not_uncaught" and status_norm == "uncaught":
        continue
    if mode == "uncaught_only" and status_norm != "uncaught":
        continue

    print(name)
PY
}

_poketracker_tracked_save_area_names() {
    python3 - <<'PY'
import json
import pathlib
import sys

home = pathlib.Path.home()
config_path = home / ".pokemon_tracker" / "config.json"

try:
    config = json.loads(config_path.read_text(encoding="utf-8"))
except Exception:
    sys.exit(0)

tracked_game = config.get("tracked_game")
if not tracked_game:
    sys.exit(0)

save_path = home / ".pokemon_tracker" / "saves" / tracked_game / "save.json"
if not save_path.exists():
    sys.exit(0)

try:
    save_data = json.loads(save_path.read_text(encoding="utf-8"))
except Exception:
    sys.exit(0)

for location in save_data.get("locations", []):
    name = location.get("name")
    if name:
        print(name)
PY
}

_poketracker_tracked_save_evolve_base_names() {
    python3 - <<'PY'
import json
import pathlib
import sys

home = pathlib.Path.home()
config_path = home / ".pokemon_tracker" / "config.json"

try:
    config = json.loads(config_path.read_text(encoding="utf-8"))
except Exception:
    sys.exit(0)

tracked_game = config.get("tracked_game")
if not tracked_game:
    sys.exit(0)

save_path = home / ".pokemon_tracker" / "saves" / tracked_game / "save.json"
if not save_path.exists():
    sys.exit(0)

try:
    save_data = json.loads(save_path.read_text(encoding="utf-8"))
except Exception:
    sys.exit(0)

pokemon_list = save_data.get("pokemon", [])
by_name = {
    str(p.get("name", "")).strip().lower(): p
    for p in pokemon_list
    if p.get("name")
}

def is_actionable_uncaught(pokemon: dict) -> bool:
    devolutions = pokemon.get("devolutions", []) or []
    for d in devolutions:
        prev = by_name.get(str(d).strip().lower())
        if not prev:
            continue
        if str(prev.get("status", "")).strip().lower() == "caught":
            return True
    return False

ranked = []
for pokemon in pokemon_list:
    name = pokemon.get("name")
    if not name:
        continue

    status = str(pokemon.get("status", "")).strip().lower()
    evolutions = pokemon.get("evolutions", []) or []

    if status == "evolvable":
        rank = 0
    elif status == "caught" and evolutions:
        rank = 1
    elif status == "uncaught" and is_actionable_uncaught(pokemon):
        rank = 2
    else:
        rank = 3

    ranked.append((rank, str(name)))

for _, name in sorted(ranked, key=lambda item: (item[0], item[1])):
    print(name)
PY
}

_poketracker_tracked_save_evolution_targets() {
    local base_name
    base_name="$1"

    python3 - "$base_name" <<'PY'
import json
import pathlib
import sys

base_name = (sys.argv[1] or "").strip().lower()
if not base_name:
    sys.exit(0)

home = pathlib.Path.home()
config_path = home / ".pokemon_tracker" / "config.json"

try:
    config = json.loads(config_path.read_text(encoding="utf-8"))
except Exception:
    sys.exit(0)

tracked_game = config.get("tracked_game")
if not tracked_game:
    sys.exit(0)

save_path = home / ".pokemon_tracker" / "saves" / tracked_game / "save.json"
if not save_path.exists():
    sys.exit(0)

try:
    save_data = json.loads(save_path.read_text(encoding="utf-8"))
except Exception:
    sys.exit(0)

pokemon_map = {
    str(p.get("name", "")).strip().lower(): p
    for p in save_data.get("pokemon", [])
    if p.get("name")
}

base = pokemon_map.get(base_name)
if not base:
    sys.exit(0)

for evo in base.get("evolutions", []) or []:
    if not evo:
        continue
    evo_lc = str(evo).strip().lower()
    target = pokemon_map.get(evo_lc)
    # If target data exists, only suggest evolutions that are not already Caught.
    if target is not None:
        status = str(target.get("status", "")).strip().lower()
        if status == "caught":
            continue
    print(str(evo))
PY
}

_poketracker_completion() {
    local cur prev cmd evolve_base i
    local -a words
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    cmd=""

    # First non-option token after executable is treated as the command.
    for ((i=1; i<COMP_CWORD; i++)); do
        if [[ "${COMP_WORDS[i]}" != -* ]]; then
            cmd="${COMP_WORDS[i]}"
            break
        fi
    done

    if [[ -z "$cmd" ]]; then
        _poketracker_match_list "$cur" \
            new delete config item catch evolve hatch reset-pokemon area pokemon-report completion exclusives -h --help
        return 0
    fi

    case "$cmd" in
        new|delete)
            if [[ "$cur" == -* ]]; then
                if [[ "$cmd" == "new" ]]; then
                    _poketracker_match_list "$cur" -o --overwrite -h --help
                else
                    _poketracker_match_list "$cur" -h --help
                fi
            else
                mapfile -t words < <(_poketracker_games)
                _poketracker_match_list "$cur" "${words[@]}"
            fi
            return 0
            ;;
        config)
            if [[ "$prev" == "-g" || "$prev" == "--game" ]]; then
                mapfile -t words < <(_poketracker_games)
                _poketracker_match_list "$cur" "${words[@]}"
                return 0
            fi

            if [[ "$cur" == -* ]]; then
                _poketracker_match_list "$cur" \
                    -l --list -g --game -r --reset -c --companion_tracker -e --evolution_track -h --help
            else
                mapfile -t words < <(_poketracker_games)
                _poketracker_match_list "$cur" "${words[@]}"
            fi
            return 0
            ;;
        item)
            _poketracker_match_list "$cur" -s --surf -SR --super-rod -GR --good-rod -OR --old-rod -h --help
            return 0
            ;;
        catch|hatch|reset-pokemon|pokemon-report)
            if [[ "$cur" == -* ]]; then
                if [[ "$cmd" == "pokemon-report" ]]; then
                    _poketracker_match_list "$cur" -l --locations -h --help
                else
                    _poketracker_match_list "$cur" -h --help
                fi
            else
                if [[ "$cmd" == "catch" || "$cmd" == "hatch" ]]; then
                    mapfile -t words < <(_poketracker_tracked_save_pokemon_names "uncaught_only")
                elif [[ "$cmd" == "reset-pokemon" ]]; then
                    mapfile -t words < <(_poketracker_tracked_save_pokemon_names "not_uncaught")
                else
                    mapfile -t words < <(_poketracker_tracked_save_pokemon_names "all")
                fi

                if [[ ${#words[@]} -eq 0 ]]; then
                    mapfile -t words < <(_poketracker_pokemon_names)
                fi
                _poketracker_match_list "$cur" "${words[@]}"
            fi
            return 0
            ;;
        evolve)
            if [[ "$prev" == "--into" ]]; then
                evolve_base=""
                for ((i=1; i<${#COMP_WORDS[@]}; i++)); do
                    if [[ "${COMP_WORDS[i]}" == "evolve" ]]; then
                        if ((i + 1 < ${#COMP_WORDS[@]})); then
                            evolve_base="${COMP_WORDS[i+1]}"
                        fi
                        break
                    fi
                done

                mapfile -t words < <(_poketracker_tracked_save_evolution_targets "$evolve_base")
                if [[ -z "$evolve_base" && ${#words[@]} -eq 0 ]]; then
                    mapfile -t words < <(_poketracker_tracked_save_pokemon_names "all")
                fi
                if [[ -z "$evolve_base" && ${#words[@]} -eq 0 ]]; then
                    mapfile -t words < <(_poketracker_pokemon_names)
                fi
                _poketracker_match_list "$cur" "${words[@]}"
                return 0
            fi

            if [[ "$cur" == -* ]]; then
                _poketracker_match_list "$cur" --into -h --help
            else
                mapfile -t words < <(_poketracker_tracked_save_evolve_base_names)
                if [[ ${#words[@]} -eq 0 ]]; then
                    mapfile -t words < <(_poketracker_tracked_save_pokemon_names "all")
                fi
                if [[ ${#words[@]} -eq 0 ]]; then
                    mapfile -t words < <(_poketracker_pokemon_names)
                fi
                _poketracker_match_list "$cur" "${words[@]}"
            fi
            return 0
            ;;
        area)
            if [[ "$cur" == -* ]]; then
                _poketracker_match_list "$cur" \
                    -S --simple -i --items-needed -w --walking -f --fishing -s --surfing -o --other -a --all -C --companion-details -h --help
            else
                mapfile -t words < <(_poketracker_tracked_save_area_names)
                if [[ ${#words[@]} -eq 0 ]]; then
                    mapfile -t words < <(_poketracker_area_names)
                fi
                _poketracker_match_list "$cur" "${words[@]}"
            fi
            return 0
            ;;
        completion)
            _poketracker_match_list "$cur" -a --areas -d --detailed -h --help
            return 0
            ;;
        exclusives)
            _poketracker_match_list "$cur" -h --help
            return 0
            ;;
    esac

    COMPREPLY=()

    return 0
}

complete -F _poketracker_completion poketracker