from PackLibrary.librarys import (
    Thread,
    tk,
    messagebox
)

from PackInterface.global_object_window import (
    main_window,
)

import PackValidations.settings_validation as settval

from mod_variables import v_version
import PackInterface.ini_settings_window as iniciateSettings
import PackValidations.exe_process_validation as exeProc

link : str
link_edit : str

global settings_window
global button_start
global label1_begin
global label2_begin
global label3


# Not Used 
def raise_above_all(window):
    window.attributes('-topmost', True)


# - Behavior Link Settings (Main Window ) - #

def enable_link_settings():

    link["state"] = "normal"
    link.config(cursor= "hand2")
    link.bind("<Button-1>", lambda e: iniciateSettings.start_settings_window())


def disable_link_settings():

    link['state'] = 'disabled'
    link.config(cursor= "")
    link.unbind('<Button-1>')

# - Behavior Button START (Main Window) - #

def enable_button_start():

    main_window.wm_attributes("-topmost", 1)
    button_start['state'] = 'normal'
    button_start['background'] = '#ffe6cc'
    button_start ['cursor']="hand2"
    button_start.config(command = on_click_two_threads)

def disable_button_start():

    button_start['state'] = 'disable'
    button_start['background'] = '#d1e0e0'
    button_start ['cursor']=""


def disable_link_edit():

    link_edit["state"] = 'disable'
    link_edit.unbind('<Button-1>')

def run_thread(name, func):

    Thread(target=status_running, args=(name, func)).start()    
     
def on_click_two_threads():
    
    # update_start_window() Check Where need to Use
    disable_link_edit()
    run_thread('process', exeProc.exe_process_steps)

def update_start_window():

    label1_begin.config(text='Events UXXI to BC\n\n-- BEST API --\n'+ v_version,)
    label2_begin.config (text = '')
    label3.config(text = '')
    
    disable_button_start()
    label3.grid_remove()
    #Position objects inside window
    label1_begin.grid(column= 0, row = 0)
    button_start.grid(column = 0, row = 1)
    link.grid(column=0, row=3, ipady=4)
    label2_begin.grid(column=0, row=4)
    enable_link_settings()

    #Center Window - position on grid
    main_window.columnconfigure(0, weight=1)
    main_window.rowconfigure(0, weight=1)
    

def status_running (name, start_process):

    def on_start():
        global running
        running = True


    def on_stop():
        global running
        running = False

    on_start()
    
    if running:

        #Not Fix Window on center...
        main_window.overrideredirect(False)

        label1_begin.config(text='Events UXXI to BC\n\n-- BEST API --\n'+ v_version)
        label2_begin.config (text = 'Running')
        label3 = tk.Label(main_window, text = '....', font =(20)) 

        label1_begin.grid(column= 0, row = 0)
        label2_begin.grid (column = 0, row = 1)
        label3.grid(column = 0, row = 2,ipady=5)
        link.grid_remove()

        main_window.columnconfigure(0, weight=1)
        main_window.rowconfigure(0, weight=1)
        main_window.update()

    

    def update_status_running ():

        if running:
            # Get the current message
            current_status = label3["text"]

            if current_status.endswith("...."): current_status = ""

            # If not, then just add a "." on the end
            else: current_status += "."

            # Update the message
            label3["text"] = current_status

            # After 1 second, update the status
            main_window.after(1000, update_status_running)
            
    
    main_window.after(0, update_status_running) 

    valid_process = start_process(settval.gl_name_file_inserted, settval.gl_opcion_manage_data,settval.gl_opcion_update_data, 
                                 settval.gl_opcion_import_data, settval.gl_name_process_to_import)

    on_stop()
    # main_window.withdraw()
    update_start_window()
    settings_window.destroy()

    if valid_process:
        messagebox.showinfo('All Files Generated', 'Check Folder .\DataProcess\BC_XML')

    main_window.deiconify()
    # main_window.after(10, main_window.destroy)

