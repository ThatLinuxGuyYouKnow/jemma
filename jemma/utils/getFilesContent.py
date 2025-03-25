import os


def get_files_content(directory="."):
    """Get content of relevant files in the project."""
    ignored_dirs = {".git", "node_modules", "venv", "env", "build", "dist", "__pycache__","android","build","macos","ios","linux","web","test","windows"}
    ignored_extensions = {".pyc", ".pyo", ".pyd", ".so", ".dll", ".class", ".exe", ".obj", ".o",".h5",".csv"}
    
    all_content = ""
    
    for root, dirs, files in os.walk(directory):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        
        for file in files:
            if not any(file.endswith(ext) for ext in ignored_extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        all_content += f"\n\nFile: {file_path}\n```\n{content}\n```\n"
                except:
                    # Skip files that can't be read as text
                    pass
    
    return all_content