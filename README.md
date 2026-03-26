# Speedtest Trigger GUI

A lightweight desktop tool designed to help maintain stable internet performance by periodically running controlled speed test triggers or lightweight connection checks.

> [!NOTE]
> This tool helps maintain your internet speed at its peak, especially in cases where performance drops when no active traffic or speed test is detected (common with ISP throttling behavior).  
>
> An Android version is also available:  
> https://github.com/rdevz-ph/SpeedtestTriggerAndroid

Built with Python and Tkinter, it serves as a lightweight alternative to running Speedtest in a web browser while giving you control over bandwidth usage.

---

## Screenshot

![Speedtest Trigger GUI](./screenshot.png)

---

## Features

- Multiple test modes:
  - Full test (download + upload)
  - Download only
  - Upload only
  - Checker mode (ISP, server, and ping only)
- Automatic loop with configurable interval (e.g., every 30 seconds)
- Displays:
  - Current ISP (Telco)
  - Best server
  - Ping
  - Mode
  - Download result
  - Upload result
  - Overall result status
- Start and stop controls
- Real-time log output
- Lightweight GUI with minimal resource usage
- Fully self-contained application

---

## Test Modes

The application allows flexible control over bandwidth usage using two options:

- Skip Download Test
- Skip Upload Test

| Configuration                  | Behavior                          |
|--------------------------------|----------------------------------|
| None checked                   | Full test (download + upload)    |
| Skip Upload                    | Download only                    |
| Skip Download                  | Upload only                      |
| Skip Download + Skip Upload    | Checker mode (no data usage)     |

Checker mode performs:
- ISP detection
- Best server selection
- Ping measurement

---

## Requirements

### Windows (Recommended)

- Download `speedtest_trigger_gui.exe` from the Releases page
- Run the application

---

### Linux (Source Run)

- Python 3
- Tkinter:
  ```
  sudo apt install python3-tk
  ```

- Install dependency:
  ```
  pip install requests
  ```

---

### Development Setup

#### Install Python

1. Download Python:  
   https://www.python.org/downloads/

2. Recommended Version:  
   Python 3.10 – 3.12

3. During installation:
   - Enable "Add Python to PATH"
   - Click Install Now

---

## Running the Application

```
python speedtest_trigger_gui.py
```

---

## Building Executable

### Windows

```
py build.py
```

### Linux

```
python3 build.py
```

Output:
```
dist/speedtest_trigger_gui
```

---

## How It Works

- Retrieves current ISP information
- Selects the best nearby server
- Measures latency (ping)
- Optionally performs download and/or upload tests
- Updates the interface with results
- Waits for the configured interval
- Repeats

---

## Notes

- Download and upload tests are configurable to control data usage
- Checker mode uses minimal bandwidth
- Recommended interval: 15–30 seconds
- Consistent server selection improves reliability for ISP behavior

---

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
