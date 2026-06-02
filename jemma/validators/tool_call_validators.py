

def validate_tool_exists(tool_name: str, tool_registry: dict):

    """Ensure a non-empty AND valid tool name has been supplied"""
    
    return tool_name and tool_name in tool_registry

