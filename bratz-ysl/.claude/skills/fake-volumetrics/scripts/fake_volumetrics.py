#!/usr/bin/env python3
"""
Fake volumetric light beams and haze for EEVEE (Blender 5.3), no volume shaders.

Beams: one additive emissive cone per spot light, apex exactly at the lamp,
axis along the lamp direction, length up to the first surface hit (the runway),
opening angle = the spot cone. Bright at the source, fading to the floor, soft
edges, slow animated noise. The cone is parented to the lamp so it always
follows it: a beam never comes "from nowhere".

Haze: a few large camera-facing planes with drifting noise alpha, additive and
very faint, layered in depth.

Run inside Blender:
    Blender -b scene.blend -P fake_volumetrics.py -- --beams --save
    Blender -b scene.blend -P fake_volumetrics.py -- --beams --prefix spot_ --strength 0.6
    Blender -b scene.blend -P fake_volumetrics.py -- --haze 4 --haze-color 1.0,0.85,0.6 --save
    Blender -b scene.blend -P fake_volumetrics.py -- --remove-volumes --beams --haze 3 --save

Arguments (after --):
    --beams              build beams for spot lights (re-running replaces them)
    --prefix a,b         only spot lights whose object name starts with a prefix
    --strength F         beam emission multiplier (default 0.3; 0.15 subtle, 0.8 strong)
    --max-length M       beam length when nothing is hit below the lamp (default 15)
    --haze N             add N haze planes in front of the active camera (re-running replaces)
    --haze-color r,g,b   haze tint (default warm 1.0,0.82,0.55)
    --haze-strength F    haze emission (default 0.015; keep it barely visible)
    --fixtures           also build a visible lamp housing + glowing lens at each beam apex
    --remove-volumes     unlink world volume and object volume shaders (the slow part)
    --save               save the .blend
"""
import math
import sys

try:
    import bpy
    from mathutils import Vector
except ImportError:
    sys.exit("Run this inside Blender: Blender -b scene.blend -P fake_volumetrics.py -- --beams")

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
BEAM_COLL = "FX_Beams"
HAZE_COLL = "FX_Haze"


def opt(name, default=None, flag=False):
    if name not in ARGS:
        return False if flag else default
    if flag:
        return True
    i = ARGS.index(name)
    if i + 1 >= len(ARGS):
        sys.exit(f"missing value after {name}")
    return ARGS[i + 1]


def fresh_collection(name):
    coll = bpy.data.collections.get(name)
    if coll:
        for o in list(coll.objects):
            bpy.data.objects.remove(o, do_unlink=True)
    else:
        coll = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(coll)
    return coll


def frame_driver(socket, expr):
    fc = socket.driver_add("default_value")
    fc.driver.type = "SCRIPTED"
    fc.driver.expression = expr  # 'frame' is available in driver namespace


def beam_material(color, strength):
    """Additive emission: Transparent + Emission * alpha(length gradient, soft edge, noise)."""
    name = f"FX_Beam_{color[0]:.2f}_{color[1]:.2f}_{color[2]:.2f}_{strength:.2f}"
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    mat = bpy.data.materials.new(name)
    mat.surface_render_method = "BLENDED"
    mat.use_backface_culling = False
    mat.use_transparency_overlap = True
    nt = mat.node_tree
    nt.nodes.clear()
    N, L = nt.nodes, nt.links
    out = N.new("ShaderNodeOutputMaterial")
    add = N.new("ShaderNodeAddShader")
    tr = N.new("ShaderNodeBsdfTransparent")
    em = N.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*color, 1)
    # length gradient: object coords, cone apex at origin, length 1 along -Z (scaled on object)
    # 1 at the lamp -> 0 at the floor, so the cone never draws a hard ellipse on the ground
    tc = N.new("ShaderNodeTexCoord")
    sep = N.new("ShaderNodeSeparateXYZ")
    L.new(tc.outputs["Object"], sep.inputs[0])
    grad = N.new("ShaderNodeMapRange")          # z: 0 (lamp) -> -1 (floor) => 1 -> 0.15
    grad.inputs["From Min"].default_value = 0.0
    grad.inputs["From Max"].default_value = -1.0
    grad.inputs["To Min"].default_value = 1.0
    grad.inputs["To Max"].default_value = 0.0
    L.new(sep.outputs["Z"], grad.inputs["Value"])
    # soft edges: facing ratio, centre of the cone denser than the rim
    lw = N.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.5
    edge = N.new("ShaderNodeMath"); edge.operation = "SUBTRACT"
    edge.inputs[0].default_value = 1.0
    L.new(lw.outputs["Facing"], edge.inputs[1])
    edge2 = N.new("ShaderNodeMath"); edge2.operation = "POWER"
    edge2.inputs[1].default_value = 3.0
    L.new(edge.outputs[0], edge2.inputs[0])
    # drifting dust/haze noise
    noise = N.new("ShaderNodeTexNoise"); noise.noise_dimensions = "4D"
    noise.inputs["Scale"].default_value = 3.0
    noise.inputs["Detail"].default_value = 2.0
    L.new(tc.outputs["Object"], noise.inputs["Vector"])
    frame_driver(noise.inputs["W"], "frame*0.01")
    nmap = N.new("ShaderNodeMapRange")
    nmap.inputs["To Min"].default_value = 0.6
    nmap.inputs["To Max"].default_value = 1.2
    L.new(noise.outputs["Fac"], nmap.inputs["Value"])
    m1 = N.new("ShaderNodeMath"); m1.operation = "MULTIPLY"
    m2 = N.new("ShaderNodeMath"); m2.operation = "MULTIPLY"
    m3 = N.new("ShaderNodeMath"); m3.operation = "MULTIPLY"
    m3.inputs[1].default_value = strength
    L.new(grad.outputs[0], m1.inputs[0]); L.new(edge2.outputs[0], m1.inputs[1])
    L.new(m1.outputs[0], m2.inputs[0]); L.new(nmap.outputs[0], m2.inputs[1])
    L.new(m2.outputs[0], m3.inputs[0])
    L.new(m3.outputs[0], em.inputs["Strength"])
    L.new(tr.outputs[0], add.inputs[0]); L.new(em.outputs[0], add.inputs[1])
    L.new(add.outputs[0], out.inputs["Surface"])
    return mat


