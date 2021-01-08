# validation.py

import pandas as pd
import re

############################################

def validate_headers(df):
        required_headers = [ 'Handle', 'Title', 'Body (HTML)', 'Option1 Name', 'Option1 Value', 'Option2 Name', 'Option2 Value', 
                            'Option3 Name', 'Option3 Value', 'Variant Price', 'Image Src', 'Variant Grams'
                            ]
        included_headers = df.columns
        missing_headers = []
        for header in required_headers:
            # CASE: Header NOT FOUND (Add to list)
            if (header not in included_headers): 
                missing_headers.append(header)
            
            # CASE: Header Found
            else: 
                pass
        
        # CASE: No Missing Headers
        if (len(missing_headers) == 0):
            print ("Headers Validated!")
            return (True, missing_headers)
        # CASE: Missing Headers
        else:
            print("We found missing headers during validation!!!")
            return (False, missing_headers)



def check_email(email=''):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        return True if re.search(regex, email) else False
    
    

def sticky_note(brand='', email='', buildtype='', filepath=''):
        note = { 'BRAND':brand, 'EMAIL':email, 'BUILDTYPE':buildtype, 'FILEPATH':filepath }
        return note
    
    

