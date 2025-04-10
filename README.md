# Jemma: Your Free Code Assistant

[![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-API-brightgreen)](https://cloud.google.com/vertex-ai/docs/generative-ai/models/gemini)
[![Colorama](https://img.shields.io/badge/colorama-terminal%20colors-brightgreen)](https://pypi.org/project/colorama/)

![jemma](jemma.jpeg)

**Description:** Jemma is a command-line tool that provides code assistance using the Google Gemini API.  It's free and easy to use.

**Installation:**

```bash
pip install .
```

**Configuration:**

Before using Jemma, you need to configure your Google Gemini API key:

```bash
jemma-configure 
```

You will be prompted to enter your API key.  This key should be stored in the  `~/.jemma/config` file. Alternatively, you can set the `GEMINI_API_KEY` environment variable.

**Usage:**

Jemma offers two main functionalities:

1. **Interactive Code Session (`jemma -s`):** Start an interactive coding session where you can ask questions and receive code suggestions.

   ```bash
   jemma -s
   ```

2. **Codebase Explanation (`jemma -e`):**  Get a detailed explanation of your current codebase, including frameworks, languages, critical logic, and potential issues.

   ```bash
   jemma -e README.md
   ```

   (Replace `README.md` with your desired output file name).


 
    

**Note:** The `.current_chat.txt` file stores the current chat history.  This file is used to maintain context during an interactive session.


## Roadmap

- [x] Fix configuration and improve the use of the configuration file
- [x] Fix edit with line enumeration
- [x] Add support for multiple models (Gemini Pro, etc.)
- [x] Implement configuration via command-line arguments
- [ ] Create command for starting new projects
- [ ] Improve error handling and logging
- [ ] Add unit tests
