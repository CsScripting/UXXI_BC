from PackLibrary.librarys import (	
  DataFrame,
  ast
)


from mod_variables import *

#When parsing String - Represantation Dict to Dict  
def parse_string_dict_to_dict (x):

    try:
        
        return ast.literal_eval(str(x))   
    
    except Exception as e:
        
        return 'InvalidConector'
    

def extract_value_dict (x, field_to_get):

    try:
        value_dict = x.get(field_to_get)
        
        if value_dict == None:

            value_dict = 'InvalidFieldConector'

        return value_dict   
    
    except Exception as e:
        
        return 'InvalidFiedlConector'
    






