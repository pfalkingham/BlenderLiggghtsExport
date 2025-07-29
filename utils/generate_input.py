import os
import bpy
from mathutils import Vector
from .mesh_utils import export_rigid_stls, export_deformable_stls
from .file_writer import write_setup_file, write_run_file

def generate_input_files(context, output_dir, deformable):
    """Generate LIGGGHTS input files for rigid or deformable meshes."""
    scene = context.scene

    # Export moving objects as STL files
    moving_objects = [bpy.data.objects[item.name] for item in scene.liggghts_moving_objects]
    if deformable:
        frame_start = scene.frame_start
        frame_end = scene.frame_end
        export_deformable_stls(output_dir, moving_objects, frame_start, frame_end)
    else:
        export_rigid_stls(output_dir, moving_objects)

    # Export tray as STL
    if scene.liggghts_tray:
        tray_filepath = os.path.join(output_dir, "simtray.stl")
        bpy.ops.object.select_all(action='DESELECT')
        scene.liggghts_tray.select_set(True)
        bpy.context.view_layer.objects.active = scene.liggghts_tray
        bpy.ops.wm.stl_export(filepath=tray_filepath, export_selected_objects=True, ascii_format=True)

    # Calculate frame rate and timesteps per frame
    frame_rate = scene.liggghts_framerate
    frame_duration = 1 / frame_rate
    timesteps_per_frame = int(frame_duration / scene.liggghts_timestep)

    # Set up simulation parameters
    setup_filepath = os.path.join(output_dir, "setup.liggghts")
    run_filepath = os.path.join(output_dir, "run.liggghts")

    simulation_params = {
        "radius": scene.liggghts_radius,
        "timestep": scene.liggghts_timestep,
        "youngs_modulus": scene.liggghts_youngs_modulus,
        "cohesion": scene.liggghts_cohesion,
        "poisson_ratio": scene.liggghts_poisson_ratio,
        "frame_rate": frame_rate,
        "timesteps_per_frame": timesteps_per_frame,
        "deformable": deformable
    }

    # Calculate world-space bounds for simulation and insertion volumes
    def calculate_world_bounds(obj):
        world_coords = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
        min_coords = Vector((min(v.x for v in world_coords), min(v.y for v in world_coords), min(v.z for v in world_coords)))
        max_coords = Vector((max(v.x for v in world_coords), max(v.y for v in world_coords), max(v.z for v in world_coords)))
        return min_coords, max_coords

    sim_min, sim_max = calculate_world_bounds(scene.liggghts_simulation_volume)
    ins_min, ins_max = calculate_world_bounds(scene.liggghts_insertion_volume)

    write_setup_file(setup_filepath, simulation_params, sim_min, sim_max, ins_min, ins_max)
    write_run_file(run_filepath, simulation_params, moving_objects)

class LIGGGHTS_OT_GenerateInput(bpy.types.Operator):
    """Generate LIGGGHTS input files for rigid or deformable meshes"""
    bl_idname = "liggghts.generate_input"
    bl_label = "Generate Input"

    filepath: bpy.props.StringProperty(subtype='DIR_PATH')
    deformable: bpy.props.BoolProperty(default=False)

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        output_dir = bpy.path.abspath(self.filepath)
        generate_input_files(context, output_dir, deformable=self.deformable)
        input_type = "Deformable" if self.deformable else "Rigid"
        self.report({'INFO'}, f"{input_type} input files generated in {output_dir}")
        return {'FINISHED'}

# Register the operator
classes = [LIGGGHTS_OT_GenerateInput]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)