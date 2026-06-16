"""
Camp Koronis Jeopardy Host — Mii-style character
Run from: blender --background --python build_host.py
Output:   jeopardy/host.glb
"""
import bpy, math, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'host.glb')

# ── Reset ──────────────────────────────────────────────────────────────────────
bpy.ops.wm.read_factory_settings(use_empty=True)
S = bpy.context.scene
S.frame_start, S.frame_end = 1, 120
S.render.fps = 30

# ── Materials ──────────────────────────────────────────────────────────────────
def mat(name, r, g, b, roughness=0.85, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    pb = m.node_tree.nodes['Principled BSDF']
    pb.inputs['Base Color'].default_value    = (r, g, b, 1)
    pb.inputs['Roughness'].default_value     = roughness
    pb.inputs['Metallic'].default_value      = metallic
    return m

M_SKIN    = mat('Skin',    0.92, 0.74, 0.58)
M_HAIR    = mat('Hair',    0.88, 0.86, 0.84)   # silver-white
M_BEARD   = mat('Beard',   0.93, 0.91, 0.89)   # slightly brighter white
M_EYE     = mat('Eye',     0.08, 0.06, 0.05)
M_GLASS   = mat('Glass',   0.12, 0.12, 0.15, roughness=0.15, metallic=0.7)
M_VEST    = mat('Vest',    0.07, 0.07, 0.09)
M_SHIRT   = mat('Shirt',   0.22, 0.44, 0.78)
M_BLUSH   = mat('Blush',   0.96, 0.78, 0.70)
M_MOUTH   = mat('Mouth',   0.55, 0.22, 0.22)
M_WHITE   = mat('White',   0.95, 0.95, 0.95)

# ── Helpers ────────────────────────────────────────────────────────────────────
def sphere(name, loc, scale, mat_obj):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = scale
    o.data.materials.append(mat_obj)
    bpy.ops.object.shade_smooth()
    return o

def cylinder(name, loc, scale, rot, mat_obj, verts=16):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, location=loc, rotation=rot)
    o = bpy.context.active_object
    o.name = name
    o.scale = scale
    o.data.materials.append(mat_obj)
    bpy.ops.object.shade_smooth()
    return o

def torus(name, loc, rot, major_r, minor_r, mat_obj):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major_r, minor_radius=minor_r,
        major_segments=32, minor_segments=12,
        location=loc, rotation=rot)
    o = bpy.context.active_object
    o.name = name
    o.data.materials.append(mat_obj)
    bpy.ops.object.shade_smooth()
    return o

def box(name, loc, scale, mat_obj):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = scale
    o.data.materials.append(mat_obj)
    return o

# ── Character geometry ─────────────────────────────────────────────────────────
# All Y-up, character faces +Y direction.
# Root sits at world origin (0,0,0), feet near Z=0.

parts = []

# -- Legs (stubby Mii legs) --
leg_L  = cylinder('LegL',  (-0.18, 0,  0.38), (0.15, 0.15, 0.38), (0,0,0), M_VEST)
leg_R  = cylinder('LegR',  ( 0.18, 0,  0.38), (0.15, 0.15, 0.38), (0,0,0), M_VEST)
foot_L = sphere('FootL', (-0.18, 0.08, 0.06), (0.16, 0.22, 0.10), M_VEST)
foot_R = sphere('FootR', ( 0.18, 0.08, 0.06), (0.16, 0.22, 0.10), M_VEST)
parts += [leg_L, leg_R, foot_L, foot_R]

# -- Body / torso --
torso  = sphere('Torso', (0, 0, 0.95), (0.52, 0.42, 0.60), M_VEST)
# Shirt peek at collar
shirt  = sphere('Shirt', (0, 0.28, 1.30), (0.24, 0.10, 0.18), M_SHIRT)
parts += [torso, shirt]

# -- Neck --
neck = cylinder('Neck', (0, 0, 1.56), (0.16, 0.16, 0.14), (0,0,0), M_SKIN)
parts.append(neck)

# -- Head (big, round, Mii-style — slightly wider than tall) --
head = sphere('Head', (0, 0, 2.06), (0.68, 0.63, 0.65), M_SKIN)
parts.append(head)

# -- Ears --
ear_L = sphere('EarL', (-0.65, 0.02, 2.06), (0.12, 0.09, 0.14), M_SKIN)
ear_R = sphere('EarR', ( 0.65, 0.02, 2.06), (0.12, 0.09, 0.14), M_SKIN)
parts += [ear_L, ear_R]

# -- Hair: thin on top, full on sides & back (gray-white) --
hair_R    = sphere('HairR',    (-0.56, -0.04, 2.22), (0.24, 0.24, 0.30), M_HAIR)
hair_L    = sphere('HairL',    ( 0.56, -0.04, 2.22), (0.24, 0.24, 0.30), M_HAIR)
hair_back = sphere('HairBack', ( 0.00, -0.48, 2.18), (0.40, 0.20, 0.32), M_HAIR)
hair_top  = sphere('HairTop',  ( 0.00, -0.08, 2.60), (0.44, 0.40, 0.10), M_HAIR)  # thin wisp on top
parts += [hair_R, hair_L, hair_back, hair_top]

