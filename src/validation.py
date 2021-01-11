# validation.py

import pandas as pd
import re
import os

############################################

def validate_headers(df = pd.DataFrame()):
    """
    Validates that a DataFrame object contains all the required headers to run the build operations.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame to be validated.

    Returns
    -------
    tp : tuple, of the form (boolean, list)
        The boolean indicates whether the validation has passed. The list contains the headers that were missing, if applicable.
    """
    required_headers = [ 'Handle', 'Title', 'Body (HTML)', 'Option1 Name', 'Option1 Value', 'Option2 Name', 'Option2 Value', 
                        'Option3 Name', 'Option3 Value', 'Variant Price', 'Image Src', 'Variant Grams' ]
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
        print ("Headers Validated!")                                # debug
        tp = (True, missing_headers)
    # CASE: Missing Headers
    else:
        print("We found missing headers during validation!!!")      # debug
        tp = (False, missing_headers)
    
    return tp



def check_email(email=''):
    """
    Checks if a string is in an email format.

    Parameters
    ----------
    email : str, optional
        The string value to be checked, by default ''

    Returns
    -------
    __ : bool
        Returns True if the string was in an email format, otherwise False.
    """
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return True if re.search(regex, email) else False
    
    

def sticky_note(brand='', email='', buildtype='', filepath=''):
    """
    Creates a dictionary for storing and sending necessary build information.

    Parameters
    ----------
    brand : str, optional
        The brand name, by default ''
    email : str, optional
        The vendor's email address (associated with their account), by default ''
    buildtype : str, optional
        The type of product CSV provided, by default ''
    filepath : str, optional
        The filepath of the CSV being referenced to create the product build, by default ''

    Returns
    -------
    note : dict
        Dictionary storing brand name, email, build type, and CSV filepath.
    """
    note = { 'BRAND':brand, 'EMAIL':email, 'BUILDTYPE':buildtype, 'FILEPATH':filepath }
    return note
    
    
