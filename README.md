M2U STUDIO CUSTOM - README
Version: v12 UCX UI FINAL

OVERVIEW
M2U Studio Custom is a Maya-side validation and FBX export helper tool for selected static mesh assets.
It is designed for Autodesk Maya users who prepare static mesh assets for Unreal Engine-oriented workflows.

The tool provides an artist-friendly shelf workflow, readable validation results, FBX export controls, UCX custom collision support, matched UCX mesh validation, custom collision target naming, and optional JSON reporting.

This README is written for the fixed v12 release based on:
- m2u_studio_custom_fixed.py
- M2U_BUILD_ID: v12_ucx_ui_final

MAIN WORKFLOW
1. Select one or more base mesh assets in Maya.
2. Open M2U Studio Custom from the M2U_Tools shelf.
3. Adjust validation settings if needed.
4. Click Validate Selected Assets.
5. Review the readable per-check results.
6. Click Export Selected Assets.
7. Choose an export folder.
8. If enabled, review the generated JSON report in the selected export folder.
9. Import the exported FBX files into Unreal Engine.
10. For UCX collision verification, open the Static Mesh in Unreal Engine and enable collision display, such as Show > Simple Collision.

INSTALLATION

Required files in the same release package:
- m2u_studio_custom_icon.png
- M2U_Studio_Custom_Installer.txt
- M2U_Studio_Custom_Installer.py
- README.txt
- FUNCTIONS.txt
- LICENCE_TERMS.txt

Installation steps:
1. Open Autodesk Maya.
2. Open Script Editor.
3. Switch to the Python tab.
4. Open M2U_Studio_Custom_Installer.txt.
5. Copy its contents and paste them into the Maya Script Editor.
   OR (Drag and drop M2U_Studio_Custom_Installer.py file in script editor)
6. Run the installer script once.
7. When prompted, select the folder where the tool should be installed.
8. Maya will create or update the M2U_Tools shelf.
9. Use the new shelf button created by the installer.

AFTER INSTALLATION
- Launch the tool from the M2U_Tools shelf.
- Use the newest v12 shelf button created by the patched installer.
After the installer has been run successfully once, you do not need to run it again for normal use.

From that point on, launch M2U Studio Custom directly from the M2U_Tools shelf button inside Maya.

Run the installer again only if:
- you move or rename the installation folder
- you replace or update the main script file
- the shelf button stops working
- you want to reinstall or refresh the shelf button

## Screenshots

<p align="center">
  <img src="M2U_Studio_Custom_V1.2.4/images/m2usc1.png" alt="M2U Studio Custom Main Interface" width="850">
</p>

<p align="center">
  <img src="M2U_Studio_Custom_V1.2.4/images/m2usc2.png" alt="M2U Studio Custom Export Options" width="850">
</p>

<p align="center">
  <img src="M2U_Studio_Custom_V1.2.4/images/m2usc3.png" alt="M2U Studio Custom UCX Collision Workflow" width="850">
</p>

<p align="center">
  <img src="M2U_Studio_Custom_V1.2.4/images/m2usc4.png" alt="M2U Studio Custom Folder Selection" width="850">
</p>

<p align="center">
  <img src="M2U_Studio_Custom_V1.2.4/images/m2usc5.png" alt="M2U Studio Custom Final Export Workflow" width="850">
</p>

TOOL SECTIONS
The UI contains the following main sections:
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
- Naming prefix rules
- Polycount limits
- Freeze transform requirements
- Clean construction history requirements
- Bounding box dimensions with tolerance
- Pivot target position with tolerance
- Grid size fit
- Grid bounds snap alignment
- Near-zero thickness warning
- UCX collision naming and presence rules
- UCX base asset matching
- Exact custom collision target names
- Matched UCX mesh quality checks
- UCX mesh shape presence
- UCX freeze transform state
- UCX construction history
- UCX polycount limit
- UCX zero thickness state
- UCX visibility state
- UCX locked transform attributes

EXPORT FEATURES
The tool can:
- Export selected ready assets to FBX
- Skip blocked assets
- Optionally export assets with warnings
- Write a JSON validation/export report
- Export matching UCX collision meshes inside the same FBX file as the main mesh
- Avoid duplicate FBX filename overwrites by creating unique export names
- Prevent UCX_* collision meshes from being treated as base export assets
- Use Base asset name or Exact custom target name for UCX matching
- Optionally control triangulate export from the UI
- Disable unnecessary FBX export elements such as cameras, lights, constraints, skins, blend shapes, and embedded textures

UCX COLLISION NAMING
For Unreal Engine custom collision, use the UCX naming convention.

Example base asset:
SM_Sofa

Single collision mesh:
UCX_SM_Sofa

Multiple collision parts:
UCX_SM_Sofa_01
UCX_SM_Sofa_02
UCX_SM_Sofa_03

If Accept Multiple Parts is enabled, matching UCX_* collision parts are included in the same FBX export selection as the main asset.

IMPORTANT UCX EXPORT NOTE
UCX collision meshes are not exported as separate FBX files.

Correct expected output:
wall_corner_01.fbx

Inside that single FBX file, the main mesh and the matching UCX collision mesh are exported together:
wall_corner_01
UCX_wall_corner_01

The tool does not create this kind of separate file by default:
UCX_wall_corner_01.fbx

In Unreal Engine, UCX meshes are imported as custom/simple collision for the Static Mesh. They may not appear as separate visible mesh assets in the Content Browser.

To verify UCX collision in Unreal Engine:
1. Import the FBX.
2. Open the imported Static Mesh asset.
3. Enable collision display, such as Show > Simple Collision.
4. Confirm that the custom/simple collision appears around the mesh.

