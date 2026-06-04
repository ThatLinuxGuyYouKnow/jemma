
class ToolCallException(Exception):

    def __init__(self, *args, model_error_feedback: str = "Incorrect Tool use"):

        self.user_facing_message = "Model produced a malformed tool call"
        self.model_error_feedback = model_error_feedback
        super().__init__(*args)


class InvalidToolArguments(ToolCallException):

    def __init__(self, *args, model_error_feedback: str = "Invalid arguments provided for this tool, try again with valid arguments"):
        super().__init__(*args, model_error_feedback=model_error_feedback)


