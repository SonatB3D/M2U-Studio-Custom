M2U STUDIO CUSTOM — README

OVERVIEW
M2U Studio Custom is a Maya tool for validating selected mesh assets against user-defined rules and exporting ready assets as FBX.
It is designed for artist-friendly use inside Autodesk Maya and focuses on a simple shelf-based workflow.

MAIN WORKFLOW
1. Select one or more mesh assets in Maya.
2. Open M2U Studio Custom from the MZU_Tools shelf button.
3. Adjust validation settings if needed.
4. Click Validate Selected Assets.
5. Review the readable per-check results.
6. Click Export Selected Assets to export valid assets as FBX.

INSTALLATION
Files required in the same folder:
- m2u_studio_custom.py
- m2u_studio_custom_icon.png
- installer_script.txt

Installation steps:
1. Open Autodesk Maya.
2. Open Script Editor.
3. Switch to the Python tab.
4. Open installer_script.txt, copy its contents, and paste them into Maya Script Editor.
5. Run the installer script once.
6. When prompted, select the folder that contains m2u_studio_custom.py and m2u_studio_custom_icon.png.
7. Maya will create or reuse the MZU_Tools shelf and add the M2U Studio Custom button.

AFTER INSTALLATION
- From then on, launch the tool from the MZU_Tools shelf.
- You do not need to run the installer again unless you move the files or want to reinstall.

TOOL SECTIONS
- Asset Scope
- Pivot Rules
- Dimension Rules
- Grid Rules
- Geometry Rules
- Naming Rules
- Collision Rules
- Export Behavior
- Actions
- Results

VALIDATION FEATURES
The tool can check:
- naming prefix rules
- polycount limits
- freeze transforms
- clean construction history
- bounding box dimensions with tolerance
- pivot target position with tolerance
- grid size fit
- UCX collision naming/presence rules

EXPORT FEATURES
- exports selected ready assets to FBX
- can skip blocked assets
- can export warning assets
- can optionally write a JSON report

IMPORTANT NOTES
- The tool works with selected mesh transforms.
- The installer shelf button uses the selected installation folder directly.
- If you move or rename the folder after installation, the shelf button may stop working.
- If that happens, place the files back in the original folder or run the installer again.
- FBX export requires Maya's FBX plugin to load correctly.

PACKAGE CONTENTS
Recommended release package:
- m2u_studio_custom.py
- m2u_studio_custom_icon.png
- installer_script.txt
- README.txt
- FUNCTIONS.txt
- LICENCE_TERMS.txt

CONTACT / OFFICIAL DISTRIBUTION
Please download the tool only from the author's official release page or official distribution location.
Unauthorized re-uploading or repackaging is not allowed.