def cone_mesh(name, radius, verts=48):
    """Open cone, apex at origin, base circle at z=-1, given base radius (unit length)."""
    me = bpy.data.meshes.new(name)
    co = [(0.0, 0.0, 0.0)] + [(radius * math.cos(2 * math.pi * i / verts),
                                radius * math.sin(2 * math.pi * i / verts), -1.0) for i in range(verts)]
    faces = [(0, 1 + i, 1 + (i + 1) % verts) for i in range(verts)]
    me.from_pydata(co, [], faces)
    me.shade_smooth()
    return me


def fixture_materials():
    body = bpy.data.materials.get("FX_FixtureBody") or bpy.data.materials.new("FX_FixtureBody")
    bsdf = body.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.02, 0.02, 0.02, 1)
        bsdf.inputs["Metallic"].default_value = 0.8
        bsdf.inputs["Roughness"].default_value = 0.35
    lens = bpy.data.materials.get("FX_FixtureLens") or bpy.data.materials.new("FX_FixtureLens")
    lb = lens.node_tree.nodes.get("Principled BSDF")
    if lb:
        lb.inputs["Emission Color"].default_value = (1.0, 0.92, 0.8, 1)
        lb.inputs["Emission Strength"].default_value = 25.0
    return body, lens


def build_fixture(lamp, coll):
    """Black can with a glowing lens, centred on the lamp, pointing where it shines."""
    body_mat, lens_mat = fixture_materials()
    r, depth = 0.16, 0.38
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, vertices=32)
    can = bpy.context.object
    bpy.ops.mesh.primitive_circle_add(radius=r * 0.82, vertices=32, fill_type="NGON")
    lensobj = bpy.context.object
    for o, mat, z in ((can, body_mat, depth / 2 - 0.02), (lensobj, lens_mat, -0.025)):
        for c in o.users_collection:
            c.objects.unlink(o)
        coll.objects.link(o)
        o.data.materials.append(mat)
        o.parent = lamp
        o.matrix_parent_inverse.identity()
        o.location = (0, 0, z)       # can sits just behind the lamp, lens faces down -Z
        o.rotation_euler = (0, 0, 0)
        o.visible_shadow = False
    lensobj.rotation_euler = (math.pi, 0, 0)  # normal towards -Z (towards the stage)
    can.name, lensobj.name = f"FX_fixture_{lamp.name}", f"FX_lens_{lamp.name}"


def build_beams(prefixes, strength, max_len, fixtures=False):
    scene = bpy.context.scene
    coll = fresh_collection(BEAM_COLL)
    deps = bpy.context.evaluated_depsgraph_get()
    count = 0
    for lamp in [o for o in scene.objects if o.type == "LIGHT" and o.data.type == "SPOT"]:
        if prefixes and not any(lamp.name.startswith(p) for p in prefixes):
            continue
        origin = lamp.matrix_world.translation.copy()
        direction = (lamp.matrix_world.to_3x3() @ Vector((0, 0, -1))).normalized()
        hit, loc, *_ = scene.ray_cast(deps, origin + direction * 0.05, direction, distance=max_len)
        length = (loc - origin).length if hit else max_len
        half = lamp.data.spot_size / 2
        radius = math.tan(half)  # for unit length
        obj = bpy.data.objects.new(f"FX_beam_{lamp.name}", cone_mesh(f"FX_beam_{lamp.name}", radius))
        coll.objects.link(obj)
        obj.parent = lamp
        obj.matrix_parent_inverse.identity()
        obj.location = (0, 0, 0)
        obj.rotation_euler = (0, 0, 0)
        obj.scale = (length, length, length)
        obj.visible_shadow = False
        c = lamp.data.color
        obj.data.materials.append(beam_material((c[0], c[1], c[2]), strength))
        if fixtures:
            build_fixture(lamp, coll)
        count += 1
    print(f"[fake-volumetrics] {count} beams built in collection {BEAM_COLL}")


