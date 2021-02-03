# app.py

import pandas as pd
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog
import webbrowser

from utils import validator as validation   # TODO: Rename/Refactor file name
from utils import drive
from utils import excel
from builder.shopify import shopify_builder
# from builder.etsy import etsy_builder

# * * * * * * * *  GLOBAL VARIABLES  * * * * * * * * * * * * *
FILEPATH = ''
STICKY_NOTE = None
QED = None

# * * * * * * * *  STYLING CONSTANTS  * * * * * * * * * * * * *
ICON_LOC = 'icon.png'
WINDOW_TITLE = "Product Builder  (Alpha 2.0)"
WINDOW_WIDTH, WINDOW_HEIGHT = (320, 218)

BTN_PADDING = 5
BTN_BORDER = 4
BTN_FONT_FAMILY = 'Segoe UI'
ENTRY_WIDTH = 35
COMBOBOX_WIDTH = 18

# * * * * * * * *  CREATE UI OBJECTS  * * * * * * * * * * * * *

# Window:
ROOT = tk.Tk()
ROOT.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
ROOT.title(WINDOW_TITLE)
ROOT.iconphoto(False, tk.PhotoImage(file=ICON_LOC))

# Tabs:
tabControl = ttk.Notebook(ROOT)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tabControl.add(tab1, text='  Step 1  ')
tabControl.add(tab2, text='  Step 2  ')
tabControl.add(tab3, text='  Step 3  ')

# Labels (TAB 2):
build_label = tk.Label(tab2, text="Type: ")
brand_label = tk.Label(tab2, text="Brand: ")
vendor_label = tk.Label(tab2, text="Email: ")

# Text Fields (TAB 2):
# Default Text Entry Values
brand_name_var = tk.StringVar(value="MY SOCKIES")
vendor_email_var = tk.StringVar(value="eat.my.shorts@yoohoo.org")

brand_name_field = tk.Entry(tab2,
                            width=ENTRY_WIDTH,
                            textvariable=brand_name_var)
vendor_email_field = tk.Entry(tab2,
                              width=ENTRY_WIDTH,
                              textvariable=vendor_email_var)

# * * * * * * * *  BUTTON FUNCTIONS  * * * * * * * * * * * * *


# Select CSV Event (TAB 1):
def select_csv():
    try:
        # Save the Name of CSV Filepath to Create a DataFrame
        global FILEPATH
        filetypes = (('csv file', '*.csv'), ('csv file', '*.csv'))
        FILEPATH = filedialog.askopenfilename(initialdir='/Desktop',
                                              title='Select a CSV file',
                                              filetypes=filetypes)
        df = pd.read_csv(FILEPATH)

        # Validate Headers
        returned_tuple = validation.validate_headers(df)

        # CASE: Missing Necessary Headers
        if(not returned_tuple[0]):
            missing_list = returned_tuple[1]
            slip = ''
            for x in missing_list:
                slip += f"+ {x}\n"

            # Form the error message
            p1 = "The CSV is missing the following required header(s): "
            err_msg = f"{p1}\n\n{slip}"
            messagebox.showerror("CSV Format Error", err_msg)

        # CASE: Empty DataFrame
        elif(len(df) == 0):
            messagebox.showwarning('Problemo!',
                                   'The selected CSV has no rows.')
        # CASE: ...or else
        else:
            pass

    # CATCH: Invalid Filepath--
    except FileNotFoundError as err:
        r = err.replace('[Errno 2]', 'ERR:')
        messagebox.showerror('Error in opening file!',
                             f"Select a valid CSV file to continue.\n\n{r}")
    # CATCH: Empty Data Error--
    except pd.errors.EmptyDataError as err:
        messagebox.showwarning('Empty Data Error!', err)


