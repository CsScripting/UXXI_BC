from PackLibrary.librarys import (
    tk
)

import PackInterface.states_objects_windows as objectState
import PackInterface.ini_user_window as iniciatUser
import PackInterface.ini_settings_window as iniciatSett


from PackInterface.global_object_window import(
    main_window,
    path_icon) 
from mod_variables import *



def start_main_window ():
    
    
    #Proprieties Window
    main_window.geometry ("230x150")
    main_window.resizable(0, 0)
    main_window.title('Events UXXI')
    main_window.eval('tk::PlaceWindow %s center' % main_window.winfo_toplevel())
    # Window Above another Windows
    main_window.wm_attributes("-topmost", 1)

    #Manage path log to generate .exe
    main_window.iconbitmap(path_icon + '/log.ico')

    #Objects inside Window:
     
    objectState.button_start = tk.Button(main_window, text = 'START', background="#d1e0e0", borderwidth=0)
    objectState.button_start['state'] = 'disabled'
    objectState.label1_begin = tk.Label(main_window, text = '\nUXXI <-> BEST\n'+ v_version)
    objectState.label2_begin = tk.Label(main_window, text = '')
    objectState.link = tk.Label(main_window, text="Process Settings",font=('Helvetica', 8, 'underline'), fg="#663300", cursor="hand2")
    objectState.link.bind("<Button-1>", lambda e: iniciatUser.start_window_user_credential())
    objectState.label3=tk.Label()

    #Position objects inside window
    objectState.label1_begin.grid(column= 0, row = 0, pady=10)
    objectState.button_start.grid(column = 0, row = 1)
    objectState.link.grid(column=0, row=3, ipady=4)
    objectState.label2_begin.grid(column=0, row=4)

    #Center Window - position on grid
    main_window.columnconfigure(0, weight=1)
    main_window.rowconfigure(0, weight=1)
            

    main_window.mainloop()
    return()