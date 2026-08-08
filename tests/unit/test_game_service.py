import pytest

# Import the module under test. The target functions are expected to be defined in
# ``backend/services/game_service.py``. Since the repository currently does not
# contain this module, the import will raise ``ImportError`` which will cause the
# test to fail – this is intentional to surface missing implementation.

@pytest.mark.parametrize(
    "function_path",
    [
        "backend.services.game_service.create_game",
        "backend.services.game_service.place_ship",
        "backend.services.game_service.fire_shot",
        "backend.services.game_service.check_winner",
    ],
)
def test_game_service_functions_exist(function_path):
    """Ensure that each game service function can be imported.

    The test will pass only if the function exists. Missing implementations will
    raise ``ImportError`` and be reported as a failure.
    """
    module_path, func_name = function_path.rsplit(".", 1)
    module = __import__(module_path, fromlist=[func_name])
    getattr(module, func_name)

