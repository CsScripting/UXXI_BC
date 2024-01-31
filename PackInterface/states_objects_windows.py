from PackLibrary.librarys import (
    Thread,
    tk,
    messagebox,
    END
)

from PackInterface.global_object_window import (
    main_window,
    names_inserted_vars,
    radio_button_vars

)

import PackValidations.settings_validation as settval

from mod_variables import v_version
import PackInterface.ini_user_window as iniciatUser
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
global firstImportProcess
global opcionImportConector
global radio_button_first_import
global radio_button_import_conector



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
    
    # start_process execute exeProc.exe_process_steps
    valid_process = start_process(settval.gl_opcion_process_to_ejecute, settval.gl_name_file_uxxi,settval.gl_name_process_to_import, 
                                  settval.gl_event_type_process, settval.gl_date_last_update, settval.gl_check_opcion_process)

    on_stop()
   
    
    settings_window.destroy()

    if valid_process:
        messagebox.showinfo('All Files Generated', 'Check Folder .\DataProcess\BC_XML')
        update_start_window()

    main_window.deiconify()


def opciones_choice_check_data ():

    fileLabel.config (font="Helvetica 8", foreground="#000000")
    exportLabel.config (font="Segoe 8", foreground="#009999")
    processImportLabel.config (font="Segoe 8", foreground="#009999")
    firstImportProcess.config (font="Segoe 8", foreground="#009999")
    firstImportProcess.config(text = 'First Import:')
    opcionImportConector.config (font="Segoe 8", foreground="#009999")

    names_inserted_vars[1].delete(0, END)
    names_inserted_vars[2].delete(0, END)
    names_inserted_vars[3].delete(0, END)
    
    
    names_inserted_vars[1].config(state = 'disable')
    names_inserted_vars[2].config(state = 'disable')
    names_inserted_vars[3].config(state = 'disable')
    names_inserted_vars[0].config(state = 'normal')
    radio_button_first_import.config(state = 'disable')
    radio_button_import_conector.config(state = 'disable')

    radio_button_first_import.deselect()
    radio_button_import_conector.deselect()

    


def opciones_choice_import_data ():

    processImportLabel.config (font="Helvetica 8", foreground="#000000")
    firstImportProcess.grid(row=4, column=0, sticky=tk.W, pady=[0,0],padx=[3,2] )
    firstImportProcess.config(text = 'First Import:',font="Helvetica 8", foreground="#000000")
    opcionImportConector.config (font="Helvetica 8", foreground="#000000")
    exportLabel.config (font="Segoe 8", foreground="#009999")
    fileLabel.config (font="Segoe 8", foreground="#009999")
    opcionImportConector.config (font="Helvetica 8", foreground="#000000")
    processImportLabel.config(text = 'Process ID:')

    names_inserted_vars[0].delete(0, END)
    names_inserted_vars[2].delete(0, END)
    names_inserted_vars[3].delete(0, END)
    
    names_inserted_vars[0].config(state = 'disable')
    names_inserted_vars[2].config(state = 'disable')
    names_inserted_vars[3].config(state = 'disable')
    names_inserted_vars[1].config(state = 'normal')

   

    opcion_radio_button_add_conector= radio_button_vars[2].get()
    
    if opcion_radio_button_add_conector == 1:

        processImportLabel.grid(pady=3,padx=[3,8] )
        processImportLabel.config(text = 'Event Type:')
        radio_button_first_import.deselect()
        radio_button_first_import.config(state = 'disable')
        
        radio_button_import_conector.config(state = 'normal')
        radio_button_import_conector.select()

    else:
    
        radio_button_first_import.config(state = 'normal')
        radio_button_first_import.select()
        radio_button_import_conector.config(state = 'disable')
        radio_button_import_conector.deselect()



