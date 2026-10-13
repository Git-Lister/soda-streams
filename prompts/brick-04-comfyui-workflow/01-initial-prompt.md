Brick 4 — ComfyUI Character Design Workflow
You are implementing Brick 4 of the Soda-Streams project.

Context
Read before starting:

docs/BLUEPRINT.md — §3 metadata schema, §6 runtime convention

docs/DEVELOPMENT.md — §9 coding standards

docs/DESIGN.md — §3 user stories (this workflow serves stories 1 and 2)

tools/sandbox/cli.py — the launcher (this workflow must work with it)

tools/validators/schema.json — the metadata schema this workflow must satisfy

Brick 1b left placeholders in
workflows/image-generation/comfyui-character-design/. Brick 4 replaces
those placeholders with a real, runnable ComfyUI workflow.

This is the first content brick. Everything before this was
infrastructure. This is where the repository starts becoming useful.

The workflow
Character Design with ComfyUI — generate character concept art
using a Stable Diffusion XL pipeline. The workflow is a thin Python
client that talks to a local ComfyUI server via its HTTP API. It takes
a text prompt, submits the workflow, waits for completion, and saves
the resulting image.

Deliverables
Modify exactly 5 files. Create exactly 4 new files. Do not create or
modify any other files.

Modified files (replace placeholders)
1. workflows/image-generation/comfyui-character-design/README.md

Structure:

markdown
# Character Design with ComfyUI

> Generate character concept art with Stable Diffusion XL, using a
> curated ComfyUI workflow. Designed for pre-production iteration:
> rough out a concept before committing time in Blender, ZBrush, or
> equivalent.

## What it does

[3–4 sentences. Explain: what a user provides (a text prompt), what the
workflow produces (an image), how (SDXL via ComfyUI), and where the
output goes (an output directory).]

## Who it's for

- Games designers sketching character concepts before modelling
- Filmmakers exploring visual language for a script
- Fine artists iterating on a composition
- Anyone who wants to try AI image generation without leaving the
  institution's hardware

## What you need

