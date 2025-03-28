import bpy
import os
from ..utils.mesh_utils import export_rigid_stls
from ..utils.file_writer import write_setup_file, write_run_file

class LIGGGHTS_OT_GenerateRigidInput(bpy.types.Operator):
    """Generate LIGGGHTS input files for rigid meshes"""
    bl_idname = "liggghts.generate_rigid"
    bl_label = "Generate Rigid Input"

    filepath: bpy.props.StringProperty(subtype='DIR_PATH')

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        scene = context.scene
        output_dir = bpy.path.abspath(self.filepath)

        # Export moving objects as STL files
        moving_objects = [bpy.data.objects[item.name] for item in scene.liggghts_moving_objects]
        export_rigid_stls(output_dir, moving_objects)

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

        sim_min = scene.liggghts_simulation_volume.bound_box[0]
        sim_max = scene.liggghts_simulation_volume.bound_box[6]
        ins_min = scene.liggghts_insertion_volume.bound_box[0]
        ins_max = scene.liggghts_insertion_volume.bound_box[6]

        write_setup_file(setup_filepath, simulation_params, sim_min, sim_max, ins_min, ins_max)
        write_run_file(run_filepath, simulation_params, moving_objects, frame_rate=1, deformable=False)

        self.report({'INFO'}, f"Rigid input files generated in {output_dir}")
        return {'FINISHED'}

# Register the operator
def register():
    bpy.utils.register_class(LIGGGHTS_OT_GenerateRigidInput)

def unregister():
    bpy.utils.unregister_class(LIGGGHTS_OT_GenerateRigidInput)