# excel.py

import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font
# from openpyxl.styles.colors import Color
# from openpyxl.styles.fills import PatternFill


def to_excel(brandname, folder_loc, dict_of_df):
    """
    Creates an Excel workbook with seperate sheets for each DataFrame object
    (named accordingly). Each sheet also gets styling (font & colorfill), as
    well as any extra blank columns (those w/o a header value) removed.

    Parameters
    ----------
    brandname : str
        The brand name used for file naming.
    folder_loc : str
        The location / path of the directory to store the file in.
    dict_of_df : dict
        A dictionary of DataFrame objects to convert to Excel worksheets.
    """
    wkbk = openpyxl.Workbook()              # Create Workbook object
    default_sheets = wkbk.sheetnames        # Create a list of sheet names

    # [1] Create the necessary Sheets and name them.
    for i, key in enumerate(dict_of_df.keys()):
        if (i < len(default_sheets)):
            sheet_name = default_sheets[i]
            active_sheet = wkbk[sheet_name]
        else:
            sheet_name = None

        # CASE: Change name of an existing sheet.
        if (sheet_name in default_sheets):
            active_sheet.title = key
        # CASE: No more defaults sheets. Add new sheet with a specific name.
        else:
            wkbk.create_sheet(index=i, title=key)

    # [2] Fill in Sheets with Formatted DataFrames.
    for key, df in dict_of_df.items():
        ws = wkbk[key]      # Select Sheet

        for row in dataframe_to_rows(df, index=False, header=True):
            ws.append(row)

    # [3] Style the Headers Because I'm Fancy.
    FONT_STYLE = Font(name='Arial', size=10, bold=True)    # Arial 10pt Bold
    # col_width = 100
    # row_height = 21

    # Color Constants:
    RED = 'FA5E52'
    PURPLE = 'C89DD1'
    DARKPURPLE = '9B78CC'
    TEAL = '9CC9D9'
    GREEN = '85C771'
    ORANGE = 'EDB561'
    YELLOW = 'F0EB69'

    color_dict = {"LINE SHEET": None,
                  "EDIT": None,
                  "MASTER IMPORT": {"A1": PURPLE,
                                    "B1": PURPLE,
                                    "C1": TEAL,
                                    "D1": GREEN,
                                    "E1": PURPLE,
                                    "F1": PURPLE,
                                    "G1": RED,
                                    "H1": RED,
                                    "I1": None,
                                    "J1": None,
                                    "K1": None,
                                    "L1": None,
                                    "M1": None,
                                    "N1": None,
                                    "O1": GREEN,
                                    "P1": YELLOW,
                                    "Q1": ORANGE
                                    },
                  "SKU KEY": {"A1": DARKPURPLE,
                              "B1": PURPLE
                              },
                  "IMAGE KEY": {"A1": PURPLE,
                                "B1": PURPLE,
                                "C1": PURPLE,
                                "D1": PURPLE,
                                "E1": ORANGE},
                  "IMAGE IMPORT": {"A1": PURPLE,
                                   "B1": PURPLE,
                                   "C1": PURPLE,
                                   "D1": PURPLE,
                                   "E1": ORANGE},
                  # "DEFAULTS": {},
                  # "VARIANTS": {}
                  }

    # Run through each sheet and style with font and colorfill.
    for key, value in color_dict.items():

        # CASE: No Color Styling Defines --> Go To Next Sheet
        if (value is None):
            continue

        # CASE: Colorfill Specified
        else:
            # Select worksheet
            ws = wkbk[key]
            # Iterator for column references
            col_iter = 1

            # Iterate through cells in the first row and apply font.
            for cell in ws['1:1']:
                # CASE) Cell Contains some value --> Apply Font!
                if (cell.value):
                    cell.font = FONT_STYLE
                # CASE) Cell contains no value --> Delete the Column
                else:
                    ws.delete_cols(col_iter)
                # Increase iterator
                col_iter += 1
        '''
            # Iterate through first row and apply colorfill from color_dict.
            for cell_range, color_const in value.items():
                # Store the cell location
                cell = ws[cell_range]
                # Apply the fill style to the cell.
                cell.fill = PatternFill(bgColor=color_const,
                                        fill_type="solid")
        '''
    # Create Workbook Name & Save Location
    workbk_nm = f"products - {brandname}"
    save_loc = f"{folder_loc}\{workbk_nm}.xlsx"  # noqa: W605

    # Save workbook to save_loc
    wkbk.save(save_loc)

    # Return the location we saved the workbook to.
    return save_loc
