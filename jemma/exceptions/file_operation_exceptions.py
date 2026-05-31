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


class BadFileReadException(FileOperationError):
    """Raised when reading a file fails due to invalid offsets or read errors."""

    def __init__(
        self,
        model_error_feedback: str,
        file_path: str = "",
        offset: int | None = None,
        user_facing_error_text: str = "Could not read file",
    ):
        details = _build_details(file_path=file_path, offset=offset)
        super().__init__(f"{model_error_feedback}{details}", user_facing_error_text)
        self.file_path = file_path
        self.offset = offset


class BadFileWriteException(FileOperationError):
    """Raised when writing to a file fails (e.g., invalid content, offsets)."""

    def __init__(
        self,
        model_error_feedback: str,
        file_path: str = "",
        offset: int | None = None,
        user_facing_error_text: str = "Could not write to file",
    ):
        details = _build_details(file_path=file_path, offset=offset)
        super().__init__(f"{model_error_feedback}{details}", user_facing_error_text)
        self.file_path = file_path
        self.offset = offset


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


# ── shared helper ────────────────────────────────────────────────────────────

def _build_details(*, file_path: str, offset: int | None) -> str:
    parts = []
    if file_path:
        parts.append(f"file: {file_path}")
    if offset is not None:
        parts.append(f"offset: {offset}")
    return f" ({', '.join(parts)})" if parts else ""