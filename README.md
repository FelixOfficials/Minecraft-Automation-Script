# Minecraft Automation Script

A Python automation script built using the **MineScript API** that demonstrates entity detection, player navigation, and interaction logic in a Minecraft environment.

This project was created as a **personal learning exercise** to explore game scripting, event-driven programming, and automation techniques.

> Some values and tokens have been sanitized before publishing this repository.

---

## Features

- **Entity scanning and filtering** – Detects nearby entities of a specific type within a configurable radius.
- **Smooth player rotation** – Uses yaw/pitch math with easing to simulate natural player movement.
- **Automated navigation** – Moves the player between predefined **points of interest (POI)**.
- **Dynamic interaction logic** – Automatically interacts with detected entities using attack or use actions.
- **Event-driven automation** – Uses MineScript's event queue to monitor chat events and trigger script behavior.
- **Optional notification system** – Demonstrates integration with the Telegram Bot API for sending status updates.

---

## How It Works

The script continuously cycles through predefined **points of interest** and performs the following actions:

1. Navigates the player to the target coordinates.
2. Scans for nearby entities that match a configured entity type.
3. Selects the **closest entity** and interacts with it.
4. Repeats the process until a stopping condition occurs.

Additional behaviors include:

- Smooth camera movement using interpolation.
- Automatic recovery if the player becomes stuck.
- Timed speed actions for efficiency.
- Chat-event monitoring for durability or stop conditions.

---

## Project Structure
- main.py
- README.md


The main script contains several logical sections:

| Section               | Purpose                                           |
|-----------------------|-------------------------------------------------|
| Configuration         | Script settings and coordinates                 |
| Helpers               | Math utilities and entity scanning              |
| Interaction Logic     | Movement and interaction with entities          |
| Main Loop             | Automation control flow                          |

---

## Technologies Used

- **Python**
- **MineScript API**
- **Telegram Bot API (optional integration)**
- Standard libraries:
  - `math`
  - `random`
  - `time`
  - `queue`
  - `requests`

---

## Configuration

Before running the script you may want to modify:

```python
POI = [
    (678.5, 96, -268.7),
    (678, 96, -291.5),
]
```
These coordinates represent points of interest the script will navigate between.

Optional Telegram notifications require setting:
```
BOT_TOKEN = "TELEGRAM_TOKEN_HERE"
CHAT_ID = 12345678990
```
These are placeholders in the public repository.

## Disclaimer

This repository is shared for **educational purposes** to demonstrate scripting techniques such as:

- Automation
- Event handling
- Spatial calculations
- API integration

Some sensitive values have been removed or replaced with placeholders before publishing.

---

## Future Improvements

Potential improvements for this project include:

- Configurable pathfinding
- Modularized interaction logic
- Configuration file support
- Improved error handling
- Logging system for script diagnostics

---

## License

This project is provided for **educational and experimentation purposes**.
