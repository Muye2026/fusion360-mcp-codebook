import unittest
import sys
import types


adsk = types.ModuleType("adsk")
adsk.core = types.ModuleType("adsk.core")
adsk.fusion = types.ModuleType("adsk.fusion")
adsk.core.CustomEventHandler = type("CustomEventHandler", (), {"__init__": lambda self: None})
adsk.core.LogLevels = type("LogLevels", (), {"ErrorLogLevel": 1})
sys.modules.setdefault("adsk", adsk)
sys.modules.setdefault("adsk.core", adsk.core)
sys.modules.setdefault("adsk.fusion", adsk.fusion)

from addin.Brepwright.fusion_bridge import operations, tool_surface


class ToolRegistryTests(unittest.TestCase):
    def test_no_duplicate_tool_names(self):
        names = [tool["name"] for tool in tool_surface.TOOL_DEFINITIONS]
        self.assertEqual(len(names), len(set(names)))

    def test_every_tool_has_handler(self):
        definition_names = {tool["name"] for tool in tool_surface.TOOL_DEFINITIONS}
        handler_names = set(operations.TOOL_HANDLERS)
        self.assertEqual(definition_names, handler_names)

    def test_required_mainline_tools_exist(self):
        required = {
            "ping",
            "get_runtime_status",
            "get_active_design_info",
            "create_cube",
            "execute_python",
            "capture_viewport",
            "mass_properties",
            "create_mounting_plate",
            "create_enclosure_shell",
            "create_bracket",
            "inspect_design",
            "export_design_pack",
            "validate_part_for_printing",
        }
        names = {tool["name"] for tool in tool_surface.TOOL_DEFINITIONS}
        self.assertTrue(required.issubset(names))

    def test_tool_schemas_are_objects(self):
        for tool in tool_surface.TOOL_DEFINITIONS:
            with self.subTest(tool=tool["name"]):
                schema = tool.get("inputSchema")
                self.assertIsInstance(schema, dict)
                self.assertEqual(schema.get("type"), "object")
                self.assertIn("properties", schema)


if __name__ == "__main__":
    unittest.main()
