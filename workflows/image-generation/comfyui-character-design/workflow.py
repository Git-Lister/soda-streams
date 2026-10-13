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
    return json.loads(path.read_text(encoding="utf-8"))


def set_prompt(workflow: dict, prompt: str, node_id: str = POSITIVE_PROMPT_NODE) -> dict:
    """Return a copy of `workflow` with the text input of `node_id` set
    to `prompt`. Does not mutate the input.
    """
    import copy

    result = copy.deepcopy(workflow)
    if node_id in result and "inputs" in result[node_id]:
        result[node_id]["inputs"]["text"] = prompt
    return result


def submit(workflow: dict, server: str = DEFAULT_SERVER) -> str:
    """POST the workflow to the ComfyUI server. Return the prompt_id.
    Raises `ConnectionError` if the server is unreachable.
    """
    payload = {"prompt": workflow, "client_id": str(uuid.uuid4())}
    response = requests.post(f"{server}/prompt", json=payload, timeout=10)
    response.raise_for_status()
    return response.json()["prompt_id"]


def wait_for_result(prompt_id: str, server: str = DEFAULT_SERVER) -> dict:
    """Poll the server's /history endpoint until the prompt completes.
    Returns the history entry. Raises `TimeoutError` after
    TIMEOUT_SECONDS, or `RuntimeError` if the prompt status is not
    successful.
    """
    start = time.time()
    while True:
        if time.time() - start > TIMEOUT_SECONDS:
            raise TimeoutError(f"Timed out after {TIMEOUT_SECONDS}s")

        response = requests.get(f"{server}/history/{prompt_id}", timeout=10)
        response.raise_for_status()
        history = response.json()

        if prompt_id in history:
            entry = history[prompt_id]
            status = entry.get("status", {})
            if status.get("status_str") == "success":
                return entry
            if status.get("status_str") == "error":
                raise RuntimeError(f"ComfyUI error: {status.get('messages', 'Unknown error')}")

        time.sleep(POLL_INTERVAL)


def report_output(history_entry: dict) -> list[str]:
    """Return a list of output filenames from a history entry."""
    outputs = history_entry.get("outputs", {})
    filenames = []
    for node_output in outputs.values():
        images = node_output.get("images", [])
        for img in images:
            filename = img.get("filename")
            if filename:
                filenames.append(filename)
    return filenames


def main(argv: list[str] | None = None) -> int:
    """Entry point. Returns 0 on success, 1 on connection failure,
    2 on server-side failure, 3 on timeout.
    """
    parser = argparse.ArgumentParser(description="Character design workflow — ComfyUI + SDXL client")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="Positive prompt")
    parser.add_argument("--negative", default=DEFAULT_NEGATIVE, help="Negative prompt")
    parser.add_argument("--server", default=DEFAULT_SERVER, help="ComfyUI server URL")
    parser.add_argument("--seed", type=int, help="Random seed (overrides workflow.json)")
    args = parser.parse_args(argv)

    try:
        workflow = load_workflow()
    except FileNotFoundError:
        print(f"Workflow JSON not found at {WORKFLOW_JSON}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"Invalid workflow JSON: {exc}", file=sys.stderr)
        return 2

    workflow = set_prompt(workflow, args.prompt, POSITIVE_PROMPT_NODE)
    workflow = set_prompt(workflow, args.negative, NEGATIVE_PROMPT_NODE)

    if args.seed is not None and "3" in workflow and "inputs" in workflow["3"]:
        workflow["3"]["inputs"]["seed"] = args.seed

    try:
        prompt_id = submit(workflow, args.server)
    except requests.ConnectionError:
        print(f"ComfyUI server not reachable at {args.server}", file=sys.stderr)
        return 1
    except requests.RequestException as exc:
        print(f"Failed to submit to ComfyUI: {exc}", file=sys.stderr)
        return 1

    try:
        history_entry = wait_for_result(prompt_id, args.server)
    except TimeoutError as exc:
        print(str(exc), file=sys.stderr)
        return 3
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    filenames = report_output(history_entry)
    for filename in filenames:
        print(f"Output: {filename}")

    return 0


if __name__ == "__main__":
    sys.exit(main())