from jemma.validators.file_operations_validators import validate_file_read_range, validate_file_exists
from jemma.exceptions.file_operation_exceptions import FileOperationError,  FileNonExistentException


def read_file_lines(file_path: str, start_line: int = 1, end_line: int = None) -> str:
    """
    Read a range of lines from a text file.

    Args:
        file_path: Path to the file (relative or absolute).
        start_line: First line to read (1 indexed, inclusive).
        end_line: Last line to read (1 indexed, inclusive). If None, reads to end of file.

    Returns:
        The selected lines as a single string, preserving original line endings.
        If start_line is out of range, returns an empty string.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If start_line < 1 or end_line < start_line.
    """

    ##First, we validate, starting from the most severe error possible

    if not validate_file_exists(file_path= file_path):
        raise FileNonExistentException(file_path=file_path)
    

    if start_line < 1:
        raise FileOperationError(model_error_feedback= 'File reads have to start at least from the first line')
    

    if end_line is not None and not validate_file_read_range(first_line= start_line, last_line= end_line):
        raise FileOperationError(model_error_feedback='Invalid file read range, end line must be greater than start line')

    with open(file_path, 'r', encoding='utf-8') as f:
        # Read all lines (lazy iteration would be more memory‑efficient for huge files,
        # but we need random access by line number; for most files, readlines is fine)
        lines = f.readlines()

    # Convert to 0‑based indexing
    start_idx = start_line - 1
    if start_idx >= len(lines):
        return ""  # start beyond file end

    if end_line is None:
        selected = lines[start_idx:]
    else:
        end_idx = end_line  # end_line is inclusive, so slice end is end_idx
        selected = lines[start_idx:end_idx]

    return ''.join(selected)