# -*- coding: utf-8 -*-
"""
M2U Studio Custom v12 - ALL-IN-ONE HARD INSTALLER

This installer writes the bundled verified v12 script to the selected folder,
then creates a fresh Maya shelf button that source-loads that exact file.
It avoids sys.path conflicts, stale .pyc files, old Maya module cache, and
wrong-folder copies.
"""
from __future__ import print_function

import os
import io
import base64
import zlib
import hashlib
import maya.cmds as cmds
import maya.mel as mel

SHELF_LABEL = "M2U_Tools"
BUTTON_LABEL = "M2U Studio Custom v12 FINAL PATCHED"
MODULE_FILE = "m2u_studio_custom_fixed.py"
ICON_FILE = "m2u_studio_custom_icon.png"
EXPECTED_BUILD_ID = "v12_ucx_ui_final"
EXPECTED_SHA256 = "70e0e397daacfeb45314db7d3bb5ca7ce141977fa1078123346f3c6a8f5825c3"

BUNDLED_SCRIPT_B64_ZLIB = """
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
MmM=
"""


def _decode_script_bytes():
    data = BUNDLED_SCRIPT_B64_ZLIB.replace("\n", "").replace("\r", "").strip()
    return zlib.decompress(base64.b64decode(data))


def _sha256(data):
    return hashlib.sha256(data).hexdigest()


def _ensure_shelf(label):
    top = mel.eval("$tmp=$gShelfTopLevel")
    children = cmds.shelfTabLayout(top, q=True, childArray=True) or []
    shelf_name = None
    for i, child in enumerate(children, start=1):
        try:
            tab_label = cmds.shelfTabLayout(top, q=True, tabLabelIndex=i)
        except Exception:
            tab_label = None
        if tab_label == label or child == label:
            shelf_name = child
            break
    if not shelf_name:
        shelf_name = cmds.shelfLayout(label, parent=top)
        cmds.shelfTabLayout(top, e=True, tabLabel=(shelf_name, label))
    return top, shelf_name


def _remove_old_m2u_buttons(shelf_name):
    labels_to_remove = set([
        "M2U Studio Custom",
        "M2U Studio Custom v12",
        "M2U Studio Custom v12 FINAL",
    ])
    for child in (cmds.shelfLayout(shelf_name, q=True, childArray=True) or []):
        try:
            label = cmds.shelfButton(child, q=True, label=True)
            if label in labels_to_remove:
                cmds.deleteUI(child)
        except Exception:
            pass


folder = cmds.fileDialog2(fileMode=3, caption="Select install folder for M2U Studio Custom v12 FINAL")
if not folder:
    raise RuntimeError("Installation cancelled.")

base_dir = folder[0]
if not os.path.isdir(base_dir):
    cmds.error("Invalid folder: " + base_dir)

script_bytes = _decode_script_bytes()
actual_sha = _sha256(script_bytes)
if actual_sha != EXPECTED_SHA256:
    cmds.error("Bundled M2U script checksum mismatch. Expected {0}, got {1}".format(EXPECTED_SHA256, actual_sha))

module_path = os.path.join(base_dir, MODULE_FILE)
with io.open(module_path, "wb") as f:
    f.write(script_bytes)

with io.open(module_path, "rb") as f:
    written_bytes = f.read()
written_sha = _sha256(written_bytes)
if written_sha != EXPECTED_SHA256:
    cmds.error("Written M2U script checksum mismatch. Expected {0}, got {1}".format(EXPECTED_SHA256, written_sha))

source_text = written_bytes.decode("utf-8", "replace")
if 'M2U_BUILD_ID = "' + EXPECTED_BUILD_ID + '"' not in source_text:
    cmds.error("Written file does not contain the expected v12 build marker: " + module_path)

icon_path = os.path.join(base_dir, ICON_FILE)
shelf_icon = icon_path if os.path.isfile(icon_path) else "commandButton.png"
if shelf_icon == "commandButton.png":
    cmds.warning("Icon file not found. Using default Maya shelf icon: " + ICON_FILE)

