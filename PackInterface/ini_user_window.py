from PackLibrary.librarys import (
    
    tk
)
from PackInterface.global_object_window import (  
    
    path_icon,
    names_inserted_vars,
    

)


import PackInterface.states_objects_windows as objectState
import PackValidations.user_validation as userValid


def start_window_user_credential():

    objectState.disable_link_settings()
    objectState.user_window = tk.Toplevel()
    objectState.user_window.title('Sign in')
    objectState.user_window.geometry ("210x125")
    objectState.user_window.resizable(0, 0)
    
    #Center Window(eval not available to object TopLevel):
    windowWidth = objectState.user_window.winfo_reqwidth()
    windowHeight = objectState.user_window.winfo_reqheight()
    positionRight = int(objectState.user_window.winfo_screenwidth()/1.97 - windowWidth/1.97)
    positionDown = int(objectState.user_window.winfo_screenheight()/1.95 - windowHeight/1.95)

    objectState.user_window.geometry("+{}+{}".format(positionRight, positionDown))
    objectState.user_window.iconbitmap(path_icon + '/log.ico')

    #Containers to distinct grid
    doubleEntry_windowGrid = tk.Frame(objectState.user_window)
    doubleButton_windowGrid = tk.Frame(objectState.user_window)

    #Pack Containers Grid
    doubleEntry_windowGrid.pack(side="top", fill="x", expand=False)
    doubleButton_windowGrid.pack(side="top", fill="both", expand=True)

    #Proportions Window
    doubleEntry_windowGrid.grid_columnconfigure(0, weight=1)
    doubleButton_windowGrid.grid_columnconfigure(0, weight=1)

    # Objects Inside doubleEntry_windowGrid

    #Config label USER NAME
    objectState.user_name_label = tk.Label(doubleEntry_windowGrid, text='User:', font="Helvetica 8", foreground="#000000")
    #Config textInsertion
    names_inserted_vars[4] = tk.Entry(doubleEntry_windowGrid,borderwidth=0,highlightbackground = '#d3d3d3',highlightthickness=1,highlightcolor='#ffb84d', width=23,justify='left',font=("Segoe 8"),background="#FFFFFF", disabledbackground="#d1e0e0")
    #Default Value (only for DEV !!!)
    objectState.names_inserted_vars[4].insert(0, 'paulovirgilio.79@gmail.com')

    #Config label PASSWORD
    objectState.password_label = tk.Label(doubleEntry_windowGrid, text='Password:', font="Helvetica 8", foreground="#000000")
    #Config textInsertion
    names_inserted_vars[5] = tk.Entry(doubleEntry_windowGrid,show = '*', borderwidth=0,highlightthickness=1,highlightbackground = '#d3d3d3',highlightcolor='#ffb84d', width=23,justify='left',font=("Segoe 8"),background="#FFFFFF", disabledbackground="#d1e0e0")
    #Default Value (only for DEV !!!)
    objectState.names_inserted_vars[5].insert(0, 'Password123!')

    #CONFIG BUTTON OK SIGN IN

    objectState.button_ok_sign_in = tk.Button(doubleButton_windowGrid, text = 'OK', font=("Segoe 8"), background='#d3d3d3', borderwidth=0, cursor="hand2", command=userValid.user_validation_steps)
    objectState.button_cancel_sign_in = tk.Button(doubleButton_windowGrid, text = 'CANCEL', font=("Segoe 8"), background='#d3d3d3', borderwidth=0, cursor="hand2", command=objectState.closing_behavior_user_window)


    #Position Objects inside Grid 
    objectState.user_name_label.grid(row=0, column=0, sticky=tk.W, pady = [20,13], padx= [2,0] )
    objectState.names_inserted_vars[4].grid(row=0, column=1, sticky='w', pady = [20,13],padx= [2,5] )

    objectState.password_label.grid(row=1, column=0, sticky=tk.W  ,padx= [4,0])
    objectState.names_inserted_vars[5].grid(row=1, column=1, sticky='w',padx=[2,11] )

    

    objectState.button_ok_sign_in.grid(row=2, column=0, sticky=tk.W,ipady=0, ipadx=30, padx=[20,7], pady=20 )
    objectState.button_cancel_sign_in.grid(row=2, column=1, sticky=tk.W,ipady=0, ipadx=17, padx=[7, 20], pady=20)

    objectState.button_ok_sign_in.bind('<Enter>', objectState.focus_button_ok)
    objectState.button_ok_sign_in.bind('<Leave>', objectState.without_focus_button_ok)

    objectState.button_cancel_sign_in.bind('<Enter>', objectState.focus_button_cancel)
    objectState.button_cancel_sign_in.bind('<Leave>', objectState.without_focus_button_cancel)

    objectState.user_window.attributes('-topmost', 'true')
    objectState.user_window.protocol("WM_DELETE_WINDOW", objectState.closing_behavior_user_window)

    

    return()