import re


class StepInfo(object):
    def __init__(self, step_text, parsed_step_text, impl):
        self.__step_text = step_text
        self.__parsed_step_text = parsed_step_text
        self.__impl = impl

    @property
    def step_text(self):
        return self.__step_text

    @property
    def parsed_step_text(self):
        return self.__parsed_step_text

    @property
    def impl(self):
        return self.__impl


class Registry(object):
    def __init__(self):
        self.__steps_map = {}

    def add_step_definition(self, step_text, func):
        parsed_step_text = re.sub('<[^<]+?>', '{}', step_text)
        self.__steps_map[parsed_step_text] = StepInfo(step_text, parsed_step_text, func)

    def is_step_implemented(self, step_text):
        return self.__steps_map.get(step_text) is not None

    def get_info(self, step_text):
        info = self.__steps_map.get(step_text)
        return info if info is not None else StepInfo(None, None, None)


registry = Registry()
