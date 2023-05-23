from PackInterface.global_object_window import (
    main_window,
    path_icon,
    names_inserted_vars,
    radio_button_vars

)

import PackInterface.states_objects_windows as objectState 
import PackValidations.settings_validation as settValid

from PackLibrary.librarys import (
    tk
)

def start_settings_window():

    global button_validation
      
    objectState.disable_link_settings()

    objectState.settings_window = tk.Toplevel()
    objectState.settings_window.title('Settings')
    objectState.settings_window.geometry ("230x112") ##Geometry (230x214) --With Iten Separator
    objectState.settings_window.resizable(0, 0)
    objectState.settings_window.iconbitmap(path_icon + '/log.ico')

    #Center Window(eval not available to object TopLevel):
    windowWidth = objectState.settings_window.winfo_reqwidth()
    windowHeight = objectState.settings_window.winfo_reqheight()
    positionRight = int(objectState.settings_window.winfo_screenwidth()/3 - windowWidth/3)
    positionDown = int(objectState.settings_window.winfo_screenheight()/2 - windowHeight/2)

    objectState.settings_window.geometry("+{}+{}".format(positionRight, positionDown))

    #Containers to distinct grid
    top_WindowGrid = tk.Frame(objectState.settings_window)
    bottom_WindowGrid = tk.Frame(objectState.settings_window)
    # check_Section_WindowGrid = tk.Frame(objectState.settings_window)

    #Pack Containers Grid
    top_WindowGrid.pack(side="top", fill="x", expand=False)
    bottom_WindowGrid.pack(side="bottom", fill="both", expand=True)
    # check_Section_WindowGrid.pack(side="bottom", fill="x", expand=False)
    
    #Proportions Window
    top_WindowGrid.grid_columnconfigure(0, weight=1)
    top_WindowGrid.grid_columnconfigure(1, weight=3)

    #Objects inside topGrid Window:

    #Config label File Data UXXI
    fileLabel = tk.Label(top_WindowGrid, text='Data UXXI:', font="Segoe 8 italic", foreground="#009999")
    #Config textInsertion
    names_inserted_vars[0] = tk.Entry(top_WindowGrid,borderwidth=0,highlightthickness=1,highlightcolor='#ffb84d', width=23,justify='left',font=("Segoe 8"),background="#ffe6cc", disabledbackground="#ffe6cc")
    #Default Value (only for DEV !!!)
    names_inserted_vars[0].insert(0, 'DatosUXXI.xlsx')


    #Config Opcion Manage Data
    manage_data_object = tk.Frame(bottom_WindowGrid)
    label_manage_data= tk.Label(manage_data_object, text='Man Data:', font="Segoe 8 italic", foreground="#009999")
    #Config Opcion Manage Data
    opcion_manage_data = tk.Checkbutton (manage_data_object, variable = radio_button_vars[0])
    opcion_manage_data.select()

    #Config Opcion Update Data
    update_data_object = tk.Frame(bottom_WindowGrid)
    label_update_data = tk.Label(update_data_object, text='Update Data:', font="Segoe 8 italic", foreground="#009999")
    #Config Opcion Manage Data
    opcion_update_data = tk.Checkbutton (update_data_object,variable = radio_button_vars[1])
    opcion_update_data.select()

    #(Opcion: Import Data):
    import_data_obejct = tk.Frame(bottom_WindowGrid)
    label_import = tk.Label(bottom_WindowGrid, text='Import Data:', font="Segoe 8 italic", foreground="#009999") 
    opcion_import_data = tk.Checkbutton (import_data_obejct, variable = radio_button_vars[2]) #, command= manage_entry_historic) 
    names_inserted_vars[1] = tk.Entry(import_data_obejct,borderwidth=0,highlightthickness=1,highlightcolor='#ffb84d', width=18,justify='left',font=("Segoe 8"),background="#ffe6cc", disabledbackground="#d1e0e0")
    # disable_entry_event_type()
    names_inserted_vars[1].insert(0, '')
    

 
    #(Last Opcion Grid: Button VAlidacion and Edit)
    aggregate_object_validation = tk.Frame(bottom_WindowGrid)
    button_validation = tk.Button(aggregate_object_validation, text = 'Submit', background="#ffe6cc", borderwidth=0, cursor="hand2", command = settValid.validation_settings_steps)
    objectState.link_edit = tk.Label(aggregate_object_validation, text="Edit",font=('Helvetica', 8, 'underline'), fg="#663300")
    # disable_link_edit()

     #Position Objects inside TopGrid 
    fileLabel.grid(row=0, column=0, sticky=tk.W, pady=5,padx=3 )
    names_inserted_vars[0].grid(row=0, column=1, sticky='w')


    manage_data_object.grid(row=1, column=0,sticky=tk.W, pady=5,padx=3 )
    update_data_object.grid(row=1, column=1,sticky=tk.W, pady=5,padx=3 )
    

    label_import.grid(row=2, column=0, sticky=tk.W, padx=3)
    import_data_obejct.grid (row=2, column=1, sticky=tk.W)
    aggregate_object_validation.grid(row=3, column=1, sticky=tk.W)


    #pack Values agregatted inside same column Grid

    label_manage_data.pack(side=tk.LEFT)
    opcion_manage_data.pack(side=tk.LEFT)
    label_update_data.pack(side=tk.LEFT)
    opcion_update_data.pack(side=tk.LEFT)
    


    #pack Values agregatted inside same column Grid
    opcion_import_data.pack(side=tk.LEFT, padx=6)
    names_inserted_vars[1].pack(side=tk.LEFT)



    objectState.link_edit.pack(side=tk.LEFT,  padx= 7)
    button_validation.pack(side=tk.LEFT, padx=55)

    #Minimize Window
    main_window.wm_state('iconic')
    # settings_window.protocol("WM_DELETE_WINDOW", closing_behavior)