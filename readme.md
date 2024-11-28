# FRET Dynamic Logic Templates
#### Matt Luckcuck - November 2024

The Dynamic Logic Templates for [FRET](https://github.com/NASA-SW-VnV/fret).

## Contents

* `basicTemplates.js` - An updated version of a file distributed with FRET. The update includes our new template file into the building of the template list
* `dlTemplates.js` - The new template file containing the definitions of the Dynamic Logic Templates
* `RLReqs.json` - a demo  requirements set showing a general template and an instantiated example of the template. 

## Installation

These instructions assume:
* You have [FRET](https://github.com/NASA-SW-VnV/fret) installed
* FRET runs ok

To install the templates in FRET:
1. Go to your FRET directory and navigate to `fret-electron/templates`
2. Rename `basicTemplates.js` to `basicTemplates.js.old` to keep it as a backup
3. Copy `basicTemplates.js` and `dlTemplates.js` from this repository into `fret-electron/templates`
4. Run `node basicTemplates.js` (from inside `fret-electron/templates`) to produce an updated copy of `templates.json`
5. Run FRET, which should now read the updated `templates.json`. The new templates should be present in the Templates drop-down when creating a requirement. 

## Uninstallation

1. Delete `basicTemplaces.js` and `dlTemplates.js` from `fret-electron/templates`
2. Rename `basicTemplates.js.old` to `basicTemplates.js`
3. Run `node basicTemplates.js` (from inside `fret-electron/templates`) 

## Papers

TBA
