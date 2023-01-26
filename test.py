import bluesky.callbacks as bc
from bluesky import plans as bp
from bluesky import RunEngine
from ophyd.sim import det, motor
from lmfit import models

RE = RunEngine()

def my_plan(detectors, motor):
    # Create a LiveFit instance
    lf = bc.LiveFit(models.LinearModel(), 'det', {'x':'motor'})
    # Register the LiveFit instance as a callback
    RE.subscribe(lf)
    # Execute the scan
    yield from bp.scan(detectors, motor, -1, 1, 11)
    # Wait for the LiveFit to finish processing the event
    lf.stop()

RE(my_plan([det], motor))
