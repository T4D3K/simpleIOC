import inspect
from copy import deepcopy


class Singleton:
    def __init__(self, cls, context=None):
        self.cls = cls
        self.context = context if context else {}


class IOC:
    def __init__(self, ioc_conf=None):
        if not ioc_conf:
            ioc_conf = {}
        self._defualt_conf = deepcopy(ioc_conf)
        self.conf = ioc_conf
        self.singletons = {}

    def reset_to_default_conf(self):
        self.conf = deepcopy(self._defualt_conf)

    def build(self, class_to_build, context=None, global_context=True, parent_class=None):
        if not context:
            context = {}
        obj = self._build_object(parent_class, class_to_build, context, global_context)
        return obj

    def _build_singleton(self, parent_class, singleton, global_context):
        if singleton.cls in self.singletons:
            return self.singletons[singleton.cls]
        obj = self._build_object(parent_class, singleton.cls, singleton.context, global_context)
        self.singletons[singleton.cls] = obj
        return obj

    def _build_object(self, parent_class, class_to_build, context, global_context):
        self_mapping = parent_class == class_to_build
        configured_params = {} if self_mapping else self.conf.get(class_to_build, {})
        if isinstance(configured_params, Singleton):
            return self._build_singleton(class_to_build, configured_params, global_context)
        if inspect.isclass(configured_params):
            return self.build(configured_params, parent_class=class_to_build)
        if not isinstance(configured_params, dict):
            return configured_params
        built_objects = {}
        sig = inspect.signature(class_to_build.__init__)
        for param_name, param in sig.parameters.items():
            to_build = configured_params.get(param_name, param.annotation)
            if param_name in context:
                built_objects[param_name] = context[param_name]
            elif not inspect.isclass(to_build):
                built_objects[param_name] = to_build
            elif inspect.isclass(to_build) and to_build != inspect._empty:
                built_objects[param_name] = self.build(to_build, context if global_context else {},
                                                       parent_class=class_to_build)
            elif param.default != inspect._empty:
                built_objects[param_name] = param.default
        obj = class_to_build(**built_objects)
        return obj
