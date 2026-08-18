import app.api.controllers
from app.infra.discovery import discover_submodules


def test_discover_submodules_finds_every_controller() -> None:
    """Undiscovered controllers never get a route."""

    modules = discover_submodules(app.api.controllers)
    names = {module.__name__ for module in modules}

    assert 'app.api.controllers.auth' in names
    assert 'app.api.controllers.health' in names
    assert all(hasattr(module, 'router') for module in modules)


def test_discover_submodules_matches_only_the_last_path_segment() -> None:
    modules = discover_submodules(app.api.controllers, 'auth')

    assert [module.__name__ for module in modules] == ['app.api.controllers.auth']


def test_discover_submodules_returns_empty_for_an_unknown_basename() -> None:
    assert discover_submodules(app.api.controllers, 'missing') == []
