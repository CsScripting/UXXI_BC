from PackLibrary.librarys import (
    tk,
    os,
    sys
)

# Objectos de janelas que podem mudar de estado inseridos em modulo states_objects_windows !!


# - Manage Main Window - #
main_window = tk.Tk()


# - Manage Icon used on Main Window and Settings Window - #

def resource_path(relative_path):
    
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path)

 
path_icon = resource_path("./log.ico")


# - Variables to Save Input´s User - #

#Save Values Inserted by User (Boxes)
names_inserted_vars = []
for i in range(6):

    check_names = tk.StringVar
    names_inserted_vars.append(check_names)

#Save on list distinct INT opciones (RadioButtones, CheckBoxes)
radio_button_vars= []
for j in range(3):

    check_radio_button = tk.IntVar()
    radio_button_vars.append(check_radio_button)




