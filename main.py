import bpy
import random

def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def setup_render():
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.render.resolution_x = 3840
    scene.render.resolution_y = 2160
    scene.frame_start = 1
    scene.frame_end = 240

def setup_world():
    world = bpy.data.worlds.new("CyberWorld")
    bpy.context.scene.world = world
    world.use_nodes = True

    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = (0.02,0.02,0.05,1)
        bg.inputs[1].default_value = 0.4

def create_road():
    bpy.ops.mesh.primitive_plane_add(size=60, location=(0,0,0))
    road = bpy.context.active_object

    mat = bpy.data.materials.new("Road")
    mat.use_nodes = True

    for n in mat.node_tree.nodes:
        if n.type == "BSDF_PRINCIPLED":
            n.inputs["Roughness"].default_value = 0.15
            n.inputs["Specular IOR Level"].default_value = 0.9

    road.data.materials.append(mat)

def create_buildings():
    for i in range(-8,9):
        for side in [-1,1]:
            bpy.ops.mesh.primitive_cube_add(size=2, location=(i*3, side*8, 2))
            b = bpy.context.active_object
            b.scale[2] = random.uniform(3,7)

def create_neon():
    def neon(x,y,z,color):
        bpy.ops.object.light_add(type='POINT', location=(x,y,z))
        l = bpy.context.active_object
        l.data.energy = 300
        l.data.color = color

    for i in range(-10,11,2):
        neon(i,5,3,(0,1,1))
        neon(i,-5,3,(1,0,1))

def create_robot():
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.7, location=(-12,0,1))
    robot = bpy.context.active_object
    robot.name = "Robot"

    robot.keyframe_insert(data_path="location", frame=1)
    robot.location.x = 12
    robot.keyframe_insert(data_path="location", frame=240)
    return robot

def setup_camera(robot):
    bpy.ops.object.camera_add(location=(-15,-6,3))
    cam = bpy.context.active_object
    bpy.context.scene.camera = cam

    track = cam.constraints.new(type='TRACK_TO')
    track.target = robot
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'

    cam.keyframe_insert(data_path="location", frame=1)
    cam.location.x = 10
    cam.keyframe_insert(data_path="location", frame=240)

def main():
    reset_scene()
    setup_render()
    setup_world()
    create_road()
    create_buildings()
    create_neon()
    robot = create_robot()
    setup_camera(robot)

    print("Cyberpunk cinematic scene ready")

if __name__ == "__main__":
    main()
