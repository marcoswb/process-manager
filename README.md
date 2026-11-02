# Process Manager

A Linux desktop application that lists running processes and lets you stop, resume, or terminate them. Process details are read mainly from the `/proc` filesystem, with a Qt (PySide6) interface that refreshes in place so the table stays readable while data updates.

## Features

- Lists processes with **PID**, **user**, **name**, **priority**, **memory usage (KB)**, **disk read (KB)**, **disk write (KB)**, and **status**
- Shows system overview in the UI:
  - Current time
  - Machine uptime
  - Total CPU usage (%)
  - Total memory usage (%)
  - Process count and counts by status
- Refresh behavior:
  - Process table and memory/status summary every **5 seconds**
  - Time, uptime, and CPU usage percentage every **1 second**
  - Incremental table updates (add new rows, remove ended processes, update changed cells) instead of rebuilding the whole list
- Process actions on the selected row:
  - **STOP** — `SIGTSTP`
  - **RESUME** — `SIGCONT`
  - **KILL** — signal `15` (`SIGTERM`)
  - **FORCE KILL** — signal `9` (`SIGKILL`)
- Table supports row selection and column sorting

## Technologies

| Component | Role |
|-----------|------|
| Python | Application language |
| [PySide6](https://doc.qt.io/qtforpython/) | GUI (`QMainWindow`, table, buttons, background threads) |
| Linux `/proc` | Primary source for process and system data |
| [psutil](https://psutil.readthedocs.io/) | Total CPU usage percentage only |

Pinned versions are in `requirements.txt` (`psutil==5.9.5`, `PySide6==6.5.2` and related packages).

## Project structure

```
process-manager/
├── main.py                 # Application entry point and main window logic
├── requirements.txt        # Python dependencies
├── models/
│   └── Process.py          # Reads per-process data from /proc
├── classes/
│   └── UpdateInfos.py      # Background threads for periodic UI updates
├── utils/
│   └── functions.py        # Helpers (time, uptime, memory total, CPU %, signals)
├── screen_ui/
│   └── screen.ui           # Qt Designer UI definition
└── LICENSE                 # MIT
```

## Prerequisites

- A **Linux** system with a `/proc` filesystem (the app does not run on Windows/macOS as written)
- Python with `pip` (no specific Python version is required beyond what the dependencies support)
- A desktop environment that can display Qt windows
- **Root privileges (`sudo`)** — required to run the application

## Installation

```bash
git clone https://github.com/marcoswb/process-manager.git
cd process-manager
pip install -r requirements.txt
```

Using a virtual environment is optional but recommended:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

This project does not use environment variables or external config files. Paths such as `/proc` and `./screen_ui/screen.ui` are fixed in the code.

## How to run

Run from the project root (so `./screen_ui/screen.ui` resolves correctly). **`sudo` is required:**

```bash
sudo python main.py
```

If you installed dependencies in a virtual environment:

```bash
sudo .venv/bin/python main.py
```

The window opens maximized.

## How to use

1. Review the process table and the summary labels at the top.
2. Click a row to select a process.
3. Use **STOP**, **RESUME**, **KILL**, or **FORCE KILL** as needed.
4. Leave the app running to keep metrics updating automatically.

Demo of an earlier run:

![Demo](https://github.com/marcoswb/process-manager/assets/48187276/10c96a25-0d34-48ba-a212-1232bcf2d794)

## Tests

This repository does not include automated tests.

## License

This project is licensed under the [MIT License](LICENSE).
