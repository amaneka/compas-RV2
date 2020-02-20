from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_rv2
from compas_rv2.rhino import RhinoFormDiagram
from compas_rv2.rhino import RhinoThrustDiagram


__commandname__ = "RV2skeleton_tomesh"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):
    RV2 = get_rv2()
    if not RV2:
        return

    settings = RV2["settings"]
    scene = RV2["scene"]

    rhinoskeleton = RV2["scene"]["skeleton"]
    form = rhinoskeleton.diagram.to_form()
    if not form:
        return
    rhinoform = RhinoFormDiagram(form)
    rhinoform.draw(settings)

    rhinothrust = RhinoThrustDiagram(form)

    scene["form"] = rhinoform
    scene["force"] = None
    scene["thrust"] = rhinothrust


# ==============================================================================
# Main
# ==============================================================================


if __name__ == "__main__":

    RunCommand(True)