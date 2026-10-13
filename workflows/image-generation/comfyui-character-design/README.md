# Character Design with ComfyUI

> Generate character concept art with Stable Diffusion XL, using a
> curated ComfyUI workflow. Designed for pre-production iteration:
> rough out a concept before committing time in Blender, ZBrush, or
> equivalent.

## What it does

This workflow generates character concept art using Stable Diffusion XL
via a local ComfyUI server. The user provides a text prompt describing
the desired character; the workflow submits the prompt to ComfyUI's HTTP
API, waits for generation to complete, and saves the resulting image to
ComfyUI's output directory.

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
```text
python main.py --listen 127.0.0.1 --port 8188
```

2. From the Soda-Streams root:
```text
python -m tools.sandbox.cli run comfyui-character-design
```

3. To specify a prompt:
```text
python workflows/image-generation/comfyui-character-design/workflow.py \
  --prompt "a wood elf ranger, leather armour, forest background"
```

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