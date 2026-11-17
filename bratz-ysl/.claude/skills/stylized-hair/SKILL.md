---
name: stylized-hair
description: Glossy stylized hair for animated doll characters in Blender 5.3 EEVEE, in the look of the Alwayz Bratz series by Pixel Zoo. Use when hair looks plastic, lumpy, flat or painted on, when hair is baked into a single Rodin or AI-generated mesh and texture, or when hair needs smooth sculpted volumes with a highlight ring and strand detail. Separates the hair from a single-mesh character by texture colour, smooths it into a clean volume, and builds a hair material with a lit highlight ring, strand grooves and darker roots.
---

# Stylized Hair

Look target (Alwayz Bratz): big smooth **volumes**, a bright **highlight ring** across the head that follows the shape, fine strand grooves only visible in the light, slightly darker roots, clean separated tips. Never particle fur, never noisy texture.

## Why AI meshes look plastic
Rodin and similar generators bake hair into the body mesh and paint it in the texture: lumpy surface, no highlight, same shading as skin. Fix in three steps: cut it out, smooth it, give it its own material.

## Recipe (single-mesh Rodin / AI characters): mask, do not cut
Tested on the Bratz Kylie Rodin model (393k faces, one 2K texture): no holes, no seam cracks, fabric-like grain gone, curls stay crisp.
```bash
B=/Applications/Blender.app/Contents/MacOS/Blender
S=.claude/skills/stylized-hair/scripts/stylized_hair.py
$B -b scene.blend -P $S -- --mask Kylie --hair-rgb 0.133,0.075,0.059 --tol 0.12 --min-z 0.82 \
   --rgb 0.010,0.0065,0.0055 --smooth-iters 8 --grooves 30 --ring 0.35 --save
```
What it does:
1. Welds the UV-seam duplicate vertices glTF creates (otherwise any smoothing opens cracks along seams).
2. Samples the texture under every vertex; vertices close to `--hair-rgb` (texture value, 0-1 as stored) and above `--min-z` of the height become hair. Morphological closing then opening on the mesh fills speckle holes and drops isolated dark specks (eyes, lashes). Result: vertex group `hair` + colour attribute `hair_mask` with a soft edge.
3. Corrective Smooth restricted to the `hair` group (`--smooth-iters`: 8 keeps curls crisp; 25+ melts thin curls into shavings).
4. Inserts the hair shader into the existing material, mixed by `hair_mask`, so skin, face and dress keep their Rodin shading.

Finding `--hair-rgb`: sample texture colours of faces on the back of the head (they are always hair); the Kylie value above came from that. Run the command, then render front, 3/4 and back: if hair edges show skin or holes, raise `--tol` by 0.02; if eyebrows or a dark dress turn into hair, lower it or raise `--min-z`.

Use a flat `--rgb` rather than `--keep-texture` on Rodin models: their painted hair texture often contains skin-coloured strips at seams, which show through.

Colours (linear): near-black brown 0.010,0.0065,0.0055 (Kylie), blue-black 0.008,0.008,0.011 (Jade), dark brown 0.05,0.025,0.012, caramel balayage 0.35,0.18,0.07, platinum 0.75,0.68,0.55, pastel pink 0.9,0.45,0.6.

### Alternative: separate hair object
For hair painted in a clean flat colour, `--split OBJ` cuts it into `OBJ_hair`, `--smooth OBJ_hair` volumises it and `--material NAME --assign OBJ_hair` shades it. Do not use it on Rodin models: texture variations leave holes in curls.

## The material
- Principled: roughness 0.28, coat 0.35 (toy gloss), darker roots from the top of the bounding box.
- **Highlight ring**: EEVEE ignores anisotropy, so the ring is built from the world normal (a latitude band), weighted by how much the surface faces the camera, broken into strands by a wave texture, and multiplied by the real lighting through Shader to RGB, so it only shows where a light hits. Tune with `--ring 0.3` to 0.8 and `--ring-pos 0.5` (lower on the head) to 0.75 (near the crown).
- Strand grooves: a soft wavy bump, off by default. `--grooves 30` gives strands sweeping up the back of an updo; 40 to 60 for long straight hair. Above 60 with distortion it reads as woven fabric.
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