- **ComfyUI** installed and running locally — see [ComfyUI docs](https://github.com/comfyanonymous/ComfyUI)
- **SDXL Base 1.0** checkpoint (`sd_xl_base_1.0.safetensors`) in
  ComfyUI's `models/checkpoints/`
- **Python 3.11+** with the dependencies in `requirements.txt`
- **A GPU** with at least 8 GB VRAM (SDXL can run on CPU but is slow)

## How to run it

1. Start ComfyUI (default port 8188):
python main.py --listen 127.0.0.1 --port 8188

text

2. From the Soda-Streams root:
python -m tools.sandbox.cli run comfyui-character-design

text

3. To specify a prompt:
python workflows/image-generation/comfyui-character-design/workflow.py
--prompt "a wood elf ranger, leather armour, forest background"

text

4. The output image is written to ComfyUI's output directory. The
workflow prints the filename when done.

## What it doesn't do

- It doesn't train or fine-tune models. It uses SDXL Base as-is.
- It doesn't do inpainting, ControlNet, or LoRA. Those are extensions
documented in `guide.md`.
- It doesn't replace a designer. It produces rough concepts to iterate
from.

## Provenance

- **Model:** SDXL Base 1.0 — Stability AI — CreativeML Open RAIL++-M
- **Workflow JSON:** hand-authored, based on the canonical SDXL text-to-image graph
- **Hardware:** runs locally; prompts and images never leave the machine

See `metadata.yaml` for the full provenance record.

## Related files

- `metadata.yaml` — machine-readable metadata
- `guide.md` — discipline-specific adaptation
- `workflow.py` — the Python entry point
- `workflow.json` — the ComfyUI workflow definition
- `requirements.txt` — Python dependencies
2. workflows/image-generation/comfyui-character-design/metadata.yaml

yaml
name: "Character Design with ComfyUI"
slug: "comfyui-character-design"
author: "Git-Lister"
tier: "curated"
discipline:
  - "games"
  - "filmmaking"
  - "fine-art"
description: "Generate character concept art with Stable Diffusion XL via ComfyUI. Iterate on designs before committing time in 3D or 2D tooling."
version: "1.0.0"
licence: "MIT"
tools:
  - name: "ComfyUI"
    version: ">=0.2.0"
    source: "https://github.com/comfyanonymous/ComfyUI"
    licence: "GPL-3.0"
  - name: "Stable Diffusion XL Base"
    version: "1.0"
    source: "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0"
    licence: "CreativeML-Open-RAIL++-M"
dependencies:
  - "requests>=2.31.0"
  - "websocket-client>=1.7.0"
entry_point: "workflow.py:main"
runtime: "python"
provenance:
  models:
    - name: "SDXL Base 1.0"
      source: "Stability AI"
      licence: "CreativeML-Open-RAIL++-M"
      training_data: "LAION-5B (per Stability AI model card)"
  ai_assistance:
    - tool: "OpenCode (Nemotron 3 Ultra)"
      role: "code generation"
created: "2026-10-13"
updated: "2026-10-13"
contributor_handle: "Git-Lister"
3. workflows/image-generation/comfyui-character-design/guide.md

Structure:

markdown
# Character Design with ComfyUI — Discipline Guide

> How to adapt this workflow for specific disciplines, and where its
> limits are.

## What this workflow assumes

[A paragraph. It assumes the user has a rough idea — a character, a
mood, a genre. It assumes the output is a starting point, not a
finished artefact. It assumes iteration is the point.]

## Games design

[2–3 paragraphs. How to use this workflow for character concepting:
iterate silhouettes, test colour palettes, generate multiple variants,
compare to reference boards. Point out that prompt engineering is not
the skill here — visual judgement is. Mention that ControlNet for pose
control is a natural extension, documented at the ComfyUI project.]

## Filmmaking

[2–3 paragraphs. Use for character mood boards, casting reference,
costume exploration. Note that SDXL's training data produces a
particular visual idiom — discuss what that means for period pieces
or non-Western settings.]

## Fine art

[2–3 paragraphs. Use as a generative sketching tool. The workflow is a
seeded system; outputs are variable. Discuss the relationship between
"prompting" and "drawing" as creative acts. Note attribution issues
when exhibiting AI-generated work.]

## Known limitations

- **Western-centric training data.** SDXL produces a specific visual
  idiom. Non-Western characters, non-standard body types, and
  non-photorealistic styles require deliberate prompting and often
  still fall short.
- **Text rendering.** SDXL does not reliably render text.
- **Hands and anatomy.** Common failure mode. Iteration or inpainting
  is usually required.
- **Consistency across images.** Not designed for character turnaround.
  Use LoRA training or IPAdapter for consistency.
- **Compute cost.** SDXL on CPU is minutes per image. On an 8 GB GPU
  it's ~15–30 seconds.

## Extending this workflow

- **ControlNet.** Pose, depth, or edge conditioning for reproducibility.
  See the ComfyUI ControlNet examples.
- **LoRA.** Fine-tuned character consistency. Train on the institution's
  hardware or use an existing LoRA.
- **Inpainting.** Fix hands, faces, or small details after generation.
- **Batch generation.** Modify the workflow JSON to increase
  `batch_size` on the `EmptyLatentImage` node.

## Provocation

If the output is "good enough", it probably isn't yet. The workflow is
a sketchbook, not a solution. Its value is in the iteration it enables,
not the images it produces.
4. workflows/image-generation/comfyui-character-design/workflow.py

Structure and behaviour:

python
"""Character design workflow — ComfyUI + SDXL client."""

from __future__ import annotations

import argparse
import json
import sys
import time
import uuid
from pathlib import Path

import requests

WORKFLOW_JSON = Path(__file__).parent / "workflow.json"
"""The ComfyUI workflow definition shipped with this workflow."""

DEFAULT_PROMPT = (
    "character concept art, front view, neutral pose, concept sheet, "
    "detailed, professional, chiaroscuro lighting"
)

DEFAULT_NEGATIVE = (
    "blurry, low quality, watermark, text, signature, deformed, "
    "extra limbs, bad anatomy"
)

DEFAULT_SERVER = "http://127.0.0.1:8188"

POSITIVE_PROMPT_NODE = "6"
"""Node ID of the positive CLIPTextEncode node in workflow.json."""

NEGATIVE_PROMPT_NODE = "7"
"""Node ID of the negative CLIPTextEncode node in workflow.json."""

POLL_INTERVAL = 1.0
TIMEOUT_SECONDS = 300


def load_workflow(path: Path = WORKFLOW_JSON) -> dict:
    """Load and return the ComfyUI workflow JSON."""


def set_prompt(workflow: dict, prompt: str, node_id: str = POSITIVE_PROMPT_NODE) -> dict:
    """Return a copy of `workflow` with the text input of `node_id` set
    to `prompt`. Does not mutate the input."""


def submit(workflow: dict, server: str = DEFAULT_SERVER) -> str:
    """POST the workflow to the ComfyUI server. Return the prompt_id.
    Raises `ConnectionError` if the server is unreachable."""


def wait_for_result(prompt_id: str, server: str = DEFAULT_SERVER) -> dict:
    """Poll the server's /history endpoint until the prompt completes.
    Returns the history entry. Raises `TimeoutError` after
    TIMEOUT_SECONDS, or `RuntimeError` if the prompt status is not
    successful."""


def report_output(history_entry: dict) -> list[str]:
    """Return a list of output filenames from a history entry."""


def main(argv: list[str] | None = None) -> int:
    """Entry point. Returns 0 on success, 1 on connection failure,
    2 on server-side failure, 3 on timeout."""
Behaviour detail:

main parses --prompt, --negative, --server, --seed.

Loads workflow.json, applies the prompt and negative via
set_prompt, optionally overrides the seed on the KSampler node
(node_id="3", inputs.seed).

Calls submit. On ConnectionError: prints
ComfyUI server not reachable at <server> to stderr and returns 1.

Calls wait_for_result. On TimeoutError: prints
Timed out waiting for ComfyUI after <seconds>s to stderr and
returns 3. On RuntimeError: prints the error to stderr and returns 2.

On success, calls report_output, prints
Output: <filename> for each, returns 0.

Uses only stdlib plus requests.

Rules:

Do not import or require any GPU library. This code must import and
run its argument parser on a machine with no GPU.

Do not reach the network during import. Only submit and
wait_for_result make HTTP calls.

No globals beyond module-level constants.

Type hints on all public functions. Google-style docstrings.

Ruff-compatible (line length 140).

5. workflows/image-generation/comfyui-character-design/workflow.json

Replace examples/ placeholder only if empty. Ship this exact workflow:

json
{
  "3": {
    "class_type": "KSampler",
    "inputs": {
      "seed": 42,
      "steps": 25,
      "cfg": 7.0,
      "sampler_name": "euler",
      "scheduler": "normal",
      "denoise": 1.0,
      "model": ["4", 0],
      "positive": ["6", 0],
      "negative": ["7", 0],
      "latent_image": ["5", 0]
    }
  },
  "4": {
    "class_type": "CheckpointLoaderSimple",
    "inputs": {
      "ckpt_name": "sd_xl_base_1.0.safetensors"
    }
  },
  "5": {
    "class_type": "EmptyLatentImage",
    "inputs": {
      "width": 1024,
      "height": 1024,
      "batch_size": 1
    }
  },
  "6": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "character concept art, front view, neutral pose, concept sheet",
      "clip": ["4", 1]
    }
  },
  "7": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "blurry, low quality, watermark, text, signature, deformed",
      "clip": ["4", 1]
    }
  },
  "8": {
    "class_type": "VAEDecode",
    "inputs": {
      "samples": ["3", 0],
      "vae": ["4", 2]
    }
  },
  "9": {
    "class_type": "SaveImage",
    "inputs": {
      "filename_prefix": "character_design",
      "images": ["8", 0]
    }
  }
}
Created files
6. workflows/image-generation/comfyui-character-design/requirements.txt

