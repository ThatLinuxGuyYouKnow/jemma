from prompt_toolkit.shortcuts import input_dialog
from prompt_toolkit.styles import Style


example_style = Style.from_dict({
    'dialog':             'bg:#88ff88',
    'dialog frame.label': 'bg:#ffffff #000000',
    'dialog.body':        'bg:#000000 #00ff00',
    'dialog shadow':      'bg:#00aa00',
})
text = input_dialog(
    title='Jemma',
    text='Enter your message:', style = example_style).run()