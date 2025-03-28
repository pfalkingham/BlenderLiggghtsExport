import bpy
import os

def export_stl(filepath, objects):
    """Export the given objects as an STL file."""
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        obj.select_set(True)
    bpy.ops.export_mesh.stl(filepath=filepath, use_selection=True)

def export_rigid_stls(output_dir, objects):
    """Export each object as a separate STL file for rigid meshes."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for obj in objects:
        filepath = os.path.join(output_dir, f"{obj.name}.stl")
        export_stl(filepath, [obj])

def export_deformable_stls(output_dir, objects, frame_start, frame_end):
    """Export objects as STL files for each frame in the range for deformable meshes."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for frame in range(frame_start, frame_end + 1):
        bpy.context.scene.frame_set(frame)
        for obj in objects:
            filepath = os.path.join(output_dir, f"{obj.name}_{frame}.stl")
            export_stl(filepath, [obj])