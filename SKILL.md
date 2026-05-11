---
name: scenemakerai
description: Generate one 2:1 equirectangular panorama from one required source image, optionally applying user scene instructions across the panorama, then automatically provide a lightweight local Pannellum visualization URL.
---

# SceneMakerAI

## Goal

Turn one source image into one fixed-position 360-style panorama:

```text
source image
-> front-view reference region on a 2:1 canvas
-> mask-aware outpainting into one equirectangular panorama
-> automatic Pannellum preview URL
```

The primary generated artifact is strictly one `2:1` equirectangular panorama image. Do not create cubemap faces.

## Completion Contract

Never stop after the image generation tool returns. The task is incomplete until the generated panorama has been copied into the agent's current working directory, a local Pannellum viewer has been created, a localhost server is running or reused, and the final response includes the localhost preview URL.

The stable output location is:

```text
<current-working-directory>/outputs/scenemakerai/<run-id>/panorama.png
```

An image path under `.codex/generated_images/...` is only a temporary image-tool cache location. It is not the final SceneMakerAI artifact.

For every completed run:

1. Copy the accepted generated image to `<run-dir>/panorama.png`.
2. Create the viewer in `<run-dir>/viewer/`.
3. Reuse an existing local static server for `<run-dir>/viewer/` if one is already running; otherwise start one.
4. Return both `<run-dir>/panorama.png` and the cache-busted localhost Pannellum URL printed by the viewer helper.

A response containing only "Generated Image" or only a `.codex/generated_images/...` path is incomplete.

## Generated Image Tool Handling

When an image generation tool returns a file under `.codex/generated_images/...`, locate that file and copy it into the active run directory as `<run-dir>/panorama.png` before continuing. Use the current-working-directory copy for validation, Pannellum viewer creation, edit loops, and final reporting.

Do not treat the image-generation cache path as durable output. If the image tool only reports a `file://` URL, convert it to the local filesystem path before copying.

## Inputs

- Required: one source image.
- Optional: user scene instructions, such as "make the background more crowded with people."

Use the source image as the starting visual reference, not an immutable region. Optional scene instructions may affect the whole panorama, including the original-visible/front-view area, when that is the natural way to satisfy the request.

## Image Quality Default

All generated and edited panoramas should be sharp, high-definition, and suitable for full-screen Pannellum viewing by default. Always include quality language in the image prompt: crisp details, clear distant objects, clean natural edges, high texture fidelity, no blur, no softness, no pixelation, no compression artifacts, and no painterly smearing.

The built-in image generation tool may not expose explicit quality or resolution controls. Do not invent tool parameters. Enforce high-definition behavior through the prompt and reject or regenerate outputs that look soft, blurry, low-resolution, or artifacted.

## Workflow

1. Inspect the source image.
   - Identify whether it is landscape, portrait, fisheye/wide-angle, indoor, outdoor, or object-centric.
   - Identify anchors to preserve: architecture, people, foreground objects, lighting, ground plane, sky/ceiling, camera height, perspective, and left/right boundary cues.
   - If the image contains real people, avoid inventing close-up new views of them unless the user explicitly asks and the request is appropriate.

2. Prepare a 2:1 panorama canvas and mask for local image files.
   - Create one run directory under the agent's current working directory, preferably `outputs/scenemakerai/<timestamp-or-short-id>/`.
   - Use `<run-dir>/prep/` for temporary canvas and mask files.
   - Run `scripts/prepare_pano_canvas.py <image> --out-dir <run-dir>/prep --width 2048 --height 1024` unless the user specifies another 2:1 size.
   - Use the generated `canvas.png`, `mask.png`, `mask-alpha.png`, `preview.png`, and `metadata.json`.
   - The default mask convention is `black=source reference white=generate`.
   - Use masks to guide outpainting structure, not to enforce that the source region must remain unchanged.
   - Use `mask-alpha.png` only when the active image tool expects transparent pixels to be generated and opaque pixels to be used as the source reference.

