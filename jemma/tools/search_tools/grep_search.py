import subprocess
import json


def search_in_files(search_term: str, path :str, file_type: str | None):

    """
    Args
        search_term: the specific search term / pattern to search for
        path: path to search in, allows for searching out of current dir
        file_type: specific file type to search for
    """

    cmd = ["rg", "--json", search_term, path]

    if file_type:

        ## searching for a specific extension

        cmd += ["--type", file_type]

    result: subprocess.CompletedProcess[str] = subprocess.run(cmd, capture_output=True, text = True)

    matches = []

    for line in result.stdout.splitlines():

        msg = json.loads(line)

        if msg["type"] == "match":

            data = msg["data"]

            matches.append({

                "file": data["path"]["text"],
                "line": data["line_number"],
                "content": data["lines"]["text"].strip()

            })


    if not matches:
        matches.append('no matches found')

    return json.dumps(matches, indent = 2)

