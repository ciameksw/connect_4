# Connect 4 Game

[![python](https://img.shields.io/badge/Python-3.14-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![ruff](https://github.com/ciameksw/connect_4/workflows/Ruff/badge.svg)](https://github.com/ciameksw/connect_4/actions?query=branch%3Amain)
[![pytest](https://github.com/ciameksw/connect_4/workflows/Pytest/badge.svg)](https://github.com/ciameksw/connect_4/actions?query=branch%3Amain)
[![markdown](https://github.com/ciameksw/connect_4/workflows/Markdown%20Lint/badge.svg)](https://github.com/ciameksw/connect_4/actions?query=branch%3Amain)
[![License: GPLv3](https://img.shields.io/badge/License-MIT-blue.svg)](https://license.md/licenses/mit-license/)

---

## Setup & Installation

**Note for Linux and MacOS users:**
If you encounter issues with Pygame installation or running the game, you may need to install additional system dependencies:

For Linux

```shell
sudo apt-get update && sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev python3-dev build-essential
```

For MacOS

```shell
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf
```

1. **Install [uv](https://github.com/astral-sh/uv) (if not installed):**

    ```shell
    pip install uv
    ```

2. **Synchronize dependencies:**

    ```shell
    uv sync
    ```

3. **Run the game:**

    ```shell
    uv run connect4
    ```

---

## Tests

```shell
uv run pytest
```

---

## Game Windows & Controls

### 1. Main Menu
The starting screen where you choose how to begin the game or access options.

**Features:**
- Start as Player 1 (you move first)
- Start as Player 2 (AI moves first)
- Go to Options

**Controls:**
- Use left button click.

---

### 2. Options Window
Allows you to customize game parameters and AI difficulty.

**Features:**
- Edit board size (rows, columns), win length, and AI parameters
- Three difficulty presets: Easy, Medium, Hard
- Save and return to menu

**Controls:**
- Use **UP/DOWN arrows** to select a parameter.
- Press **ENTER** to edit, type a new value, then **ENTER** to confirm.
- Click a difficulty button to quickly set recommended AI settings.
- Press **ESC** to save changes and return to the main menu.

---

### 3. Game Window
The main gameplay screen where you play Connect 4 against the AI.

**Features:**
- Interactive Connect 4 board
- ESC to return to menu
- End-of-game message (win/tie)

**Controls:**
- Click the left mouse button to place a token.
- After your move, the AI will play automatically.
- Press **ESC** to return to the main menu (game progress will be lost).
- When the game ends, a message will appear above the board.

---

## References

- [Singleton pattern reference](https://www.geeksforgeeks.org/python/singleton-pattern-in-python-a-complete-guide/)
- [Minimax for Connect 4 reference](https://www.deepexploration.org/blog/minimax-algorithm-for-connect-4)

---
Copyright (c) 2026 Maciej Kwapisz
