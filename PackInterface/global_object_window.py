from PackLibrary.librarys import (
    tk,
    os,
    sys
)

#Manage Main Window
global main_window
main_window = tk.Tk()

#Manage Icon used on Main Window and Settings Window

def resource_path(relative_path):
    
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path)

global path_icon 
path_icon = resource_path("./log.ico")

global names_inserted_vars
names_inserted_vars = []
for i in range(3):

    check_names = tk.StringVar
    names_inserted_vars.append(check_names)

#Save on list distinct INT opciones (RadioButtones, CheckBoxes)
global radio_button_vars 
radio_button_vars= []
for j in range(1):

    check_radio_button = tk.IntVar()
    radio_button_vars.append(check_radio_button)
