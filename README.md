# 2D Endless Wave Survival Game

A 2D top‑down shooter where you survive as many enemy waves as possible. The project is written in **Python** using **Pygame** and is meant as a small demo game.

## Features
- Infinite waves with progressive difficulty
- Upgrade menu between waves
- Melee and ranged combat
- Dash ability with cooldown
- Heads‑up display for health, stamina and gold

## Requirements
- Python 3.11+
- [Pygame](https://www.pygame.org/) 2.5+

## Installation
```bash
# Clone repository
git clone https://github.com/username/2D-Endless-Wave-Survival-Game.git
cd 2D-Endless-Wave-Survival-Game

# Install dependencies
pip install pygame
```

## Running the Game
```bash
python main.py
```

## Running Tests
The `tests/` folder contains PyTest based unit tests. Execute them with:
```bash
pytest
```

## Project Structure
- `main.py` – game loop and state management
- `level.py` – level, camera and wave logic
- `player.py` – player behaviour and controls
- `enemy.py` – enemy AI
- `weapon.py`, `bullet.py` – combat mechanics

## Contributing
Contributions are welcome. Please open a pull request with a clear description of your changes.

## License
This project is licensed under the terms of the [MIT License](LICENSE)