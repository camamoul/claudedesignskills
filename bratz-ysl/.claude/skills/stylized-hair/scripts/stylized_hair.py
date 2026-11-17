#!/usr/bin/env python3
"""
Stylized glossy hair for Rodin-style character meshes (Blender 5.3, EEVEE or Cycles).

Look target: Alwayz Bratz / Pixel Zoo hair - smooth sculpted volumes, a strong
glossy highlight band across the strands, fine strand grooves, slightly darker
roots, clean lighter tips. No particle hair: fast and stable in EEVEE.

Tools:
  0. --mask OBJ         RECOMMENDED for single-mesh (Rodin) characters: paint a soft hair
                        mask from the texture colour, smooth only the hair, blend the
                        hair shader in. No cut, no holes, works with an existing rig.
  1. --split OBJ        cut the hair out by texture colour (only for clean, flat-painted hair)
  2. --smooth OBJ       turn a separate lumpy hair shell into a smooth volume
  3. --material NAME    build the glossy hair material and assign it (--assign OBJ)

Run inside Blender:
    Blender -b scene.blend -P stylized_hair.py -- --split kylie --hair-rgb 0.05,0.03,0.02 --tol 0.12
    Blender -b scene.blend -P stylized_hair.py -- --smooth kylie_hair
    Blender -b scene.blend -P stylized_hair.py -- --material kylie --rgb 0.03,0.02,0.015 --assign kylie_hair --save
    # all in one, keeping the painted texture colour under the gloss:
    Blender -b scene.blend -P stylized_hair.py -- --split jade --hair-rgb 0.04,0.04,0.05 \
        --smooth jade_hair --material jade --keep-texture --assign jade_hair --save

Arguments (after --):
    --mask OBJ           RECOMMENDED for single-mesh (Rodin) characters: no cut, no holes. Paints a
                         soft hair mask from the texture colour, smooths only the hair (vertex group
                         'hair'), blends the hair shader in through the 'hair_mask' attribute
    --smooth-iters N     smoothing strength for --mask (default 30; 15 keeps more sculpted detail)
    --split OBJ          object to cut; creates OBJ_hair (faces whose texture colour is close to --hair-rgb)
    --hair-rgb r,g,b     hair colour to look for in the texture, linear 0-1 (pick it from a render/texture)
    --tol F              colour distance tolerance (default 0.12; raise if hair is patchy)
    --min-z F            only faces above this fraction of the object height (default 0.55: keeps the head)
    --smooth OBJ         smooth/volumise a hair object (corrective smooth + subdivision + shade smooth)
    --material NAME      create material HAIR_NAME
    --rgb r,g,b          base colour (linear) when not keeping the texture (default dark brown)
    --keep-texture       use the object's existing image texture as base colour (Rodin paint)
    --assign OBJ         assign HAIR_NAME to every slot of OBJ
    --grooves F          strand groove bump density (default 0 = off; 40-80 for long straight hair)
    --ring F             highlight ring strength (default 0.5; 0 disables)
    --ring-pos F         ring height on the head = world normal Z (default 0.6; higher = nearer the crown)
    --save               save the .blend
"""
import sys

try:
    import bpy
    import numpy as np
except ImportError:
    sys.exit("Run this inside Blender: Blender -b scene.blend -P stylized_hair.py -- --material x")

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def opt(name, default=None, flag=False):
    if name not in ARGS:
        return False if flag else default
    if flag:
        return True
    i = ARGS.index(name)
    if i + 1 >= len(ARGS):
        sys.exit(f"missing value after {name}")
    return ARGS[i + 1]


def rgb(text):
    vals = tuple(float(v) for v in text.split(","))
    if len(vals) != 3:
        raise ValueError(f"expected r,g,b, got {text}")
    return vals


def get_obj(name):
    obj = bpy.data.objects.get(name)
    if not obj or obj.type != "MESH":
        sys.exit(f"mesh object not found: {name} (meshes: {[o.name for o in bpy.data.objects if o.type == 'MESH']})")
    return obj