text
requests>=2.31.0
websocket-client>=1.7.0
7. workflows/image-generation/comfyui-character-design/examples/README.md

markdown
# Examples

Sample outputs from this workflow live here once generated.

To produce an example:

1. Start ComfyUI with the SDXL Base 1.0 checkpoint loaded.
2. Run the workflow with a representative prompt.
3. Copy the output image here.
4. Add a short caption with the prompt used and the date.

Example outputs are illustrative, not prescriptive. They show what
the workflow produces, not what it should produce.
8. tests/workflows/test_comfyui_workflow.py

python
"""Smoke tests for the ComfyUI character design workflow.

These tests do NOT require ComfyUI, a GPU, or network access. They
verify the workflow's structure, metadata validity, and the graceful
handling of the "server not running" case.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

WORKFLOW_DIR = (
    Path(__file__).resolve().parents[2]
    / "workflows"
    / "image-generation"
    / "comfyui-character-design"
)


class TestWorkflowJSON:
    """The ComfyUI workflow definition is well-formed."""

    def test_loads_as_json(self) -> None: ...
    def test_has_required_node_types(self) -> None: ...
    def test_prompt_nodes_are_strings(self) -> None: ...
    def test_ksampler_has_seed(self) -> None: ...


class TestMetadata:
    """The workflow's metadata validates against the schema."""

    def test_metadata_validates(self) -> None: ...
    def test_tier_is_curated(self) -> None: ...
    def test_declares_sdxl_model(self) -> None: ...


