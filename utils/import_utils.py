import importlib.util
import inspect
import os

from config import PathConfig
from core.audit_event_handler import AuditEventHandler
from core.plugin import Plugin


class DynamicImportError(Exception):
    pass


def _dynamic_import(base_class: type, file_name: str) -> dict[str, type]:
    classes = {}
    modules_dir = PathConfig.MODULES_DIR
    if modules_dir[-1] == "/":
        modules_dir = modules_dir[:-1]
    for module in os.listdir(modules_dir):
        if module == "__pycache__":
            continue
        if not os.path.isdir(f"{modules_dir}/{module}"):
            continue

        file_path = f"{modules_dir}/{module}/{file_name}"
        module_type_name = file_name.split(".")[0]
        spec = importlib.util.spec_from_file_location(module_type_name, file_path)
        if not spec or not spec.loader:
            raise DynamicImportError(f"Failed to import {module} from {file_path}")
        module_from_spec = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module_from_spec)
        for _, obj in inspect.getmembers(module_from_spec, inspect.isclass):
            if (
                obj.__module__ == module_type_name
            ):  # make sure the class is defined in the module and not imported
                if issubclass(obj, base_class):
                    classes[module] = obj
    return classes


def import_plugins() -> list[Plugin]:
    imported_plugins = _dynamic_import(Plugin, "plugin.py")
    instantiated_plugins: list[Plugin] = []
    for module, plugin in imported_plugins.items():
        if issubclass(plugin, Plugin):
            instantiated_plugins.append(plugin(module))
    return instantiated_plugins


def import_event_handlers() -> list[AuditEventHandler]:
    imported_handlers = _dynamic_import(AuditEventHandler, "audit_event_handler.py")
    instantiated_handlers: list[AuditEventHandler] = []
    for _, handler in imported_handlers.items():
        if issubclass(handler, AuditEventHandler):
            instantiated_handlers.append(handler())
    return instantiated_handlers
