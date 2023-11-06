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
    

def extract_value_dict (x):

    try:
        value_dict = x.get(v_dict_id_uxxi)
        
        return value_dict   
    except Exception as e:
        
        return 'InvalidConector'