def find_image(obj):
    for slot in obj.material_slots:
        mat = slot.material
        if mat and mat.node_tree:
            for n in mat.node_tree.nodes:
                if n.type == "TEX_IMAGE" and n.image:
                    return n.image
    return None


def split_by_texture(obj, hair_rgb, tol, min_z):
    img = find_image(obj)
    if img is None:
        sys.exit(f"{obj.name}: no image texture found to sample")
    w, h = img.size
    px = np.empty(w * h * 4, dtype=np.float32)
    img.pixels.foreach_get(px)
    px = px.reshape(h, w, 4)[:, :, :3]
    me = obj.data
    uv = me.uv_layers.active.data
    zs = np.array([v.co.z for v in me.vertices])
    z0, z1 = zs.min(), zs.max()
    target = np.array(hair_rgb, dtype=np.float32)
    keep = np.zeros(len(me.polygons), dtype=bool)
    for p in me.polygons:
        if (p.center.z - z0) / max(z1 - z0, 1e-6) < min_z:
            continue
        u = sum(uv[i].uv.x for i in p.loop_indices) / p.loop_total
        v = sum(uv[i].uv.y for i in p.loop_indices) / p.loop_total
        col = px[min(h - 1, max(0, int(v * h))), min(w - 1, max(0, int(u * w)))]
        keep[p.index] = np.linalg.norm(col - target) < tol
    if not keep.any():
        sys.exit(f"{obj.name}: no face matched hair colour {hair_rgb} (tol {tol}); sample the real colour first")
    me.polygons.foreach_set("select", keep)
    me.update()
    bpy.ops.object.mode_set(mode="OBJECT") if bpy.context.object and bpy.context.object.mode != "OBJECT" else None
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_mode(type="FACE")
    bpy.ops.object.mode_set(mode="OBJECT")
    me.polygons.foreach_set("select", keep)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.separate(type="SELECTED")
    bpy.ops.object.mode_set(mode="OBJECT")
    hair = [o for o in bpy.context.selected_objects if o != obj][0]
    hair.name = f"{obj.name}_hair"
    # keep the hair following the rig if the body was skinned
    if obj.parent and obj.parent.type == "ARMATURE":
        hair.parent = obj.parent
    print(f"[stylized-hair] split {int(keep.sum())} of {len(keep)} faces into {hair.name}")
    return hair


def smooth_volume(obj):
    for mod in list(obj.modifiers):
        if mod.name.startswith("HAIR_"):
            obj.modifiers.remove(mod)
    cs = obj.modifiers.new("HAIR_smooth", "CORRECTIVE_SMOOTH")
    cs.factor = 0.8
    cs.iterations = 25
    cs.smooth_type = "LENGTH_WEIGHTED"
    cs.use_only_smooth = True
    sub = obj.modifiers.new("HAIR_subdiv", "SUBSURF")
    sub.levels = 1
    sub.render_levels = 2
    obj.data.shade_smooth()
    # armature (if any) must stay first so smoothing happens after deformation
    for i, mod in enumerate(obj.modifiers):
        if mod.type == "ARMATURE" and i != 0:
            with bpy.context.temp_override(object=obj):
                bpy.ops.object.modifier_move_to_index(modifier=mod.name, index=0)
    print(f"[stylized-hair] {obj.name}: corrective smooth + subdivision added")


