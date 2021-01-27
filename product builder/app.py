# app.py

import pandas as pd
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog

from utils import validator as validation
from builder.shopify import shopify_builder
# from builder.etsy import etsy_builder

# * * * * * * * *  GLOBAL VARIABLES  * * * * * * * * * * * * *
FILEPATH = ''
STICKY_NOTE = None
QED = None

# * * * * * * * *  STYLING CONSTANTS  * * * * * * * * * * * * *
ICON_LOC = 'icon.png'
WINDOW_TITLE = "Product Builder  (Alpha 1)"
WINDOW_DIMENSIONS = '320x218'
BTN_PADDING = 5
BTN_BORDER = 4
BTN_FONT_FAMILY = 'Segoe UI'
ENTRY_WIDTH = 35
COMBOBOX_WIDTH = 18

# * * * * * * * *  CREATE UI OBJECTS  * * * * * * * * * * * * *

# Window:
ROOT = tk.Tk()
ROOT.geometry(WINDOW_DIMENSIONS)
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
                slip += "+ {}\n".format(x)
            messagebox.showerror("CSV Format Error",
                                 "The CSV selected is missing the following " +
                                 "required header(s):\n\n" + slip)
        # CASE: Empty DataFrame
        elif(len(df) == 0):
            messagebox.showwarning('Problemo!',
                                   'The selected CSV has no rows.')
        # CASE: ...or else
        else:
            pass

    # CATCH: Invalid Filepath--
    except FileNotFoundError as e:
        messagebox.showerror('Error in opening file!',
                             "Select a valid CSV file to continue.\n\n"
                             + str(e).replace('[Errno 2]', 'ERR:'))
    # CATCH: Empty Data Error--
    except pd.errors.EmptyDataError as e:
        messagebox.showwarning('Empty Data Error!', e)


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
        messagebox.showwarning("Warning -- File Not Found",
                               "Please select a CSV file in Step 1.\n\n" +
                               str(err).replace('[Errno 2]', 'ERR:'))
        # End process
        return

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
        # Confirm Input
        confirm = messagebox.askyesno('Confirmation',
                                      'Is the following information correct?' +
                                      '\n\nBrand Name:    ' + str(brand) +
                                      '\nVendor Email:  ' + str(email) +
                                      '\nBuild Type:       ' + str(buildtype) +
                                      "\n\nCSV's Filepath:\n" + str(FILEPATH)
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
            messagebox.showinfo('Confirmation',
                                'Process cancelled.')


# Convert CSV Event (TAB 3):
def convert_csv():
    global STICKY_NOTE
    # CASE: Input Confirmed and Submitted
    if(STICKY_NOTE is not None):
        confirm_convert = messagebox.askyesno('Confirmation',
                                              'Would like to proceed?')
        # YES --
        if(confirm_convert is True):
            build_type = STICKY_NOTE["BUILDTYPE"]
            print("DEBUG: Conversion Confirmed for Takeoff!")  # debug
            global QED

            # CASE: Shopify Build
            if(build_type == 'Shopify'):
                QED = shopify_builder(STICKY_NOTE)
            # CASE: Etsy Build
            # elif(build_type == 'Etsy'):
            #   QED = etsy_builder(STICKY_NOTE)

            # CASE: ...or else
            else:
                QED = pd.DataFrame(STICKY_NOTE)

            messagebox.showinfo('Complete!',
                                "The CSV is converted and is ready " +
                                "to export.\n\n[Statistics -- Coming Soon!]" +
                                "\n\n • number_of_rows_processed" +
                                "\n • execution_time_in_seconds" +
                                "\n • num_defaults_and_variants_ratio" +
                                "\n • number_of_option_columns_created"
                                )
            # TODO: Add Stats Information to Message

        # NO --
        else:
            messagebox.showinfo('Confirmation',
                                'Process cancelled')
    # CASE: Step 2 Not Confirmed
    else:
        messagebox.showwarning('More Info Required',
                               'Confirm and submit the information in ' +
                               'Step 2 to continue.')


# Export CSV Event (TAB 3):
def export_csv():
    global QED
    global STICKY_NOTE

    # CASE: Cannot Export Yet...
    if(QED is None):
        messagebox.showwarning('Warning -- Conversion Not Complete!',
                               'You must convert the CSV before you can '
                               + 'export the files.')
    # CASE: Converted and Ready to Export
    else:
        brandname = STICKY_NOTE["BRAND"]

        # Create Folder & Store Path
        folder_loc = validation.create_brand_folder(brandname=brandname)
        # Store CSVs in the Folder
        validation.store_csvs(brandname=brandname,
                              folder_loc=folder_loc,
                              dict_of_df=QED)
        # Message Folder Name
        messagebox.showinfo("Finished!",
                            "Files have been stored at:\n" +
                            str(folder_loc))


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

# TAB BAR
tabControl.grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)

# TAB1
choose_csv_btn.grid(row=1, column=2, pady=65, padx=100)

# TAB2
brand_label.grid(row=1, column=0, padx=5, pady=15)
brand_name_field.grid(row=1, column=1, padx=5, pady=15)

vendor_label.grid(row=2, column=0, padx=5, pady=5)
vendor_email_field.grid(row=2, column=1, padx=5, pady=5)

build_label.grid(row=3, column=0, padx=5, pady=15)
build_combobox.grid(row=3, column=1, padx=5, pady=15, sticky=tk.W)
build_combobox.current(0)       # Sets default selection to the first option

submit_btn.grid(row=4, column=1, padx=70, pady=8, sticky=tk.W)

# TAB3
convert_btn.grid(row=0, column=0, padx=90, pady=30)
export_btn.grid(row=1, column=0, padx=90, pady=0)

# Infinite Window Loop:
ROOT.mainloop()
