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

# -- Body / torso (blue shirt) --
torso  = sphere('Torso', (0, 0, 0.95), (0.52, 0.42, 0.60), M_SHIRT)
# Collar peek
collar = sphere('Collar', (0, 0.28, 1.40), (0.22, 0.10, 0.14), M_SHIRT)
parts += [torso, collar]

# -- Suspenders (two black straps over shoulders, front + back) --
# Front straps — longer and lower so they run down under the belly to the pants
susp_FL = box('SuspFL', (-0.20, 0.45, 0.92), (0.05, 0.02, 0.56), M_VEST)
susp_FR = box('SuspFR', ( 0.20, 0.45, 0.92), (0.05, 0.02, 0.56), M_VEST)
# Back straps
susp_BL = box('SuspBL', (-0.20, -0.42, 0.98), (0.05, 0.02, 0.50), M_VEST)
susp_BR = box('SuspBR', ( 0.20, -0.42, 0.98), (0.05, 0.02, 0.50), M_VEST)
# Shoulder crossover pieces
susp_SL = box('SuspSL', (-0.20, 0.0, 1.46), (0.05, 0.42, 0.02), M_VEST)
susp_SR = box('SuspSR', ( 0.20, 0.0, 1.46), (0.05, 0.42, 0.02), M_VEST)
parts += [susp_FL, susp_FR, susp_BL, susp_BR, susp_SL, susp_SR]

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
hair_R     = sphere('HairR',     (-0.56, -0.04, 2.24), (0.26, 0.26, 0.34), M_HAIR)
hair_L     = sphere('HairL',     ( 0.56, -0.04, 2.24), (0.26, 0.26, 0.34), M_HAIR)
hair_back  = sphere('HairBack',  ( 0.00, -0.48, 2.20), (0.44, 0.22, 0.36), M_HAIR)
hair_top   = sphere('HairTop',   ( 0.00, -0.06, 2.56), (0.56, 0.52, 0.20), M_HAIR)  # fuller crown
hair_topF  = sphere('HairTopF',  ( 0.00,  0.18, 2.46), (0.48, 0.30, 0.16), M_HAIR)  # front fringe
hair_crown = sphere('HairCrown', ( 0.00, -0.20, 2.62), (0.40, 0.40, 0.14), M_HAIR)  # back crown
parts += [hair_R, hair_L, hair_back, hair_top, hair_topF, hair_crown]

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
parts += [eye_L, eye_R, shine_L, shine_R]

# -- Glasses (round wire frames — character's signature feature) --
# Two torus lenses, a bridge, and temples. Pushed forward (higher Y) so they
# sit clearly in front of the face instead of clipping into the skin.
gl_L = torus('GlassL', (-0.22, 0.70, 2.16), (math.pi/2, 0, 0), 0.13, 0.022, M_GLASS)
gl_R = torus('GlassR', ( 0.22, 0.70, 2.16), (math.pi/2, 0, 0), 0.13, 0.022, M_GLASS)
bridge   = cylinder('GlassBridge',  (0,    0.72, 2.16), (0.018, 0.018, 0.09), (0, math.pi/2, 0), M_GLASS)
temple_L = cylinder('TempleL', (-0.50, 0.45, 2.16), (0.015, 0.015, 0.24), (0, math.pi/2, 0.32), M_GLASS)
temple_R = cylinder('TempleR', ( 0.50, 0.45, 2.16), (0.015, 0.015, 0.24), (0, math.pi/2,-0.32), M_GLASS)
parts += [gl_L, gl_R, bridge, temple_L, temple_R]

# -- Arms (blue shirt sleeves) --
arm_L     = cylinder('ArmL',     (-0.68, 0.00, 1.18), (0.17, 0.17, 0.40), (0, 0,  0.25), M_SHIRT)
arm_R     = cylinder('ArmR',     ( 0.68, 0.00, 1.18), (0.17, 0.17, 0.40), (0, 0, -0.25), M_SHIRT)
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

# ── Rigid skinning ─────────────────────────────────────────────────────────────
# Each Mii part is a solid prop — bind it 100% to a single bone so nothing
# deforms or bleeds (auto weights were dragging the ears during big arm moves).
def bone_for(nm):
    if nm == 'Neck': return 'Neck'
    if nm == 'ArmL': return 'UpperArmL'
    if nm == 'ArmR': return 'UpperArmR'
    if nm in ('ForearmL', 'HandL', 'ForearmR', 'HandR'): return nm
    if nm == 'LegL': return 'ThighL'
    if nm == 'LegR': return 'ThighR'
    if nm == 'FootL': return 'ShinL'
    if nm == 'FootR': return 'ShinR'
    HEAD_KW = ('Head','Ear','Hair','Beard','Mustache','Nose','Eye','Shine','Glass','Temple','Bridge')
    if any(nm.startswith(k) for k in HEAD_KW): return 'Head'
    return 'Chest'   # torso, collar, shirt, suspenders