def build_hair_nodes(nt, base_rgb, image=None, grooves=0.0, ring_center=0.6, ring_width=0.09,
                     ring_strength=0.5, darken_roots=True, uv_name=None):
    """Build the hair shader inside node tree nt; return the output shader socket."""
    N, L = nt.nodes, nt.links
    bsdf = N.new("ShaderNodeBsdfPrincipled")
    total = N.new("ShaderNodeAddShader")               # principled + lit highlight ring
    L.new(bsdf.outputs[0], total.inputs[0])
    bsdf.inputs["Roughness"].default_value = 0.34
    bsdf.inputs["Specular IOR Level"].default_value = 0.5
    bsdf.inputs["Coat Weight"].default_value = 0.2       # toy gloss, not lacquer
    bsdf.inputs["Coat Roughness"].default_value = 0.15
    bsdf.inputs["Anisotropic"].default_value = 0.75      # Cycles only; EEVEE ignores it -> ring below
    tan = N.new("ShaderNodeTangent")
    tan.direction_type = "RADIAL"
    tan.axis = "Z"
    L.new(tan.outputs[0], bsdf.inputs["Tangent"])
    tc = N.new("ShaderNodeTexCoord")
    # base colour: flat colour, or the painted texture pushed darker and richer
    if image:
        tex = N.new("ShaderNodeTexImage")
        tex.image = image
        if uv_name:
            uvn = N.new("ShaderNodeUVMap"); uvn.uv_map = uv_name
            L.new(uvn.outputs[0], tex.inputs["Vector"])
        else:
            L.new(tc.outputs["UV"], tex.inputs["Vector"])
        hsv = N.new("ShaderNodeHueSaturation")
        hsv.inputs["Saturation"].default_value = 1.1
        hsv.inputs["Value"].default_value = 0.55
        L.new(tex.outputs["Color"], hsv.inputs["Color"])
        base = hsv.outputs["Color"]
    else:
        rgbn = N.new("ShaderNodeRGB")
        rgbn.outputs[0].default_value = (*base_rgb, 1)
        base = rgbn.outputs[0]
    if darken_roots:
        sep = N.new("ShaderNodeSeparateXYZ")
        L.new(tc.outputs["Generated"], sep.inputs[0])
        root = N.new("ShaderNodeMapRange")               # top of bbox (roots) darker
        root.inputs["From Min"].default_value = 1.0
        root.inputs["From Max"].default_value = 0.6
        root.inputs["To Min"].default_value = 0.65
        root.inputs["To Max"].default_value = 1.0
        L.new(sep.outputs["Z"], root.inputs["Value"])
        mul = N.new("ShaderNodeMix")
        mul.data_type = "RGBA"
        mul.blend_type = "MULTIPLY"
        mul.inputs["Factor"].default_value = 1.0
        gray = N.new("ShaderNodeCombineColor")
        for i in range(3):
            L.new(root.outputs[0], gray.inputs[i])
        L.new(base, mul.inputs["A"]); L.new(gray.outputs[0], mul.inputs["B"])
        L.new(mul.outputs["Result"], bsdf.inputs["Base Color"])
    else:
        L.new(base, bsdf.inputs["Base Color"])
    # strand grooves: fine vertical bands, slightly wavy, as a bump (not a texture you can see as stripes)
    if grooves > 0:
        wave = N.new("ShaderNodeTexWave")
        wave.wave_type = "BANDS"
        wave.bands_direction = "X"
        wave.inputs["Scale"].default_value = grooves
        wave.inputs["Distortion"].default_value = 1.5
        wave.inputs["Detail"].default_value = 0.0
        L.new(tc.outputs["Object"], wave.inputs["Vector"])
        bump = N.new("ShaderNodeBump")
        bump.inputs["Strength"].default_value = 0.2
        bump.inputs["Distance"].default_value = 0.002
        L.new(wave.outputs["Fac"], bump.inputs["Height"])
        L.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    # "angel ring" highlight (works in EEVEE): a latitude band where the world normal points
    # slightly up, strongest where the surface faces the camera, broken into strands,
    # and shown only where light actually hits (Shader to RGB)
    geo = N.new("ShaderNodeNewGeometry")
    sy = N.new("ShaderNodeSeparateXYZ")
    L.new(geo.outputs["Normal"], sy.inputs[0])
    d = N.new("ShaderNodeMath"); d.operation = "SUBTRACT"; d.inputs[1].default_value = ring_center
    L.new(sy.outputs["Z"], d.inputs[0])
    ad = N.new("ShaderNodeMath"); ad.operation = "ABSOLUTE"
    L.new(d.outputs[0], ad.inputs[0])
    band = N.new("ShaderNodeMapRange")
    band.interpolation_type = "SMOOTHERSTEP"
    band.inputs["From Min"].default_value = ring_width
    band.inputs["From Max"].default_value = 0.0
    L.new(ad.outputs[0], band.inputs["Value"])
    brk = N.new("ShaderNodeTexWave")
    brk.wave_type = "BANDS"
    brk.bands_direction = "X"
    brk.inputs["Scale"].default_value = max(grooves, 1.0) * 0.12
    brk.inputs["Distortion"].default_value = 1.2
    L.new(tc.outputs["Object"], brk.inputs["Vector"])
    brkr = N.new("ShaderNodeMapRange")
    brkr.inputs["To Min"].default_value = 0.55
    L.new(brk.outputs["Fac"], brkr.inputs["Value"])
    diff = N.new("ShaderNodeBsdfDiffuse")
    s2r = N.new("ShaderNodeShaderToRGB")
    L.new(diff.outputs[0], s2r.inputs[0])
    lit = N.new("ShaderNodeRGBToBW")
    L.new(s2r.outputs["Color"], lit.inputs[0])
    lw = N.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.5
    face = N.new("ShaderNodeMath"); face.operation = "SUBTRACT"; face.inputs[0].default_value = 1.0
    L.new(lw.outputs["Facing"], face.inputs[1])
    m0 = N.new("ShaderNodeMath"); m0.operation = "MULTIPLY"
    L.new(band.outputs[0], m0.inputs[0]); L.new(face.outputs[0], m0.inputs[1])
    m1 = N.new("ShaderNodeMath"); m1.operation = "MULTIPLY"
    m2 = N.new("ShaderNodeMath"); m2.operation = "MULTIPLY"
    m3 = N.new("ShaderNodeMath"); m3.operation = "MULTIPLY"; m3.inputs[1].default_value = ring_strength
    L.new(m0.outputs[0], m1.inputs[0]); L.new(brkr.outputs[0], m1.inputs[1])
    L.new(m1.outputs[0], m2.inputs[0]); L.new(lit.outputs[0], m2.inputs[1])
    L.new(m2.outputs[0], m3.inputs[0])
    ring = N.new("ShaderNodeEmission")
    ring.inputs["Color"].default_value = (1.0, 0.93, 0.85, 1)
    L.new(m3.outputs[0], ring.inputs["Strength"])
    L.new(ring.outputs[0], total.inputs[1])
    return total.outputs[0]