# Submit Input Event (TAB 2):
def submit_input():
    global FILEPATH
    brand = brand_name_var.get().strip()
    email = vendor_email_var.get().strip()
    buildtype = build_var.get()

    try:
        df = pd.read_csv(FILEPATH)
        returned_tuple = validation.validate_headers(df)

    except FileNotFoundError as err:
        r = err.replace('[Errno 2]', 'ERR:')
        err_str = f"Please select a CSV file in Step 1.\n\n{r}"
        messagebox.showwarning("Warning -- File Not Found", err_str)
        # End process
        return

    # Some input validation...
    # CASE: Empty Brand Name
    if(brand == ""):
        messagebox.showwarning("Warning -- More Info Required",
                               "No brand name specified.")
    # CASE: Email Invalid
    elif(not validation.check_email(email)):
        messagebox.showwarning("Warning -- Info Validation",
                               "The email address entered is invalid.")
    # CASE: Missing Headers
    elif(not returned_tuple[0]):
        messagebox.showerror("CSV Format Error",
                             "The CSV is missing required headers.")
    # CASE: Empty DataFrame
    elif(len(df) == 0):
        messagebox.showwarning('Problemo!', 'The selected CSV has no rows.')
    # CASE: Looks Good
    else:
        # Confirm User's Input:
        confirm = messagebox.askyesno('Confirmation',
                                      "Is the following information correct?" +
                                      f"\n\nBrand Name:    {brand}" +
                                      f"\nVendor Email:  {email}" +
                                      f"\nBuild Type:       {buildtype}" +
                                      f"\n\nCSV's Filepath:\n{FILEPATH}"
                                      )
        # YES --
        if(confirm):
            messagebox.showinfo('Complete', 'Information Submitted!')
            # Empty text fields.
            brand_name_var.set('')
            vendor_email_var.set('')
            print('DEBUG: Information Submitted!')  # debug

            # Store Important Info to Send to Builder
            global STICKY_NOTE
            STICKY_NOTE = validation.sticky_note(brand,
                                                 email,
                                                 buildtype,
                                                 FILEPATH)
        # NO --
        else:
            messagebox.showinfo('Confirmation', 'Process cancelled.')


# Convert CSV Event (TAB 3):
def convert_csv():
    global STICKY_NOTE
    # CASE: Input Confirmed and Submitted
    if(STICKY_NOTE is not None):
        confirm = messagebox.askyesno('Confirmation',
                                      'Would like to proceed?')
        # YES --
        if(confirm):
            build_type = STICKY_NOTE["BUILDTYPE"]
            print("DEBUG: Conversion Confirmed for Takeoff!")  # debug
            global QED

            # CASE: Shopify Build
            if(build_type == 'Shopify'):
                # Store a dict of formatted DataFrames into *global* var QED.
                QED = shopify_builder(STICKY_NOTE)

            '''
            # CASE: Etsy Build
            elif(build_type == 'Etsy'):
                QED = etsy_builder(STICKY_NOTE)
            '''

            # Piece together strings and stats for Completion Message.
            p1 = "The CSV is converted and is ready to export."
            p2 = "[Statistics -- Coming Soon!]"

            # TODO: Add Stats Information to Message
            s1 = "• number_of_rows_processed."
            s2 = "• execution_time_in_seconds."
            s3 = "• num_defaults_and_variants_ratio."
            s4 = "• number_of_option_columns_created."
            complete_msg = f"{p1}\n\n{p2}\n\n {s1}\n {s2}\n {s3}\n {s4}"

            # Prompt Completion Message & Build Stats
            messagebox.showinfo('Complete!', complete_msg)

        # NO --
        else:
            messagebox.showinfo('Confirmation', 'Process cancelled')

    # CASE: Step 2 Not Confirmed
    else:
        warn_msg = "Confirm and submit the information in Step 2 to continue."
        messagebox.showwarning('More Info Required', warn_msg)


