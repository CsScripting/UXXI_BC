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
    doubleEntry_windowGrid_botton = tk.Frame(objectState.settings_window)
    tripleEntry_windowGrid = tk.Frame(objectState.settings_window)
    final_WindowGrid = tk.Frame(objectState.settings_window)

    #Pack Containers Grid
    top_WindowGrid.pack(side="top", fill="x", expand=False)
    doubleEntry_windowGrid.pack(side="top", fill="both", expand=True)
    tripleEntry_windowGrid.pack(side="top", fill="both", expand=True)
    doubleEntry_windowGrid_botton.pack(side="top", fill="both", expand=True)
    final_WindowGrid.pack(side="bottom", fill="both", expand=False)
    
    
    #Proportions Window
    top_WindowGrid.grid_columnconfigure(0, weight=1)
    top_WindowGrid.grid_columnconfigure(1, weight=3)
    final_WindowGrid.grid_columnconfigure(0, weight=3)


    #Objects inside topGrid Window:

    #Configuraciones RadioButtons

    opciones_process = tk.Frame(top_WindowGrid)
    objectState.check_data_opcion= tk.Radiobutton(opciones_process, text = 'Check Data',font="Helvetica 8", cursor="hand2", variable=radio_button_vars[0], value=0, command=objectState.opciones_choice_check_data)
    objectState.import_data_opcion= tk.Radiobutton(opciones_process, text = 'Import', font="Helvetica 8", cursor="hand2",variable=radio_button_vars[0], value=1,command=objectState.opciones_choice_import_data)
    objectState.csv_opcion= tk.Radiobutton(opciones_process, text = 'CSV', font="Helvetica 8", cursor="hand2",variable=radio_button_vars[0], value=2, command=objectState.opciones_choice_export_csv)
    objectState.check_data_opcion.select()
    
    
    # Objects Inside doubleEntry_windowGrid

    #Config label File Data UXXI
    objectState.fileLabel = tk.Label(doubleEntry_windowGrid, text='Data UXXI:', font="Helvetica 8", foreground="#000000")
    #Config textInsertion
    names_inserted_vars[0] = tk.Entry(doubleEntry_windowGrid,borderwidth=0,highlightbackground = '#d3d3d3',highlightthickness=1,highlightcolor='#ffb84d', width=23,justify='left',font=("Segoe 8"),background="#FFFFFF", disabledbackground="#d1e0e0")
    #Default Value (only for DEV !!!)
    objectState.names_inserted_vars[0].insert(0, 'horarios_2023_24_pruebas.csv')


    #Config label File Data UXXI
    objectState.processImportLabel = tk.Label(doubleEntry_windowGrid, text='Process ID:', font="Segoe 8 italic", foreground="#009999")
    #Config textInsertion
    objectState.names_inserted_vars[1] = tk.Entry(doubleEntry_windowGrid,borderwidth=0,highlightbackground = '#d3d3d3',highlightthickness=1,highlightcolor='#ffb84d', width=23,justify='left',font=("Segoe 8"),background="#FFFFFF", disabledbackground="#d1e0e0")


    #(Opcion: export Data):
    
    objectState.exportLabel = tk.Label(doubleEntry_windowGrid, text='Export Csv:', font="Segoe 8 italic", foreground="#009999") 
    

    data_pack = tk.Frame(doubleEntry_windowGrid)
    objectState.names_inserted_vars[2] = tk.Entry(data_pack,borderwidth=0,highlightbackground = '#d3d3d3',highlightthickness=1,highlightcolor='#ffb84d', width=11,justify='left',font=("Segoe 8"),background="#FFFFFF", disabledbackground="#d1e0e0")
    objectState.names_inserted_vars[2].insert(0, 'Acad. year')
    objectState.names_inserted_vars[3] = tk.Entry(data_pack,borderwidth=0,highlightbackground = '#d3d3d3',highlightthickness=1,highlightcolor='#ffb84d', width=11,justify='left',font=("Segoe 8"),background="#FFFFFF", disabledbackground="#d1e0e0")
    objectState.names_inserted_vars[3].insert(0, 'Last Update')

     #(Opcion First Import):
    objectState.firstImportProcess = tk.Label(doubleEntry_windowGrid_botton, text='First Import:', font="Helvetica 8", foreground="#000000") 
    objectState.radio_button_first_import = tk.Checkbutton (doubleEntry_windowGrid_botton, variable = radio_button_vars[1]) 



    
    #When Start State
    objectState.opciones_choice_check_data()
    
    

 
    #(Last Opcion Grid: Button VAlidacion and Edit)
    objectState.object_validation = tk.Frame(final_WindowGrid)
    objectState.button_validation = tk.Button(objectState.object_validation, text = 'Submit', font=("Segoe 8"), background='#ffe6cc', borderwidth=0, cursor="hand2", command = settValid.validation_settings_steps)
    objectState.link_edit = tk.Label(objectState.object_validation, text="Edit",font=('Helvetica', 8, 'underline'), fg="#663300")
    objectState.disable_link_edit()

    


     #Position Objects inside Grid 
    
    opciones_process.grid(row=0, column=0, sticky=tk.W, pady=0,padx=3)
    
    objectState.fileLabel.grid(row=1, column=0, sticky=tk.W, pady=3,padx=[3,10] )
    objectState.names_inserted_vars[0].grid(row=1, column=1, sticky='w')
    
    objectState.processImportLabel.grid(row=2, column=0, sticky=tk.W, pady=3,padx=[3,10] )
    names_inserted_vars[1].grid(row=2, column=1, sticky='w')
    
    objectState.exportLabel.grid(row=3, column=0, sticky=tk.W, pady=[3,0],padx=[3,0] )
    data_pack.grid(row=3, column=1, sticky='w',pady=[3,0], padx=[0,0])

    objectState.firstImportProcess.grid(row=4, column=0, sticky=tk.W, pady=[0,0],padx=[3,2] )
    objectState.radio_button_first_import.grid(row=4, column=1, sticky=tk.W, pady=[0,0],padx=[2,0] )
   

    objectState.object_validation.grid(row=5, column=1, sticky=tk.W)


    #Pack Values TopGrid --- opciones
    objectState.check_data_opcion.pack(side=tk.LEFT,)
    objectState.import_data_opcion.pack(side=tk.LEFT, padx=6)
    objectState.csv_opcion.pack(side=tk.LEFT)
    

    objectState.names_inserted_vars[2].pack(side=tk.LEFT)
    objectState.names_inserted_vars[3].pack(side=tk.LEFT, padx = [3,0])
 

    objectState.link_edit.pack(side=tk.LEFT,padx = [0,42], pady = [0,12])
    objectState.button_validation.pack(side=tk.LEFT, ipady=0, ipadx=9, padx = [0,10], pady = [0,12])

    #Minimize Window
    # main_window.wm_state('iconic')
    objectState.settings_window.protocol("WM_DELETE_WINDOW", objectState.closing_behavior_settings)

