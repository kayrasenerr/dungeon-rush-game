# Dungeon Rush

**Dungeon Rush** is a 2D action-arcade game built in Python using the **Pygame** library [cite: 1]. Navigate through the dungeon grid, fight off enemies using close-combat sword swings or thrown knives, and collect food to stay alive while chasing high scores [cite: 1].

---

## 🎮 Game Features

- **Fluid Movement & Jumping:** Move horizontally and jump across elevated platforms to dodge enemies and position your attacks [cite: 1].
- **Combat Mechanics:**
  - **Sword Swing (Melee):** Attack close-range enemies [cite: 1].
  - **Knife Throwing (Ranged):** Shoot directional knives at enemies from a distance [cite: 1].
- **Item Drops & Ammo Management:** Gain additional thrown knives as your score increases (2 knives per 5 score points) [cite: 1].
- **Health & Food System:** Enemies deal damage on contact [cite: 1]. Collect randomly spawned food items to restore up to +50 health [cite: 1].
- **Score Tracking & High Score:** Real-time UI displaying current score, high score, health bar, and remaining knife count [cite: 1].

---

## 🎮 Controls

| Action | Key / Input |
|---|---|
| **Move Left** | Left Arrow (`←`) [cite: 1] |
| **Move Right** | Right Arrow (`→`) [cite: 1] |
| **Jump Up** | Up Arrow (`↑`) [cite: 1] |
| **Drop Down** | Down Arrow (`↓`) [cite: 1] |
| **Sword Attack** | Spacebar (`Space`) [cite: 1] |
| **Throw Knife** | Left Shift (`LShift`) [cite: 1] |
| **Restart Game** | Spacebar (`Space`) *(On Game Over screen)* [cite: 1] |

---

## 📁 Required Assets & Folder Structure

Ensure your project folder is organized with the required image assets placed under the `notebook/project/` path [cite: 1]:

```text
dungeon_rush/
│
├── main.py
└── notebook/
    └── project/
        ├── backgroundb.png
        ├── right.png
        ├── left.png
        ├── right_attack.png
        ├── left_attack.png
        ├── enemyright.png
        ├── enemyleft.png
        ├── knife.png
        └── food.png
```

---

## 🚀 How to Run

### 1. Prerequisites
Make sure you have Python 3 installed along with `pygame` [cite: 1]:

```bash
pip install pygame
```

### 2. Running the Game
Run the Python script directly:

```bash
python main.py
```

---

## 🛠️ Code Architecture

The project is structured using Object-Oriented Programming (OOP) principles [cite: 1]:

- **`Entity`**: Base class handling positions and collision bounds [cite: 1].
- **`Player`**: Manages movement, combat cooldowns, ammo, jump state, and health [cite: 1].
- **`Enemy`**: Spawns randomly, tracks the player's movement, and deals contact damage [cite: 1].
- **`Knife`**: Sub-entity representing moving projectile attacks [cite: 1].
- **`Food`**: Consumable items that spawn randomly across the map [cite: 1].
- **`Healthbar` & `GameOverScreen`**: UI components managing HUD rendering and game loop transitions [cite: 1].
- **`Game` & `GameManager`**: Central game loop, input handling, entity updates, and collision logic [cite: 1].
