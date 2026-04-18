


***

# Sea Battle (Terminal Edition) 🌊🚢

A classic Sea Battle (Battleship) game implemented in Python, featuring a sophisticated Terminal User Interface (TUI) and an intelligent AI opponent. 

Unlike simple text-based games, this project utilizes the `urwid` library to create an interactive, grid-based visual experience directly in your terminal.

## ✨ Features

*   **Interactive TUI:** A polished terminal interface using `urwid` for a \"game-like\" feel.
*   **Smart AI Opponent:** The computer doesn't just guess; it tracks \"wounds\" and intelligently targets adjacent cells when it hits a ship.
*   **Automatic Ship Placement:** Uses a collision-detection algorithm to ensure ships are placed legally and randomly at the start of every game.
*   **Real-time Status Updates:** Live tracking of remaining ships and game state (Your Turn / Computer Turn).
*   **Visual Feedback:** Distinct symbols for hits, misses, and sunk ships.

## 🛠️ Tech Stack

*   **Language:** Python 3.x
*   **Library:** [urwid](https://urwid.org/) (Terminal User Interface library)
*   **Logic:** Object-Oriented Programming (OOP) principles applied to game state management.

## 🚀 Getting Started

### Prerequisites

You will need Python installed on your system. It is recommended to use a virtual environment.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SenoraDeSombras/sea-battle-game.git
   cd sea-battle-game
   ```

2. **Create and activate a virtual environment (Optional but recommended):**
   ```bash
   # Windows
   python -m venv venv
   .\\venv\\Scripts\\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install urwid
   ```

4. **Run the game:**
   ```bash
   python game.py
   ```
   
## 🎮 How to Play

The game is played on two 10x10 grids. 
*   **Left Grid:** Your fleet (represented by `H`).
*   **Right Grid:** The enemy fleet (hidden until you strike).

### Controls
*   **Click / Enter:** Fire a shot at the selected coordinate.
*   **`s` Key:** Show your own ships (useful for checking your layout).
*   **`q` Key:** Quit the game.

### Legend
| Symbol | Meaning |
| :--- | :--- |
| `.` | Unknown / Water |
| `a` | Miss (Water) |
| `H` | Your Ship |
| `X` | Damaged Ship |
| `Y` | Sunk Ship |

## 🧠 Technical Implementation

### Game Logic (`boards.py`)
The core engine is built using an Object-Oriented approach:
*   `sShip`: Manages individual ship health and coordinate tracking.
*   `sPlayer`: Manages the player's board state and ship positions.
*   `sBattle`: The orchestrator. It handles the complex logic of ship placement, collision detection, and the AI's decision-making process.

### AI Logic
The AI implements a \"memory\" system. If the AI strikes a coordinate and finds a ship, it records that location as a \"wound\" and prioritizes checking adjacent cells in the next turn to ensure a kill.

## 📂 Project Structure

```text
.
├── game.py          # TUI logic and game loop (Urwid implementation)
├── boards.py        # Game engine, AI logic, and Ship classes
└── README.md        # Project documentation
```

## 👤 Author

**SenoraDeSombras**
*   GitHub: [@SenoraDeSombras](https://github.com/SenoraDeSombras)

---
*Feel free to ⭐ this repository if you found it helpful!*

***

### 
