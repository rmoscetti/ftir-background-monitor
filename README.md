# FT-IR background monitor

This small project is intended for Thermo Fisher OMNIC workflows.

Two scripts are included:

- `plot_spectrum.py` reads `background_stability.TSV` and writes `current_background.png`
- `view_plot.py` opens `current_background.png` in a small window and refreshes it when the file changes
- `start_view_plot.ps1` starts `view_plot.py` with `pythonw.exe`, so the black terminal window is not shown

The viewer is meant to stay open while OMNIC runs the plot script in a loop and the background is monitored during ATR/HATR cleaning.

`plot_spectrum.py` also keeps a reference copy called `background_stability_old.TSV`. The first saved spectrum is drawn in red, while the current one is drawn in blue.

## Windows setup

Install Scoop from PowerShell:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```

Install `uv` with Scoop:

```powershell
scoop install uv
```

The use of `uv` is recommended because it simplifies the Windows setup and allows Python 3.14 and the required packages to be installed locally for this workflow.

Install Python 3.14:

```powershell
uv python install 3.14
```

Install the dependencies into `.deps`:

```powershell
uv pip install --python 3.14 --target .deps -r requirements.txt
```

## How to use it in OMNIC

1. `view_plot.py` must be started outside OMNIC, before the monitoring loop begins.

   The recommended launcher is `start_view_plot.ps1`.

   The path to `pythonw.exe` inside `start_view_plot.ps1` must be edited so that it matches the Python executable installed on the target system.

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\start_view_plot.ps1
```

2. Inside the OMNIC workflow, an EXE node must be added to the repeated cycle.

   In that node:

   - the executable must be the full path to `python3.14`
   - the argument must be the full path to `plot_spectrum.py`

   Example:

```powershell
Executable: C:\Users\username\AppData\Roaming\uv\python\cpython-3.14-windows-x86_64-none\python.exe
Argument: C:\path\to\FT-IR\plot_spectrum.py
```

3. The workflow should keep running until it is stopped by the operator.

At each cycle:

- `plot_spectrum.py` reads `background_stability.TSV`
- on the first run, `background_stability_old.TSV` is created
- it draws the old spectrum in red and the current spectrum in blue
- it updates the timestamp at the top of the image
- it overwrites `current_background.png`
- `view_plot.py` detects the change and refreshes the window

## Important notes

- the OMNIC workflow must export the TSV as `background_stability.TSV`
- the script is hardcoded to that file name, so if you change it in OMNIC you must change it in `plot_spectrum.py` too
- the red reference spectrum can be reset by deleting `background_stability_old.TSV`
- `plot_spectrum.py` does not open any window; it just updates the PNG and exits
- Python packages are loaded from the `.deps` folder
