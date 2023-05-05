from PackInterface.global_object_window import (
    main_window,
    path_icon,
    names_inserted_vars,
    radio_button_vars

)
from PackLibrary.librarys import (
    tk
)

def start_settings_window():

    global button_validation
    global opcion_historic
    global link_edit
    

    # disable_link_settings()
    

    # Proprieties Window
    global settings_window
    settings_window = tk.Toplevel()
    settings_window.title('Settings')
    settings_window.geometry ("230x112") ##Geometry (230x214) --With Iten Separator
    settings_window.resizable(0, 0)
    settings_window.iconbitmap(path_icon + '/log.ico')

    #Center Window(eval not available to object TopLevel):
    windowWidth = settings_window.winfo_reqwidth()
    windowHeight = settings_window.winfo_reqheight()
    positionRight = int(settings_window.winfo_screenwidth()/3 - windowWidth/3)
    positionDown = int(settings_window.winfo_screenheight()/2 - windowHeight/2)

    settings_window.geometry("+{}+{}".format(positionRight, positionDown))

    #Containers to distinct grid
    top_WindowGrid = tk.Frame(settings_window)
    bottom_WindowGrid = tk.Frame(settings_window)
    # check_Section_WindowGrid = tk.Frame(settings_window)

    #Pack Containers Grid
    top_WindowGrid.pack(side="top", fill="x", expand=False)
    bottom_WindowGrid.pack(side="bottom", fill="both", expand=True)
    # check_Section_WindowGrid.pack(side="bottom", fill="x", expand=False)
    
    #Proportions Window
    top_WindowGrid.grid_columnconfigure(0, weight=1)
    top_WindowGrid.grid_columnconfigure(1, weight=3)

    #Objects inside topGrid Window:

    #Config label File Events
    fileLabel = tk.Label(top_WindowGrid, text='File Events:', font="Segoe 8 italic", foreground="#009999")
    #Config textInsertion
    names_inserted_vars[0] = tk.Entry(top_WindowGrid,borderwidth=0,highlightthickness=1,highlightcolor='#ffb84d', width=23,justify='left',font=("Segoe 8"),background="#ffe6cc", disabledbackground="#ffe6cc")
    #Default Value (only for DEV !!!)
    names_inserted_vars[0].insert(0, 'UPO_All_Events_Primer_22_23.csv')


    #Config label File Student Groups
    file_student_group = tk.Label(top_WindowGrid, text='BEST Data:', font="Segoe 8 italic", foreground="#009999")
    #Config textInsertion
    names_inserted_vars[1] = tk.Entry(top_WindowGrid,borderwidth=0,highlightthickness=1,highlightcolor='#ffb84d', width=23,justify='left',font=("Segoe 8"),background="#ffe6cc", disabledbackground="#ffe6cc")
    #Default Value (only for DEV !!!)
    names_inserted_vars[1].insert(0, 'DataBestUPO.xlsx')

    #(First Opcion: With ID):
    agregate_object_historic = tk.Frame(bottom_WindowGrid)
    insert_historic = tk.Label(bottom_WindowGrid, text='File Class:', font="Segoe 8 italic", foreground="#009999") 
    opcion_historic = tk.Checkbutton (agregate_object_historic, variable = radio_button_vars[0]) #, command= manage_entry_historic) 
    names_inserted_vars[2] = tk.Entry(agregate_object_historic,borderwidth=0,highlightthickness=1,highlightcolor='#ffb84d', width=18,justify='left',font=("Segoe 8"),background="#ffe6cc", disabledbackground="#d1e0e0")
    # disable_entry_event_type()
    names_inserted_vars[2].insert(0, 'AddClassrooms_202301.xlsx')
    

 
    #(Last Opcion Grid: Button VAlidacion and Edit)
    aggregate_object_validation = tk.Frame(bottom_WindowGrid)
    button_validation = tk.Button(aggregate_object_validation, text = 'Submit', background="#ffe6cc", borderwidth=0, cursor="hand2") #, command = data_validation)
    link_edit = tk.Label(aggregate_object_validation, text="Edit",font=('Helvetica', 8, 'underline'), fg="#663300")
    # disable_link_edit()

     #Position Objects inside TopGrid 
    fileLabel.grid(row=0, column=0, sticky=tk.W, pady=5,padx=3 )
    names_inserted_vars[0].grid(row=0, column=1, sticky='w')
    file_student_group.grid(row=1, column=0, sticky=tk.W, pady=5,padx=3 )
    names_inserted_vars[1].grid(row=1, column=1, sticky='w')

    insert_historic.grid(row=2, column=0, sticky=tk.W, padx=3)
    agregate_object_historic.grid (row=2, column=1, sticky=tk.W)
    aggregate_object_validation.grid(row=3, column=1, sticky=tk.W)

    #pack Values agregatted inside same column Grid
    opcion_historic.pack(side=tk.LEFT, padx=6)
    names_inserted_vars[2].pack(side=tk.LEFT)
    link_edit.pack(side=tk.LEFT,  padx= 35)
    button_validation.pack(side=tk.LEFT, padx=15)

    main_window.wm_state('iconic')
    # settings_window.protocol("WM_DELETE_WINDOW", closing_behavior)