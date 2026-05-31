from jemma.tools.file_operations import write_to_file, read_file
from jemma.tools.search_tools import grep_search

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Tool for reading file content",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The *absolute* path of the file to be read",
                    },
                    "start_line": {
                        "type": "integer",
                        "description": "Line to start reading from. Omit to read from the top.",
                        "nullable": True
                    },
                    "end_line": {
                        "type": "integer",
                        "description": "Line to stop reading at. Omit to read until end of file.",
                        "nullable": True
                    },
                },
                "required": ["file_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_to_file",
            "description": "Tool for writing content to a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The *absolute* path of the file to write to",
                    },
                    "new_content": {
                        "type": "string",
                        "description": "The content to write",
                    },
                    "old_content": {
                        "type": "string",
                        "description": "The exact content being replaced. Pass null if the file is empty.",
                        "nullable": True
                    },
                    "start_line": {
                        "type": "integer",
                        "description": "Line to start replacement from. Pass null if the file is empty.",
                        "nullable": True
                    },
                    "end_line": {
                        "type": "integer",
                        "description": "Line to end replacement at. Pass null if the file is empty.",
                        "nullable": True
                    },
                },
                "required": ["file_path", "new_content", "old_content"],
            },
        },
    },

    {
        "type" : "function",
        "function":{
           "name":"write_new_file",
             "description":"Tool for writing to a new file",
             "parameters":{
                 "type": "object",
                 "properties":{
                     "file_path":{
                         "type":"string",
                         "description": "The *absolute* path of the new file to create and write to"
                     },
                     "content":{
                         "type":"string",
                         "description":"Content of the new file"
                     },

                 },
                 "required":["file_path", "content"]
             }
        }
    },
    {
        "type": "function",
        "function":{
            "name":"grep_search",
            "description":"Search for a pattern / search term within all files in a certain directory OR matches within a particular file. Returns matches and files found in",
            "parameters":{
                "type":"object",
                "properties":{
                    "search_term":{
                        "type":"string",
                        "description":"Pattern / term to search for"},
                    "path":{
                        "type":"string",
                        "description":" *absolute* path to perform search in, can be file or directory"
                    },
                    "file_type":{
                        "type":"string",
                        "description":"specific file type to search for, ie: py, js rs. Omit if search is not specific to a file type"
                    }
                },
                "required":["search_term", "path"]
            }
        }
    }
]

TOOL_FUNCTIONS: dict[str, callable] = {
    "read_file": read_file.read_file_lines,
    "write_to_file": write_to_file.replace_lines_in_file,
    "write_new_file":write_to_file.write_new_file,
    "grep_search": grep_search.search_in_files
}