def hair_material(name, base_rgb, keep_texture_from=None, grooves=0.0,
                  ring_center=0.6, ring_width=0.09, ring_strength=0.5):
    mat = bpy.data.materials.get(f"HAIR_{name}") or bpy.data.materials.new(f"HAIR_{name}")
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    img = find_image(keep_texture_from) if keep_texture_from else None
    sock = build_hair_nodes(nt, base_rgb, img, grooves, ring_center, ring_width, ring_strength)
    nt.links.new(sock, out.inputs["Surface"])
    return mat


def edge_arrays(me):
    ev = np.empty(len(me.edges) * 2, dtype=np.int64)
    me.edges.foreach_get("vertices", ev)
    ev = ev.reshape(-1, 2)
    return ev[:, 0], ev[:, 1]


def weld_groups(co):
    """Index of coincident-vertex group per vertex (glTF splits vertices along UV seams)."""
    keys = np.round(co / 1e-5).astype(np.int64)
    _, inv = np.unique(keys, axis=0, return_inverse=True)
    return inv.ravel()


def weld_max(mask, grp):
    g = np.full(grp.max() + 1, -np.inf, dtype=mask.dtype)
    np.maximum.at(g, grp, mask)
    return g[grp]


def morph(mask, a, b, grow):
    out = mask.copy()
    op = np.maximum if grow else np.minimum
    op.at(out, a, mask[b])
    op.at(out, b, mask[a])
    return out


