import os
import sys
import bson
import logging
import importlib.util
from datetime import datetime
from pythonjsonlogger import jsonlogger
from cloeepy.config import Config
from cloeepy.logger import Logger

class CloeePy(object):
    """
    CloeePy is a singleton application context. This is the core of the framework.
    """
    class __CloeePy:
        def __init__(self):
            self.config = Config()
            if hasattr(self.config.CloeePy, "Logging"):
                logger = Logger(self.config.CloeePy.Logging)
                self.log = logger.logger
                self._log = logger._logger
            else:
                logger = Logger()
                self.log = logger.logger
                self._log = logger._logger

            # log initializes success
            self._log.info("CloeePy Initialized: Config Path: [%s]" % self.config.get_path())
            self._init_plugins()

        def _init_plugins(self):
            """
            Iterates through list of configured plugins and instantiates them.
            ImportError is raised if plugin can't be found in PYTHONPATH.
            """
            if hasattr(self.config.CloeePy, "Plugins"):
                for k, v in self.config.as_dict()["CloeePy"]["Plugins"].items():
                    module = None
                    spec = importlib.util.find_spec(k)
                    if spec is None:
                        raise ImportError("Unable to find Plugin %s. Try executing 'pip install %s'" % (k, k))
                    else:
                        self._log.debug("Initializing Plugin %s" % k)
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        sys.modules[k] = module

                    module_class_instance = module.get_class()(v, self.log)
                    setattr(self, module_class_instance.get_context_name(), module_class_instance.get_context_value())

    instance = None

    def __new__(cls):
        if not CloeePy.instance:
            CloeePy.instance = CloeePy.__CloeePy()
        return CloeePy.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)