from getgauge.registry import registry


def step(step_text):
    def _step(func):
        # Storing function in registry, so that it can be called when Gauge requests
        registry.add_step_definition(step_text, func)
        return func

    return _step
