import os
from pathlib import Path
 
from jemma.utils.terminalPrettifier import errorText, successText, warningText

def set_api_key():
    """Interactive configuration of the Gemini API key."""
    print (""" 

                                                                                                   
                                                                                                         
          JJJJJJJJJJJ                                                                                    
          J:::::::::J                                                                                    
          J:::::::::J                                                                                    
          JJ:::::::JJ                                                                                    
            J:::::J    eeeeeeeeeeee       mmmmmmm    mmmmmmm      mmmmmmm    mmmmmmm     aaaaaaaaaaaaa   
            J:::::J  ee::::::::::::ee   mm:::::::m  m:::::::mm  mm:::::::m  m:::::::mm   a::::::::::::a  
            J:::::J e::::::eeeee:::::eem::::::::::mm::::::::::mm::::::::::mm::::::::::m  aaaaaaaaa:::::a 
            J:::::je::::::e     e:::::em::::::::::::::::::::::mm::::::::::::::::::::::m           a::::a 
            J:::::Je:::::::eeeee::::::em:::::mmm::::::mmm:::::mm:::::mmm::::::mmm:::::m    aaaaaaa:::::a 
JJJJJJJ     J:::::Je:::::::::::::::::e m::::m   m::::m   m::::mm::::m   m::::m   m::::m  aa::::::::::::a 
J:::::J     J:::::Je::::::eeeeeeeeeee  m::::m   m::::m   m::::mm::::m   m::::m   m::::m a::::aaaa::::::a 
J::::::J   J::::::Je:::::::e           m::::m   m::::m   m::::mm::::m   m::::m   m::::ma::::a    a:::::a 
J:::::::JJJ:::::::Je::::::::e          m::::m   m::::m   m::::mm::::m   m::::m   m::::ma::::a    a:::::a 
 JJ:::::::::::::JJ  e::::::::eeeeeeee  m::::m   m::::m   m::::mm::::m   m::::m   m::::ma:::::aaaa::::::a 
   JJ:::::::::JJ     ee:::::::::::::e  m::::m   m::::m   m::::mm::::m   m::::m   m::::m a::::::::::aa:::a
     JJJJJJJJJ         eeeeeeeeeeeeee  mmmmmm   mmmmmm   mmmmmmmmmmmm   mmmmmm   mmmmmm  aaaaaaaaaa  aaaa
                                                                                                         
                                                                                                         """)
    api_key = input("Enter your Gemini API key: ").strip()
    
    if api_key:
        # Create config directory if it doesn't exist
        config_dir = Path.home() / ".jemma"
        os.makedirs(config_dir, exist_ok=True)
        
        # Write API key to config file
        with open(config_dir / "config", "w") as f:
            f.write(f"GEMINI_API_KEY={api_key}\n")
        
        print(successText(f"API key saved to {config_dir}/config"))
        print(warningText('You should probably run '+ successText(text='jemma -configure',)+ warningText(' to set preferences')))
        return True
    else:
        print(errorText("No API key provided. Configuration cancelled."))
        return False