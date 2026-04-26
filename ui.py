"""Tkinter UI for Minesweeper."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from config import (
    BG_COLOR,
    BUTTON_FLAG,
    BUTTON_HIDDEN,
    BUTTON_MINE,
    BUTTON_REVEALED,
    DEFAULT_DIFFICULTY,
    DIFFICULTIES,
    PANEL_COLOR,
    TEXT_DARK,
    TEXT_LIGHT,
)
from game_logic import Board


NUMBER_COLORS = {
    1: "#1E4ED8",
    2: "#17803D",
    3: "#D91C1C",
    4: "#4B2CA7",
    5: "#A84A00",
    6: "#0E7A7A",
    7: "#111111",
    8: "#525252",
}


class MinesweeperApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title(WINDOW_TITLE)
    def __init__(self) -> None:
        super().__init__()

        self.current_difficulty = DEFAULT_DIFFICULTY
        difficulty_config = DIFFICULTIES[self.current_difficulty]
        self.grid_size = difficulty_config["size"]
        self.mine_count = difficulty_config["mines"]

        self.title(f"Minesweeper ({self.grid_size}x{self.grid_size})")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)

        self.board = Board(size=self.grid_size, mine_count=self.mine_count)

        self.status_var = tk.StringVar(value="Game started. Good luck!")
        self.mines_left_var = tk.StringVar(value="")
        self.difficulty_var = tk.StringVar(value=self.current_difficulty)

        self.buttons: list[list[tk.Button]] = []
        self.board_frame: tk.Frame | None = None
        self.difficulty_buttons: dict[str, tk.Button] = {}

        self._build_layout()
        self._refresh_board()

    def _build_layout(self) -> None:
        top_panel = tk.Frame(self, bg=PANEL_COLOR, padx=10, pady=10)
        top_panel.pack(fill="x", padx=10, pady=(10, 6))

        status_label = tk.Label(
            top_panel,
            textvariable=self.status_var,
            bg=PANEL_COLOR,
            fg=TEXT_LIGHT,
            anchor="w",
            font=("Segoe UI", 10, "bold"),
        )
        status_label.pack(side="left", fill="x", expand=True)

        mines_label = tk.Label(
            top_panel,
            textvariable=self.mines_left_var,
            bg=PANEL_COLOR,
            fg=TEXT_LIGHT,
            font=("Segoe UI", 10),
        )
        mines_label.pack(side="left", padx=(10, 0))

        new_game_btn = tk.Button(
            top_panel,
            text="New Game",
            command=self._start_new_game,
            bg="#3E4A66",
            fg=TEXT_LIGHT,
            activebackground="#4D5B7A",
            activeforeground=TEXT_LIGHT,
            relief="flat",
            padx=12,
            pady=5,
            font=("Segoe UI", 10, "bold"),
        )
        new_game_btn.pack(side="right", padx=(10, 0))

        # Difficulty panel
        difficulty_panel = tk.Frame(self, bg=PANEL_COLOR, padx=10, pady=8)
        difficulty_panel.pack(fill="x", padx=10, pady=(0, 6))

        difficulty_label = tk.Label(
            difficulty_panel,
            text="Difficulty:",
            bg=PANEL_COLOR,
            fg=TEXT_LIGHT,
            font=("Segoe UI", 9, "bold"),
        )
        difficulty_label.pack(side="left", padx=(0, 8))

        for difficulty in DIFFICULTIES.keys():
            btn = tk.Button(
                difficulty_panel,
                text=difficulty,
                command=lambda d=difficulty: self._set_difficulty(d),
                bg="#3E4A66" if difficulty == self.current_difficulty else "#5B6C8F",
                fg=TEXT_LIGHT,
                activebackground="#4D5B7A",
                activeforeground=TEXT_LIGHT,
                relief="flat",
                padx=10,
                pady=4,
                font=("Segoe UI", 9, "bold"),
            )
            btn.pack(side="left", padx=4)
            self.difficulty_buttons[difficulty] = btn

        self.board_frame = tk.Frame(self, bg=BG_COLOR, padx=8, pady=8)
        self.board_frame.pack(padx=8, pady=(0, 10))

        self._build_board()

    def _build_board(self) -> None:
        """Dynamically build the board grid."""
        # Clear old buttons
        self.buttons.clear()

        # Clear old board frame widgets
        if self.board_frame:
            for child in self.board_frame.winfo_children():
                child.destroy()

        for row in range(self.grid_size):
            row_buttons: list[tk.Button] = []
            for col in range(self.grid_size):
                btn = tk.Button(
                    self.board_frame,
                    width=2,
                    height=1,
                    font=("Segoe UI", 10, "bold"),
                    relief="ridge",
                    bd=1,
                    bg=BUTTON_HIDDEN,
                    fg=TEXT_LIGHT,
                    activebackground=BUTTON_HIDDEN,
                    activeforeground=TEXT_LIGHT,
                    command=lambda r=row, c=col: self._on_left_click(r, c),
                )
                btn.grid(row=row, column=col, padx=1, pady=1)
                btn.bind("<Button-3>", lambda event, r=row, c=col: self._on_right_click(r, c))
                btn.bind("<Button-2>", lambda event, r=row, c=col: self._on_right_click(r, c))
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def _set_difficulty(self, difficulty: str) -> None:
        """Switch difficulty and start a new game."""
        if difficulty == self.current_difficulty:
            return

        self.current_difficulty = difficulty
        difficulty_config = DIFFICULTIES[difficulty]
        self.grid_size = difficulty_config["size"]
        self.mine_count = difficulty_config["mines"]

        # Update window title
        self.title(f"Minesweeper ({self.grid_size}x{self.grid_size})")

        # Update board
        self.board = Board(size=self.grid_size, mine_count=self.mine_count)

        # Rebuild board UI
        self._build_board()
        self._refresh_board()

        # Update button styles
        for btn_name, btn in self.difficulty_buttons.items():
            if btn_name == difficulty:
                btn.config(bg="#3E4A66")
            else:
                btn.config(bg="#5B6C8F")

        self.status_var.set(f"{difficulty} difficulty ({self.grid_size}x{self.grid_size}). New map loaded!")

    def _start_new_game(self) -> None:
        self.board.new_game()
        self.status_var.set("New map generated. Good luck!")
        self._refresh_board()

    def _on_left_click(self, row: int, col: int) -> None:
        result = self.board.reveal(row, col)
        self._refresh_board()

        if result == "mine":
            self.status_var.set("Boom! You hit a mine.")
            messagebox.showinfo("Game Over", "You hit a mine. Try a new game!")
        elif result == "win":
            self.status_var.set("Great job! You cleared the board.")
            messagebox.showinfo("You Win", "You found all safe cells!")

    def _on_right_click(self, row: int, col: int) -> str:
        self.board.toggle_flag(row, col)
        self._refresh_board()
        return "break"

    def _refresh_board(self) -> None:
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                cell = self.board.grid[row][col]
                btn = self.buttons[row][col]

                if cell.is_revealed:
                    if cell.is_mine:
                        btn.config(text="*", bg=BUTTON_MINE, fg=TEXT_LIGHT)
                    else:
                        text = "" if cell.adjacent_mines == 0 else str(cell.adjacent_mines)
                        number_color = NUMBER_COLORS.get(cell.adjacent_mines, TEXT_DARK)
                        btn.config(text=text, bg=BUTTON_REVEALED, fg=number_color)
                else:
                    if cell.is_flagged:
                        btn.config(text="F", bg=BUTTON_HIDDEN, fg=BUTTON_FLAG)
                    else:
                        btn.config(text="", bg=BUTTON_HIDDEN, fg=TEXT_LIGHT)

        mines_left = max(0, self.mine_count - self.board.flags_used())
        self.mines_left_var.set(f"Mines: {self.mine_count} | Flags Left: {mines_left}")

