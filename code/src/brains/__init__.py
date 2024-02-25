from . import base, human_driver, autonomous, autonomous_demo
from typing import TypedDict
import types


class ModuleTypes(TypedDict):
    autonomous: types.ModuleType
    base: types.ModuleType
    human_driver: types.ModuleType
    autonomous_demo: types.ModuleType


Types: ModuleTypes = {
    "autonomous": autonomous,
    "base": base,
    "human_driver": human_driver,
    "autonomous_demo": autonomous_demo
}
