import gc

import pytest


@pytest.fixture(autouse=True)
def collect_garbage_in_main_thread():
    """Python's garbage collector runs in whichever thread happens to need memory,
    for example in the background import thread of a MainWindow. If it frees Qt
    objects of an earlier test there, the tests can hang or crash. So the automatic
    collection stays off during the tests, and the garbage of each test is freed
    here, in the main thread."""
    gc.disable()
    yield
    gc.collect()
