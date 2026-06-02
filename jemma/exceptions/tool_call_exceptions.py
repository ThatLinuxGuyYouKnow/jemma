
class ToolCallException(Exception):

    def __init__(self, *args, model_error_feedback: str):

        self.user_facing_message = "Model produced a malformed tool call",
        self.model_error_feedback = "Incorrect Tool use"
        super().__init__(*args)


class InvalidToolArguments(ToolCallException):

    def __init__(self, *args, model_error_feedback):
        super().__init__(*args, model_error_feedback=model_error_feedback)