def blur(mask, a, b):
    acc = np.zeros_like(mask)
    cnt = np.zeros_like(mask)
    np.add.at(acc, a, mask[b]); np.add.at(acc, b, mask[a])
    np.add.at(cnt, a, 1.0); np.add.at(cnt, b, 1.0)
    nbmean = np.where(cnt > 0, acc / np.maximum(cnt, 1), mask)
    return (mask + nbmean) * 0.5


def mask_hair(obj, hair_rgb, tol, min_z, base_rgb, keep_texture, ring_center, ring_strength,
              grooves, smooth_iters=30, close=2):
    """No cut: paint a soft 'hair' mask on the single mesh, smooth only there, blend a hair shader in."""
    img = find_image(obj)
    if img is None:
        sys.exit(f"{obj.name}: no image texture found to sample")
    w, h = img.size
    px = np.empty(w * h * 4, dtype=np.float32)
    img.pixels.foreach_get(px)
    px = px.reshape(h, w, 4)[:, :, :3]
    me = obj.data
    # weld the UV-seam duplicates glTF creates, otherwise smoothing opens cracks along seams
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(me)
    before = len(bm.verts)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    bm.to_mesh(me)
    bm.free()
    me.update()
    print(f"[stylized-hair] {obj.name}: welded {before - len(me.vertices)} seam vertices")
    nloops = len(me.loops)
    uvs = np.empty(nloops * 2, dtype=np.float32)
    me.uv_layers.active.data.foreach_get("uv", uvs)
    uvs = uvs.reshape(-1, 2)
    lv = np.empty(nloops, dtype=np.int32)
    me.loops.foreach_get("vertex_index", lv)
    cols = px[np.clip((uvs[:, 1] * h).astype(int), 0, h - 1), np.clip((uvs[:, 0] * w).astype(int), 0, w - 1)]
    dist = np.linalg.norm(cols - np.array(hair_rgb, dtype=np.float32), axis=1)
    loop_hit = (dist < tol).astype(np.float32)
    nv = len(me.vertices)
    hit = np.zeros(nv, dtype=np.float32)
    np.maximum.at(hit, lv, loop_hit)
    co = np.empty(nv * 3, dtype=np.float32)
    me.vertices.foreach_get("co", co)
    z = co.reshape(-1, 3)[:, 2]
    zn = (z - z.min()) / max(z.max() - z.min(), 1e-6)
    hit[zn < min_z] = 0
    a, b = edge_arrays(me)
    grp = weld_groups(co.reshape(-1, 3))
    hit = weld_max(hit, grp)          # a seam vertex is hair if any of its twins is
    m = hit
    for _ in range(close):            # closing: fill speckle holes in curls / highlights
        m = weld_max(morph(m, a, b, True), grp)
    for _ in range(close):
        m = -weld_max(-morph(m, a, b, False), grp)
    for _ in range(close):            # opening: drop isolated dark specks (eyes, lashes) far from the hair
        m = -weld_max(-morph(m, a, b, False), grp)
    for _ in range(close):
        m = weld_max(morph(m, a, b, True), grp)
    soft = m.copy()
    for _ in range(3):                # soft edge for the shader blend
        soft = weld_max(blur(soft, a, b), grp)
    vg = obj.vertex_groups.get("hair") or obj.vertex_groups.new(name="hair")
    for wv in np.unique(np.round(soft[soft > 0.01], 2)):   # batch vertices by weight
        ids = np.nonzero(np.round(soft, 2) == wv)[0].tolist()
        vg.add(ids, float(wv), "REPLACE")
    attr = me.color_attributes.get("hair_mask") or me.color_attributes.new("hair_mask", "FLOAT_COLOR", "POINT")
    rgba = np.repeat(soft[:, None], 4, axis=1)
    rgba[:, 3] = 1
    attr.data.foreach_set("color", rgba.ravel())
    for mod in list(obj.modifiers):
        if mod.name.startswith("HAIR_"):
            obj.modifiers.remove(mod)
    cs = obj.modifiers.new("HAIR_smooth", "CORRECTIVE_SMOOTH")
    cs.vertex_group = "hair"
    cs.factor = 1.0
    cs.iterations = smooth_iters
    cs.smooth_type = "LENGTH_WEIGHTED"
    cs.use_only_smooth = True
    me.shade_smooth()
    # blend the hair shader into every material of the object, driven by the mask
    for slot in obj.material_slots:
        mat = slot.material
        if not mat or not mat.node_tree or mat.get("hair_blended"):
            continue
        nt = mat.node_tree
        outn = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
        if not outn.inputs["Surface"].is_linked:
            continue
        orig = outn.inputs["Surface"].links[0].from_socket
        hair_sock = build_hair_nodes(nt, base_rgb, img if keep_texture else None, grooves,
                                     ring_center=ring_center, ring_strength=ring_strength,
                                     darken_roots=False, uv_name=me.uv_layers.active.name)
        at = nt.nodes.new("ShaderNodeAttribute")
        at.attribute_name = "hair_mask"
        mix = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(at.outputs["Fac"], mix.inputs["Fac"])
        nt.links.new(orig, mix.inputs[1])
        nt.links.new(hair_sock, mix.inputs[2])
        nt.links.new(mix.outputs[0], outn.inputs["Surface"])
        mat["hair_blended"] = True
    print(f"[stylized-hair] {obj.name}: hair mask on {int((m > 0.5).sum())} of {nv} vertices, "
          f"smoothed {smooth_iters} it., hair shader blended in")