# -- Beard (big fluffy white) --
beard_main  = sphere('BeardMain',  ( 0.00,  0.26, 1.80), (0.50, 0.28, 0.42), M_BEARD)
beard_chin  = sphere('BeardChin',  ( 0.00,  0.38, 1.64), (0.36, 0.25, 0.30), M_BEARD)
beard_L     = sphere('BeardL',     (-0.30,  0.20, 1.85), (0.24, 0.20, 0.28), M_BEARD)
beard_R     = sphere('BeardR',     ( 0.30,  0.20, 1.85), (0.24, 0.20, 0.28), M_BEARD)
mustache    = sphere('Mustache',   ( 0.00,  0.38, 1.94), (0.30, 0.16, 0.12), M_BEARD)
parts += [beard_main, beard_chin, beard_L, beard_R, mustache]

# -- Nose --
nose = sphere('Nose', (0, 0.60, 2.00), (0.12, 0.10, 0.10), M_BLUSH)
parts.append(nose)

# -- Eyes (dark circles, Mii-style) --
eye_L = sphere('EyeL', (-0.22, 0.56, 2.16), (0.09, 0.07, 0.09), M_EYE)
eye_R = sphere('EyeR', ( 0.22, 0.56, 2.16), (0.09, 0.07, 0.09), M_EYE)
# Eye shine
shine_L = sphere('ShineL', (-0.19, 0.60, 2.19), (0.03, 0.03, 0.03), M_WHITE)
shine_R = sphere('ShineR', ( 0.19, 0.60, 2.19), (0.03, 0.03, 0.03), M_WHITE)
# Cheek blush
cheek_L = sphere('CheekL', (-0.40, 0.50, 2.02), (0.18, 0.10, 0.06), M_BLUSH)
cheek_R = sphere('CheekR', ( 0.40, 0.50, 2.02), (0.18, 0.10, 0.06), M_BLUSH)
parts += [eye_L, eye_R, shine_L, shine_R, cheek_L, cheek_R]

# -- Glasses (round wire frames — character's signature feature) --
# Two torus lenses, a bridge, and temples
gl_L = torus('GlassL', (-0.22, 0.57, 2.16), (math.pi/2, 0, 0), 0.13, 0.022, M_GLASS)
gl_R = torus('GlassR', ( 0.22, 0.57, 2.16), (math.pi/2, 0, 0), 0.13, 0.022, M_GLASS)
bridge   = cylinder('GlassBridge',  (0,    0.59, 2.16), (0.018, 0.018, 0.09), (0, math.pi/2, 0), M_GLASS)
temple_L = cylinder('TempleL', (-0.48, 0.40, 2.16), (0.015, 0.015, 0.20), (0, math.pi/2, 0.28), M_GLASS)
temple_R = cylinder('TempleR', ( 0.48, 0.40, 2.16), (0.015, 0.015, 0.20), (0, math.pi/2,-0.28), M_GLASS)
parts += [gl_L, gl_R, bridge, temple_L, temple_R]

# -- Arms --
arm_L     = cylinder('ArmL',     (-0.68, 0.00, 1.18), (0.17, 0.17, 0.40), (0, 0,  0.25), M_VEST)
arm_R     = cylinder('ArmR',     ( 0.68, 0.00, 1.18), (0.17, 0.17, 0.40), (0, 0, -0.25), M_VEST)
forearm_L = cylinder('ForearmL', (-0.84, 0.04, 0.72), (0.14, 0.14, 0.34), (0, 0.18, 0.12), M_SHIRT)
forearm_R = cylinder('ForearmR', ( 0.84, 0.04, 0.72), (0.14, 0.14, 0.34), (0,-0.18,-0.12), M_SHIRT)
hand_L    = sphere('HandL', (-0.96, 0.08, 0.40), (0.18, 0.16, 0.20), M_SKIN)
hand_R    = sphere('HandR', ( 0.96, 0.08, 0.40), (0.18, 0.16, 0.20), M_SKIN)
parts += [arm_L, arm_R, forearm_L, forearm_R, hand_L, hand_R]

# ── Armature ───────────────────────────────────────────────────────────────────
bpy.ops.object.armature_add(location=(0, 0, 0))
rig = bpy.context.active_object
rig.name = 'HostRig'
rig.show_in_front = True

bpy.ops.object.mode_set(mode='EDIT')
eb = rig.data.edit_bones

def bone(name, head, tail, parent=None):
    b = eb.new(name)
    b.head = head; b.tail = tail
    if parent: b.parent = eb[parent]
    return b

bone('Root',      (0,0,0),       (0,0,0.4))
bone('Hips',      (0,0,0.75),    (0,0,1.0),   'Root')
bone('Spine',     (0,0,1.0),     (0,0,1.4),   'Hips')
bone('Chest',     (0,0,1.4),     (0,0,1.65),  'Spine')
bone('Neck',      (0,0,1.65),    (0,0,1.88),  'Chest')
bone('Head',      (0,0,1.88),    (0,0,2.55),  'Neck')

