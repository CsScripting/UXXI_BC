import PackInterface.ini_main_window as iniciateMainWindow
from PackLibrary.librarys import (
    traceback,
    tk,
    messagebox
)

def run_app ():

    try:

        iniciateMainWindow.start_main_window()

    except Exception as E:  

       
       messagebox.showerror('Error', 'Contact:\n\n' + 'info@bulletsolutions.com')

       print(traceback.format_exc())