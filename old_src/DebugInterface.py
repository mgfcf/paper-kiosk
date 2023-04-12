class DebugInterface (object):
    """Defines general interface for debugging operations"""

    def print_event(self, event):
        raise NotImplementedError("Functions needs to be implemented")

    def print_forecast(self, forecast):
        raise NotImplementedError("Functions needs to be implemented")

    def print_line(self, content):
        raise NotImplementedError("Functions needs to be implemented")

    def print_err(self, exception, msg=""):
        raise NotImplementedError("Functions needs to be implemented")
