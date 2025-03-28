import bpy
import os
from ..utils.mesh_utils import export_rigid_stls

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

        # Generate setup.liggghts file
        setup_filepath = os.path.join(output_dir, "setup.liggghts")
        with open(setup_filepath, "w") as setup_file:
            setup_file.write("# LIGGGHTS setup script\n")
            setup_file.write(f"# Simulation volume: {scene.liggghts_simulation_volume.name}\n")
            setup_file.write(f"# Tray: {scene.liggghts_tray.name}\n")
            setup_file.write(f"# Insertion volume: {scene.liggghts_insertion_volume.name}\n")
            setup_file.write(f"# Radius: {scene.liggghts_radius}\n")
            setup_file.write(f"# Timestep: {scene.liggghts_timestep}\n")
            setup_file.write(f"# Young's Modulus: {scene.liggghts_youngs_modulus}\n")
            setup_file.write(f"# Cohesion: {scene.liggghts_cohesion}\n")
            setup_file.write(f"# Poisson Ratio: {scene.liggghts_poisson_ratio}\n")

        self.report({'INFO'}, f"Rigid input files generated in {output_dir}")
        return {'FINISHED'}

# Register the operator
def register():
    bpy.utils.register_class(LIGGGHTS_OT_GenerateRigidInput)

def unregister():
    bpy.utils.unregister_class(LIGGGHTS_OT_GenerateRigidInput)