def opciones_choice_export_csv ():

    exportLabel.config (font="Helvetica 8", foreground="#000000")
    fileLabel.config (font="Segoe 8", foreground="#009999")
    processImportLabel.config (font="Segoe 8", foreground="#009999")
    firstImportProcess.grid(row=4, column=0, sticky=tk.W, pady=[0,0],padx=[3,0] )
    firstImportProcess.config(text = 'First Export:',font="Helvetica 8", foreground="#000000")

    names_inserted_vars[0].delete(0, END)
    names_inserted_vars[1].delete(0, END)
    
    
    names_inserted_vars[0].config(state = 'disable')
    names_inserted_vars[1].config(state = 'disable')
    names_inserted_vars[2].config(state = 'normal')
    names_inserted_vars[3].config(state = 'disable')

    
    radio_button_first_import.config(state = 'normal')
    radio_button_first_import.select()
    names_inserted_vars[2].insert(0, 'Event Type')
    opcionImportConector.config (font="Segoe 8", foreground="#009999")
    radio_button_import_conector.config(state = 'disable')
    radio_button_import_conector.deselect()


    

def all_opciones_disables_after_submit():

    names_inserted_vars[0].config(state = 'disable')
    names_inserted_vars[1].config(state = 'disable')
    names_inserted_vars[2].config(state = 'disable')
    names_inserted_vars[3].config(state = 'disable')
    check_data_opcion.config(state = 'disable')
    import_data_opcion.config(state = 'disable')
    firstImportProcess.config (font="Segoe 8", foreground="#009999")
    opcionImportConector.config (font="Segoe 8", foreground="#009999")
    radio_button_import_conector.config(state = 'disable')
    radio_button_first_import.config(state = 'disable')

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


def remove_opciones_import_schedules():

    opcion_radio_button_add_conector= radio_button_vars[2].get()

    if opcion_radio_button_add_conector == 1:

        radio_button_first_import.deselect()
        firstImportProcess.config (font="Segoe 8", foreground="#009999")

        names_inserted_vars[1].delete(0, END)
        radio_button_first_import.config(state = 'disable')
        processImportLabel.grid(pady=3,padx=[3,8] )
        processImportLabel.config(text = 'Event Type:')
        
        

    else:

        radio_button_first_import.deselect()
        firstImportProcess.config (font="Helvetica 8", foreground="#000000")
        radio_button_first_import.config(state = 'normal')
        processImportLabel.grid(pady=3,padx=[3,10] )
        processImportLabel.config(text = 'Process ID:')
        names_inserted_vars[1].delete(0, END)


def opciones_choice_first_import_and_first_export (): # CHECK COMPORTAMENTOS DISTINTOS CONFORME É IMPORT OU EXPORT

    verifiy_opcion_process = radio_button_vars[0].get()
    verifiy_opcion_first_import = radio_button_vars[1].get()

    if ((verifiy_opcion_process == 1) & (verifiy_opcion_first_import == 1)): #SE IMPORT E OPÇÂO FIRST IMPORT Seleccionada

        radio_button_import_conector.deselect()
        radio_button_import_conector.config(state = 'disable')
        opcionImportConector.config (font="Helvetica 8", foreground="#009999")

    elif ((verifiy_opcion_process == 1) & (verifiy_opcion_first_import == 0)): #SE IMPORT E OPÇÂO FIRST IMPORT Deselecionado

       
        radio_button_import_conector.config(state = 'normal')
        opcionImportConector.config (font="Helvetica 8", foreground="#000000")


    elif ((verifiy_opcion_process == 2) & (verifiy_opcion_first_import == 1)): #SE EXPORT E OPÇÂO FIRST EXPORT Selecionado

        names_inserted_vars[3].delete(0, END)
        names_inserted_vars[3].config(state = 'disable')
        



    elif ((verifiy_opcion_process == 2) & (verifiy_opcion_first_import == 0)): #SE EXPORT E OPÇÂO FIRST EXPORT DesSelecionado

        names_inserted_vars[3].config(state = 'normal')
        names_inserted_vars[3].insert(0, 'yyyy-mm-dd')
        

    

        





        











   
    
    




    
    
    

