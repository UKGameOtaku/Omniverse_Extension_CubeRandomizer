import omni.ext
import omni.ui as ui
import omni.usd
from pxr import UsdGeom, Gf
import random


# Functions and vars are available to other extension as usual in python: `example.python_ext.some_public_function(x)`
def some_public_function(x: int):
    print("[omni.cube.randomizer] some_public_function was called with x: ", x)
    return x ** x


# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class OmniCubeRandomizerExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[omni.cube.randomizer] omni cube randomizer startup")

        usd_context = omni.usd.get_context()

        self._count = 0

        self._window = ui.Window("Cube Randomizer", width=300, height=300)
        with self._window.frame:
            with ui.VStack():
                label = ui.Label("Creates a Cube with randomized Size and Shape")

                def on_click():
                    self._count += 1
                    label.text = f"count: {self._count}"

                    stage = usd_context.get_stage()
                    cube_path = '/World/Cube'
                    cube = UsdGeom.Cube.Define(stage, cube_path)
                    cube.CreateSizeAttr(random.random())
                    cube.CreateDisplayColorAttr([Gf.Vec3f(random.random(), random.random(), random.random())])

                def on_reset():
                    self._count = 0
                    label.text = "empty"

                on_reset()

                with ui.HStack():
                    ui.Button("Randomize", clicked_fn=on_click)
                    ui.Button("Reset", clicked_fn=on_reset)

    def on_shutdown(self):
        print("[omni.cube.randomizer] omni cube randomizer shutdown")
