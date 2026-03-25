# FT-IR background monitor

This repository contains helper scripts for a Thermo Fisher OMNIC Paradigm workflow used to check background stability during ATR/HATR cleaning.

Included scripts:

- `plot_spectrum.py` reads `background_stability.TSV` and updates `current_background.png`
- `view_plot.py` displays `current_background.png` in a separate window and refreshes it when the file changes
- `start_view_plot.ps1` starts `view_plot.py` with `pythonw.exe`, so no terminal window is shown

The viewer is started outside OMNIC. Inside the OMNIC loop, only `plot_spectrum.py` is executed.

## Files used by the workflow

- `background_stability.TSV` - current background exported by OMNIC
- `background_stability_old.TSV` - first saved background kept as reference
- `current_background.png` - image updated by `plot_spectrum.py`

The reference spectrum is plotted in red. The current spectrum is plotted in blue.

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

The use of `uv` is recommended because it simplifies Windows setup and allows Python 3.14 and the required packages to be installed locally for this workflow.

Install Python 3.14:

```powershell
uv python install 3.14
```

Install the Python packages into `.deps`:

```powershell
uv pip install --python 3.14 --target .deps -r requirements.txt
```

## Viewer startup

The viewer is started outside OMNIC.

Command:

```powershell
.\start_view_plot.ps1
```

`start_view_plot.ps1` must be edited so that the path to `pythonw.exe` matches the Python installation available on the target PC.

## OMNIC loop example

The following cropped screenshot shows the part of the workflow used for the background-check loop:

![OMNIC loop example](docs/omnic_loop_crop.jpg)

Loop sequence:

1. `BG checker` is an `EXE` node that runs `plot_spectrum.py`
2. `BG switch` is the user decision node
3. If the result is `True`, the background is still not acceptable and a new background must be acquired
4. `BG snapshot` acquires the new background
5. `BG save` saves it as `background_stability.TSV`
6. `BG loop` returns to the beginning of the cycle
7. If the result is `False`, the loop is exited and the workflow continues

Meaning of the decision:

- `True` indicates that the crystal/module is still dirty and the loop must continue
- `False` indicates that the background is acceptable and the loop can stop

## EXE node configuration

Inside the repeated OMNIC cycle, add an `EXE` node.

Set it as follows:

- `Executable`: full path to `python3.14` or `python.exe`
- `Argument`: full path to `plot_spectrum.py`

Example:

```text
Executable: C:\Users\username\AppData\Roaming\uv\python\cpython-3.14-windows-x86_64-none\python.exe
Argument: C:\path\to\FT-IR\plot_spectrum.py
```

## Operations at each cycle

- `plot_spectrum.py` reads `background_stability.TSV`
- if `background_stability_old.TSV` does not exist yet, it is created from the first available TSV
- the comparison plot is written to `current_background.png`
- `view_plot.py` refreshes the displayed image automatically
- the operator decides whether another background acquisition is needed

## Important notes

- OMNIC must export the background with the exact name `background_stability.TSV`
- if that file name is changed in the workflow, it must also be changed in `plot_spectrum.py`
- if a new red reference must be created, delete `background_stability_old.TSV`
- `plot_spectrum.py` does not open any window; it only updates the PNG and exits
