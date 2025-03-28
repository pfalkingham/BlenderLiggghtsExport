import bpy
import os
from mathutils import Vector
from ..utils.mesh_utils import export_deformable_stls
from ..utils.file_writer import write_setup_file, write_run_file

class LIGGGHTS_OT_GenerateDeformableInput(bpy.types.Operator):
    """Generate LIGGGHTS input files for deformable meshes"""
    bl_idname = "liggghts.generate_deformable"
    bl_label = "Generate Deformable Input"

    filepath: bpy.props.StringProperty(subtype='DIR_PATH')

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        scene = context.scene
        output_dir = bpy.path.abspath(self.filepath)

        # Export moving objects as STL files for each frame
        moving_objects = [bpy.data.objects[item.name] for item in scene.liggghts_moving_objects]
        frame_start = scene.frame_start
        frame_end = scene.frame_end
        export_deformable_stls(output_dir, moving_objects, frame_start, frame_end)

        # Export tray as STL
        if scene.liggghts_tray:
            tray_filepath = os.path.join(output_dir, "simtray.stl")
            bpy.ops.object.select_all(action='DESELECT')
            scene.liggghts_tray.select_set(True)
            bpy.context.view_layer.objects.active = scene.liggghts_tray
            bpy.ops.wm.stl_export(filepath=tray_filepath, export_selected_objects=True)

        # Generate setup.liggghts and run.liggghts files
        setup_filepath = os.path.join(output_dir, "setup.liggghts")
        run_filepath = os.path.join(output_dir, "run.liggghts")

        simulation_params = {
            "radius": scene.liggghts_radius,
            "timestep": scene.liggghts_timestep,
            "youngs_modulus": scene.liggghts_youngs_modulus,
            "cohesion": scene.liggghts_cohesion,
            "poisson_ratio": scene.liggghts_poisson_ratio
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

        # Calculate timesteps per frame
        frame_rate = scene.liggghts_framerate  # Use the framerate from the UI
        frame_duration = 1 / frame_rate
        timesteps_per_frame = int(frame_duration / scene.liggghts_timestep)

        # Pass timesteps_per_frame to write_run_file
        write_run_file(run_filepath, simulation_params, moving_objects, frame_rate=frame_rate, deformable=True, timesteps_per_frame=timesteps_per_frame)

        self.report({'INFO'}, f"Deformable input files generated in {output_dir}")
        return {'FINISHED'}

# Register the operator
def register():
    bpy.utils.register_class(LIGGGHTS_OT_GenerateDeformableInput)

def unregister():
    bpy.utils.unregister_class(LIGGGHTS_OT_GenerateDeformableInput)