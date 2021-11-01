from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from copy import deepcopy
import compas_rhino
from compas_rhino.ui import CommandMenu
from compas_rhino.geometry import RhinoSurface
from compas_rhino.artists import MeshArtist
from compas_rv2.rhino import get_scene
from compas_rv2.datastructures import Pattern
from compas_rv2.rhino import SurfaceObject
from compas_rv2.rhino import rv2_undo
from compas_rv2.rhino import rv2_error

from compas.geometry import Vector
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.datastructures import mesh_flip_cycles , Mesh, meshes_join_and_weld
from compas.datastructures import meshes_join
from compas.utilities import pairwise

vertices = [
    [0, 0.0, 0.0],
    [8, 0, 0.0],
    [5, 5, 0],
    [0, 4, 0.0]
]

faces = [
        [0, 1, 2,3]
]

mesh = Mesh.from_vertices_and_faces(vertices, faces)

def mesh_fast_copy(other):
    subd = Mesh()
    subd.vertex = deepcopy(other.vertex)
    subd.face = deepcopy(other.face)
    subd.facedata = deepcopy(other.facedata)
    subd.halfedge = deepcopy(other.halfedge)
    subd._max_face = other._max_face
    subd._max_vertex = other._max_vertex
    return subd

def subdivide_face(mesh, fkey):
    
    x, y, z = mesh.face_centroid(fkey)
    centr_vert = mesh.add_vertex(x=x, y=y, z=z)
    face_verts = mesh.face_vertices(fkey)

    #find midpoints of edges-------------------------------------------------------------
    mid_verts = []
    for u,v in pairwise(face_verts):

        t = 0.5
        # coordinates
        x, y, z = mesh.edge_point(u, v, t)

        # the split vertex
        mid_vert = mesh.add_vertex(x=x, y=y, z=z)
        mid_verts.append(mid_vert)
    
    #create new faces----------------------------------------------------------------------
    new_faces = []
    new_vertices = []
    for i, (f, m) in enumerate(zip(face_verts, mid_verts)):
        new_face = mesh.add_face([face_verts[i], mid_verts[i], centr_vert, mid_verts[(len(mid_verts)-1)-i]])
        new_faces.append(new_face)
        new_vertices.extend ([face_verts[i], mid_verts[i], mid_verts[(len(mid_verts)-1)-i]])
    
    new_vertices.insert(2, centr_vert)
    mesh.delete_face(fkey)
    
    return mesh 

faces = list(mesh.faces())
for face in faces:
    new_mesh = subdivide_face(mesh, face)

artist = MeshArtist(new_mesh, layer= "new_mesh")
artist.clear_layer()
artist.draw_faces(join_faces=True)

def mesh_subdivide_faces(mesh, cls=Mesh):
    meshes = []
    subd = mesh_fast_copy(mesh)
    subd.clear()

    faces = list(mesh.faces())
    for face in faces:
        new_mesh = subdivide_face(mesh, face)
        meshes.append(new_mesh)

    subd_mesh = meshes_join_and_weld(meshes, precision=None, cls=cls)
    subd_mesh = meshes_join(meshes, cls=cls)

    return subd_mesh

def mesh_subdivide_faces_2(mesh):
    faces = []
    verts = []
    for face in mesh.faces():
        new_mesh, new_verts, new_faces = subdivide_face(mesh, face)
        faces.extend(new_faces)
        verts.extend(new_verts)
    subd = mesh.from_vertices_and_faces(verts, faces)
    return subd

#subd = mesh_subdivide_faces_2(mesh)

def mesh_split_edges(mesh, edges, n):
    subd = mesh_fast_copy(mesh)
    for u, v in edges:
        mesh_split_edge(subd, u, v, n)

    return subd

def tri_face(mesh, fkey):
    centroid = mesh.face_centroid(fkey)
    centroid_vector = Vector(*centroid)
    normal = mesh.face_normal(fkey)
    normal_vector = Vector(*normal)
    new_vertex = centroid_vector
    #new_keys = mesh.insert_vertex(fkey, xyz=new_vertex, return_fkeys=True)[1]
    face_verts = mesh.face_vertices(fkey)

    new_keys = []

    for i, v in enumerate(face_verts):
        next_v = face_verts[(i+1) % len(face_verts)]
        new_v = new_vertex
        new_face_key = mesh.add_face([v, next_v, new_v])
        new_keys.append(new_face_key)

    mesh.delete_face(fkey)
    return new_keys

#=====================================================================================
subd_tri = mesh.copy()
fkeys = list(subd_tri.faces())

for f in fkeys[:-1]:
    new_keys = tri_face(subd_tri, f)
    for k in new_keys:
        newkeys = tri_face(subd_tri, k)

artist = MeshArtist(subd_tri, layer="aa_mesh")
artist.clear_layer()
artist.draw_faces(join_faces=True)
