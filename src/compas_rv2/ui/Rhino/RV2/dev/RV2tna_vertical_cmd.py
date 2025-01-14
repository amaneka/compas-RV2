from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import get_proxy
from compas.geometry import subtract_vectors
from compas.geometry import length_vector
from compas_rv2.rhino import rv2_undo
from compas_rv2.rhino import rv2_error

# import Rhino


__commandname__ = "RV2tna_vertical"


@rv2_error()
@rv2_undo
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    proxy = get_proxy()
    if not proxy:
        return

    vertical = proxy.function('compas_tna.equilibrium.vertical_from_zmax_proxy')

    form = scene.get('form')[0]
    force = scene.get('force')[0]
    thrust = scene.get('thrust')[0]

    if not form:
        print("There is no FormDiagram in the scene.")
        return

    if not force:
        print("There is no ForceDiagram in the scene.")
        return

    if not thrust:
        print("There is no ThrustDiagram in the scene.")
        return

    bbox = form.datastructure.bounding_box_xy()
    diagonal = length_vector(subtract_vectors(bbox[2], bbox[0]))

    zmax = scene.settings['Solvers']['tna.vertical.zmax']
    kmax = scene.settings['Solvers']['tna.vertical.kmax']

    options = ['TargetHeight']

    while True:
        option = compas_rhino.rs.GetString('Press Enter to run or ESC to exit.', strings=options)

        if option is None:
            print("Vetical equilibrium aborted!")
            return

        if not option:
            break

        if option == 'TargetHeight':
            new_zmax = compas_rhino.rs.GetReal('Enter target height of the ThrustDiagram', zmax, 0.0, 1.0 * diagonal)
            if new_zmax or new_zmax is not None:
                zmax = new_zmax

    scene.settings['Solvers']['tna.vertical.zmax'] = zmax

    result = vertical(form.datastructure.data, zmax, kmax=kmax)

    if not result:
        print("Vertical equilibrium failed!")
        return

    formdata, scale = result

    # store in advance such that it can be reset
    thrust_name = thrust.name

    force.datastructure.attributes['scale'] = scale
    form.datastructure.data = formdata
    thrust.datastructure.data = formdata

    # the name of the thrust diagram is stored in the attribute dict of the mesh
    # therefore the name must be reset explicitly
    thrust.name = thrust_name

    form.datastructure.dual = force.datastructure
    force.datastructure.primal = form.datastructure
    thrust.datastructure.dual = force.datastructure

    thrust.settings['_is.valid'] = True

    scene.update()

    print('Vertical equilibrium found!')
    print('ThrustDiagram object successfully created with target height of {}.'.format(zmax))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