# Export CSV Event (TAB 3):
def export_csv():
    global QED
    global STICKY_NOTE

    # CASE: Cannot Export Yet...
    if(QED is None):
        messagebox.showwarning('Warning -- Conversion Not Complete!',
                               'You must convert the CSV before you can ' +
                               'export the files.')
    # CASE: Converted and Ready to Export
    else:
        # Define variables necessary for making the directory.
        brandname = STICKY_NOTE["BRAND"]
        mainfolder = 'Desktop'

        # Generate prompt message / warning
        m0 = 'Please note that exporting this product build will:'
        m1 = f'- Create a folder in/on your {mainfolder}.'
        m2 = '- Create a Google Sheet in your Drive (permissions required).'
        m3 = '- Open the new Sheet in the browser.'
        m4 = 'Would you still like to continue?'
        glue_str = f'{m0}\n\n{m1}\n{m2}\n{m3}\n\n{m4}'
        prompt = messagebox.askyesno('BEFORE YOU EXPORT!', glue_str)

        # Process Confirmation:
        if (prompt):
            # [1] Create Folder & Store the its Path
            folder_loc = validation.create_brand_folder(brandname=brandname,
                                                        mainfolder=mainfolder)

            # [2] Throw DataFrames into an Excel document.
            excel_doc_loc = excel.to_excel(brandname, folder_loc, QED)

            # [3] Send Excel workbook to Google Sheets.
            title = f"products - {brandname} [created with 🐍]"
            gsheet_url = drive.google_drive(upload_file_loc=excel_doc_loc,
                                            title=title)

            '''
            # Store CSVs in the Folder
            validation.store_csvs(brandname=brandname,
                                folder_loc=folder_loc,
                                dict_of_df=QED)
            '''
            # [4] Open the new Google sheet in the browser.
            webbrowser.open(url=gsheet_url, new=2)


# * * * * * * *  CREATE BUTTON & DROPDOWN OBJECTS  * * * * * * * * * * * *

# Buttons
choose_csv_btn = tk.Button(tab1,
                           text="Select CSV",
                           command=select_csv,
                           bg='#FFAC14',   # orange
                           font=(BTN_FONT_FAMILY, 12, 'bold'),
                           padx=BTN_PADDING,
                           pady=BTN_PADDING,
                           bd=BTN_BORDER)

submit_btn = tk.Button(tab2,
                       text="Submit",
                       command=submit_input,
                       bg='#19D5EE',       # light blue
                       font=(BTN_FONT_FAMILY, 10, 'bold'),
                       padx=BTN_PADDING,
                       pady=1,
                       bd=BTN_BORDER
                       )

convert_btn = tk.Button(tab3,
                        text="Convert CSV",
                        command=convert_csv,
                        bg='#9AD259',       # green
                        font=(BTN_FONT_FAMILY, 12, 'bold'),
                        padx=BTN_PADDING,
                        pady=BTN_PADDING,
                        bd=BTN_BORDER
                        )

export_btn = tk.Button(tab3,
                       text="Export CSVs",
                       command=export_csv,
                       bg='#BA45CE',       # purple
                       font=(BTN_FONT_FAMILY, 12, 'bold'),
                       padx=BTN_PADDING,
                       pady=BTN_PADDING,
                       bd=BTN_BORDER
                       )

# Dropdown Menu
build_var = tk.StringVar()
bvalues = ['Shopify',
           # 'Etsy',
           # 'Wix',
           # 'Square',
           # 'WooCommerce',
           # 'BigCommerce'
           ]

build_combobox = ttk.Combobox(tab2,
                              width=COMBOBOX_WIDTH,
                              values=bvalues,
                              textvariable=build_var,
                              state='readonly'
                              )

# * * * * * * *  LAYOUT WIDGETS / UI COMPONENTS  * * * * * * * * * *

# == TAB BAR ==
tabControl.grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)

# | TAB1 |
choose_csv_btn.grid(row=1, column=2, pady=65, padx=100)

# | TAB2 |
brand_label.grid(row=1, column=0, padx=5, pady=15)
brand_name_field.grid(row=1, column=1, padx=5, pady=15)

vendor_label.grid(row=2, column=0, padx=5, pady=5)
vendor_email_field.grid(row=2, column=1, padx=5, pady=5)

build_label.grid(row=3, column=0, padx=5, pady=15)
build_combobox.grid(row=3, column=1, padx=5, pady=15, sticky=tk.W)
build_combobox.current(0)       # Sets default selection to the first option

submit_btn.grid(row=4, column=1, padx=70, pady=8, sticky=tk.W)

# | TAB3 |
convert_btn.grid(row=0, column=0, padx=90, pady=30)
export_btn.grid(row=1, column=0, padx=90, pady=0)

# Infinite Window Loop:
ROOT.mainloop()
