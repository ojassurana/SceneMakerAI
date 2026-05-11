# Prompting Reference

Use these prompts as starting points. Add concrete scene details only after inspecting the source image.

## Masked Outpainting Prompt

```text
Create one single 2:1 equirectangular 360 panorama from this canvas. Preserve the original photo region exactly as the protected front-facing view. Fill only the masked/blank areas as the missing left, right, back, upward, and downward views from the same fixed camera position.

Keep the same scene identity, architecture, lighting, weather, ground plane, ceiling or sky, camera height, and perspective. Make the panorama seamless at the left and right edges. Output one wide equirectangular panorama only. No text, watermark, frame, UI, collage, cubemap, or multiple panels.
```

## Optional Scene Instruction Addendum

```text
Apply this user instruction only to the generated/outpainted regions, not to the protected original photo region: "{user_instruction}"
```

## Reference-Only Prompt

Use this only when no mask-capable editing tool is available, and tell the user exact preservation is not guaranteed.

```text
Using the attached image as the source front-view reference, create one single 2:1 equirectangular 360 panorama. Preserve the visible source scene as closely as possible. Extend the scene naturally to the left, right, behind, above, and below as if standing in one fixed spot. Apply any optional user scene instruction only to the newly invented surrounding areas. Make it suitable for a fixed-position panorama viewer with seamless left/right wrapping. Output one wide panorama only, not a collage, not a cubemap, and not six images.
```

## Scene Detail Checklist

- Location type: cafe, plaza, office, room, street, corridor, landscape.
- Foreground anchors: table, laptop, chair, person, plant, door, window.
- Structural anchors: ceiling, overhang, walls, columns, building facades.
- Ground/sky: pavement pattern, grass, indoor floor, clouds, ceiling lights.
- Lighting: daylight, warm indoor, overcast, night, shadows.
