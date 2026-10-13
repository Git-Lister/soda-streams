# Character Design with ComfyUI — Discipline Guide

> How to adapt this workflow for specific disciplines, and where its
> limits are.

## What this workflow assumes

This workflow assumes the user has a rough idea — a character, a mood,
a genre. It assumes the output is a starting point, not a finished
artefact. It assumes iteration is the point. The workflow is a
seeded system; outputs are variable. Its value is in the iteration it
enables, not the images it produces.

## Games design

Use this workflow for character concepting: iterate silhouettes, test
colour palettes, generate multiple variants, compare to reference
boards. Prompt engineering is not the skill here — visual judgement
is. The workflow produces rough concepts that can be refined in Blender,
ZBrush, or 2D tooling. ControlNet for pose control is a natural
extension, documented at the ComfyUI project. For production assets,
consider training a LoRA on the character design to maintain
consistency across multiple generations.

## Filmmaking

Use for character mood boards, casting reference, costume exploration.
Note that SDXL's training data produces a particular visual idiom —
Western-centric, photorealistic bias. For period pieces or non-Western
settings, deliberate prompting and post-processing are required. The
workflow can generate quick turnaround references for costume
departments or concept artists, but should not be treated as final
production artwork.

## Fine art

Use as a generative sketching tool. The relationship between
"prompting" and "drawing" as creative acts is the central question.
Outputs are variable; treat them as studies, not finished pieces. When
exhibiting AI-generated work, attribution issues arise — document the
model, prompt, and workflow used. The workflow is a seeded system; its
value is in the iteration it enables, not the images it produces.

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
- **ComfyUI server restart required.** The workflow does not handle
  ComfyUI server restarts mid-run. If the server is restarted, the
  prompt_id becomes invalid and the workflow must be resubmitted.

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