for o in parts:
    bn = bone_for(o.name)
    vg = o.vertex_groups.new(name=bn)
    vg.add(list(range(len(o.data.vertices))), 1.0, 'REPLACE')
    m = o.modifiers.new('arm', 'ARMATURE')
    m.object = rig
    o.parent = rig   # rig is at the origin (identity), so no offset correction needed

# ── Animation system ──────────────────────────────────────────────────────────
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode='POSE')
PB = rig.pose.bones
for pb in PB:
    pb.rotation_mode = 'XYZ'

# All bones we touch — reset to rest each frame before posing so leftover
# rotations from one clip never bleed into the next.
POSED = ['Chest','Spine','Head','Neck','Hips',
         'UpperArmL','ForearmL','HandL','UpperArmR','ForearmR','HandR',
         'ThighL','ShinL','ThighR','ShinR']

rig.animation_data_create()

def make_action(name, n_frames, pose_fn):
    """Build a standalone action from a per-frame pose function and stash it
    to its own NLA track so the glTF exporter emits it as a named clip."""
    action = bpy.data.actions.new(name)
    rig.animation_data.action = action
    for f in range(1, n_frames + 1):
        bpy.context.scene.frame_set(f)
        # reset to rest pose
        for n in POSED:
            PB[n].rotation_euler = (0, 0, 0)
            PB[n].location = (0, 0, 0)
        pose_fn(f, n_frames)
        for n in POSED:
            PB[n].keyframe_insert('rotation_euler', frame=f)
            PB[n].keyframe_insert('location', frame=f)
    # stash to NLA + clear active slot for the next action
    track = rig.animation_data.nla_tracks.new()
    track.name = name
    track.strips.new(name, 1, action)
    rig.animation_data.action = None
    return action

TAU = 2 * math.pi

# NOTE: bones point straight up, so in pose-local space the bone's Y axis is
# world "up". Vertical hops/bounces therefore use location.y, NOT location.z.

# ── Idle: breathing, gentle head bob, light arm sway (loops) ──────────────────
def pose_idle(f, N):
    t = (f - 1) / N * TAU
    PB['Chest'].location = (0, math.sin(t) * 0.018, 0)
    PB['Head'].rotation_euler = (math.sin(t*0.5)*0.04, 0, math.sin(t*0.3)*0.05)
    sway = math.sin(t) * 0.04
    PB['UpperArmL'].rotation_euler = (sway, 0, 0)
    PB['UpperArmR'].rotation_euler = (-sway, 0, 0)
    curl = math.sin(t*0.7 + 0.5) * 0.03
    PB['ForearmL'].rotation_euler = (curl, 0, 0)
    PB['ForearmR'].rotation_euler = (-curl, 0, 0)

# ── VICTORY 1: Cheer — arms out in a wide V, waving, gentle bounce ────────────
def pose_cheer(f, N):
    t = (f - 1) / N * TAU
    PB['Hips'].location = (0, abs(math.sin(t * 2)) * 0.06, 0)   # small bounce
    PB['Chest'].rotation_euler = (-0.1, 0, 0)
    PB['Head'].rotation_euler = (-0.15, 0, math.sin(t*3)*0.07)
    # arms held out in a V (~shoulder height), waving side to side
    wave = math.sin(t * 4) * 0.22
    PB['UpperArmL'].rotation_euler = (0, 0,  1.25 + wave)
    PB['UpperArmR'].rotation_euler = (0, 0, -1.25 - wave)
    PB['ForearmL'].rotation_euler = (-0.2, 0, 0)
    PB['ForearmR'].rotation_euler = (-0.2, 0, 0)

# ── VICTORY 2: Jump — real hop with both hands straight overhead ──────────────
def pose_jump(f, N):
    t = (f - 1) / N * TAU
    hop = abs(math.sin(t * 2)) * 0.32          # clear vertical hop (local Y)
    PB['Hips'].location = (0, hop, 0)
    tuck = hop / 0.32
    PB['ThighL'].rotation_euler = (0.3 * tuck, 0, 0)
    PB['ThighR'].rotation_euler = (0.3 * tuck, 0, 0)
    PB['ShinL'].rotation_euler = (-0.4 * tuck, 0, 0)
    PB['ShinR'].rotation_euler = (-0.4 * tuck, 0, 0)
    PB['Chest'].rotation_euler = (-0.08, 0, 0)
    PB['Head'].rotation_euler = (-0.2, 0, 0)
    # arms straight up overhead
    PB['UpperArmL'].rotation_euler = (0, 0,  2.05)
    PB['UpperArmR'].rotation_euler = (0, 0, -2.05)
    PB['ForearmL'].rotation_euler = (-0.12, 0, 0)
    PB['ForearmR'].rotation_euler = (-0.12, 0, 0)