COLLISION MATCH MODES
Collision Rules include two match modes.

Base asset name:
If the selected base asset is named:
SM_Table

The expected collision names are:
UCX_SM_Table
UCX_SM_Table_01
UCX_SM_Table_02

Exact custom target name:
If Custom Target Name is set to:
Chair_A

The expected collision names are:
UCX_Chair_A
UCX_Chair_A_01
UCX_Chair_A_02

Use Exact custom target name when the visual mesh selection name and the intended Unreal collision target name are different.

MATCHED UCX MESH VALIDATION
The v12 UI adds the following controls inside Collision Rules:
- Validate Matched UCX Meshes
- UCX Mesh Validation Severity

When Validate Matched UCX Meshes is enabled, the tool checks matched UCX collision meshes in addition to checking whether they exist and match the correct name.

Matched UCX mesh validation can check:
- Has Mesh Shape
- Freeze Transform
- History
- Polycount
- Zero Thickness
- Visibility
- Locked Attributes

UCX Mesh Validation Severity controls how UCX mesh quality failures affect the base asset:
- off: do not apply UCX mesh validation results to warnings or blocking issues
- warning: report UCX mesh validation failures as warnings
- blocking: report UCX mesh validation failures as blocking issues and prevent export when Skip Blocked Assets is enabled

UCX_* objects are still not treated as base assets. Select the main render mesh. The tool will find matching UCX meshes and validate them as collision helpers.


FRONT AXIS AND PIVOT NOTES
The tool treats the Y axis as the height/up axis in the Maya scene.

Supported front axis options:
- +X
- -X
- +Z
- -Z

The +Y and -Y front axis options were removed in the fixed version to avoid conflicting with height/up-based pivot calculations.

Pivot target calculations are performed on the horizontal X/Z plane while keeping Y as the vertical axis.


GRID VALIDATION NOTES
Grid validation can check both:
- Bounding box dimensions against the selected grid step
- Bounding box min/max coordinates against the selected grid step when Check Bounds Snap is enabled

Example:
If Grid Step is 10 cm, the tool can check whether minX, minY, minZ, maxX, maxY, and maxZ align to the 10 cm grid.

This is useful for modular environment assets where both size and placement must align cleanly to a grid.


ZERO THICKNESS NOTES
The fixed version includes a working Zero Thickness validation option.

If width, height, or depth is below or equal to the configured tolerance, the tool reports a warning. This helps detect very thin or nearly flat geometry that may cause issues in a game asset pipeline.

The same near-zero thickness concept is also used for matched UCX mesh validation when Validate Matched UCX Meshes is enabled.


JSON REPORT
If Write JSON Report is enabled, the tool writes a report file to the selected export folder.

The report includes:
- Profile name
- Front axis
- Total checked assets
- Ready assets
- Warning assets
- Blocked assets
- Exported assets
- Skipped assets
- Failed exports
- Per-asset validation results
- Collision matching data
- Matched UCX mesh validation data
- Export messages

The report is written using UTF-8 encoding for better support of special characters in asset names.


IMPORTANT NOTES
- The tool works with selected mesh transforms.
- Select the main render mesh, not only the UCX collision mesh.
- UCX_* transforms are not treated as base assets.
- UCX_* transforms are used as collision meshes only when they match the selected base asset or the custom target name.
- Matching UCX collision meshes are exported inside the same FBX file as the main mesh.
- The tool does not create separate FBX files for UCX collision meshes.
- In Unreal Engine, UCX meshes are imported as custom/simple collision for the Static Mesh.
- To verify UCX collision in Unreal Engine, open the imported Static Mesh asset and enable collision display.
- FBX export requires Maya's FBX plugin to load correctly.
- This tool does not automatically import assets into Unreal Engine.
- The generated FBX files can be imported manually into Unreal Engine or used with a separate Unreal Python / Editor Utility import pipeline.
- This is a Maya-side validation and export helper tool, not a full Unreal Engine importer.


VERSION NOTES
This fixed v12 release includes the following major updates:
- UCX collision meshes are included in FBX export selection.
- UCX collision meshes are documented as being exported inside the same FBX, not as separate FBX files.
- Collision Match Mode is functional.
- Custom Target Name support is functional.
- Matched UCX Mesh Validation controls are visible inside Collision Rules.
- Validate Matched UCX Meshes is available.
- UCX Mesh Validation Severity is available.
- Matched UCX mesh validation can report UCX-specific mesh quality issues.
- Grid Bounds Snap validation is active.
- Zero Thickness validation is active.
- +Y and -Y front axis options were removed for pivot consistency.
- The script is import-safe and launches through show().
- JSON report writing uses UTF-8 support.
- Duplicate FBX filename overwrites are reduced.
- UCX_* meshes are excluded from base asset selection.
- FBX export settings were expanded.
- The installer uses the correct M2U_Tools shelf name.
- The patched all-in-one installer avoids Maya module cache and wrong-path issues.

COMPATIBILITY

M2U Studio Custom is designed to work inside Autodesk Maya 2024 and newer versions.

The installer and tool use Maya's built-in Python environment, maya.cmds, and maya.mel. No external Python packages or PyMEL installation are required.

Tested/targeted environment:
- Autodesk Maya 2024+
- Maya Script Editor > Python tab
- Maya UI / shelf workflow
- FBX plugin available through Maya


CONTACT / OFFICIAL DISTRIBUTION
Please download the tool only from the author's official release page or official distribution location.
Unauthorized re-uploading, repackaging, or redistribution is not allowed.

Please download the tool only from the author's official release page or official distribution location.
Unauthorized re-uploading or repackaging is not allowed.
