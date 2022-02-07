from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rv2.rhino import get_scene
from compas_rv2.rhino import get_proxy
from compas.geometry import add_vectors, scale_vector
from compas_rv2.rhino import rv2_undo
from compas_rv2.rhino import rv2_error

from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist

__commandname__ = "RV2materialisation"


def subdivide_dual(mesh):
    dual = mesh.dual()
    return dual


def draw_orientation(mesh):
    artist = MeshArtist(mesh, layer="RV2::Normals")
    artist.clear_layer()
    artist.draw_edges()
    artist.draw_vertexnormals(scale=1)


def offsets(mesh):
    idos = mesh.copy()
    edos = mesh.copy()

    for vertex in mesh.vertices():
        point = mesh.vertex_coordinates(vertex)
        normal = mesh.vertex_normal(vertex)
        thickness = 0.10
        idos.vertex_attributes(vertex, 'xyz', add_vectors(point, scale_vector(normal, +0.5 * thickness)))
        edos.vertex_attributes(vertex, 'xyz', add_vectors(point, scale_vector(normal, -0.5 * thickness)))
    return idos, edos


def draw_offsets(idos, edos):
    artist = MeshArtist(None)

    artist.mesh = idos
    artist.layer = "RV2::Idos"
    artist.clear_layer()
    artist.draw_faces(color=(255, 0, 0))

    artist.mesh = edos
    artist.layer = "RV2::Edos"
    artist.clear_layer()
    artist.draw_faces(color=(0, 0, 255))


def materialisation_blocks(idos, edos):
    blocks = []

    for face in idos.faces():
        bottom = idos.face_coordinates(face)
        top = edos.face_coordinates(face)

        f = len(bottom)

        faces = [
            list(range(f)),
            list(range(f + f - 1, f - 1, -1))]

        for i in range(f - 1):
            faces.append([i, i + f, i + f + 1, i + 1])
        faces.append([f - 1, f + f - 1, f, 0])

        block = Mesh.from_vertices_and_faces(bottom + top, faces)
        blocks.append(block)

    return blocks


def draw_blocks(blocks):
    artist = MeshArtist(None, layer="RV2::Blocks")
    artist.clear_layer()

    for block in blocks:
        artist.mesh = block
        artist.draw_faces(color=(0, 255, 255), join_faces=True)


@rv2_error()
@rv2_undo
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    proxy = get_proxy()
    if not proxy:
        return

    # vertical = proxy.function('compas_tna.equilibrium.vertical_from_zmax_proxy')

    form = scene.get('form')[0]
    thrust = scene.get('thrust')[0]

    if not form:
        print("There is no FormDiagram in the scene.")
        return

    if not thrust:
        print("There is no ThrustDiagram in the scene.")
        return

    mesh = thrust.datastructure

    mesh = subdivide_dual(mesh)
    scene.add(mesh, name='dual_mesh')
    draw_orientation(mesh)
    mesh_idos = offsets(mesh)[0]
    mesh_edos = offsets(mesh)[1]
    draw_offsets(mesh_idos, mesh_edos)
    blocks = materialisation_blocks(mesh_idos, mesh_edos)
    draw_blocks(blocks)

    # 9. update scene
    scene.clear()
    scene.update()

# ==============================================================================
# Main
# ==============================================================================


if __name__ == "__main__":

    RunCommand(True)
