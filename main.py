"""Entry point for the Minesweeper Tkinter app."""

from ui import MinesweeperApp


def main() -> None:
    app = MinesweeperApp()
    app.mainloop()


if __name__ == "__main__":
    main()

