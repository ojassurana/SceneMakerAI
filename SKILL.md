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
   - Run `scripts/prepare_pano_canvas.py <image> --out-dir <work-dir> --width 2048 --height 1024` unless the user specifies another 2:1 size.
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

6. Automatically create a local Pannellum preview.
   - Run `scripts/create_pannellum_viewer.py <panorama-path> --out-dir <viewer-dir>`.
   - Start a local static server from that viewer directory, for example `python -m http.server 8000`.
   - If the port is busy, use another available port.
   - Return the final panorama path and the localhost Pannellum viewer URL.

## Output Rules

- Always return the final `2:1` equirectangular panorama image path.
- Always return the local Pannellum preview URL.
- Do not output cubemap faces.
- Do not imply the result is a walkable 3D reconstruction. It is a fixed-point panorama.