class TestWorkflowModule:
    """The Python entry point imports and behaves correctly."""

    def test_module_imports(self) -> None: ...
    def test_default_prompt_is_set(self) -> None: ...
    def test_set_prompt_returns_copy(self) -> None: ...
    def test_set_prompt_does_not_mutate_input(self) -> None: ...
    def test_set_prompt_updates_correct_node(self) -> None: ...
    def test_main_reports_connection_error(self, capsys: pytest.CaptureFixture[str]) -> None: ...
Test detail:

test_loads_as_json — json.loads on workflow.json returns a dict.

test_has_required_node_types — the values include at least
KSampler, CheckpointLoaderSimple, CLIPTextEncode, VAEDecode,
SaveImage.

test_prompt_nodes_are_strings — nodes 6 and 7 have
inputs.text as strings.

test_ksampler_has_seed — node 3 has inputs.seed.

test_metadata_validates — uses tools.validators.validate.validate_file
to validate the workflow's metadata.yaml. Result status must be
"valid".

test_tier_is_curated — metadata tier == "curated".

test_declares_sdxl_model — metadata provenance.models[0].name
contains "SDXL".

test_module_imports — imports the workflow module by path
(importlib.util.spec_from_file_location).

test_default_prompt_is_set — the module has a DEFAULT_PROMPT
constant of type str.

test_set_prompt_returns_copy — set_prompt(wf, "x") returns a
different dict object.

test_set_prompt_does_not_mutate_input — after set_prompt, the
original dict's node 6 text is unchanged.

test_set_prompt_updates_correct_node — the returned dict's node 6
inputs.text equals the given prompt.

test_main_reports_connection_error — call main(["--server", "http://127.0.0.1:1"]) with a port that refuses connections.
Assert return code is 1 and stderr contains "not reachable". This
may take up to 5 seconds due to connection timeout.

Modified files (continued)
9. DEVLOG.md

Prepend:

markdown
## YYYY-MM-DD — Brick 4: ComfyUI character design workflow

**Built:** First content workflow. ComfyUI + SDXL character design with
a real workflow.json, a Python HTTP client, discipline guide, and smoke
tests. Metadata validates as curated tier with full provenance.

**Learned:** To be filled in.

**Changed:** To be filled in.

**Next:** Brick 5 (RAG research assistant workflow).
10. ROADMAP.md

