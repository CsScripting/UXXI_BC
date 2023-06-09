from PackInterface.global_object_window import (
    main_window,
    path_icon,
    names_inserted_vars,
    radio_button_vars,

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
    objectState.settings_window.geometry ("230x150") ##Geometry (230x214) --With Iten Separator
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
    doubleEntry_windowGrid = tk.Frame(objectState.settings_window)
    tripleEntry_windowGrid = tk.Frame(objectState.settings_window)
    final_WindowGrid = tk.Frame(objectState.settings_window)

    #Pack Containers Grid
    top_WindowGrid.pack(side="top", fill="x", expand=False)
    doubleEntry_windowGrid.pack(side="top", fill="both", expand=True)
    tripleEntry_windowGrid.pack(side="top", fill="both", expand=True)
    final_WindowGrid.pack(side="bottom", fill="both", expand=False)
    
    
    #Proportions Window
    top_WindowGrid.grid_columnconfigure(0, weight=1)
    top_WindowGrid.grid_columnconfigure(1, weight=3)
    final_WindowGrid.grid_columnconfigure(0, weight=3)


    #Objects inside topGrid Window:

    #Configuraciones RadioButtons

    opciones_process = tk.Frame(top_WindowGrid)
    check_data_opcion= tk.Radiobutton(opciones_process, text = 'Check Data',font="Helvetica 8", cursor="hand2", variable=radio_button_vars[0], value=0, command=objectState.opciones_choice_check_data)
    import_data_opcion= tk.Radiobutton(opciones_process, text = 'Import', font="Helvetica 8", cursor="hand2",variable=radio_button_vars[0], value=1,command=objectState.opciones_choice_import_data)
    csv_opcion= tk.Radiobutton(opciones_process, text = 'CSV', font="Helvetica 8", cursor="hand2",variable=radio_button_vars[0], value=2, command=objectState.opciones_choice_export_csv)
    check_data_opcion.select()
    
    
    # Objects Inside doubleEntry_windowGrid

    #Config label File Data UXXI
    objectState.fileLabel = tk.Label(doubleEntry_windowGrid, text='Data UXXI:', font="Helvetica 8", foreground="#000000")
    #Config textInsertion
    names_inserted_vars[0] = tk.Entry(doubleEntry_windowGrid,borderwidth=0,highlightthickness=1,highlightcolor='#ffb84d', width=23,justify='left',font=("Segoe 8"),background="#ffe6cc", disabledbackground="#d1e0e0")
    #Default Value (only for DEV !!!)
    objectState.names_inserted_vars[0].insert(0, 'HorariosPrimer_23_24.xlsx')


    #Config label File Data UXXI
    objectState.processImportLabel = tk.Label(doubleEntry_windowGrid, text='Process ID:', font="Segoe 8 italic", foreground="#009999")
    #Config textInsertion
    objectState.names_inserted_vars[1] = tk.Entry(doubleEntry_windowGrid,borderwidth=0,highlightthickness=1,highlightcolor='#ffb84d', width=23,justify='left',font=("Segoe 8"),background="#ffe6cc", disabledbackground="#d1e0e0")


    #(Opcion: export Data):
    
    objectState.exportLabel = tk.Label(doubleEntry_windowGrid, text='Export Csv:', font="Segoe 8 italic", foreground="#009999") 
    

    data_pack = tk.Frame(doubleEntry_windowGrid)
    objectState.names_inserted_vars[2] = tk.Entry(data_pack,borderwidth=0,highlightthickness=1,highlightcolor='#ffb84d', width=10,justify='left',font=("Segoe 8"),background="#ffe6cc", disabledbackground="#d1e0e0")
    objectState.names_inserted_vars[2].insert(0, 'Begin Date')
    objectState.names_inserted_vars[3] = tk.Entry(data_pack,borderwidth=0,highlightthickness=1,highlightcolor='#ffb84d', width=10,justify='left',font=("Segoe 8"),background="#ffe6cc", disabledbackground="#d1e0e0")
    objectState.names_inserted_vars[3].insert(0, 'End Date')
    
    #When Start State
    objectState.opciones_choice_check_data()
    
    

 
    #(Last Opcion Grid: Button VAlidacion and Edit)
    object_validation = tk.Frame(final_WindowGrid)
    button_validation = tk.Button(object_validation, text = 'Submit', background="#ffe6cc", borderwidth=0, cursor="hand2", command = settValid.validation_settings_steps)
    objectState.link_edit = tk.Label(object_validation, text="Edit",font=('Helvetica', 8, 'underline'), fg="#663300")
    # disable_link_edit()

     #Position Objects inside Grid 
    
    opciones_process.grid(row=0, column=0, sticky=tk.W, pady=3,padx=3)
    
    objectState.fileLabel.grid(row=1, column=0, sticky=tk.W, pady=3,padx=3 )
    objectState.names_inserted_vars[0].grid(row=1, column=1, sticky='w')
    
    objectState.processImportLabel.grid(row=2, column=0, sticky=tk.W, pady=3,padx=3 )
    names_inserted_vars[1].grid(row=2, column=1, sticky='w')
    
    objectState.exportLabel.grid(row=3, column=0, sticky=tk.W, pady=3,padx=3 )
    data_pack.grid(row=3, column=1, sticky='w')
   

    object_validation.grid(row=4, column=1, sticky=tk.W)


    #Pack Values TopGrid --- opciones
    check_data_opcion.pack(side=tk.LEFT,)
    import_data_opcion.pack(side=tk.LEFT, padx=6)
    csv_opcion.pack(side=tk.LEFT, padx=6)
    

    objectState.names_inserted_vars[2].pack(side=tk.LEFT, padx = 2)
    objectState.names_inserted_vars[3].pack(side=tk.LEFT, padx = 10)
 

    objectState.link_edit.pack(side=tk.LEFT,padx = 55)
    button_validation.pack(side=tk.LEFT, padx = 5)

    #Minimize Window
    main_window.wm_state('iconic')
    # settings_window.protocol("WM_DELETE_WINDOW", closing_behavior)

