import os
import imp
import json
import codecs
import logging


def relative_path_to_abs(reference_path, relative_path):
    # If reference path is a file eg. plugin json file get dirname
    # and add the relative path to it
    if os.path.isfile(reference_path):
        reference_path = os.path.dirname(reference_path)
    return(os.path.join(reference_path, relative_path))


def import_module(path, module_name):
    file, pathname, description = imp.find_module(module_name, [path])
    return(imp.load_module(module_name, file, pathname, description))


def get_plugin(config_path, module_props):
    module = import_module(os.path.dirname(config_path), module_props["module"])
    return(module.Plugin(config_path, module_props))


def open_file(path, mode, func):
    try:
        with codecs.open(path, mode=mode, encoding="utf-8") as f:
            func(f)
    except (OSError, IOError):
        logging.exception("Opening file failed: %s" (path))


def json_dump(path, data):
    open_file(path, "w", lambda x: json.dump(data, x, indent=2))


def json_load(path):
    try:
        with codecs.open(path, mode="r", encoding="utf-8") as f:
            data = json.load(f)
        return(data)
    except (OSError, IOError):
        logging.exception("Opening file failed: %s" (path))
