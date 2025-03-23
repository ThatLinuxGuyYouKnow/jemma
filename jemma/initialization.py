def initializeJemma():
    with open(".jemma-config.toml","w") as f:
     print('What model would you like jemma to use')
     print(' 1 for Gemini 2.0')
     print(' 2 for Gemini2.0-Flash')
     model_selection = input('>')
     if model_selection != '1' or '2':
       print('Enter a valid option')
       initializeJemma()
     if model_selection=='1':
        f.write('model : Gemini 2.0')
     if model_selection == '2':
        f.write('model : Gemini 2.0 Flash')
    