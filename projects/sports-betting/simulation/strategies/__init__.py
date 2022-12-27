from importlib import import_module
from inspect import isclass
from pkgutil import iter_modules
from typing import List

from simulation.strategy import BaseStrategy


def discover_strategies() -> List[BaseStrategy]:
    submodules = [i for i in iter_modules(__path__)]
    known_strategies = set()
    strategies = []

    for submodule in submodules:
        module = import_module(f".{submodule.name}", package="simulation.strategies")

        for e in dir(module):
            obj = getattr(module, e)
            if isclass(obj) and issubclass(obj, BaseStrategy) and obj != BaseStrategy:
                if obj.__name__ in known_strategies:
                    # TODO: Maybe add additional namespace based on which submodule it comes from
                    raise RuntimeError(
                        f"Strategy {obj.__name__} already exists, please rename the duplicate"
                    )
                known_strategies.add(obj.__name__)

                strategies.append(obj)

    return strategies