markdown
## Built
- [x] Provenance infrastructure
- [x] Repository skeleton
- [x] Full repository scaffold
- [x] Metadata schema
- [x] Launcher CLI
- [x] ComfyUI workflow

## Next
- [ ] RAG workflow
...
Rules
Do not run ComfyUI. Tests must not require it. The
test_main_reports_connection_error test deliberately targets an
unreachable port.

Do not make network requests during import, test collection, or
any test other than test_main_reports_connection_error.

Do not modify any file outside the 10 listed.

Do not invent URLs. ComfyUI's GitHub URL and Hugging Face SDXL
URL are given above. The repository URL is
https://github.com/Git-Lister/soda-streams.

Follow docs/DEVELOPMENT.md §9.

Print only what is specified in main's behaviour.

Verification
The virtual environment is at .venv/ and its Python is 3.11. Run
every command using the venv's Python explicitly.

Copy the full terminal transcript into your response inside a fenced
code block titled VERIFICATION. Include each command with a $
prefix on its own line, and its complete output below.

Do not summarize. Do not paraphrase. If you cannot run shell
commands in this session, say so explicitly and skip this section —
do not fabricate output.

text
$ git status
$ .venv\Scripts\python.exe -m ruff check .
$ .venv\Scripts\python.exe -m pytest tests/ -v
$ .venv\Scripts\python.exe -m tools.sandbox.cli list
$ .venv\Scripts\python.exe -m tools.sandbox.cli info comfyui-character-design
$ .venv\Scripts\python.exe -m tools.validators.validate_all
Expected:

git status — 5 modified, 4 new, nothing else.

ruff check . — All checks passed!

pytest — 69 remain from before; 13 new from
test_comfyui_workflow.py; no failures, no errors. One skip
(assistant placeholder).

sandbox list — now shows one workflow:
comfyui-character-design [curated] games, filmmaking, fine-art

sandbox info comfyui-character-design — prints Name, Slug, Tier,
Discipline, Description, Version, Licence lines. Exit 0.

validate_all — 1 valid (this workflow), 3 skipped (the remaining
placeholders), 0 invalid.

Output
Report:

Every file created (full path)

Every file modified (full path)

The VERIFICATION code block (or the explicit note that shell
commands could not be run)

Any deviations from the spec, with justification

Also Fill In
Actual Output section of
prompts/brick-04-comfyui-workflow/01-initial-prompt.md — one
paragraph summary.

Learned and Changed fields in the DEVLOG entry above.

Commit Message
text
feat(workflows): add ComfyUI character design workflow

- workflows/image-generation/comfyui-character-design/
  - README, guide, workflow.json, workflow.py, requirements.txt
  - Full metadata.yaml (curated tier, SDXL provenance)
  - examples/README.md
- tests/workflows/test_comfyui_workflow.py — 13 smoke tests
- DEVLOG and ROADMAP updated

Generated with OpenCode (Nemotron 3 Ultra)
Prompt: prompts/brick-04-comfyui-workflow/01-initial-prompt.md

## Actual Output

Replaced 5 placeholder files in workflows/image-generation/comfyui-character-design/ with real implementations: README.md (full documentation with what/who/needs/run/provenance), metadata.yaml (curated tier, SDXL provenance), guide.md (discipline guide with games/filmmaking/fine-art sections, limitations, extensions), workflow.py (ComfyUI HTTP client with submit/poll/report logic, --prompt/--negative/--server/--seed args, proper exit codes), workflow.json (canonical SDXL text-to-image graph with KSampler, CheckpointLoaderSimple, CLIPTextEncode x2, VAEDecode, SaveImage). Created 4 new files: requirements.txt (requests, websocket-client), examples/README.md (instructions for adding sample outputs), tests/workflows/test_comfyui_workflow.py (13 smoke tests covering JSON structure, metadata validation, module imports, set_prompt behavior, connection error handling). Updated DEVLOG.md and ROADMAP.md. All verification commands pass.

══════════════════════════════════════════════════════════════════════
END BRICK 4 SPEC