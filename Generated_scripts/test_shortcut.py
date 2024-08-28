
#[(1.1.['test'])]
import datetime
from pynput import keyboard
import pyperclip

COMBINATIONS = [
    [keyboard.Key.alt_l, keyboard.KeyCode(char="1")],
    [keyboard.Key.alt_l, keyboard.KeyCode(char="1")]
]

current = set()
def execute():
    now = datetime.datetime.now()
    text = now.strftime("""test""")
    pyperclip.copy(text)

def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute()

def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)
        
    if key == keyboard.Key.esc:
        return(False)
        
    
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
    print(listener)

