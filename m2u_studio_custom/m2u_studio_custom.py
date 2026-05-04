import os
import re
import json
import maya.cmds as cmds
import maya.mel as mel


class StudioCustomWindow(object):
    WINDOW_NAME = "m2uStudioCustomWindow"
    WINDOW_TITLE = "M2U Studio Custom"

    def __init__(self):
        self.widgets = {}
        self.last_results = []

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------
    def show(self):
        if cmds.window(self.WINDOW_NAME, exists=True):
            cmds.deleteUI(self.WINDOW_NAME)

        self.widgets = {}
        self.last_results = []

        cmds.window(self.WINDOW_NAME, title=self.WINDOW_TITLE, sizeable=True, widthHeight=(640, 900))
        cmds.scrollLayout(childResizable=True)
        cmds.columnLayout(adjustableColumn=True, rowSpacing=8)

        self._build_header()
        self._build_asset_scope_frame()
        self._build_pivot_frame()
        self._build_dimension_frame()
        self._build_grid_frame()
        self._build_geometry_frame()
        self._build_naming_frame()
        self._build_collision_frame()
        self._build_export_frame()
        self._build_actions_frame()
        self._build_results_frame()

        cmds.showWindow(self.WINDOW_NAME)

    def _section_frame(self, title):
        return cmds.frameLayout(
            label=title,
            collapsable=True,
            collapse=False,
            marginWidth=10,
            marginHeight=8
        )

    def _build_header(self):
        cmds.separator(height=8, style="none")
        cmds.text(label="M2U Studio Custom", align="left", height=24, font="boldLabelFont")
        cmds.text(
            label="User-defined validation specification for selected assets.",
            align="left",
            height=20
        )
        cmds.separator(height=8, style="in")

    def _build_asset_scope_frame(self):
        self._section_frame("Asset Scope")
        cmds.columnLayout(adjustableColumn=True, rowSpacing=6)

        self.widgets["selection_mode_label"] = cmds.textFieldGrp(
            label="Selection Mode",
            text="Selected Assets",
            editable=False,
            columnWidth=[(1, 140), (2, 260)]
        )

        self.widgets["front_axis"] = cmds.optionMenuGrp(
            label="Front Axis",
            columnWidth=[(1, 140), (2, 260)]
        )
        for item in ["+X", "-X", "+Y", "-Y", "+Z", "-Z"]:
            cmds.menuItem(label=item)
        cmds.optionMenuGrp(self.widgets["front_axis"], e=True, value="+X")

        cmds.setParent("..")
        cmds.setParent("..")

    def _build_pivot_frame(self):
        self._section_frame("Pivot Rules")
        cmds.columnLayout(adjustableColumn=True, rowSpacing=6)

        self.widgets["pivot_enabled"] = cmds.checkBoxGrp(
            numberOfCheckBoxes=1,
            label="Enable Pivot Check",
            value1=True
        )

        self.widgets["pivot_target"] = cmds.optionMenuGrp(
            label="Pivot Target",
            columnWidth=[(1, 140), (2, 260)]
        )
        pivot_targets = [
            "Center",
            "Bottom Center",
            "Bottom Front Center",
            "Bottom Back Center",
            "Bottom Left Center",
            "Bottom Right Center",
            "Bottom Front Left",
            "Bottom Front Right",
            "Bottom Back Left",
            "Bottom Back Right",
            "Front Center",
            "Back Center",
            "Left Center",
            "Right Center",
            "Top Center",
            "Top Front Center",
            "Top Back Center",
            "Top Left Center",
            "Top Right Center",
            "Top Front Left",
            "Top Front Right",
            "Top Back Left",
            "Top Back Right",
        ]
        for item in pivot_targets:
            cmds.menuItem(label=item)
        cmds.optionMenuGrp(self.widgets["pivot_target"], e=True, value="Bottom Front Center")

        self.widgets["pivot_tolerance"] = cmds.floatFieldGrp(
            numberOfFields=1,
            label="Pivot Tolerance (cm)",
            value1=0.5,
            columnWidth=[(1, 140), (2, 120)]
        )

        self.widgets["pivot_severity"] = cmds.optionMenuGrp(
            label="Severity",
            columnWidth=[(1, 140), (2, 260)]
        )
        for item in ["off", "warning", "blocking"]:
            cmds.menuItem(label=item)
        cmds.optionMenuGrp(self.widgets["pivot_severity"], e=True, value="warning")

        cmds.setParent("..")
        cmds.setParent("..")

    def _build_dimension_frame(self):
        self._section_frame("Dimension Rules")
        cmds.columnLayout(adjustableColumn=True, rowSpacing=6)

        self.widgets["dimension_enabled"] = cmds.checkBoxGrp(
            numberOfCheckBoxes=1,
            label="Enable Dimension Check",
            value1=True
        )

        self.widgets["expected_width"] = cmds.floatFieldGrp(
            numberOfFields=1,
            label="Expected Width (cm)",
            value1=100.0,
            columnWidth=[(1, 140), (2, 120)]
        )
        self.widgets["expected_height"] = cmds.floatFieldGrp(
            numberOfFields=1,
            label="Expected Height (cm)",
            value1=300.0,
            columnWidth=[(1, 140), (2, 120)]
        )
        self.widgets["expected_depth"] = cmds.floatFieldGrp(
            numberOfFields=1,
            label="Expected Depth (cm)",
            value1=20.0,
            columnWidth=[(1, 140), (2, 120)]
        )
        self.widgets["size_tolerance"] = cmds.floatFieldGrp(
            numberOfFields=1,
            label="Size Tolerance (cm)",
            value1=0.5,
            columnWidth=[(1, 140), (2, 120)]
        )

        self.widgets["dimension_severity"] = cmds.optionMenuGrp(
            label="Severity",
            columnWidth=[(1, 140), (2, 260)]
        )
        for item in ["off", "warning", "blocking"]:
            cmds.menuItem(label=item)
        cmds.optionMenuGrp(self.widgets["dimension_severity"], e=True, value="blocking")

        cmds.setParent("..")
        cmds.setParent("..")

    def _build_grid_frame(self):
        self._section_frame("Grid Rules")
        cmds.columnLayout(adjustableColumn=True, rowSpacing=6)

        self.widgets["grid_enabled"] = cmds.checkBoxGrp(
            numberOfCheckBoxes=1,
            label="Enable Grid Check",
            value1=True
        )
        self.widgets["grid_step"] = cmds.floatFieldGrp(
            numberOfFields=1,
            label="Grid Step (cm)",
            value1=10.0,
            columnWidth=[(1, 140), (2, 120)]
        )
        self.widgets["grid_snap"] = cmds.checkBoxGrp(
            numberOfCheckBoxes=1,
            label="Check Bounds Snap",
            value1=True
        )

        self.widgets["grid_severity"] = cmds.optionMenuGrp(
            label="Severity",
            columnWidth=[(1, 140), (2, 260)]
        )
        for item in ["off", "warning", "blocking"]:
            cmds.menuItem(label=item)
        cmds.optionMenuGrp(self.widgets["grid_severity"], e=True, value="warning")

        cmds.setParent("..")
        cmds.setParent("..")

    def _build_geometry_frame(self):
        self._section_frame("Geometry Rules")
        cmds.columnLayout(adjustableColumn=True, rowSpacing=6)

        self.widgets["max_polycount"] = cmds.intFieldGrp(
            numberOfFields=1,
            label="Max Polycount",
            value1=5000,
            columnWidth=[(1, 140), (2, 120)]
        )
        self.widgets["freeze_required"] = cmds.checkBoxGrp(
            numberOfCheckBoxes=1,
            label="Freeze Required",
            value1=True
        )
        self.widgets["history_required"] = cmds.checkBoxGrp(
            numberOfCheckBoxes=1,
            label="Clean History Required",
            value1=True
        )
        self.widgets["zero_thickness"] = cmds.checkBoxGrp(
            numberOfCheckBoxes=1,
            label="Zero Thickness Warning",
            value1=True
        )

        cmds.setParent("..")
        cmds.setParent("..")

    def _build_naming_frame(self):
        self._section_frame("Naming Rules")
        cmds.columnLayout(adjustableColumn=True, rowSpacing=6)

        self.widgets["prefix_enabled"] = cmds.checkBoxGrp(
            numberOfCheckBoxes=1,
            label="Enable Prefix Rule",
            value1=False
        )
        self.widgets["naming_prefix"] = cmds.textFieldGrp(
            label="Naming Prefix",
            text="SM_",
            columnWidth=[(1, 140), (2, 200)]
        )

        self.widgets["name_severity"] = cmds.optionMenuGrp(
            label="Severity",
            columnWidth=[(1, 140), (2, 260)]
        )
        for item in ["off", "warning", "blocking"]:
            cmds.menuItem(label=item)
        cmds.optionMenuGrp(self.widgets["name_severity"], e=True, value="warning")

        cmds.setParent("..")
        cmds.setParent("..")

    def _build_collision_frame(self):
        self._section_frame("Collision Rules")
        cmds.columnLayout(adjustableColumn=True, rowSpacing=6)

        self.widgets["ucx_enabled"] = cmds.checkBoxGrp(
            numberOfCheckBoxes=1,
            label="Check UCX Collision",
            value1=True
        )

        self.widgets["collision_requirement"] = cmds.optionMenuGrp(
            label="Collision Requirement",
            columnWidth=[(1, 140), (2, 260)]
        )
        for item in ["Off", "UCX required", "UCX optional", "No custom collision allowed"]:
            cmds.menuItem(label=item)
        cmds.optionMenuGrp(self.widgets["collision_requirement"], e=True, value="UCX required")

        self.widgets["match_mode"] = cmds.optionMenuGrp(
            label="Match Mode",
            columnWidth=[(1, 140), (2, 260)]
        )
        for item in ["Base asset name", "Exact custom target name"]:
            cmds.menuItem(label=item)
        cmds.optionMenuGrp(self.widgets["match_mode"], e=True, value="Base asset name")

        self.widgets["accept_multiple_parts"] = cmds.checkBoxGrp(
            numberOfCheckBoxes=1,
            label="Accept Multiple Parts",
            value1=True
        )

        self.widgets["collision_severity"] = cmds.optionMenuGrp(
            label="Severity",
            columnWidth=[(1, 140), (2, 260)]
        )
        for item in ["off", "warning", "blocking"]:
            cmds.menuItem(label=item)
        cmds.optionMenuGrp(self.widgets["collision_severity"], e=True, value="warning")

        cmds.setParent("..")
        cmds.setParent("..")

    def _build_export_frame(self):
        self._section_frame("Export Behavior")
        cmds.columnLayout(adjustableColumn=True, rowSpacing=6)

        self.widgets["export_ready_assets"] = cmds.checkBoxGrp(
            numberOfCheckBoxes=1,
            label="Export Ready Assets",
            value1=True
        )
        self.widgets["skip_blocked_assets"] = cmds.checkBoxGrp(
            numberOfCheckBoxes=1,
            label="Skip Blocked Assets",
            value1=True
        )
        self.widgets["export_warning_assets"] = cmds.checkBoxGrp(
            numberOfCheckBoxes=1,
            label="Export Warning Assets",
            value1=True
        )
        self.widgets["write_json_report"] = cmds.checkBoxGrp(
            numberOfCheckBoxes=1,
            label="Write JSON Report",
            value1=True
        )

        cmds.setParent("..")
        cmds.setParent("..")

    def _build_actions_frame(self):
        self._section_frame("Actions")
        cmds.columnLayout(adjustableColumn=True, rowSpacing=8)

        cmds.button(
            label="Validate Selected Assets",
            height=36,
            command=lambda *_: self.validate_selected_assets()
        )
        cmds.button(
            label="Export Selected Assets",
            height=36,
            command=lambda *_: self.export_selected_assets()
        )
        cmds.button(
            label="Clear Results",
            height=28,
            command=lambda *_: self.clear_results()
        )

        cmds.setParent("..")
        cmds.setParent("..")

    def _build_results_frame(self):
        self._section_frame("Results")
        cmds.columnLayout(adjustableColumn=True, rowSpacing=6)

        self.widgets["summary_text"] = cmds.text(
            label="No validation run yet.",
            align="left",
            height=24
        )
        self.widgets["results_scroll"] = cmds.scrollField(
            editable=False,
            wordWrap=True,
            text="",
            height=340
        )

        cmds.setParent("..")
        cmds.setParent("..")

    # ---------------------------------------------------------
    # Rule data
    # ---------------------------------------------------------
    def get_rule_data(self):
        return {
            "profile": "Studio Custom",
            "asset_scope": {
                "selection_mode": "Selected Assets",
                "front_axis": cmds.optionMenuGrp(self.widgets["front_axis"], q=True, value=True),
            },
            "pivot_rules": {
                "enabled": cmds.checkBoxGrp(self.widgets["pivot_enabled"], q=True, value1=True),
                "target": cmds.optionMenuGrp(self.widgets["pivot_target"], q=True, value=True),
                "tolerance_cm": cmds.floatFieldGrp(self.widgets["pivot_tolerance"], q=True, value1=True),
                "severity": cmds.optionMenuGrp(self.widgets["pivot_severity"], q=True, value=True),
            },
            "dimension_rules": {
                "enabled": cmds.checkBoxGrp(self.widgets["dimension_enabled"], q=True, value1=True),
                "expected_width_cm": cmds.floatFieldGrp(self.widgets["expected_width"], q=True, value1=True),
                "expected_height_cm": cmds.floatFieldGrp(self.widgets["expected_height"], q=True, value1=True),
                "expected_depth_cm": cmds.floatFieldGrp(self.widgets["expected_depth"], q=True, value1=True),
                "tolerance_cm": cmds.floatFieldGrp(self.widgets["size_tolerance"], q=True, value1=True),
                "severity": cmds.optionMenuGrp(self.widgets["dimension_severity"], q=True, value=True),
            },
            "grid_rules": {
                "enabled": cmds.checkBoxGrp(self.widgets["grid_enabled"], q=True, value1=True),
                "grid_step_cm": cmds.floatFieldGrp(self.widgets["grid_step"], q=True, value1=True),
                "check_bounds_snap": cmds.checkBoxGrp(self.widgets["grid_snap"], q=True, value1=True),
                "severity": cmds.optionMenuGrp(self.widgets["grid_severity"], q=True, value=True),
            },
            "geometry_rules": {
                "max_polycount": cmds.intFieldGrp(self.widgets["max_polycount"], q=True, value1=True),
                "freeze_required": cmds.checkBoxGrp(self.widgets["freeze_required"], q=True, value1=True),
                "clean_history_required": cmds.checkBoxGrp(self.widgets["history_required"], q=True, value1=True),
                "zero_thickness_warning": cmds.checkBoxGrp(self.widgets["zero_thickness"], q=True, value1=True),
            },
            "naming_rules": {
                "enabled": cmds.checkBoxGrp(self.widgets["prefix_enabled"], q=True, value1=True),
                "prefix": cmds.textFieldGrp(self.widgets["naming_prefix"], q=True, text=True),
                "severity": cmds.optionMenuGrp(self.widgets["name_severity"], q=True, value=True),
            },
            "collision_rules": {
                "enabled": cmds.checkBoxGrp(self.widgets["ucx_enabled"], q=True, value1=True),
                "requirement": cmds.optionMenuGrp(self.widgets["collision_requirement"], q=True, value=True),
                "match_mode": cmds.optionMenuGrp(self.widgets["match_mode"], q=True, value=True),
                "accept_multiple_parts": cmds.checkBoxGrp(self.widgets["accept_multiple_parts"], q=True, value1=True),
                "severity": cmds.optionMenuGrp(self.widgets["collision_severity"], q=True, value=True),
            },
            "export_behavior": {
                "export_ready_assets": cmds.checkBoxGrp(self.widgets["export_ready_assets"], q=True, value1=True),
                "skip_blocked_assets": cmds.checkBoxGrp(self.widgets["skip_blocked_assets"], q=True, value1=True),
                "export_warning_assets": cmds.checkBoxGrp(self.widgets["export_warning_assets"], q=True, value1=True),
                "write_json_report": cmds.checkBoxGrp(self.widgets["write_json_report"], q=True, value1=True),
            }
        }

    # ---------------------------------------------------------
    # Scene helpers
    # ---------------------------------------------------------
    def get_selected_transforms(self):
        selected = cmds.ls(selection=True, long=True, type="transform") or []
        valid = []
        for obj in selected:
            shapes = cmds.listRelatives(obj, shapes=True, noIntermediate=True, fullPath=True) or []
            mesh_shapes = [s for s in shapes if cmds.nodeType(s) == "mesh"]
            if mesh_shapes:
                valid.append(obj)
        return valid

    def short_name(self, node):
        return node.split("|")[-1]

    def safe_filename(self, name):
        return re.sub(r'[^A-Za-z0-9._-]+', '_', name)

    def get_world_bbox(self, transform):
        bb = cmds.exactWorldBoundingBox(transform)
        return {
            "minX": bb[0], "minY": bb[1], "minZ": bb[2],
            "maxX": bb[3], "maxY": bb[4], "maxZ": bb[5]
        }

    def get_bbox_sizes(self, transform):
        bb = self.get_world_bbox(transform)
        return (
            abs(bb["maxX"] - bb["minX"]),
            abs(bb["maxY"] - bb["minY"]),
            abs(bb["maxZ"] - bb["minZ"])
        )

    def get_pivot_position(self, transform):
        pos = cmds.xform(transform, q=True, ws=True, rp=True)
        return (pos[0], pos[1], pos[2])

    def _front_back_left_right_from_axis(self, bb, front_axis):
        x_mid = (bb["minX"] + bb["maxX"]) * 0.5
        y_mid = (bb["minY"] + bb["maxY"]) * 0.5
        z_mid = (bb["minZ"] + bb["maxZ"]) * 0.5

        front = [x_mid, y_mid, z_mid]
        back = [x_mid, y_mid, z_mid]
        left = [x_mid, y_mid, z_mid]
        right = [x_mid, y_mid, z_mid]

        if front_axis == "+X":
            front[0] = bb["maxX"]
            back[0] = bb["minX"]
            left[2] = bb["minZ"]
            right[2] = bb["maxZ"]
        elif front_axis == "-X":
            front[0] = bb["minX"]
            back[0] = bb["maxX"]
            left[2] = bb["maxZ"]
            right[2] = bb["minZ"]
        elif front_axis == "+Y":
            front[1] = bb["maxY"]
            back[1] = bb["minY"]
            left[0] = bb["minX"]
            right[0] = bb["maxX"]
        elif front_axis == "-Y":
            front[1] = bb["minY"]
            back[1] = bb["maxY"]
            left[0] = bb["maxX"]
            right[0] = bb["minX"]
        elif front_axis == "+Z":
            front[2] = bb["maxZ"]
            back[2] = bb["minZ"]
            left[0] = bb["maxX"]
            right[0] = bb["minX"]
        elif front_axis == "-Z":
            front[2] = bb["minZ"]
            back[2] = bb["maxZ"]
            left[0] = bb["minX"]
            right[0] = bb["maxX"]

        return tuple(front), tuple(back), tuple(left), tuple(right)

    def get_target_pivot_position(self, transform, pivot_target, front_axis):
        bb = self.get_world_bbox(transform)

        cx = (bb["minX"] + bb["maxX"]) * 0.5
        cy = (bb["minY"] + bb["maxY"]) * 0.5
        cz = (bb["minZ"] + bb["maxZ"]) * 0.5

        front, back, left, right = self._front_back_left_right_from_axis(bb, front_axis)

        target_map = {
            "Center": (cx, cy, cz),

            "Bottom Center": (cx, bb["minY"], cz),
            "Bottom Front Center": (front[0], bb["minY"], front[2]),
            "Bottom Back Center": (back[0], bb["minY"], back[2]),
            "Bottom Left Center": (left[0], bb["minY"], left[2]),
            "Bottom Right Center": (right[0], bb["minY"], right[2]),

            "Front Center": (front[0], cy, front[2]),
            "Back Center": (back[0], cy, back[2]),
            "Left Center": (left[0], cy, left[2]),
            "Right Center": (right[0], cy, right[2]),

            "Top Center": (cx, bb["maxY"], cz),
            "Top Front Center": (front[0], bb["maxY"], front[2]),
            "Top Back Center": (back[0], bb["maxY"], back[2]),
            "Top Left Center": (left[0], bb["maxY"], left[2]),
            "Top Right Center": (right[0], bb["maxY"], right[2]),
        }

        bottom_y = bb["minY"]
        top_y = bb["maxY"]

        if front_axis in ["+X", "-X"]:
            if front_axis == "+X":
                front_x = bb["maxX"]
                back_x = bb["minX"]
                left_z = bb["minZ"]
                right_z = bb["maxZ"]
            else:
                front_x = bb["minX"]
                back_x = bb["maxX"]
                left_z = bb["maxZ"]
                right_z = bb["minZ"]

            target_map.update({
                "Bottom Front Left": (front_x, bottom_y, left_z),
                "Bottom Front Right": (front_x, bottom_y, right_z),
                "Bottom Back Left": (back_x, bottom_y, left_z),
                "Bottom Back Right": (back_x, bottom_y, right_z),
                "Top Front Left": (front_x, top_y, left_z),
                "Top Front Right": (front_x, top_y, right_z),
                "Top Back Left": (back_x, top_y, left_z),
                "Top Back Right": (back_x, top_y, right_z),
            })

        elif front_axis in ["+Z", "-Z"]:
            if front_axis == "+Z":
                front_z = bb["maxZ"]
                back_z = bb["minZ"]
                left_x = bb["maxX"]
                right_x = bb["minX"]
            else:
                front_z = bb["minZ"]
                back_z = bb["maxZ"]
                left_x = bb["minX"]
                right_x = bb["maxX"]

            target_map.update({
                "Bottom Front Left": (left_x, bottom_y, front_z),
                "Bottom Front Right": (right_x, bottom_y, front_z),
                "Bottom Back Left": (left_x, bottom_y, back_z),
                "Bottom Back Right": (right_x, bottom_y, back_z),
                "Top Front Left": (left_x, top_y, front_z),
                "Top Front Right": (right_x, top_y, front_z),
                "Top Back Left": (left_x, top_y, back_z),
                "Top Back Right": (right_x, top_y, back_z),
            })

        return target_map.get(pivot_target, (cx, cy, cz))

    def find_ucx_matches(self, asset_name, accept_multiple_parts=True):
        transforms = cmds.ls(type="transform", long=True) or []
        matches = []
        base_pattern = "UCX_{0}".format(asset_name)

        for node in transforms:
            short = self.short_name(node)
            if short == base_pattern:
                matches.append(short)
                continue
            if accept_multiple_parts and short.startswith(base_pattern + "_"):
                matches.append(short)

        return sorted(set(matches))

    def get_polycount_for_transform(self, transform):
        shapes = cmds.listRelatives(transform, shapes=True, noIntermediate=True, fullPath=True) or []
        mesh_shapes = [s for s in shapes if cmds.nodeType(s) == "mesh"]
        total_faces = 0
        for shape in mesh_shapes:
            try:
                total_faces += cmds.polyEvaluate(shape, face=True) or 0
            except Exception:
                pass
        return total_faces

    def has_freeze_issue(self, transform):
        try:
            tx = cmds.getAttr(transform + ".translateX")
            ty = cmds.getAttr(transform + ".translateY")
            tz = cmds.getAttr(transform + ".translateZ")
            rx = cmds.getAttr(transform + ".rotateX")
            ry = cmds.getAttr(transform + ".rotateY")
            rz = cmds.getAttr(transform + ".rotateZ")
            sx = cmds.getAttr(transform + ".scaleX")
            sy = cmds.getAttr(transform + ".scaleY")
            sz = cmds.getAttr(transform + ".scaleZ")
            return not (
                abs(tx) < 1e-6 and abs(ty) < 1e-6 and abs(tz) < 1e-6 and
                abs(rx) < 1e-6 and abs(ry) < 1e-6 and abs(rz) < 1e-6 and
                abs(sx - 1.0) < 1e-6 and abs(sy - 1.0) < 1e-6 and abs(sz - 1.0) < 1e-6
            )
        except Exception:
            return False

    def has_history_issue(self, transform):
        history = cmds.listHistory(transform, pruneDagObjects=True) or []
        filtered = []
        for node in history:
            if node == transform:
                continue
            node_type = cmds.nodeType(node)
            if node_type in ["mesh", "shadingEngine", "groupId", "transform"]:
                continue
            filtered.append(node)
        return len(filtered) > 0, filtered

    def _make_check(self, status, reason):
        return {"status": status, "reason": reason}

    def _add_issue(self, result, severity, message):
        if severity == "blocking":
            result["blocking_issues"].append(message)
        elif severity == "warning":
            result["warnings"].append(message)

    def _is_multiple_of_step(self, value, step, epsilon=1e-4):
        if step <= 0.0:
            return False
        ratio = value / step
        return abs(ratio - round(ratio)) <= epsilon

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------
    def validate_asset(self, transform, rule_data):
        short_name = self.short_name(transform)

        result = {
            "asset_name": short_name,
            "asset_path": transform,
            "profile": "Studio Custom",
            "warnings": [],
            "blocking_issues": [],
            "ready_for_export": True,
            "checks": {},
            "export": {
                "status": "not_run",
                "message": ""
            }
        }

        naming_rules = rule_data["naming_rules"]
        if not naming_rules["enabled"]:
            result["checks"]["Naming"] = self._make_check("Pass", "Prefix rule disabled")
        else:
            prefix = naming_rules["prefix"] or ""
            if short_name.startswith(prefix):
                result["checks"]["Naming"] = self._make_check("Pass", "Name matches required prefix: {0}".format(prefix))
            else:
                result["checks"]["Naming"] = self._make_check("Fail", "Name does not start with required prefix: {0}".format(prefix))
                self._add_issue(result, naming_rules["severity"], "Name does not start with required prefix: {0}".format(prefix))

        polycount = self.get_polycount_for_transform(transform)
        max_poly = rule_data["geometry_rules"]["max_polycount"]
        if polycount <= max_poly:
            result["checks"]["Polycount"] = self._make_check("Pass", "{0} / {1}".format(polycount, max_poly))
        else:
            result["checks"]["Polycount"] = self._make_check("Fail", "{0} / {1}".format(polycount, max_poly))
            self._add_issue(result, "blocking", "Polycount exceeds maximum: {0} > {1}".format(polycount, max_poly))

        if not rule_data["geometry_rules"]["freeze_required"]:
            result["checks"]["Freeze Transform"] = self._make_check("Pass", "Freeze check disabled")
        else:
            freeze_issue = self.has_freeze_issue(transform)
            if freeze_issue:
                result["checks"]["Freeze Transform"] = self._make_check("Fail", "Transform values are not frozen")
                self._add_issue(result, "blocking", "Freeze Transform requirement not satisfied.")
            else:
                result["checks"]["Freeze Transform"] = self._make_check("Pass", "Transform values are frozen")

        if not rule_data["geometry_rules"]["clean_history_required"]:
            result["checks"]["History"] = self._make_check("Pass", "History check disabled")
        else:
            history_issue, history_nodes = self.has_history_issue(transform)
            if history_issue:
                preview = ", ".join(history_nodes[:5])
                result["checks"]["History"] = self._make_check("Fail", "Construction history found: {0}".format(preview))
                self._add_issue(result, "warning", "Construction history found: {0}".format(preview))
            else:
                result["checks"]["History"] = self._make_check("Pass", "No construction history found")

        dim_rules = rule_data["dimension_rules"]
        if not dim_rules["enabled"] or dim_rules["severity"] == "off":
            result["checks"]["Dimensions"] = self._make_check("Pass", "Dimension check disabled")
        else:
            width, height, depth = self.get_bbox_sizes(transform)
            tol = dim_rules["tolerance_cm"]
            ew = dim_rules["expected_width_cm"]
            eh = dim_rules["expected_height_cm"]
            ed = dim_rules["expected_depth_cm"]

            width_diff = abs(width - ew)
            height_diff = abs(height - eh)
            depth_diff = abs(depth - ed)

            passed = width_diff <= tol and height_diff <= tol and depth_diff <= tol

            if passed:
                result["checks"]["Dimensions"] = self._make_check(
                    "Pass",
                    "Expected W/H/D: {:.3f}, {:.3f}, {:.3f} | Actual: {:.3f}, {:.3f}, {:.3f} | Tolerance: {:.3f}".format(
                        ew, eh, ed, width, height, depth, tol
                    )
                )
            else:
                result["checks"]["Dimensions"] = self._make_check(
                    "Fail",
                    "Expected W/H/D: {:.3f}, {:.3f}, {:.3f} | Actual: {:.3f}, {:.3f}, {:.3f} | Diff: {:.3f}, {:.3f}, {:.3f} | Tolerance: {:.3f}".format(
                        ew, eh, ed, width, height, depth, width_diff, height_diff, depth_diff, tol
                    )
                )
                self._add_issue(
                    result,
                    dim_rules["severity"],
                    "Dimension mismatch. Expected W/H/D: {:.3f}, {:.3f}, {:.3f} | Actual: {:.3f}, {:.3f}, {:.3f}".format(
                        ew, eh, ed, width, height, depth
                    )
                )

        pivot_rules = rule_data["pivot_rules"]
        if not pivot_rules["enabled"] or pivot_rules["severity"] == "off":
            result["checks"]["Pivot"] = self._make_check("Pass", "Pivot check disabled")
        else:
            pivot_target = pivot_rules["target"]
            front_axis = rule_data["asset_scope"]["front_axis"]
            tolerance = pivot_rules["tolerance_cm"]

            actual = self.get_pivot_position(transform)
            expected = self.get_target_pivot_position(transform, pivot_target, front_axis)

            dx = abs(actual[0] - expected[0])
            dy = abs(actual[1] - expected[1])
            dz = abs(actual[2] - expected[2])

            passed = dx <= tolerance and dy <= tolerance and dz <= tolerance

            if passed:
                result["checks"]["Pivot"] = self._make_check(
                    "Pass",
                    "Target: {0} | Actual: ({1:.3f}, {2:.3f}, {3:.3f}) | Expected: ({4:.3f}, {5:.3f}, {6:.3f}) | Tolerance: {7:.3f}".format(
                        pivot_target,
                        actual[0], actual[1], actual[2],
                        expected[0], expected[1], expected[2],
                        tolerance
                    )
                )
            else:
                result["checks"]["Pivot"] = self._make_check(
                    "Fail",
                    "Target: {0} | Actual: ({1:.3f}, {2:.3f}, {3:.3f}) | Expected: ({4:.3f}, {5:.3f}, {6:.3f}) | Delta: ({7:.3f}, {8:.3f}, {9:.3f}) | Tolerance: {10:.3f}".format(
                        pivot_target,
                        actual[0], actual[1], actual[2],
                        expected[0], expected[1], expected[2],
                        dx, dy, dz,
                        tolerance
                    )
                )
                self._add_issue(result, pivot_rules["severity"], "Pivot does not match target: {0}".format(pivot_target))

        grid_rules = rule_data["grid_rules"]
        if not grid_rules["enabled"] or grid_rules["severity"] == "off":
            result["checks"]["Grid"] = self._make_check("Pass", "Grid check disabled")
        else:
            step = grid_rules["grid_step_cm"]
            width, height, depth = self.get_bbox_sizes(transform)

            width_ok = self._is_multiple_of_step(width, step)
            height_ok = self._is_multiple_of_step(height, step)
            depth_ok = self._is_multiple_of_step(depth, step)

            passed = width_ok and height_ok and depth_ok

            if passed:
                result["checks"]["Grid"] = self._make_check(
                    "Pass",
                    "Bounds W/H/D: {:.3f}, {:.3f}, {:.3f} fit grid step {:.3f}".format(width, height, depth, step)
                )
            else:
                result["checks"]["Grid"] = self._make_check(
                    "Fail",
                    "Bounds W/H/D: {:.3f}, {:.3f}, {:.3f} do not fit grid step {:.3f}".format(width, height, depth, step)
                )
                self._add_issue(result, grid_rules["severity"], "Bounding box size does not fit grid step: {0}".format(step))

        collision_rules = rule_data["collision_rules"]
        if not collision_rules["enabled"] or collision_rules["requirement"] == "Off" or collision_rules["severity"] == "off":
            result["checks"]["UCX Collision"] = self._make_check("Pass", "UCX collision check disabled")
        else:
            matches = self.find_ucx_matches(short_name, collision_rules["accept_multiple_parts"])
            requirement = collision_rules["requirement"]

            if requirement == "UCX required":
                if matches:
                    result["checks"]["UCX Collision"] = self._make_check("Pass", "Matching UCX found: {0}".format(", ".join(matches[:4])))
                else:
                    expected = "UCX_{0}".format(short_name)
                    if collision_rules["accept_multiple_parts"]:
                        expected += " or UCX_{0}_*".format(short_name)
                    result["checks"]["UCX Collision"] = self._make_check("Fail", "No matching UCX found. Expected: {0}".format(expected))
                    self._add_issue(result, collision_rules["severity"], "No matching UCX collision mesh found.")

            elif requirement == "UCX optional":
                if matches:
                    result["checks"]["UCX Collision"] = self._make_check("Pass", "Optional UCX found: {0}".format(", ".join(matches[:4])))
                else:
                    result["checks"]["UCX Collision"] = self._make_check("Pass", "No UCX found, but optional")

            elif requirement == "No custom collision allowed":
                if matches:
                    result["checks"]["UCX Collision"] = self._make_check("Fail", "UCX exists, but current rule does not allow it")
                    self._add_issue(result, collision_rules["severity"], "UCX collision mesh found, but not allowed by current rule.")
                else:
                    result["checks"]["UCX Collision"] = self._make_check("Pass", "No custom UCX found")

        result["ready_for_export"] = len(result["blocking_issues"]) == 0
        return result

    def validate_current_selection(self):
        rule_data = self.get_rule_data()
        selected = self.get_selected_transforms()
        results = []

        if not selected:
            return [], rule_data

        for transform in selected:
            results.append(self.validate_asset(transform, rule_data))

        self.last_results = results
        return results, rule_data

    # ---------------------------------------------------------
    # Export
    # ---------------------------------------------------------
    def ensure_fbx_plugin_loaded(self):
        try:
            if not cmds.pluginInfo("fbxmaya", q=True, loaded=True):
                cmds.loadPlugin("fbxmaya")
            return True, ""
        except Exception as exc:
            return False, str(exc)

    def export_transform_to_fbx(self, transform, export_path):
        original_selection = cmds.ls(selection=True, long=True) or []

        try:
            cmds.select(transform, r=True)
            mel.eval('FBXResetExport;')
            mel.eval('FBXExportSmoothingGroups -v true;')
            mel.eval('FBXExportHardEdges -v false;')
            mel.eval('FBXExportTangents -v true;')
            mel.eval('FBXExportSmoothMesh -v false;')
            mel.eval('FBXExportInstances -v false;')
            mel.eval('FBXExportInAscii -v false;')
            mel.eval('FBXExportAnimationOnly -v false;')
            mel.eval('FBXExportBakeComplexAnimation -v false;')
            mel.eval('FBXExportInputConnections -v false;')

            export_path_mel = export_path.replace("\\", "/")
            mel.eval('FBXExport -f "{0}" -s;'.format(export_path_mel))
            return True, ""
        except Exception as exc:
            return False, str(exc)
        finally:
            if original_selection:
                try:
                    cmds.select(original_selection, r=True)
                except Exception:
                    pass
            else:
                try:
                    cmds.select(clear=True)
                except Exception:
                    pass

    def write_json_report(self, export_folder, rule_data, results, export_summary):
        report_data = {
            "profile": "Studio Custom",
            "selection_mode": "Selected Assets",
            "front_axis": rule_data["asset_scope"]["front_axis"],
            "total_assets": len(results),
            "ready_assets": sum(1 for r in results if r["ready_for_export"]),
            "warning_assets": sum(1 for r in results if r["ready_for_export"] and r["warnings"]),
            "blocked_assets": sum(1 for r in results if not r["ready_for_export"]),
            "exported_assets": export_summary["exported_assets"],
            "skipped_assets": export_summary["skipped_assets"],
            "failed_exports": export_summary["failed_exports"],
            "assets": results
        }

        report_path = os.path.join(export_folder, "m2u_studio_custom_report.json")
        with open(report_path, "w") as f:
            json.dump(report_data, f, indent=2)
        return report_path

    # ---------------------------------------------------------
    # Result formatting
    # ---------------------------------------------------------
    def _format_user_summary(self, results):
        total = len(results)
        blocked = sum(1 for r in results if not r.get("ready_for_export"))
        warning = sum(1 for r in results if r.get("ready_for_export") and r.get("warnings"))
        ready = total - blocked
        return "Assets checked: {0} | Ready: {1} | Warning: {2} | Blocked: {3}".format(
            total, ready, warning, blocked
        )

    def _get_asset_status_label(self, asset_result):
        if asset_result.get("blocking_issues"):
            return "Blocked"
        if asset_result.get("warnings"):
            return "Ready with warning"
        return "Ready"

    def _format_user_results(self, results, include_export=False):
        lines = []
        ordered_checks = [
            "Naming",
            "Polycount",
            "Freeze Transform",
            "History",
            "Dimensions",
            "Pivot",
            "Grid",
            "UCX Collision",
        ]

        for result in results:
            lines.append(result.get("asset_name", "UnnamedAsset"))
            lines.append("  Status: {0}".format(self._get_asset_status_label(result)))
            lines.append("  Checks:")

            for check_name in ordered_checks:
                check_data = result.get("checks", {}).get(check_name)
                if not check_data:
                    continue
                lines.append(
                    "    - {0}: {1} — {2}".format(
                        check_name,
                        check_data.get("status", "Unknown"),
                        check_data.get("reason", "")
                    )
                )

            if include_export:
                export_data = result.get("export", {})
                lines.append("  Export: {0} — {1}".format(
                    export_data.get("status", "not_run"),
                    export_data.get("message", "")
                ))

            lines.append("")

        return "\n".join(lines).strip()

    def _format_export_summary(self, export_folder, results, report_path=None):
        exported = sum(1 for r in results if r.get("export", {}).get("status") == "exported")
        skipped = sum(1 for r in results if r.get("export", {}).get("status") == "skipped")
        failed = sum(1 for r in results if r.get("export", {}).get("status") == "failed")

        lines = []
        lines.append("Export Folder: {0}".format(export_folder))
        lines.append("Exported: {0} | Skipped: {1} | Failed: {2}".format(exported, skipped, failed))
        if report_path:
            lines.append("JSON Report: {0}".format(report_path))
        lines.append("")
        return "\n".join(lines)

    # ---------------------------------------------------------
    # Actions
    # ---------------------------------------------------------
    def validate_selected_assets(self):
        results, _rule_data = self.validate_current_selection()

        if not results:
            cmds.warning("No mesh transform selected.")
            cmds.text(self.widgets["summary_text"], e=True, label="No valid mesh transform selected.")
            cmds.scrollField(self.widgets["results_scroll"], e=True, text="")
            return

        cmds.text(self.widgets["summary_text"], e=True, label=self._format_user_summary(results))
        cmds.scrollField(self.widgets["results_scroll"], e=True, text=self._format_user_results(results, include_export=False))

    def export_selected_assets(self):
        results, rule_data = self.validate_current_selection()

        if not results:
            cmds.warning("No mesh transform selected.")
            cmds.text(self.widgets["summary_text"], e=True, label="No valid mesh transform selected.")
            cmds.scrollField(self.widgets["results_scroll"], e=True, text="")
            return

        folder = cmds.fileDialog2(
            fileMode=3,
            caption="Select Export Folder"
        )

        if not folder:
            cmds.text(self.widgets["summary_text"], e=True, label="Export cancelled.")
            cmds.scrollField(self.widgets["results_scroll"], e=True, text=self._format_user_results(results, include_export=False))
            return

        export_folder = folder[0]

        ok, plugin_error = self.ensure_fbx_plugin_loaded()
        if not ok:
            cmds.warning("FBX plugin could not be loaded.")
            cmds.text(self.widgets["summary_text"], e=True, label="FBX plugin could not be loaded.")
            cmds.scrollField(
                self.widgets["results_scroll"],
                e=True,
                text="Export could not start.\nFBX plugin load failed: {0}".format(plugin_error)
            )
            return

        export_behavior = rule_data["export_behavior"]

        export_summary = {
            "exported_assets": 0,
            "skipped_assets": 0,
            "failed_exports": 0
        }

        for result in results:
            asset_name = result["asset_name"]
            transform = result["asset_path"]
            status_label = self._get_asset_status_label(result)

            if not result["ready_for_export"]:
                if export_behavior["skip_blocked_assets"]:
                    result["export"]["status"] = "skipped"
                    result["export"]["message"] = "Blocked asset skipped"
                    export_summary["skipped_assets"] += 1
                    continue
                else:
                    result["export"]["status"] = "failed"
                    result["export"]["message"] = "Blocked asset not exported"
                    export_summary["failed_exports"] += 1
                    continue

            if result["warnings"] and not export_behavior["export_warning_assets"]:
                result["export"]["status"] = "skipped"
                result["export"]["message"] = "Warning asset skipped by export settings"
                export_summary["skipped_assets"] += 1
                continue

            if not export_behavior["export_ready_assets"]:
                result["export"]["status"] = "skipped"
                result["export"]["message"] = "Export of ready assets disabled"
                export_summary["skipped_assets"] += 1
                continue

            filename = self.safe_filename(asset_name) + ".fbx"
            export_path = os.path.join(export_folder, filename)

            success, error_message = self.export_transform_to_fbx(transform, export_path)
            if success:
                result["export"]["status"] = "exported"
                result["export"]["message"] = export_path
                export_summary["exported_assets"] += 1
            else:
                result["export"]["status"] = "failed"
                result["export"]["message"] = error_message
                export_summary["failed_exports"] += 1

        report_path = None
        if export_behavior["write_json_report"]:
            try:
                report_path = self.write_json_report(export_folder, rule_data, results, export_summary)
            except Exception as exc:
                cmds.warning("JSON report could not be written: {0}".format(exc))

        self.last_results = results

        summary_text = self._format_user_summary(results)
        export_text = self._format_export_summary(export_folder, results, report_path=report_path)
        result_text = export_text + self._format_user_results(results, include_export=True)

        cmds.text(self.widgets["summary_text"], e=True, label=summary_text)
        cmds.scrollField(self.widgets["results_scroll"], e=True, text=result_text)

    def clear_results(self):
        self.last_results = []
        cmds.text(self.widgets["summary_text"], e=True, label="Results cleared.")
        cmds.scrollField(self.widgets["results_scroll"], e=True, text="")


ui = StudioCustomWindow()
ui.show()