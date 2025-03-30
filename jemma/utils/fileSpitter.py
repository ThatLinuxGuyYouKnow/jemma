import os

from jemma.utils.terminalPrettifier import errorText



def spitAllFiles(paths):
    """Recursively list all files in given directories."""
    for path in paths:
        if os.path.isfile(path) and path[0] != '.':
         
            return os.path.abspath(path)
        elif os.path.isdir(path) and path[0] != '.':
            
            
            try:
                with os.scandir(path) as entries:
                    for entry in entries:
                        # Recursively process each entry with full path
                        spitAllFiles([entry.path])
                        return os.path.abspath(path)
            except PermissionError:
                print(errorText(f"Permission denied: {path}"))
        else:
            print(errorText(f"Invalid path: {path}"))