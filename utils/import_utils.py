import os
import importlib.util
import inspect

def dynamic_import(base_class: type, directory: str) -> list:
    objects = []
    for file in os.listdir(directory):
        if not file.endswith(".py"):
            continue
        module_name = file.split('.')[0]
        file_path = directory + '/' + file
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == module_name:  # make sure the class is defined in the module and not imported
                if issubclass(obj, base_class):
                    objects.append(obj)
    return objects
