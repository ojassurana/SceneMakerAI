# Prompting Reference

Use these prompts as starting points. Add concrete scene details only after inspecting the source image.

## Default Quality Addendum

Include this in every generation and edit prompt:

```text
Render as a sharp, high-definition spherical 360 equirectangular environment map suitable for full-screen Pannellum viewing. Preserve crisp details, clear distant objects, clean natural edges, and high texture fidelity. Avoid blur, softness, pixelation, compression artifacts, painterly smearing, warped details, and low-resolution output.
```

## Masked Outpainting Prompt

```text
Create one single true spherical 360 equirectangular environment map from this canvas. It will be wrapped onto the inside of a sphere in Pannellum, so it must feel like a fixed-position look-around world, not a normal flat panoramic photo. Preserve the original photo region as the front-facing view unless the user explicitly requested a change to that original-visible area. Fill the missing left, right, back, upward, and downward views from the same fixed camera position.

Keep the same scene identity, architecture, lighting, weather, ground plane, ceiling or sky, camera height, and perspective. Make the environment seamless at the left and right edges. Render as a sharp, high-definition spherical 360 environment map suitable for full-screen viewing, with crisp details, clear distant objects, clean natural edges, and high texture fidelity. Avoid blur, softness, pixelation, compression artifacts, painterly smearing, warped details, and low-resolution output. Output one 2:1 equirectangular environment-map image only. Do not create a normal wide-angle landscape photo, cinematic banner, flat scenic panorama, cropped strip, collage, cubemap, or multiple panels. No text, watermark, frame, or UI.
```

## Optional Scene Instruction Addendum

```text
Apply this user instruction to the generated surrounding 360 environment where visually appropriate. Do not change the original-visible/front-view region unless the instruction explicitly asks to alter that region: "{user_instruction}"
```

## Reference-Only Prompt

Use this when no mask-capable editing tool is available or when the user instruction should affect the original-visible/front-view region.

```text
Using the attached image as the source front-view reference, create one single true spherical 360 equirectangular environment map. It will be wrapped onto the inside of a sphere in Pannellum, so it must feel like a fixed-position look-around world, not a normal flat panoramic photo. Preserve the visible source scene as the main front-view basis unless the user explicitly requested a change to that original-visible area. Extend the scene naturally to the left, right, behind, above, and below as if standing in one fixed spot. Apply any optional user scene instruction to the generated surrounding 360 environment where visually appropriate. Make it suitable for a fixed-position panorama viewer with seamless left/right wrapping. Render as a sharp, high-definition spherical 360 environment map suitable for full-screen viewing, with crisp details, clear distant objects, clean natural edges, and high texture fidelity. Avoid blur, softness, pixelation, compression artifacts, painterly smearing, warped details, and low-resolution output. Output one 2:1 equirectangular environment-map image only. Do not create a normal wide-angle landscape photo, cinematic banner, flat scenic panorama, cropped strip, collage, cubemap, or multiple panels.
```

## Panorama Edit Prompt

Use this after the user has already previewed a panorama and asks for an edit.

```text
Edit this existing 2:1 spherical 360 equirectangular environment map according to this request: "{edit_request}"

Preserve the spherical equirectangular projection, 2:1 aspect ratio, fixed camera position, horizon continuity, and seamless left/right wrapping. Keep unrelated scene content unchanged. Keep the edited environment map sharp and high-definition for full-screen viewing, with crisp details, clear distant objects, clean natural edges, and high texture fidelity. Avoid blur, softness, pixelation, compression artifacts, painterly smearing, warped details, and low-resolution output. Output one edited 2:1 equirectangular environment-map image only. Do not flatten it into a normal panoramic photo, scenic strip, or banner. No text, watermark, frame, UI, collage, cubemap, or multiple panels.
```

## Scene Detail Checklist

- Location type: cafe, plaza, office, room, street, corridor, landscape.
- Foreground anchors: table, laptop, chair, person, plant, door, window.
- Structural anchors: ceiling, overhang, walls, columns, building facades.
- Ground/sky: pavement pattern, grass, indoor floor, clouds, ceiling lights.
- Lighting: daylight, warm indoor, overcast, night, shadows.
