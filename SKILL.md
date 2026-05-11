---
name: scenemakerai
description: Generate one 2:1 equirectangular panorama from one required source image, optionally applying user scene instructions only to hallucinated/outpainted regions, then automatically provide a lightweight local Pannellum visualization URL.
---

# SceneMakerAI

## Goal

Turn one source image into one fixed-position 360-style panorama:

```text
source image
-> protected front-view region on a 2:1 canvas
-> mask-aware outpainting into one equirectangular panorama
-> automatic Pannellum preview URL
```

The primary generated artifact is strictly one `2:1` equirectangular panorama image. Do not create cubemap faces.

## Completion Contract

Never stop after the image generation tool returns. The task is incomplete until the generated panorama has been copied into this repo, a local Pannellum viewer has been created, a localhost server is running or reused, and the final response includes the localhost preview URL.

The stable output location is:

```text
/Users/ojassurana/Desktop/SceneMaker/outputs/scenemakerai/<run-id>/panorama.png
```

An image path under `.codex/generated_images/...` is only a temporary image-tool cache location. It is not the final SceneMakerAI artifact.

For every completed run:

1. Copy the accepted generated image to `<run-dir>/panorama.png`.
2. Create the viewer in `<run-dir>/viewer/`.
3. Start or reuse a local static server for `<run-dir>/viewer/`.
4. Return both `<run-dir>/panorama.png` and the localhost Pannellum URL.

A response containing only "Generated Image" or only a `.codex/generated_images/...` path is incomplete.

## Generated Image Tool Handling

When an image generation tool returns a file under `.codex/generated_images/...`, locate that file and copy it into the active run directory as `<run-dir>/panorama.png` before continuing. Use the repo-local copy for validation, Pannellum viewer creation, edit loops, and final reporting.

Do not treat the image-generation cache path as durable output. If the image tool only reports a `file://` URL, convert it to the local filesystem path before copying.

## Inputs

- Required: one source image.
- Optional: user scene instructions, such as "make the background more crowded with people."

Apply optional scene instructions only to generated/outpainted regions. Treat the original source image area as immutable.

## Workflow

1. Inspect the source image.
   - Identify whether it is landscape, portrait, fisheye/wide-angle, indoor, outdoor, or object-centric.
   - Identify anchors to preserve: architecture, people, foreground objects, lighting, ground plane, sky/ceiling, camera height, perspective, and left/right boundary cues.
   - If the image contains real people, preserve visible identity and placement only in the original protected area. Do not invent close-up new views of them unless the user explicitly asks and the request is appropriate.

2. Prepare a 2:1 panorama canvas and mask for local image files.
   - Create one run directory, preferably `outputs/scenemakerai/<timestamp-or-short-id>/`.
   - Use `<run-dir>/prep/` for temporary canvas and mask files.
   - Run `scripts/prepare_pano_canvas.py <image> --out-dir <run-dir>/prep --width 2048 --height 1024` unless the user specifies another 2:1 size.
   - Use the generated `canvas.png`, `mask.png`, `mask-alpha.png`, `preview.png`, and `metadata.json`.
   - The default mask convention is `black=protected white=generate`.
   - Use `mask-alpha.png` only when the active image tool expects transparent pixels to be generated and opaque pixels to be preserved.

3. Generate one equirectangular panorama.
   - Prefer an image editing/outpainting tool that accepts both an image and a mask.
   - Ask for one single `2:1` equirectangular panorama, not a collage and not six separate images.
   - Preserve the source image area as the front-view region.
   - Apply optional user scene instructions only to masked/generated regions.
   - Extend missing left, right, back, up, and down views plausibly from the same fixed camera position.
   - Request seamless left/right wraparound.
   - Save or copy the accepted generated panorama to `<run-dir>/panorama.png`.
   - Read `references/prompting.md` for compact prompt templates.

4. Handle tool limitations honestly.
   - If the available image tool supports mask editing, use the mask and require exact preservation of the source region.
   - If only a reference-style image generation tool is available, state that exact original-pixel preservation is not guaranteed.
   - Do not claim factual reconstruction of unseen areas. The missing scene content is generated.

5. Verify the panorama.
   - Confirm the output is one image with width:height approximately `2:1`.
   - Confirm the front-view scene remains recognizable.
   - Confirm optional instructions are reflected only in the generated surroundings.
   - Check whether the left and right edges can wrap without an obvious hard seam.
   - Regenerate or correct any non-2:1 output before finalizing.
   - After the final initial panorama is accepted and stored at `<run-dir>/panorama.png`, delete `<run-dir>/prep/` unless the user asks to keep intermediate files for debugging.

6. Automatically create a local Pannellum preview.
   - Run `scripts/create_pannellum_viewer.py <run-dir>/panorama.png --out-dir <run-dir>/viewer`.
   - Start a local static server from that viewer directory, for example `python -m http.server 8000`.
   - If the port is busy, use another available port.
   - Return the final panorama path and the localhost Pannellum viewer URL.

## Edit Loop

When the user asks for changes after seeing a preview:

1. Use the latest final equirectangular panorama as the edit source.
2. Use an image editing tool, not a fresh source-image-to-panorama generation, unless the requested change requires starting over.
3. Preserve the `2:1` equirectangular format, camera position, horizon continuity, and seamless left/right wrapping.
4. Apply the user's requested change while preserving unrelated scene content.
5. Save the edited result as a new final panorama image in the same run directory, such as `<run-dir>/panorama-edit-01.png`.
6. Re-run `scripts/create_pannellum_viewer.py <edited-panorama-path> --out-dir <run-dir>/viewer`, replacing the previous viewer image.
7. Return the edited panorama path and the refreshed localhost Pannellum URL.

If the edit request would break the fixed-position panorama assumption or requires factual unseen details, state the limitation and make only a plausible visual edit.

## Output Rules

- Always return the final repo-local `2:1` equirectangular panorama image path under `outputs/scenemakerai/<run-id>/panorama.png`.
- Always return the local Pannellum preview URL.
- Keep only the accepted final panorama image, the active `viewer/` folder needed for the preview URL, and any user-requested saved variants.
- Delete temporary prep artifacts after the initial panorama is accepted: `canvas.png`, `mask.png`, `mask-alpha.png`, `preview.png`, and `metadata.json`.
- Do not output cubemap faces.
- Do not imply the result is a walkable 3D reconstruction. It is a fixed-point panorama.
