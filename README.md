# OldMaid - Arcade Card Game

## What is the game and game rules
This project is a digital adaptation of the classic card game **Old Maid**, built with a unique twist involving health points (hearts). 

You play against a computer opponent. The game consists of 19 cards: 9 matching pairs and 1 Joker. 

**Rules:**
* At the start, cards are dealt to both players. Any matching pairs in your initial hand are automatically discarded.
* Players take turns drawing one random card from their opponent's hand.
* If the drawn card makes a pair with a card in your hand, the pair is discarded.
* **The Twist:** You have 3 lives (hearts). If you draw the Joker from your opponent, you lose 1 heart!
* **Win Conditions:** You win if you are the first to discard all your cards, or if your opponent loses all their hearts.
* **Lose Conditions:** You lose if you run out of hearts, or if your opponent clears their hand and leaves you holding the Joker.

## Technical features
This project is built using modern Python development practices and features a robust underlying architecture.

* **Graphics & GUI:** Built using the [Python Arcade](https://api.arcade.academy/) library for 2D rendering, sprite management, and mouse interactions.
* **Architecture:** Used Object-Oriented Programming (OOP) separating the game logic engine (`GameEngine`) from the graphical views (`MenuView`, `TableView`, `RuleView`).
* **CI/CD Pipeline:** Fully automated GitHub Actions workflows (`.github/workflows/lint.yml` and `test.yml`) that run on every push and pull request to the `main` branch.
* **Testing:** Comprehensive unit test suite using `pytest`, `pytest-cov`, and `pytest-mock` covering game engine logic, graphical interfaces, and player mechanics.
* **Code Quality & Linting:** Strict static analysis and formatting enforced via `pylint`, `flake8`, `mypy`, `black`, and `isort`.

## Prerequisites
To run this game locally, you will need:
* **Python**: Python 3.12 or higher (the CI pipeline supports up to Python 3.14).
* **Git** *(Optional)*: To clone the repository to your local machine.

## How to install

   ```bash
# Clone the repository
git clone https://github.com/zMasterRed/CardGame.git

# Enter the project directory
cd CardGame

# (Optional) Create and activate a virtual environment
# On Windows
python -m venv venv
venv\Scripts\activate

# On Linux / macOS
python3 -m venv venv 
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m src.main
```