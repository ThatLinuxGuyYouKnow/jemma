import atexit
import json
import signal
import sys
from jemma.model.modelInteraction import modelInteraction
from jemma.utils.replaceFileContentByLines import replace_lines_in_file
from jemma.utils.terminalPrettifier import errorText, responseFormatter, successText
def handle_exit(signum=None, frame=None):
    """Handle program exit with proper cleanup and status code"""
    
    print("\nExiting Jemma...")
    sys.exit(0 if signum in (signal.SIGINT, signal.SIGTERM) else 1)

# Register the exit handler
atexit.register(handle_exit)
signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)
def editCode(directoryStructure: str, fileContents: str, userPrompt: str):
    """Generate and apply code changes based on user request"""
    prompt = f"""
    Return fixes/features as JSON patches. Format:
    {{
      "changes": [
        {{
          "file": "path/to/file",
          "isNewFile": "false",
          "start_line": 1,
          "end_line": 2,
          "replacement": ["line1", "line2"]
        }}
      ],
      "narration": "Description of changes"
    }}
    
    User request: {userPrompt}
    Directory structure: {directoryStructure}
    File contents: {fileContents}
    
    Respond with *ONLY* valid JSON"""
    
    try:
        modelResponse = modelInteraction(prompt=prompt, isJsonResponse=True)
        print(responseFormatter(modelResponse))
        change_count = processChanges(modelResponse)
        print(successText(f"Successfully applied {change_count} changes"))
        return change_count
    except json.JSONDecodeError as e:
        print(errorText(f"Invalid JSON response: {e}"))
    except Exception as e:
        print(errorText(f"Error processing changes: {e}"))

def processChanges(modelResponse: str) -> int:
    """Apply changes from JSON response to files"""
    response_data = json.loads(modelResponse)
    file_patches = response_data.get("changes", [])
    change_count = 0

    for patch in file_patches:
        try:
            file_path = patch['file']
            is_new = patch.get('isNewFile', 'false').lower() == 'true'
            replacement = patch.get('replacement', [])
            
            if is_new:
                # Create new file with content
                with open(file_path, "w", encoding='utf-8') as f:
                    f.write('\n'.join(replacement))
                change_count += 1
            else:
                # Modify existing file
                start_line = int(patch['start_line'])
                end_line = int(patch['end_line'])
                replace_lines_in_file(
                    file_path=file_path,
                    start_line=start_line,
                    end_line=end_line,
                    new_content='\n'.join(replacement)
                )
                change_count += 1
                
        except KeyError as e:
            print(errorText(f"Missing required field in patch: {e}"))
        except IOError as e:
            print(errorText(f"File operation failed for {file_path}: {e}"))
    
    return change_count