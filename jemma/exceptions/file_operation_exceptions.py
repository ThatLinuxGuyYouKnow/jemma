class FileOperationError(Exception):
    """Base exception for all file operation errors in Jemma."""

    def __init__(
        self,
        model_error_feedback: str,
        user_facing_error_text: str = "Model produced malformed output",
    ):
        super().__init__(f"{user_facing_error_text}: {model_error_feedback}")
        self.model_error_feedback = model_error_feedback
        self.user_facing_error_text = user_facing_error_text




class FileNonExistentException(FileOperationError):
    """Raised when an operation references a file that does not exist."""

    def __init__(
        self,
        file_path: str,
        model_error_feedback: str = "",
        user_facing_error_text: str = "File not found",
    ):
        feedback = model_error_feedback or f"File does not exist: {file_path}"
        super().__init__(f"{feedback} (file: {file_path})", user_facing_error_text)
        self.file_path = file_path


 