bone('ShoulderL', (-0.10,0,1.55),(-0.52,0,1.48), 'Chest')
bone('UpperArmL', (-0.52,0,1.48),(-0.80,0,1.00), 'ShoulderL')
bone('ForearmL',  (-0.80,0,1.00),(-0.96,0,0.55), 'UpperArmL')
bone('HandL',     (-0.96,0,0.55),(-1.06,0,0.30), 'ForearmL')

bone('ShoulderR', ( 0.10,0,1.55),( 0.52,0,1.48), 'Chest')
bone('UpperArmR', ( 0.52,0,1.48),( 0.80,0,1.00), 'ShoulderR')
bone('ForearmR',  ( 0.80,0,1.00),( 0.96,0,0.55), 'UpperArmR')
bone('HandR',     ( 0.96,0,0.55),( 1.06,0,0.30), 'ForearmR')

bone('ThighL',    (-0.18,0,0.75),(-0.18,0,0.40), 'Hips')
bone('ShinL',     (-0.18,0,0.40),(-0.18,0,0.06), 'ThighL')
bone('ThighR',    ( 0.18,0,0.75),( 0.18,0,0.40), 'Hips')
bone('ShinR',     ( 0.18,0,0.40),( 0.18,0,0.06), 'ThighR')

bpy.ops.object.mode_set(mode='OBJECT')

# ── Parent all meshes to rig ───────────────────────────────────────────────────
for o in parts:
    o.select_set(True)
rig.select_set(True)
bpy.context.view_layer.objects.active = rig
bpy.ops.object.parent_set(type='ARMATURE_AUTO')

# ── Idle animation (120f = 4s loop at 30fps) ──────────────────────────────────
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode='POSE')
PB = rig.pose.bones
for pb in PB:
    pb.rotation_mode = 'XYZ'

FRAMES = 120
for f in range(1, FRAMES + 1):
    bpy.context.scene.frame_set(f)
    t = (f - 1) / FRAMES * 2 * math.pi

    # Breathing — gentle chest rise
    PB['Chest'].location = (0, 0, math.sin(t) * 0.018)
    PB['Chest'].keyframe_insert('location', frame=f)

    # Head bob + slight look-around
    PB['Head'].rotation_euler = (
        math.sin(t * 0.5) * 0.04,       # slow nod
        0,
        math.sin(t * 0.3) * 0.05        # gentle side turn
    )
    PB['Head'].keyframe_insert('rotation_euler', frame=f)

    # Arms sway gently (idle hang)
    sway = math.sin(t) * 0.04
    PB['UpperArmL'].rotation_euler = (sway, 0, 0)
    PB['UpperArmR'].rotation_euler = (-sway, 0, 0)
    PB['UpperArmL'].keyframe_insert('rotation_euler', frame=f)
    PB['UpperArmR'].keyframe_insert('rotation_euler', frame=f)

    # Forearm slight idle curl
    curl = math.sin(t * 0.7 + 0.5) * 0.03
    PB['ForearmL'].rotation_euler = (curl, 0, 0)
    PB['ForearmR'].rotation_euler = (-curl, 0, 0)
    PB['ForearmL'].keyframe_insert('rotation_euler', frame=f)
    PB['ForearmR'].keyframe_insert('rotation_euler', frame=f)

bpy.ops.object.mode_set(mode='OBJECT')
if rig.animation_data and rig.animation_data.action:
    rig.animation_data.action.name = 'Idle'

# ── Wave animation (frames 121–180) ───────────────────────────────────────────
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode='POSE')
S.frame_end = 180

for f in range(121, 181):
    bpy.context.scene.frame_set(f)
    t = (f - 121) / 60 * 2 * math.pi

    # Right arm raises and waves
    PB['UpperArmR'].rotation_euler = (-0.9, 0, -0.3)
    PB['ForearmR'].rotation_euler  = (-0.3 + math.sin(t * 2) * 0.4, 0, 0)
    PB['Head'].rotation_euler      = (0.05, 0, -0.12)  # looks toward raised arm

    PB['UpperArmR'].keyframe_insert('rotation_euler', frame=f)
    PB['ForearmR'].keyframe_insert('rotation_euler', frame=f)
    PB['Head'].keyframe_insert('rotation_euler', frame=f)

    # Left arm stays down
    PB['UpperArmL'].rotation_euler = (0, 0, 0)
    PB['UpperArmL'].keyframe_insert('rotation_euler', frame=f)

bpy.ops.object.mode_set(mode='OBJECT')

# ── Export GLB ────────────────────────────────────────────────────────────────
bpy.ops.export_scene.gltf(
    filepath=OUT,
    export_format='GLB',
    export_animations=True,
    export_skins=True,
    export_morph=False,
    export_apply=False,
)
print(f'\n✓ Host exported → {OUT}\n')
