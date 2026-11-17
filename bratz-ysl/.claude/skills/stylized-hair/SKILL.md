---
name: stylized-hair
description: Glossy stylized hair for animated doll characters in Blender 5.3 EEVEE, in the look of the Alwayz Bratz series by Pixel Zoo. Use when hair looks plastic, lumpy, flat or painted on, when hair is baked into a single Rodin or AI-generated mesh and texture, or when hair needs smooth sculpted volumes with a highlight ring and strand detail. Separates the hair from a single-mesh character by texture colour, smooths it into a clean volume, and builds a hair material with a lit highlight ring, strand grooves and darker roots.
---

# Stylized Hair

Look target (Alwayz Bratz): big smooth **volumes**, a bright **highlight ring** across the head that follows the shape, fine strand grooves only visible in the light, slightly darker roots, clean separated tips. Never particle fur, never noisy texture.

## Why AI meshes look plastic
Rodin and similar generators bake hair into the body mesh and paint it in the texture: lumpy surface, no highlight, same shading as skin. Fix in three steps: cut it out, smooth it, give it its own material.

## Recipe
```bash
B=/Applications/Blender.app/Contents/MacOS/Blender
S=.claude/skills/stylized-hair/scripts/stylized_hair.py
# 1. find the hair colour: render or open the texture and pick a hair pixel (linear 0-1)
# 2. cut, smooth, shade (keep the painted colour under the gloss)
$B -b scene.blend -P $S -- --split Kylie --hair-rgb 0.04,0.03,0.025 --tol 0.12 \
   --smooth Kylie_hair --material kylie --keep-texture --assign Kylie_hair --save
```
- `--split` keeps faces above `--min-z` (default 0.55 of the height) whose texture colour is within `--tol` of `--hair-rgb`. Check the count printed; patchy result means raise `--tol` slightly, eyebrows or dark clothes caught means lower it or raise `--min-z`.
- If the character is skinned, the hair object is re-parented to the same armature; keep the Armature modifier first (the script reorders it).
- `--smooth` adds Corrective Smooth (25 iterations) and Subdivision (render level 2): lumps disappear, the silhouette stays.
- Without `--keep-texture`, `--rgb` sets a flat colour: black hair 0.012,0.010,0.010, dark brown 0.05,0.025,0.012, caramel 0.35,0.18,0.07, platinum 0.75,0.68,0.55, pastel pink 0.9,0.45,0.6.

## The material
- Principled: roughness 0.28, coat 0.35 (toy gloss), darker roots from the top of the bounding box.
- **Highlight ring**: EEVEE ignores anisotropy, so the ring is built from the world normal (a latitude band), weighted by how much the surface faces the camera, broken into strands by a wave texture, and multiplied by the real lighting through Shader to RGB, so it only shows where a light hits. Tune with `--ring 0.4` to 1.0 and `--ring-pos 0.5` (lower on the head) to 0.75 (near the crown).
- Strand grooves: a fine wavy bump (`--grooves 60`, 0 disables). Raise for long straight hair, lower for short cuts.
- In Cycles the ring is not computed (Shader to RGB is EEVEE only); real anisotropy takes over.

## Shape rules (when modelling new hair)
- Build hair as a few big locks (curves with a flattened, tapered bevel or sculpted volumes), not hundreds of strands.
- Separate the tips into 3 to 6 points per lock; keep the crown smooth.
- Bangs and face-framing locks are separate objects so they can overlap the face cleanly.
- Rim light from behind in warm gold is what makes the silhouette read against a black set.

## Check
Render a close-up at 50 % with the shot's lighting: one clear ring, no stripes visible at a distance, no lumps on the silhouette, roots slightly darker than the lengths.

## Related skills
blender-hair-grooming (real hair curves), blender-stylized-npr (toon looks), blender-lighting (rim light).