def assign(mat, obj):
    if not obj.material_slots:
        obj.data.materials.append(mat)
    for slot in obj.material_slots:
        slot.material = mat
    print(f"[stylized-hair] {mat.name} -> {obj.name}")


def main():
    try:
        hair_rgb = rgb(opt("--hair-rgb", "0.05,0.03,0.02"))
        base_rgb = rgb(opt("--rgb", "0.05,0.025,0.012"))
        tol = float(opt("--tol", 0.12))
        min_z = float(opt("--min-z", 0.55))
        grooves = float(opt("--grooves", 0))
        ring = float(opt("--ring", 0.5))
        ring_pos = float(opt("--ring-pos", 0.6))
    except ValueError as err:
        print(f"bad argument: {err}")
        sys.exit(1)
    if opt("--mask"):
        mask_hair(get_obj(opt("--mask")), hair_rgb, tol, min_z, base_rgb,
                  opt("--keep-texture", flag=True), ring_pos, ring, grooves,
                  smooth_iters=int(opt("--smooth-iters", 30)))
    split_name = opt("--split")
    hair_obj = None
    source = None
    if split_name:
        source = get_obj(split_name)
        hair_obj = split_by_texture(source, hair_rgb, tol, min_z)
    if opt("--smooth"):
        smooth_volume(hair_obj if hair_obj and opt("--smooth") == hair_obj.name else get_obj(opt("--smooth")))
    if opt("--material"):
        target = opt("--assign")
        tex_src = None
        if opt("--keep-texture", flag=True):
            tex_src = get_obj(target) if target else source
        mat = hair_material(opt("--material"), base_rgb, tex_src, grooves,
                            ring_center=ring_pos, ring_strength=ring)
        if target:
            assign(mat, get_obj(target))
        else:
            print(f"[stylized-hair] created {mat.name} (no --assign given)")
    if opt("--save", flag=True) and bpy.data.filepath:
        bpy.ops.wm.save_mainfile()
        print(f"[stylized-hair] saved {bpy.data.filepath}")


main()
