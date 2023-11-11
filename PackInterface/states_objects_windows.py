from PackLibrary.librarys import (
    Thread,
    tk,
    messagebox
)

from PackInterface.global_object_window import (
    main_window,
    names_inserted_vars

)

import PackValidations.settings_validation as settval

from mod_variables import v_version
import PackInterface.ini_user_window as iniciatUser
import PackInterface.ini_settings_window as iniciateSettings
import PackValidations.exe_process_validation as exeProc


global settings_window
global button_start
global label1_begin
global label2_begin
global label3
global fileLabel
global processImportLabel
global exportLabel
global button_validation
global check_data_opcion
global import_data_opcion
global csv_opcion
global object_validation

#WINDOW USER BWP
global user_window
global password_label
global user_name_label
global button_ok_sign_in
global button_cancel_sign_in



link : str
link_edit : str



# Not Used 
def raise_above_all(window):
    window.attributes('-topmost', True)

# - BEHAVIOR BUTTON GENERAL - #


def focus_button_ok(e):
    
    button_ok_sign_in.config(background='#ffdba6', foreground = "#3D85C6")

def without_focus_button_ok(e):
    
    button_ok_sign_in.config(background= '#d3d3d3', foreground= 'black')

def focus_button_cancel(e):
    
    button_cancel_sign_in.config(background='#ffdba6', foreground = "#3D85C6")

def without_focus_button_cancel(e):
    
    button_cancel_sign_in.config(background= '#d3d3d3', foreground= 'black')




# - Behavior Link Settings (Main Window ) - #

def enable_link_settings():

    link["state"] = "normal"
    link.config(cursor= "hand2")
    link.bind("<Button-1>", lambda e: iniciatUser.start_window_user_credential())


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
    link_edit.config(cursor= "")
    link_edit.unbind('<Button-1>')
    

def enable_link_edit():


    link_edit["state"] = 'normal'
    link_edit.config(cursor= "hand2")
    link_edit.bind("<Button-1>", lambda e: edit_opciones_window_settings())
    
    

def disable_button_submit():

    global button_validation

    button_validation['state'] = 'disable'
    button_validation['background'] = '#d1e0e0'
    button_validation ['cursor']=""
    
    


def enable_button_submit():

    button_validation['state'] = 'normal'
    button_validation['background'] = '#ffe6cc'
    button_validation ['cursor']="hand2"



def run_thread(name, func):

    Thread(target=status_running, args=(name, func)).start()    
     
def on_click_two_threads():
    
    # update_start_window() Check Where need to Use
    disable_link_edit()
    run_thread('process', exeProc.exe_process_steps)

def update_start_window():

    global label3

    disable_button_start()
    label2_begin.config (text = '')
    label3.config(text = '')
    label3.grid_remove()

    #Position objects inside window
    label1_begin.grid(column= 0, row = 0, pady=[10,0])
    button_start.grid(column = 0, row = 1)
    link.grid(column=0, row=3, ipady=4)
    label2_begin.grid(column=0, row=4)

    #Center Window - position on grid
    main_window.columnconfigure(0, weight=1)
    main_window.rowconfigure(0, weight=1)

    enable_link_settings()
    

def status_running (name, start_process):

    global label3

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

        label1_begin.config(text='\nUXXI <-> BEST\n'+ v_version)
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

    valid_process = start_process(settval.gl_opcion_process_to_ejecute, settval.gl_name_file_uxxi,settval.gl_name_process_to_import, 
                                 settval.gl_academic_year_process, settval.gl_date_last_update)

    on_stop()
   
    
    settings_window.destroy()

    if valid_process:
        messagebox.showinfo('All Files Generated', 'Check Folder .\DataProcess\BC_XML')
        update_start_window()

    main_window.deiconify()


def opciones_choice_check_data ():

    fileLabel.config (font="Helvetica 8", foreground="#000000")
    exportLabel.config (font="Segoe 8 italic", foreground="#009999")
    processImportLabel.config (font="Segoe 8 italic", foreground="#009999")
    
    names_inserted_vars[1].config(state = 'disable')
    names_inserted_vars[2].config(state = 'disable')
    names_inserted_vars[3].config(state = 'disable')
    names_inserted_vars[0].config(state = 'normal')

    


def opciones_choice_import_data ():

    processImportLabel.config (font="Helvetica 8", foreground="#000000")
    exportLabel.config (font="Segoe 8 italic", foreground="#009999")
    fileLabel.config (font="Segoe 8 italic", foreground="#009999")
    
    names_inserted_vars[0].config(state = 'disable')
    names_inserted_vars[2].config(state = 'disable')
    names_inserted_vars[3].config(state = 'disable')
    names_inserted_vars[1].config(state = 'normal')

    


def opciones_choice_export_csv ():

    exportLabel.config (font="Helvetica 8", foreground="#000000")
    fileLabel.config (font="Segoe 8 italic", foreground="#009999")
    processImportLabel.config (font="Segoe 8 italic", foreground="#009999")
    
    names_inserted_vars[0].config(state = 'disable')
    names_inserted_vars[1].config(state = 'disable')
    names_inserted_vars[2].config(state = 'normal')
    names_inserted_vars[3].config(state = 'normal')

    names_inserted_vars[2].delete(0, 'end')
    names_inserted_vars[3].delete(0, 'end')

    names_inserted_vars[2].insert(0, '2023_24 Primer')
    names_inserted_vars[3].insert(0, 'yyyy-mm-dd')

    

def all_opciones_disables_after_submit():

    names_inserted_vars[0].config(state = 'disable')
    names_inserted_vars[1].config(state = 'disable')
    names_inserted_vars[2].config(state = 'disable')
    names_inserted_vars[3].config(state = 'disable')
    check_data_opcion.config(state = 'disable')
    import_data_opcion.config(state = 'disable')
    csv_opcion.config(state = 'disable')
    enable_link_edit()


def edit_opciones_window_settings():


    if settval.gl_opcion_process_to_ejecute == 0:

        opciones_choice_check_data()
    
    elif settval.gl_opcion_process_to_ejecute ==1:

        opciones_choice_import_data()

    else:

        opciones_choice_export_csv()

    check_data_opcion.config(state = 'normal')    
    import_data_opcion.config(state = 'normal')
    csv_opcion.config(state = 'normal')
    disable_button_start()
    enable_button_submit()
    disable_link_edit()


def closing_behavior_settings():
 
    if messagebox.askokcancel("Close Settings", "Do you want to quit? \n\n All SETTINGS Values Will Be LOST !!"):

        enable_link_settings()
        disable_button_start()
        settings_window.destroy()
        main_window.state('normal')


def closing_behavior_user_window():

    enable_link_settings()
    user_window.destroy()


    



   
    
    




    
    
    