3. Generate one equirectangular panorama.
   - Prefer an image editing/outpainting tool that accepts both an image and a mask.
   - Ask for one single `2:1` equirectangular panorama, not a collage and not six separate images.
   - Use the source image area as the front-view reference region.
   - Apply optional user scene instructions across the panorama where visually appropriate, including the front-view region if needed.
   - Extend missing left, right, back, up, and down views plausibly from the same fixed camera position.
   - Request seamless left/right wraparound.
   - Request sharp high-definition output using the Image Quality Default language.
   - Save or copy the accepted generated panorama to `<run-dir>/panorama.png`.
   - Read `references/prompting.md` for compact prompt templates.

4. Handle tool limitations honestly.
   - If the available image tool supports mask editing, use the mask for outpainting structure when helpful, but do not require exact preservation of the source region.
   - If only a reference-style image generation tool is available, use the source image as the main visual reference.
   - If a mask tool would prevent a requested change to the front-view/source region, generate the panorama from reference or edit the accepted panorama afterward so the requested change can affect that region.
   - Do not claim factual reconstruction of unseen areas. The missing scene content is generated.

5. Verify the panorama.
   - Confirm the output is one image with width:height approximately `2:1`.
   - Confirm the front-view scene remains recognizable.
   - Confirm optional instructions are reflected in the panorama where visually appropriate.
   - Confirm the image looks sharp enough for full-screen Pannellum viewing, with clear texture detail and no obvious blur, pixelation, compression artifacts, or painterly smearing.
   - Check whether the left and right edges can wrap without an obvious hard seam.
   - Regenerate or correct any non-2:1 output before finalizing.
   - Regenerate or edit any output that is visibly low-definition or soft.
   - After the final initial panorama is accepted and stored at `<run-dir>/panorama.png`, delete `<run-dir>/prep/` unless the user asks to keep intermediate files for debugging.

6. Automatically create a local Pannellum preview.
   - Run `scripts/create_pannellum_viewer.py <run-dir>/panorama.png --out-dir <run-dir>/viewer`.
   - Before starting a server, check whether a localhost server is already serving `<run-dir>/viewer/`. If yes, reuse that server and port.
   - Start a new static server from `<run-dir>/viewer/`, for example `python -m http.server 8000`, only when no suitable server is already running.
   - If the preferred port is busy with an unrelated server, use another available port.
   - Return the final panorama path and the cache-busted localhost Pannellum viewer URL printed by the script.

## Edit Loop

When the user asks for changes after seeing a preview:

1. Use the latest final equirectangular panorama as the edit source.
2. Use an image editing tool, not a fresh source-image-to-panorama generation, unless the requested change requires starting over.
3. Preserve the `2:1` equirectangular format, camera position, horizon continuity, and seamless left/right wrapping.
4. Apply the user's requested change while preserving unrelated scene content and the sharp high-definition quality standard.
5. Save the edited result as a new final panorama image in the same run directory, such as `<run-dir>/panorama-edit-01.png`.
6. Re-run `scripts/create_pannellum_viewer.py <edited-panorama-path> --out-dir <run-dir>/viewer`; it must create a content-hashed viewer image filename and a cache-busted URL.
7. Return the edited panorama path and the new cache-busted localhost Pannellum URL. Do not reuse a bare `http://localhost:<port>/` URL after edits.

If the edit request would break the fixed-position panorama assumption or requires factual unseen details, state the limitation and make only a plausible visual edit.

## Output Rules

- Always return the final `2:1` equirectangular panorama image path under `<current-working-directory>/outputs/scenemakerai/<run-id>/panorama.png`.
- Always return the cache-busted local Pannellum preview URL printed by `scripts/create_pannellum_viewer.py`.
- Keep only the accepted final panorama image, the active `viewer/` folder needed for the preview URL, and any user-requested saved variants.
- Delete temporary prep artifacts after the initial panorama is accepted: `canvas.png`, `mask.png`, `mask-alpha.png`, `preview.png`, and `metadata.json`.
- Do not output cubemap faces.
- Do not imply the result is a walkable 3D reconstruction. It is a fixed-point panorama.
