import os

from jemma.utils.terminalPrettifier import errorText



    """Recursively list all files in given directories."""
    files = []
    for path in paths:
        if os.path.isfile(path) and not path.startswith('.'):
            files.append(os.path.abspath(path))
        elif os.path.isdir(path) and not path.startswith('.'):
            try:
                with os.scandir(path) as entries:
                    for entry in entries:
                        # Recursively process each entry with full path
                        if entry.is_file():
                            files.append(os.path.abspath(entry.path))
                        elif entry.is_dir():
                            files.extend(spitAllFiles([entry.path]))
            except PermissionError:
                print(errorText(f"Permission denied: {path}"))
        else:
            print(errorText(f"Invalid path: {path}"))
    return files
