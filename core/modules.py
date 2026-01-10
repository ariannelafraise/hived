import importlib.util
import inspect
import os

from core.audit_event_handler import AuditEventHandler
from core.config import PathConfig
from core.notifier import Notifier
from core.plugin import Plugin


class DynamicModuleImportError(Exception):
    """
    An error that occured trying to dynamically import a module.
    """

    pass


def _dynamic_import(base_class: type, file_name: str) -> dict[str, type]:
    """
    Dynamically imports all modules matching the query. Modules are located in subfolders of
    the 'modules' directory.

    Parameters:
        base_class: the module class to be imported
        file_name: the file name to look into

    Example: _dynamic_import(Plugin, "plugins.py") ->
    Imports all 'Plugin' modules found in "plugins.py" files in all subfolders of the 'modules' directory.
    """
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

        if not os.path.isfile(file_path):
            continue

        module_type_name = file_name.split(".")[0]

        spec = importlib.util.spec_from_file_location(module_type_name, file_path)
        if not spec or not spec.loader:
            raise DynamicModuleImportError(
                f"Failed to import {module} from {file_path}"
            )
        module_from_spec = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module_from_spec)

        for _, obj in inspect.getmembers(module_from_spec, inspect.isclass):
            # make sure the class is defined in the module and not imported
            if obj.__module__ == module_type_name:
                if issubclass(obj, base_class):
                    classes[module] = obj
    return classes


def import_plugins() -> list[Plugin]:
    """
    Imports all plugins and returns them into a list.
    Plugins are looked for in subfolders of the 'modules' directory,
    in 'plugins.py' files.
    """
    imported_plugins = _dynamic_import(Plugin, "plugins.py")
    instantiated_plugins: list[Plugin] = []
    for module, plugin in imported_plugins.items():
        if issubclass(plugin, Plugin):
            instantiated_plugins.append(plugin(module))
    return instantiated_plugins


def import_event_handlers() -> list[AuditEventHandler]:
    """
    Imports all audit event handlers and returns them into a list.
    Audit event handlers are looked for in subfolders of the 'modules' directory,
    in 'audit_event_handlers.py' files.
    """
    imported_handlers = _dynamic_import(AuditEventHandler, "audit_event_handlers.py")
    instantiated_handlers: list[AuditEventHandler] = []
    for _, handler in imported_handlers.items():
        if issubclass(handler, AuditEventHandler):
            instantiated_handlers.append(handler())
    return instantiated_handlers


def import_notifiers() -> list[Notifier]:
    """
    Imports all notifiers and returns them into a list.
    Notifiers are looked for in subfolders of the 'modules' directory,
    in 'notifiers.py' files.
    """
    imported_notifiers = _dynamic_import(Notifier, "notifiers.py")
    instantiated_notifiers: list[Notifier] = []
    for _, notifier in imported_notifiers.items():
        if issubclass(notifier, Notifier):
            instantiated_notifiers.append(notifier())
    return instantiated_notifiers
