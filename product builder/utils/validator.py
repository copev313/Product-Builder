# validation.py

import os
import pandas as pd
import re

# - - - - - - - - - - - - - - - - - - - - - - - -


def validate_headers(df=pd.DataFrame()):
    """
    Validates that a DataFrame object contains all the required headers
    to run the build operations.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame to be validated.

    Returns
    -------
    tp : tuple, of the form (boolean, list)
        The boolean indicates whether the validation has passed. The list
        contains the headers that were missing, if applicable.
    """
    required_headers = ['Handle', 'Title', 'Body (HTML)', 'Option1 Name',
                        'Option1 Value', 'Option2 Name', 'Option2 Value',
                        'Option3 Name', 'Option3 Value', 'Variant Price',
                        'Image Src', 'Variant Grams'
                        ]
    included_headers = df.columns
    missing_headers = []

    for header in required_headers:
        # CASE) Header NOT FOUND (Add to missing headers list)
        if (header not in included_headers):
            missing_headers.append(header)
        # CASE) Header Found
        else:
            pass

    # CASE: No Missing Headers
    if (len(missing_headers) == 0):
        print("Headers Validated!")  # debug
        tp = (True, missing_headers)
    # CASE: Missing Headers
    else:
        print("We found missing headers during validation!!!")  # debug
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
    regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    return True if re.search(regex, email) else False


def sticky_note(brand='', email='', buildtype='', filepath=''):
    """
    Creates a dictionary for storing and sending necessary build information.

    Parameters
    ----------
    brand : str, optional
        The brand name, by default ''
    email : str, optional
        The vendor's email address (associated with their account),
        by default ''.
    buildtype : str, optional
        The type of product CSV provided, by default ''
    filepath : str, optional
        The filepath of the CSV being referenced to create the product build,
        by default ''.

    Returns
    -------
    dict
        Dictionary storing brand name, email, build type, and CSV filepath.
    """
    return {'BRAND': brand, 'EMAIL': email,
            'BUILDTYPE': buildtype, 'FILEPATH': filepath}


def create_brand_folder(brandname='', mainfolder='Downloads'):
    """
    Creates a directory in 'mainfolder' of the users folder
    named 'brandname'.

    Parameters
    ----------
    brandname : str, optional
        The brand name, by default ''
    mainfolder : str, optional
        The main folder in the user's directory to create the folder,
        by default 'Downloads'.

    Returns
    -------
    directory_location: str
        The path where the directory was created.
    """
    # "C:Users/{username}"
    currentuser = os.path.expanduser("~")
    # Default Directory Location
    directory_location = "{cu}\{mf}\{bn}".format(cu=currentuser,
                                                 mf=mainfolder,
                                                 bn=brandname)
    # Returns bool - Whether The Folder Exists Already in the Given Location
    folder_exists = os.path.isdir(directory_location)
    # Iterator used to make name unique
    i = 1

    # Handle Naming in Case of FileExistsError
    while folder_exists:
        # Alter the Name with Iterating Number
        directory_location = directory_location + " ({int})".format(int=i)
        folder_exists = os.path.isdir(directory_location)
        i += 1

    # Create Directory
    try:
        # this mode allows read/write file operations in the created directory
        os.mkdir(directory_location, mode=0o666)
        print("Successfully created directory: " + directory_location)  # debug
    except FileExistsError:
        print("Error! This folder seems to already exist in: Downloads.")

    return directory_location


def store_csvs(brandname, folder_loc, dict_of_df):
    """
    Stores DataFrame values from a dictionary as CSV files in a folder
    at 'folder_loc'.

    Parameters
    ----------
    brandname : str
        The brand name.
    folder_location : str
        The path to the folder's location
    dict_of_df : dict (of the form: {str: pandas.DataFrame})
        A dictionary storing formatted DataFrames.
    """
    # Store each DataFrame as CSV in the folder
    try:
        for key, value in dict_of_df.items():
            pathway = "{fl}\products - {bn} - {k}.csv".format(fl=folder_loc,
                                                              bn=brandname,
                                                              k=key)
            value.to_csv(pathway, header=True, index=False)
    except FileNotFoundError as err:
        print("Error! " + err)
