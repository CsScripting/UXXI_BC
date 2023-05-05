from PackLibrary.librarys import (
    tk
)
from PackInterface.global_object_window import(
    resource_path
)

import PackInterface.ini_settings_window as iniciateSettings
from PackInterface.global_object_window import main_window
from mod_variables import *



def start_main_window ():
    
    #path used on log secundary window
    global path_icon
    global link
    global button_start
    global label1_begin
    global label2_begin
    
    
    #Proprieties Window
    main_window.geometry ("230x150")
    main_window.resizable(0, 0)
    main_window.title('Events XML')
    main_window.eval('tk::PlaceWindow %s center' % main_window.winfo_toplevel())
    main_window.wm_attributes("-topmost", 1)

    #Manage path log to generate .exe
    path_icon = resource_path("./log.ico")
    main_window.iconbitmap(path_icon + '/log.ico')

    #Objects inside Window:
     
    button_start = tk.Button(main_window, text = 'START', background="#d1e0e0", borderwidth=0)
    button_start['state'] = 'disabled'
    label1_begin = tk.Label(main_window, text = 'Events BC to BTT\n\n-- AGG XML --\n'+ v_version)
    label2_begin = tk.Label(main_window, text = '')
    link = tk.Label(main_window, text="Process Settings",font=('Helvetica', 8, 'underline'), fg="#663300", cursor="hand2")
    link.bind("<Button-1>", lambda e: iniciateSettings.start_settings_window())

    #Position objects inside window
    label1_begin.grid(column= 0, row = 0, pady=10)
    button_start.grid(column = 0, row = 1)
    link.grid(column=0, row=3, ipady=4)
    label2_begin.grid(column=0, row=4)

    #Center Window - position on grid
    main_window.columnconfigure(0, weight=1)
    main_window.rowconfigure(0, weight=1)
            

    main_window.mainloop()
    return()