top, shelf_name = _ensure_shelf(SHELF_LABEL)
_remove_old_m2u_buttons(shelf_name)

launch_cmd = """
import os
import io
import hashlib
import maya.cmds as cmds

module_path = r\"{module_path}\"
expected_build = \"{expected_build}\"
expected_sha = \"{expected_sha}\"

if not os.path.isfile(module_path):
    cmds.confirmDialog(
        title=\"M2U Studio Custom v12 FINAL\",
        message=\"Script file not found:\\n\" + module_path,
        button=[\"OK\"],
        icon=\"critical\"
    )
    raise RuntimeError(\"M2U script file not found: \" + module_path)

with io.open(module_path, \"rb\") as f:
    source_bytes = f.read()

actual_sha = hashlib.sha256(source_bytes).hexdigest()
source_text = source_bytes.decode(\"utf-8\", \"replace\")

if actual_sha != expected_sha:
    cmds.confirmDialog(
        title=\"M2U Studio Custom v12 FINAL\",
        message=\"Wrong script file content at this path.\\n\\nExpected SHA256:\\n\" + expected_sha + \"\\n\\nActual SHA256:\\n\" + actual_sha + \"\\n\\nLoaded file:\\n\" + module_path,
        button=[\"OK\"],
        icon=\"critical\"
    )
    raise RuntimeError(\"M2U script checksum mismatch: \" + module_path)

marker = 'M2U_BUILD_ID = \"' + expected_build + '\"'
if marker not in source_text:
    cmds.confirmDialog(
        title=\"M2U Studio Custom v12 FINAL\",
        message=\"The selected file does not contain the v12 build marker.\\n\\nLoaded file:\\n\" + module_path,
        button=[\"OK\"],
        icon=\"critical\"
    )
    raise RuntimeError(\"M2U v12 build marker missing: \" + module_path)

namespace = {{
    \"__file__\": module_path,
    \"__name__\": \"__m2u_v12_source_loaded__\",
}}
code = compile(source_text, module_path, \"exec\")
exec(code, namespace)

build_id = namespace.get(\"M2U_BUILD_ID\", \"unknown\")
if build_id != expected_build:
    cmds.confirmDialog(
        title=\"M2U Studio Custom v12 FINAL\",
        message=\"Expected build \" + expected_build + \" but loaded: \" + str(build_id) + \"\\n\\nLoaded file:\\n\" + module_path,
        button=[\"OK\"],
        icon=\"critical\"
    )
    raise RuntimeError(\"M2U build mismatch: \" + str(build_id))

show_func = namespace.get(\"show\")
if not show_func:
    cmds.confirmDialog(
        title=\"M2U Studio Custom v12 FINAL\",
        message=\"show() function was not found in the loaded script.\\n\\nLoaded file:\\n\" + module_path,
        button=[\"OK\"],
        icon=\"critical\"
    )
    raise RuntimeError(\"M2U show() missing\")

print(\"M2U v12 FINAL source-loaded from:\", module_path)
print(\"M2U v12 FINAL SHA256:\", actual_sha)
show_func()
""".format(module_path=module_path.replace("\\", "\\\\"), expected_build=EXPECTED_BUILD_ID, expected_sha=EXPECTED_SHA256)

cmds.shelfButton(
    parent=shelf_name,
    label=BUTTON_LABEL,
    annotation="M2U Studio Custom v12 FINAL - source-loaded exact file",
    image1=shelf_icon,
    style="iconOnly",
    sourceType="python",
    command=launch_cmd
)

cmds.shelfTabLayout(top, e=True, selectTab=shelf_name)
cmds.confirmDialog(
    title="M2U Installer v12 FINAL",
    message=(
        "Installed M2U Studio Custom v12 FINAL.\n\n"
        "Script written to:\n" + module_path + "\n\n"
        "SHA256:\n" + EXPECTED_SHA256 + "\n\n"
        "Use the NEW shelf button labeled:\n" + BUTTON_LABEL
    ),
    button=["OK"]
)
