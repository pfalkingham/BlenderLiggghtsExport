import bpy

class LIGGGHTS_PT_MainPanel(bpy.types.Panel):
    """Main Panel for LIGGGHTS Addon"""
    bl_label = "LIGGGHTS Input Generator"
    bl_idname = "LIGGGHTS_PT_MainPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'LIGGGHTS'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Moving Objects
        layout.label(text="Select Moving Objects:")
        layout.template_list("UI_UL_list", "moving_objects", scene, "liggghts_moving_objects", scene, "liggghts_moving_objects_index")
        row = layout.row()
        row.operator("liggghts.add_moving_object", text="Add Selected")
        row.operator("liggghts.remove_moving_object", text="Remove Selected")

        # Tray
        layout.label(text="Select Tray:")
        row = layout.row()
        row.prop(scene, "liggghts_tray", text="")
        row.operator("liggghts.set_tray", text="Set Tray")

        # Insertion Volume
        layout.label(text="Select Insertion Volume:")
        row = layout.row()
        row.prop(scene, "liggghts_insertion_volume", text="")
        row.operator("liggghts.set_insertion_volume", text="Set Insertion Volume")

        # Simulation Volume
        layout.label(text="Select Simulation Volume:")
        row = layout.row()
        row.prop(scene, "liggghts_simulation_volume", text="")
        row.operator("liggghts.set_simulation_volume", text="Set Simulation Volume")

        # Parameters
        layout.label(text="Parameters:")
        layout.prop(scene, "liggghts_radius", text="Radius")
        layout.prop(scene, "liggghts_timestep", text="Timestep")
        layout.prop(scene, "liggghts_youngs_modulus", text="Young's Modulus")
        layout.prop(scene, "liggghts_cohesion", text="Cohesion")
        layout.prop(scene, "liggghts_poisson_ratio", text="Poisson Ratio")

        # Generate Buttons
        layout.label(text="Generate LIGGGHTS Input Files:")
        layout.operator("liggghts.generate_deformable", text="Deformable Mesh")
        layout.operator("liggghts.generate_rigid", text="Rigid Mesh")

# Register the panel
def register():
    bpy.utils.register_class(LIGGGHTS_PT_MainPanel)

def unregister():
    bpy.utils.unregister_class(LIGGGHTS_PT_MainPanel)

if __name__ == "__main__":
    register()