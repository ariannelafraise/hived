import importlib.util
import inspect
import os
from typing import Any

from hivedapi import AuditEventHandler, HivectlPlugin


class ExternalApplicationImportError(Exception):
    """
    An error that occured trying to import an external application.
    """

    pass


def _load_base_classes_from_file(base_class: type, path: str) -> list[Any]:
    classes = []
    path_elements = path.split("/")
    file_name = path_elements[-1]
    spec = importlib.util.spec_from_file_location(file_name, path)
    if not spec or not spec.loader:
        raise ExternalApplicationImportError(f"Failed to import {file_name} from {path}")
    module_from_spec = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module_from_spec)

    for _, obj in inspect.getmembers(module_from_spec, inspect.isclass):
        # make sure the class is defined in the module and not imported
        if obj.__module__ == file_name:
            if issubclass(obj, base_class) and not inspect.isabstract(obj):
                classes.append(obj)
    return classes


def _explore_dir(base_class: type, path: str) -> list[Any]:
    classes = []
    if path.split("/")[-1].startswith("."):
        return classes

    for item in os.listdir(path):
        if os.path.isdir(f"{path}/{item}"):
            classes += _explore_dir(base_class, f"{path}/{item}")
        elif item.endswith(".py") and os.path.isfile(f"{path}/{item}"):
            classes += _load_base_classes_from_file(base_class, f"{path}/{item}")
    return classes


def _dynamic_import(base_class: type) -> list[type]:
    """
    Import all external applications' modules matching the query.

    Parameters:
        base_class: the module class to be imported

    Example: _dynamic_import(Plugin) ->
    Imports all 'Plugin' modules found in all the external applications that were registered to Hived.
    """
    classes = []
    with open("/etc/hived/apps", "r") as file:
        for app_directory in file:
            if app_directory[-1] == "/":
                app_directory = app_directory[:-1]
            app_directory = app_directory.replace("\n", "")
            classes += _explore_dir(base_class, app_directory)
    return classes


def import_plugins() -> list[HivectlPlugin]:
    """
    Import all plugins from all external applications and returns them into a list.
    """
    imported_plugins = _dynamic_import(HivectlPlugin)
    instantiated_plugins: list[HivectlPlugin] = []
    for plugin in imported_plugins:
        if issubclass(plugin, HivectlPlugin) and not inspect.isabstract(plugin):
            instantiated_plugins.append(plugin())
    return instantiated_plugins


def import_event_handlers() -> list[AuditEventHandler]:
    """
    Import all audit event handlers from all external applications and returns them into a list.
    """
    imported_handlers = _dynamic_import(AuditEventHandler)
    instantiated_handlers: list[AuditEventHandler] = []
    for handler in imported_handlers:
        if issubclass(handler, AuditEventHandler) and not inspect.isabstract(handler):
            instantiated_handlers.append(handler())
    return instantiated_handlers
