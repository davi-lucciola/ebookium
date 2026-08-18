import importlib
import pkgutil
from types import ModuleType


def discover_submodules(
    package: ModuleType, basename: str | None = None
) -> list[ModuleType]:
    """Import submodules of `package`.

    When `basename` is set, only modules whose last path segment matches are
    returned (same contract as the knock-finance helper). When omitted, every
    non-package submodule is imported — used to collect routers from
    `app.api.controllers`.
    """
    modules = [
        importlib.import_module(info.name)
        for info in pkgutil.walk_packages(
            package.__path__, prefix=f'{package.__name__}.'
        )
        if not info.ispkg
    ]

    if basename is None:
        return modules

    return [
        module for module in modules if module.__name__.rsplit('.', 1)[-1] == basename
    ]
