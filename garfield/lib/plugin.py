import file_utils


class BasePlugin(object):
    """Both plugins and subplugins extend this"""
    def __init__(self, config_file_path, plugin_props):
        self._config_file_path = config_file_path
        self._props = plugin_props

        # This will point to an object consisting of all helpers
        # like do a socket connection, http request, regex match etc..
        self.helpers = None
