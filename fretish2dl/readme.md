# FRETISH2DL

Script to translate FRETISH requirements the use our DL templates into a DL Specification, suitable for integration into a hybrid program.

## Needs

* Python 3

## Assumes

* Requirements (and only the requirements) are in a json file exported from FRET
* The requirements were built using out DL Templates

## Usage

This is a terminal program that takes the requirements `filename` and the `project_name` (which is used in one component of the DL Specification:

```
FRETISH 2 dL [-h] [-f FORMAT] filename project_name
```

For example:

```
python3 fretish2dl.py tempControl.json TmpCtrl
```

runs the program on a file called `tempControl.json` with the project name as `TmpCtrl`.

For now, the `-f` or `--format` flags are not active.
