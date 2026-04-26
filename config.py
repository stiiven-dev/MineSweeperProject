"""Configuration values for the Tkinter Minesweeper project."""

# Difficulty settings: (grid_size, mine_count)
DIFFICULTIES = {
    "Easy": {"size": 10, "mines": 15},
    "Medium": {"size": 15, "mines": 40},
    "Hard": {"size": 20, "mines": 70},
}
DEFAULT_DIFFICULTY = "Medium"
GRID_SIZE = DIFFICULTIES[DEFAULT_DIFFICULTY]["size"]
WINDOW_TITLE = "Minesweeper (15x15)"

# Color palette (simple and clean).
BG_COLOR = "#1E2230"
PANEL_COLOR = "#2A3144"
BUTTON_HIDDEN = "#5B6C8F"
BUTTON_REVEALED = "#DDE3F0"
BUTTON_MINE = "#E25555"
BUTTON_FLAG = "#F0C44C"
TEXT_LIGHT = "#F4F7FF"
TEXT_DARK = "#1A2030"

