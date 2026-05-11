# Prompting Reference

Use these prompts as starting points. Add concrete scene details only after inspecting the source image.

## Default Quality Addendum

Include this in every generation and edit prompt:

```text
Render as a sharp, high-definition panorama suitable for full-screen viewing. Preserve crisp details, clear distant objects, clean natural edges, and high texture fidelity. Avoid blur, softness, pixelation, compression artifacts, painterly smearing, warped details, and low-resolution output.
```

## Masked Outpainting Prompt

```text
Create one single 2:1 equirectangular 360 panorama from this canvas. Use the original photo region as the front-facing visual reference, but it does not need to remain pixel-identical if the user instruction requires a visual change. Fill the missing left, right, back, upward, and downward views from the same fixed camera position.

Keep the same scene identity, architecture, lighting, weather, ground plane, ceiling or sky, camera height, and perspective. Make the panorama seamless at the left and right edges. Render as a sharp, high-definition panorama suitable for full-screen viewing, with crisp details, clear distant objects, clean natural edges, and high texture fidelity. Avoid blur, softness, pixelation, compression artifacts, painterly smearing, warped details, and low-resolution output. Output one wide equirectangular panorama only. No text, watermark, frame, UI, collage, cubemap, or multiple panels.
```

## Optional Scene Instruction Addendum

```text
Apply this user instruction across the panorama where visually appropriate, including the original-visible/front-view region if needed: "{user_instruction}"
```

## Reference-Only Prompt

Use this when no mask-capable editing tool is available or when the user instruction should affect the original-visible/front-view region.

```text
Using the attached image as the source front-view reference, create one single 2:1 equirectangular 360 panorama. Use the visible source scene as the main visual basis. Extend the scene naturally to the left, right, behind, above, and below as if standing in one fixed spot. Apply any optional user scene instruction across the panorama where visually appropriate, including the original-visible/front-view region if needed. Make it suitable for a fixed-position panorama viewer with seamless left/right wrapping. Render as a sharp, high-definition panorama suitable for full-screen viewing, with crisp details, clear distant objects, clean natural edges, and high texture fidelity. Avoid blur, softness, pixelation, compression artifacts, painterly smearing, warped details, and low-resolution output. Output one wide panorama only, not a collage, not a cubemap, and not six images.
```

## Panorama Edit Prompt

Use this after the user has already previewed a panorama and asks for an edit.

```text
Edit this existing 2:1 equirectangular 360 panorama according to this request: "{edit_request}"

Preserve the equirectangular projection, 2:1 aspect ratio, fixed camera position, horizon continuity, and seamless left/right wrapping. Keep unrelated scene content unchanged. Keep the edited panorama sharp and high-definition for full-screen viewing, with crisp details, clear distant objects, clean natural edges, and high texture fidelity. Avoid blur, softness, pixelation, compression artifacts, painterly smearing, warped details, and low-resolution output. Output one edited wide panorama image only. No text, watermark, frame, UI, collage, cubemap, or multiple panels.
```

## Scene Detail Checklist

- Location type: cafe, plaza, office, room, street, corridor, landscape.
- Foreground anchors: table, laptop, chair, person, plant, door, window.
- Structural anchors: ceiling, overhang, walls, columns, building facades.
- Ground/sky: pavement pattern, grass, indoor floor, clouds, ceiling lights.
- Lighting: daylight, warm indoor, overcast, night, shadows.
