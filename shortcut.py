import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
import os.path

global_shortcut = ""
global_text = ""


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(500, 200, 800, 800)
        self.setWindowTitle("custom shortcut")
        self.setWindowIcon(QIcon("channel.jpg"))
        self.setToolTip("custom shortcut")

        self.label_Zwischenablage = QtWidgets.QLabel(self)
        self.label_Zwischenablage.setText("What should be copied into the clipboard : ")
        self.label_Zwischenablage.resize(250,20)
        self.label_Zwischenablage.move(10,50)

        self.label_DATE = QtWidgets.QLabel(self)
        self.label_DATE.setText("DATE = Current Date ")
        self.label_DATE.resize(250,20)
        self.label_DATE.move(10,80)

        self.label_TIME = QtWidgets.QLabel(self)
        self.label_TIME.setText("TIME = Current time ")
        self.label_TIME.resize(250,20)
        self.label_TIME.move(10,110)

        self.textBox = QtWidgets.QPlainTextEdit(self)
        self.textBox.resize(500,400)
        self.textBox.move(250, 50)
        
        self.label_shortcut = QtWidgets.QLabel(self)
        self.label_shortcut.setText("Alt +  ")
        self.label_shortcut.move(10,200)

        self.shortcut = QtWidgets.QLineEdit(self)
        self.shortcut.resize(20,30)
        self.shortcut.setMaxLength(1)
        self.shortcut.move(40, 200)

        self.label_attention = QtWidgets.QLabel(self)
        self.label_attention.setText('   "    and ' + "   '    are not valid ")
        self.label_attention.resize(400,20)
        self.label_attention.move(10,230)

        self.label_filename = QtWidgets.QLabel(self)
        self.label_filename.setText("filename: ")
        self.label_filename.move(10,300)

        self.filename_text = QtWidgets.QPlainTextEdit(self)
        self.filename_text.resize(150,30)
        self.filename_text.move(80, 300)

        self.radiobutton_new = QtWidgets.QRadioButton(self)
        self.radiobutton_new.move(20, 340)
        self.radiobutton_new.setText("new file")
        self.radiobutton_new.toggled.connect(self.toggle_new)

        self.radiobutton_append = QtWidgets.QRadioButton(self)
        self.radiobutton_append.move(20, 360)
        self.radiobutton_append.setText("extend file")
        self.radiobutton_append.toggled.connect(self.toggle_append)

        self.generate = QtWidgets.QPushButton(self)
        self.generate.setText("generate")
        self.generate.move(90, 400)
        self.generate.clicked.connect(self.save_shortcut) 

        self.chosen_shortcut = ""
        self.shortcut_copy = ""
        self.written_text = ""
        self.new_file = True
        self.file_name = ""
        self.show()

    def toggle_new(self):
        self.new_file = True

    def toggle_append(self):
        self.new_file = False

    def save_shortcut(self):
        self.chosen_shortcut = self.shortcut.text()
        self.written_text = self.textBox.toPlainText()
        self.check_shortcut()


    def check_shortcut(self):
        allowed_symbols = "!§$%&/()=?ß*#+,.-;:_"

        if self.chosen_shortcut.isnumeric():
            self.shortcut_copy = self.chosen_shortcut
        
        elif self.chosen_shortcut in allowed_symbols:
            self.shortcut_copy = self.chosen_shortcut
        
        elif self.chosen_shortcut.isalpha():

            if self.chosen_shortcut.isupper():
                self.shortcut_copy = self.chosen_shortcut.lower()

            elif self.chosen_shortcut.islower():
                self.shortcut_copy = self.chosen_shortcut.upper()

        else:
            raise Exception("Combination invalid")
            # do something to signal you cant chose that as a shortcut
        self.checktext()
    
    def checktext(self):
        self.written_text = self.written_text.replace("DATE", "%d.%m.%Y")
        self.written_text = self.written_text.replace("TIME", "%H:%M")
        self.write_file()

    def write_file(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        


        self.file_name = "Generated_scripts/" + self.filename_text.toPlainText() + ".py"

        if os.path.isfile(self.file_name) and not self.new_file:
            self.append_file()
            return



        
        with open(self.file_name, 'w') as file:
            file.write(
        '''
#[({}.{}.{})]
import datetime
from pynput import keyboard
import pyperclip

COMBINATIONS = [
    [keyboard.Key.alt_l, keyboard.KeyCode(char="{}")],
    [keyboard.Key.alt_l, keyboard.KeyCode(char="{}")]
]

current = set()
def execute():
    now = datetime.datetime.now()
    text = now.strftime("""{}""")
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

'''.format(self.chosen_shortcut, self.shortcut_copy, self.written_text.split("\n"),
           self.chosen_shortcut, self.shortcut_copy, self.written_text))
    
    def append_file(self):
        with open(self.file_name, "r") as file:
            previous_infos = file.readlines()[1][1:-1] #the 1: takes out the "#" and the :-1 takes out the "/n"

        self.next_infos = previous_infos[:-1] + ";({}.{}.{})]".format(self.chosen_shortcut,self.shortcut_copy,self.written_text.split("\n"))
        previous_infos = previous_infos.strip("][").split(";") #muss ich wahrscheinlich noch ändern, wenn mehere previous infos da sind

        previous_infos_right_format = []
        for i,info in enumerate(previous_infos):
            temporary_info = [info[1],info[3],info[5:-1]]
            previous_infos_right_format.append(temporary_info[:-1])
            text = ""
            for line in temporary_info[-1].strip("][").replace("'", "").replace(" ", "").split(","):#because the text is splitted up in lines, we have to format them as well
                text += (line + "\n")
            previous_infos_right_format[i].append(text[:-1])

        previous_infos_right_format.append([self.chosen_shortcut, self.shortcut_copy,self.written_text])
        self.xth_shortcut = len(previous_infos_right_format)#just the number that keeps up with how myna shortcuts there are

        print(previous_infos_right_format)
        print(previous_infos)
        print(previous_infos_right_format[1])
        print(previous_infos_right_format[1][0])
        self.combinations = ""
        self.if_statements = ""
        for i,info in enumerate(previous_infos_right_format):
            self.combinations +=  '[keyboard.Key.alt_l, keyboard.KeyCode(char="{}")], [keyboard.Key.alt_l, keyboard.KeyCode(char="{}")],\n'.format(info[0],info[1])
            self.if_statements +=  '    if number == {}: text = now.strftime("""{}""")\n'.format(i, info[2])

        self.combinations = self.combinations[:-2]#removes the las comma
        print(self.combinations)
        print(self.if_statements)

        with open(self.file_name, 'w') as file:
            file.write(
        '''
#{}
import datetime
from pynput import keyboard
import pyperclip

COMBINATIONS = [
    {}
]
current = set()
def execute(number):
    now = datetime.datetime.now()
{}
    pyperclip.copy(text)

def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        for i in range({}):
            if all(k in current for k in COMBINATIONS[2*i]) or all(k in current for k in COMBINATIONS[(2*i)+1]):
                execute(i)

def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)
        
    if key == keyboard.Key.esc:
        return(False)
        
    
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
    print(listener)

'''.format(self.next_infos, self.combinations, self.if_statements, self.xth_shortcut))

app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())