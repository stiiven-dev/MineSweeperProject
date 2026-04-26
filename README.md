# Minesweeper Project

A simple and pretty Minesweeper game for a college project, built with Python and Tkinter.

## Features
- **3 difficulty levels with scaling grid**:
  - Easy: 10×10 grid, 15 mines
  - Medium: 15×15 grid, 40 mines
  - Hard: 20×20 grid, 70 mines
- Randomized mine map every new game
- Switch difficulties anytime – board resizes and updates instantly
- Left click to reveal cells
- Right click to place/remove flags
- Clean UI with status bar and difficulty buttons

## Project Structure
- `main.py` - app entry point
- `ui.py` - Tkinter interface and event handling
- `game_logic.py` - board generation and game rules
- `config.py` - board settings and colors

## Requirements
- Python 3.10+
- Tkinter (usually included with standard Python on Windows)

## Run
```bash
python main.py
```

## Controls
- Left click: reveal a cell
- Right click: toggle flag  
- Difficulty buttons: switch between Easy, Medium, and Hard
- "New Game": create a fresh randomized board with current difficulty