# ── VICTORY 3: Clap — hands meet in front of the chest repeatedly ─────────────
def pose_clap(f, N):
    t = (f - 1) / N * TAU
    clap = (math.sin(t * 5) + 1) / 2   # 0 = apart, 1 = together
    PB['Hips'].location = (0, abs(math.sin(t * 2)) * 0.04, 0)
    PB['Head'].rotation_euler = (-0.06, 0, 0)
    PB['Chest'].rotation_euler = (-0.04, 0, 0)
    # upper arms raised to the side a bit, then forearms swing inward to meet
    PB['UpperArmL'].rotation_euler = (0, 0,  0.85)
    PB['UpperArmR'].rotation_euler = (0, 0, -0.85)
    # forearm X bends them forward so hands sit in FRONT of the body;
    # Z swings them toward the centre to clap.
    PB['ForearmL'].rotation_euler = (-1.3, 0,  0.55 - clap * 0.5)
    PB['ForearmR'].rotation_euler = (-1.3, 0, -0.55 + clap * 0.5)

# ── WRONG 1: Head shake "no" — slump, head turns side to side ─────────────────
def pose_shake(f, N):
    t = (f - 1) / N * TAU
    PB['Chest'].rotation_euler = (0.12, 0, 0)       # slump forward
    PB['Hips'].location = (0, -0.04, 0)
    PB['Head'].rotation_euler = (0.08, 0, math.sin(t * 3) * 0.35)  # shake no
    PB['UpperArmL'].rotation_euler = (0.15, 0, 0)
    PB['UpperArmR'].rotation_euler = (0.15, 0, 0)

# ── WRONG 2: Slump — shoulders drop, head hangs ───────────────────────────────
def pose_slump(f, N):
    t = (f - 1) / N * TAU
    drop = min(1.0, f / (N * 0.4))                  # ease into the slump
    settle = math.sin(t * 1.5) * 0.02
    PB['Chest'].rotation_euler = (0.30 * drop, 0, 0)
    PB['Hips'].location = (0, -0.10 * drop, 0)
    PB['Head'].rotation_euler = (0.45 * drop + settle, 0, 0)
    PB['UpperArmL'].rotation_euler = (0.25 * drop, 0, 0)
    PB['UpperArmR'].rotation_euler = (0.25 * drop, 0, 0)
    PB['ForearmL'].rotation_euler = (0.2 * drop, 0, 0)
    PB['ForearmR'].rotation_euler = (0.2 * drop, 0, 0)

# ── WRONG 3: Shrug — arms out, palms up, head tilt ────────────────────────────
def pose_shrug(f, N):
    t = (f - 1) / N * TAU
    hold = min(1.0, f / (N * 0.35))
    wobble = math.sin(t * 2) * 0.05
    PB['Head'].rotation_euler = (0.05, 0, 0.18 + wobble)
    PB['Chest'].rotation_euler = (0.04, 0, 0)
    # upper arms lift out to the sides a little, forearms rotate palms-up
    PB['UpperArmL'].rotation_euler = (0, 0, -0.6 * hold)
    PB['UpperArmR'].rotation_euler = (0, 0,  0.6 * hold)
    PB['ForearmL'].rotation_euler = (-1.0 * hold, 0, 0)
    PB['ForearmR'].rotation_euler = (-1.0 * hold, 0, 0)

make_action('Idle',    120, pose_idle)
make_action('Cheer',    60, pose_cheer)
make_action('Jump',     60, pose_jump)
make_action('Clap',     60, pose_clap)
make_action('Shake',    60, pose_shake)
make_action('Slump',    70, pose_slump)
make_action('Shrug',    70, pose_shrug)

bpy.ops.object.mode_set(mode='OBJECT')

# ── Export GLB ────────────────────────────────────────────────────────────────
bpy.ops.export_scene.gltf(
    filepath=OUT,
    export_format='GLB',
    export_animations=True,
    export_animation_mode='ACTIONS',
    export_nla_strips=True,
    export_skins=True,
    export_morph=False,
    export_apply=False,
)
print(f'\n✓ Host exported → {OUT}\n')
