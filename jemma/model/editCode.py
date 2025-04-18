import atexit
import json
import signal
import sys
from jemma.model.modelInteraction import modelInteraction
from jemma.utils.replaceFileContentByLines import replace_lines_in_file
from jemma.utils.terminalPrettifier import errorText, responseFormatter, successText
 
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
        response_data = json.loads(modelResponse)

        # Handle both list and dict responses for narration
        if isinstance(response_data, list) and len(response_data) > 0:
            narration = response_data[0].get("narration", "No narration provided.")
        elif isinstance(response_data, dict):
            narration = response_data.get("narration", "No narration provided.")
        else:
            narration = "No narration provided."
            
        print(narration)

        change_count = processChanges(modelResponse)
            
        if change_count > 0:
            print(successText(
                f"Successfully applied {change_count} " 
                f"{'changes' if change_count > 1 else 'change'}"))

    except json.JSONDecodeError as e:
        print(errorText(f"Invalid JSON response: {e}"))
    except Exception as e:
        print(errorText(f"Error processing changes: {e}"))

def processChanges(modelResponse: str) -> int:
    """Apply changes from JSON response to files"""
    try:
        response_data = json.loads(modelResponse)
     
        file_patches = []
        if isinstance(response_data, list):
            # Iterate through all items in the list and collect changes
            for item in response_data:
                if isinstance(item, dict):
                    file_patches.extend(item.get("changes", []))
        elif isinstance(response_data, dict):
            # Handle single dictionary response
            file_patches = response_data.get("changes", [])
        else:
            print(errorText(f"Unexpected response format: {type(response_data)}"))
            return 0
        
        change_count = 0
        for patch in file_patches:
            try:
                file_path = patch['file']
              
                is_new_raw = patch.get('isNewFile', 'false')
                if isinstance(is_new_raw, bool):
                    is_new = is_new_raw
                else:
                    is_new = str(is_new_raw).lower() == 'true'
                
                replacement = patch.get('replacement', [])
                
                if is_new:
                    with open(file_path, "w", encoding='utf-8') as f:
                        f.write('\n'.join(replacement))
                    change_count += 1
                else:
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
            except Exception as e:
                print(errorText(f"Error processing patch: {e}"))
                
        return change_count
        
    except json.JSONDecodeError as e:
        print(errorText(f"Invalid JSON format: {e}"))
        return 0
    except Exception as e:
        print(errorText(f"Error processing changes: {e}"))
        return 0