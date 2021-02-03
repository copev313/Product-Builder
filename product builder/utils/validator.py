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
    required_headers = ['Handle', 'Title', 'Body (HTML)',
                        'Option1 Name', 'Option1 Value',
                        'Option2 Name', 'Option2 Value',
                        'Option3 Name', 'Option3 Value',
                        'Variant Price', 'Image Src',
                        'Variant Grams'
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
        print("DEBUG: Headers Validated!")  # debug
        return (True, missing_headers)
    # CASE: Missing Headers
    else:
        print("DEBUG: We found missing headers during validation!!!")  # debug
        return (False, missing_headers)


def check_email(email=''):
    """
    Checks if a string is in an email format.

    Parameters
    ----------
    email : str, optional
        The string value to be checked, by default ''

    Returns
    -------
    bool
        Returns True if the string is in an email format, otherwise False.
    """
    raw = r"^[a-zA-Z0-9._%+-]{3,}[@][a-zA-Z0-9-.]{2,}[.][a-zA-Z]{2,4}$"
    regex = re.compile(raw)
    return True if re.search(regex, email) else False


def sticky_note(brand='', email='', buildtype='Shopify', filepath=''):
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
        Dictionary storing the brand name, email, build type, and CSV filepath.
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
        The brand name used for the folder's name, by default ''
    mainfolder : str, optional
        The main workspace in the user's directory to create the folder,
        by default 'Downloads'.

    Returns
    -------
    directory_location: str
        The path where the directory was created.
    """
    # "C:Users/{username}"
    currentuser = os.path.expanduser("~")

    # Default Directory Location
    dir_loc = f"{currentuser}\{mainfolder}\{brandname}"  # noqa: W605

    # Returns bool - Whether the folder exists already in the given location.
    folder_exists = os.path.isdir(dir_loc)

    # Initialize just in case we need an alternative save location.
    new_dir_loc = ''

    # Iterator used to make name unique.
    i = 1

    # Handle Naming in Case of FileExistsError
    while folder_exists:
        # Change the name with an iterating number.
        new_dir_loc = f"{dir_loc} ({i})"
        # Re-evaluate if the folder exists.
        folder_exists = os.path.isdir(new_dir_loc)
        i += 1

    # Once Directory Location is Confirmed Unique --> Create Directory
    try:
        # CASE: Alternate Folder Path Was Created.
        if (new_dir_loc):
            dir_loc = new_dir_loc
        # CASE: No Alternate Path Needed -- Use Default Path
        else:
            pass

        # Create the Directory in the Proper Location w/ Read/Write Permissions
        os.makedirs(dir_loc, mode=0o666)
        print(f"DEBUG: Successfully created directory: {dir_loc}")  # debug

    except FileExistsError:
        print(f"ERR: This folder already exist in: {mainfolder}")  # debug

    return dir_loc


# NOTE: MAY NOT NEED TO STORE AS CSV FILES AFTER ALL (MAY JUST KEEP AS BACKUPS)
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
    # Stores each DataFrame as a CSV in the folder's location.
    try:
        for key, df in dict_of_df.items():
            path = f"{folder_loc}\products - {brandname} - {key}.csv"  # noqa
            df.to_csv(path, header=True, index=False)

    except FileNotFoundError as err:
        print(f"Error! -- {err}")
