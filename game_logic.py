"""Core game logic for Minesweeper."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import random
from typing import Iterable


@dataclass
class Cell:
    is_mine: bool = False
    adjacent_mines: int = 0
    is_revealed: bool = False
    is_flagged: bool = False


class Board:
    def __init__(self, size: int, mine_count: int) -> None:
        self.size = size
        self.mine_count = mine_count
        self.grid: list[list[Cell]] = []
        self.game_over = False
        self.won = False
        self.revealed_safe_cells = 0
        self.total_safe_cells = size * size - mine_count
        self.new_game()

    def new_game(self) -> None:
        self.grid = [[Cell() for _ in range(self.size)] for _ in range(self.size)]
        self.game_over = False
        self.won = False
        self.revealed_safe_cells = 0
        self._place_mines()
        self._calculate_adjacency()

    def reveal(self, row: int, col: int) -> str:
        if self.game_over or self.won:
            return "ignore"

        cell = self.grid[row][col]
        if cell.is_revealed or cell.is_flagged:
            return "ignore"

        if cell.is_mine:
            self.game_over = True
            cell.is_revealed = True
            self._reveal_all_mines()
            return "mine"

        self._flood_reveal(row, col)

        if self.revealed_safe_cells >= self.total_safe_cells:
            self.won = True
            return "win"

        return "ok"

    def toggle_flag(self, row: int, col: int) -> str:
        if self.game_over or self.won:
            return "ignore"

        cell = self.grid[row][col]
        if cell.is_revealed:
            return "ignore"

        cell.is_flagged = not cell.is_flagged
        return "flag"

    def flags_used(self) -> int:
        return sum(cell.is_flagged for line in self.grid for cell in line)

    def _place_mines(self) -> None:
        all_positions = [(r, c) for r in range(self.size) for c in range(self.size)]
        mine_positions = random.sample(all_positions, k=self.mine_count)
        for row, col in mine_positions:
            self.grid[row][col].is_mine = True

    def _calculate_adjacency(self) -> None:
        for row in range(self.size):
            for col in range(self.size):
                cell = self.grid[row][col]
                if cell.is_mine:
                    continue
                cell.adjacent_mines = sum(
                    1 for nr, nc in self._neighbors(row, col) if self.grid[nr][nc].is_mine
                )

    def _flood_reveal(self, start_row: int, start_col: int) -> None:
        queue: deque[tuple[int, int]] = deque([(start_row, start_col)])

        while queue:
            row, col = queue.popleft()
            cell = self.grid[row][col]

            if cell.is_revealed or cell.is_flagged:
                continue

            cell.is_revealed = True
            self.revealed_safe_cells += 1

            if cell.adjacent_mines != 0:
                continue

            # Reveal surrounding empty area when current cell has zero neighboring mines.
            for nr, nc in self._neighbors(row, col):
                neighbor = self.grid[nr][nc]
                if not neighbor.is_revealed and not neighbor.is_mine and not neighbor.is_flagged:
                    queue.append((nr, nc))

    def _reveal_all_mines(self) -> None:
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col].is_mine:
                    self.grid[row][col].is_revealed = True

    def _neighbors(self, row: int, col: int) -> Iterable[tuple[int, int]]:
        for d_row in (-1, 0, 1):
            for d_col in (-1, 0, 1):
                if d_row == 0 and d_col == 0:
                    continue
                n_row, n_col = row + d_row, col + d_col
                if 0 <= n_row < self.size and 0 <= n_col < self.size:
                    yield n_row, n_col

