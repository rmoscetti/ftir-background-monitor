# FT-IR background monitor

Simple scripts for visual monitoring of FT-IR background stability.

These scripts are intended for Thermo Fisher OMNIC workflows:

- `plot_spectrum.py` reads `background_stability.TSV` and generates `current_background.png`
- `view_plot.py` displays `current_background.png` in a window and reloads it when the file changes
- the TSV file name configured in the OMNIC workflow must match the file name expected by `plot_spectrum.py`

Typical use case:

- the operator starts the viewer once
- the OMNIC workflow runs the plot script repeatedly
- the PNG is overwritten at each cycle and the window shows the updated background plot
- this allows the operator to visually verify when the ATR/HATR module has been fully cleaned

## Windows installation

Install Scoop from PowerShell:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```

Install `uv` with Scoop:

```powershell
scoop install uv
```

Using `uv` is recommended because it simplifies setup on Windows, makes Python 3.14 installation easier, and installs the required packages locally for this workflow.

Install Python 3.14:

```powershell
uv python install 3.14
```

Install the dependencies locally into `.deps`:

```powershell
uv pip install --python 3.14 --target .deps -r requirements.txt
```

## Workflow usage

1. Configure the workflow to run `view_plot.py` before starting the monitoring cycle:

```powershell
python3.14 view_plot.py
```

2. Configure the workflow cycle so that it repeatedly runs:

```powershell
python3.14 plot_spectrum.py
```

3. Keep the workflow running until the user decides to stop it.

At each cycle:

- `plot_spectrum.py` always reads `background_stability.TSV`
- it updates the timestamp shown at the top of the plot
- it overwrites `current_background.png`
- `view_plot.py` detects the change and refreshes the window

TSV file name requirement:

- the OMNIC workflow must export the spectrum as `background_stability.TSV`
- `plot_spectrum.py` is hardcoded to read `background_stability.TSV`
- if you change the TSV file name in the workflow, you must change it in `plot_spectrum.py` as well

Notes:

- `plot_spectrum.py` does not open any window and exits immediately
- `view_plot.py` should be started before the cyclic plot execution begins
- the workflow should be configured to repeat `plot_spectrum.py` until the operator manually interrupts the process
- Python dependencies are loaded from the `.deps` folder