def haze_material(color, strength):
    mat = bpy.data.materials.new("FX_Haze")
    mat.surface_render_method = "BLENDED"
    nt = mat.node_tree
    nt.nodes.clear()
    N, L = nt.nodes, nt.links
    out = N.new("ShaderNodeOutputMaterial")
    add = N.new("ShaderNodeAddShader")
    tr = N.new("ShaderNodeBsdfTransparent")
    em = N.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*color, 1)
    tc = N.new("ShaderNodeTexCoord")
    noise = N.new("ShaderNodeTexNoise"); noise.noise_dimensions = "4D"
    noise.inputs["Scale"].default_value = 1.5
    noise.inputs["Detail"].default_value = 3.0
    L.new(tc.outputs["Generated"], noise.inputs["Vector"])
    frame_driver(noise.inputs["W"], "frame*0.004")
    ramp = N.new("ShaderNodeMapRange")
    ramp.inputs["From Min"].default_value = 0.45
    ramp.inputs["From Max"].default_value = 0.8
    # soft fade towards plane borders so no edge is ever visible
    grad = N.new("ShaderNodeTexGradient"); grad.gradient_type = "SPHERICAL"
    mapg = N.new("ShaderNodeMapping")
    mapg.inputs["Location"].default_value = (-0.5, -0.5, 0)  # centre generated coords
    L.new(tc.outputs["Generated"], mapg.inputs["Vector"])
    L.new(mapg.outputs[0], grad.inputs["Vector"])
    L.new(noise.outputs["Fac"], ramp.inputs["Value"])
    m1 = N.new("ShaderNodeMath"); m1.operation = "MULTIPLY"
    m2 = N.new("ShaderNodeMath"); m2.operation = "MULTIPLY"
    m2.inputs[1].default_value = strength
    L.new(ramp.outputs[0], m1.inputs[0]); L.new(grad.outputs["Fac"], m1.inputs[1])
    L.new(m1.outputs[0], m2.inputs[0])
    L.new(m2.outputs[0], em.inputs["Strength"])
    L.new(tr.outputs[0], add.inputs[0]); L.new(em.outputs[0], add.inputs[1])
    L.new(add.outputs[0], out.inputs["Surface"])
    return mat


def build_haze(n, color, strength):
    scene = bpy.context.scene
    cam = scene.camera
    if not cam:
        print("[fake-volumetrics] no active camera, haze skipped")
        return
    coll = fresh_collection(HAZE_COLL)
    mat = haze_material(color, strength)
    for i in range(n):
        dist = 4 + i * 4
        bpy.ops.mesh.primitive_plane_add(size=1)
        p = bpy.context.object
        for c in p.users_collection:
            c.objects.unlink(p)
        coll.objects.link(p)
        p.name = f"FX_haze_{i}"
        p.data.materials.append(mat)
        p.visible_shadow = False
        p.parent = cam
        p.matrix_parent_inverse.identity()
        p.location = (0.3 * (i % 2 - 0.5), 0, -dist)
        size = dist * 1.6
        p.scale = (size * 2.4, size, 1)
        p.rotation_euler = (0, 0, 0.3 * i)
    print(f"[fake-volumetrics] {n} haze planes parented to camera {cam.name}")


def remove_volumes():
    removed = 0
    for mat in bpy.data.materials:
        if not mat.node_tree:
            continue
        for node in mat.node_tree.nodes:
            if node.type == "OUTPUT_MATERIAL" and node.inputs["Volume"].is_linked:
                for link in list(node.inputs["Volume"].links):
                    mat.node_tree.links.remove(link)
                    removed += 1
    for world in bpy.data.worlds:
        if world.node_tree:
            for node in world.node_tree.nodes:
                if node.type == "OUTPUT_WORLD" and node.inputs["Volume"].is_linked:
                    for link in list(node.inputs["Volume"].links):
                        world.node_tree.links.remove(link)
                        removed += 1
    print(f"[fake-volumetrics] removed {removed} volume links")


def main():
    try:
        strength = float(opt("--strength", 0.3))
        max_len = float(opt("--max-length", 15))
        haze_n = int(opt("--haze", 0))
        haze_color = tuple(float(v) for v in opt("--haze-color", "1.0,0.82,0.55").split(","))
        haze_strength = float(opt("--haze-strength", 0.015))
    except ValueError as err:
        print(f"bad argument: {err}")
        sys.exit(1)
    prefixes = [p for p in (opt("--prefix", "") or "").split(",") if p]
    if opt("--remove-volumes", flag=True):
        remove_volumes()
    if opt("--beams", flag=True):
        build_beams(prefixes, strength, max_len, opt("--fixtures", flag=True))
    if haze_n > 0:
        build_haze(haze_n, haze_color, haze_strength)
    if opt("--save", flag=True) and bpy.data.filepath:
        bpy.ops.wm.save_mainfile()
        print(f"[fake-volumetrics] saved {bpy.data.filepath}")


main()
