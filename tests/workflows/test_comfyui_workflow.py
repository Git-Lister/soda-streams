"""Smoke tests for the ComfyUI character design workflow.

These tests do NOT require ComfyUI, a GPU, or network access. They
verify the workflow's structure, metadata validity, and the graceful
handling of the "server not running" case.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from tools.validators.validate import validate_file

WORKFLOW_DIR = (
    Path(__file__).resolve().parents[2]
    / "workflows"
    / "image-generation"
    / "comfyui-character-design"
)


class TestWorkflowJSON:
    """The ComfyUI workflow definition is well-formed."""

    def test_loads_as_json(self) -> None:
        """json.loads on workflow.json returns a dict."""
        path = WORKFLOW_DIR / "workflow.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        assert isinstance(data, dict)
        assert len(data) > 0

    def test_has_required_node_types(self) -> None:
        """The values include at least KSampler, CheckpointLoaderSimple,
        CLIPTextEncode, VAEDecode, SaveImage.
        """
        path = WORKFLOW_DIR / "workflow.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        class_types = {node["class_type"] for node in data.values() if "class_type" in node}
        required = {"KSampler", "CheckpointLoaderSimple", "CLIPTextEncode", "VAEDecode", "SaveImage"}
        assert required.issubset(class_types)

    def test_prompt_nodes_are_strings(self) -> None:
        """Nodes 6 and 7 have inputs.text as strings."""
        path = WORKFLOW_DIR / "workflow.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        for node_id in ("6", "7"):
            assert node_id in data
            text = data[node_id]["inputs"]["text"]
            assert isinstance(text, str)
            assert len(text) > 0

    def test_ksampler_has_seed(self) -> None:
        """Node 3 has inputs.seed."""
        path = WORKFLOW_DIR / "workflow.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        assert "3" in data
        assert "seed" in data["3"]["inputs"]


class TestMetadata:
    """The workflow's metadata validates against the schema."""

    def test_metadata_validates(self) -> None:
        """Uses tools.validators.validate.validate_file to validate the
        workflow's metadata.yaml. Result status must be "valid".
        """
        path = WORKFLOW_DIR / "metadata.yaml"
        result = validate_file(path)
        assert result.status == "valid"

    def test_tier_is_curated(self) -> None:
        """Metadata tier == "curated"."""
        import yaml
        path = WORKFLOW_DIR / "metadata.yaml"
        metadata = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert metadata["tier"] == "curated"

    def test_declares_sdxl_model(self) -> None:
        """Metadata provenance.models[0].name contains "SDXL"."""
        import yaml
        path = WORKFLOW_DIR / "metadata.yaml"
        metadata = yaml.safe_load(path.read_text(encoding="utf-8"))
        models = metadata.get("provenance", {}).get("models", [])
        assert len(models) > 0
        assert "SDXL" in models[0]["name"]


class TestWorkflowModule:
    """The Python entry point imports and behaves correctly."""

    def test_module_imports(self) -> None:
        """Imports the workflow module by path (importlib.util.spec_from_file_location)."""
        workflow_py = WORKFLOW_DIR / "workflow.py"
        spec = importlib.util.spec_from_file_location("workflow", workflow_py)
        assert spec is not None
        assert spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        assert hasattr(module, "main")
        assert hasattr(module, "load_workflow")
        assert hasattr(module, "set_prompt")
        assert hasattr(module, "submit")
        assert hasattr(module, "wait_for_result")
        assert hasattr(module, "report_output")

    def test_default_prompt_is_set(self) -> None:
        """The module has a DEFAULT_PROMPT constant of type str."""
        workflow_py = WORKFLOW_DIR / "workflow.py"
        spec = importlib.util.spec_from_file_location("workflow", workflow_py)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        assert hasattr(module, "DEFAULT_PROMPT")
        assert isinstance(module.DEFAULT_PROMPT, str)
        assert len(module.DEFAULT_PROMPT) > 0

    def test_set_prompt_returns_copy(self) -> None:
        """set_prompt(wf, "x") returns a different dict object."""
        workflow_py = WORKFLOW_DIR / "workflow.py"
        spec = importlib.util.spec_from_file_location("workflow", workflow_py)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        workflow = module.load_workflow()
        result = module.set_prompt(workflow, "test prompt")
        assert result is not workflow
        assert result is not workflow["6"]  # deep copy check

    def test_set_prompt_does_not_mutate_input(self) -> None:
        """After set_prompt, the original dict's node 6 text is unchanged."""
        workflow_py = WORKFLOW_DIR / "workflow.py"
        spec = importlib.util.spec_from_file_location("workflow", workflow_py)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        workflow = module.load_workflow()
        original_text = workflow["6"]["inputs"]["text"]
        module.set_prompt(workflow, "new prompt")
        assert workflow["6"]["inputs"]["text"] == original_text

    def test_set_prompt_updates_correct_node(self) -> None:
        """The returned dict's node 6 inputs.text equals the given prompt."""
        workflow_py = WORKFLOW_DIR / "workflow.py"
        spec = importlib.util.spec_from_file_location("workflow", workflow_py)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        workflow = module.load_workflow()
        result = module.set_prompt(workflow, "custom prompt")
        assert result["6"]["inputs"]["text"] == "custom prompt"

    def test_main_reports_connection_error(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Call main(["--server", "http://127.0.0.1:1"]) with a port that
        refuses connections. Assert return code is 1 and stderr contains
        "not reachable". This may take up to 5 seconds due to connection
        timeout.
        """
        workflow_py = WORKFLOW_DIR / "workflow.py"
        spec = importlib.util.spec_from_file_location("workflow", workflow_py)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        exit_code = module.main(["--server", "http://127.0.0.1:1"])
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "not reachable" in captured.err.lower()