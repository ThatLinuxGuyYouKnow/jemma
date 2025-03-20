import os



def spitAllFiles(paths):
    """Recursively list all files in given directories."""
    for path in paths:
        if os.path.isfile(path) and path[0] != '.':
            # If it's a file, just print it
            print(f"File: {os.path.abspath(path)}")
        elif os.path.isdir(path) and path[0] != '.':
            # If it's a directory, process its contents
            print(f"\nDirectory: {os.path.abspath(path)}")
            try:
                with os.scandir(path) as entries:
                    for entry in entries:
                        # Recursively process each entry with full path
                        spitAllFiles([entry.path])
            except PermissionError:
                print(f"Permission denied: {path}")
        else:
            print(f"Invalid path: {path}")