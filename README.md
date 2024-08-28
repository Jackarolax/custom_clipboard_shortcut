You can create a custom shortcut for copying your desired text into the clipboard with ALT + (a key of your choice) by opening the shortcut.py file and configuring it in the ui.

Be sure to check "new file" when creating the shortcut for the first time and "extend file" when adding another shortcut to an existing file.

When you click "generate", a file will be generated that has to be run in the background for the created shortcut to be active. If the file is closed, the shortcut won't function anymore.

The keyword DATE and TIME will automatically copy in the current date and time when pressing the shortcut into the clipboard for added functionality when using it to help with doing automated commets with timestamps. 


Attention!!
you have to run the following commands in the command line, before the program can work:
pip install PyQt5
pip install pynput
pip install pyperclip