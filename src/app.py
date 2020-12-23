# app.py

import pandas as pd
import tkinter as tk
import tkinter.ttk as ttk
import re
from tkinter import messagebox, filedialog

filepath = ''
buildtype = ''
notepad = {}

# Styling Constants
ICON_LOC = './icon.png'
BTN_PADDING = 5
BTN_BORDER = 4
BTN_FONT_FAMILY = 'Segoe UI'
ENTRY_WIDTH = 35
COMBOBOX_WIDTH = 18
# * * * * * * * * * * * * * * * * * #

# Create Window
root = tk.Tk()
root.geometry('320x225')
root.title("Product Builder (v.0.1.3)")
root.iconphoto(False, tk.PhotoImage(file=ICON_LOC))


# Create Tabs
tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tabControl.add(tab1, text=' Step 1 ')
tabControl.add(tab2, text=' Step 2 ')
tabControl.add(tab3, text=' Step 3 ')


# Labels
build_label = tk.Label( tab2, text="Type: " )
brand_label = tk.Label( tab2, text="Brand: ")
vendor_label = tk.Label( tab2, text="Email: ")

# Fields
brand_name_var = tk.StringVar(value="MY SOCKS")                     # Default Text Entry Values
vendor_email_var = tk.StringVar(value="eatmysocks@yahoo.org")

brand_name_field = tk.Entry( tab2, width=ENTRY_WIDTH, textvariable=brand_name_var )
vendor_email_field = tk.Entry( tab2, width=ENTRY_WIDTH, textvariable=vendor_email_var )                               


# * * * BUTTON COMMAND FUNCTIONS * * * #

# Select CSV Event:
def select_csv():
    try: 
        # Save the Name of CSV Filepath to Create a DataFrame
        global filepath
        filepath = filedialog.askopenfilename(  initialdir = '/Desktop', 
                                                title = 'Select a CSV file', 
                                                filetypes = (('csv file','*.csv'), ('csv file','*.csv'))) 
        print(filepath)
        df = pd.read_csv(filepath)

        # CASE: Empty DataFrame
        if(len(df) == 0):                
            messagebox.showwarning('Problemo!', 'The selected CSV has no rows.')
            
        else: 
            pass    
        
    # CATCH: Invalid Filepath
    except FileNotFoundError as err: 
        messagebox.showerror('Error in opening file!', err )


# Submit Input Event
def submit_input():
    global buildtype
    brand = brand_name_var.get().strip()
    email = vendor_email_var.get().strip()
    buildtype = build_var.get()
    
    def return_input(brand='', email='', buildtype='', filepath=''):
        notepad = {'brand':brand, 'email':email, 'buildtype':buildtype, 'filepath':filepath}
    
    def check_email(email=''):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        return True if re.search(regex, email) else False
    
    
    # CASE: No CSV Path Selected
    if(filepath == ""):
        messagebox.showwarning("More Info Required", "No CSV file path selected.")
    
    # CASE: Empty Brand Name
    elif(brand == ""):
        messagebox.showwarning("More Info Required", "No brand name specified.")
    
    # CASE: Email Invalid
    elif( not check_email(email) ):    
        messagebox.showwarning("Input Validation", "The email address entered is invalid.")
    
    # CASE: Looks good...    
    else:
        # Confirm Input
        confirm_info = messagebox.askyesno('Confirmation', 
                                           'Is the following info correct?\n\n'+
                                           'Brand Name:  {}\n'.format(brand)+
                                           'Vendor Email:  {}\n'.format(email)+
                                           'Build Type:  {}\n\n'.format(buildtype)+
                                           'File Path: {}'.format(filepath)
                                        )
        # YES -- 
        if(confirm_info):
            global notepad
            messagebox.showinfo('Complete', 'Information Submitted!')
            brand_name_var.set('submitted')     
            vendor_email_var.set('submitted')
            notepad = return_input(brand, email, buildtype, filepath)
        
        # NO --
        else:
            messagebox.showinfo('Submission Cancelled', 
                                'Please make the proper changes and try again.')


# Convert CSV Event:
def convert_csv():
    global notepad
    # Input Confirmed and Submitted
    if(notepad != {}):
        confirm_convert = messagebox.askokcancel('Confirmation', 'Are you sure you would like to proceed.')
    
        # YES --
        if(confirm_convert): pass #maybe have a loading screen
        
        # NO --
        else:
            messagebox.showinfo('Confirmation', 'Cancelled')
        
    else:
        messagebox.showwarning('More Info Required', 'Please confirm and submit the information in Step 2.')
        
    
# Export CSV Event:      
def export_csv(df):
    export_path = filedialog.asksaveasfilename(defaultextention='.csv')
    df.to_csv( export_path, index=False, header=True )


# * * * * * * * * * * * * * * * * * #

# Buttons
choose_csv_btn = tk.Button( tab1,
                            text="Select CSV",
                            command=select_csv,
                            bg='#FFAC14',   # orange
                            font=(BTN_FONT_FAMILY, 12, 'bold'),
                            padx=BTN_PADDING,
                            pady=BTN_PADDING,
                            bd=BTN_BORDER
                            )

submit_btn = tk.Button( tab2, 
                        text="Submit",
                        command=submit_input,
                        bg='#19D5EE',       # light blue       
                        font=(BTN_FONT_FAMILY, 10, 'bold'),
                        padx=BTN_PADDING,
                        pady=BTN_PADDING,
                        bd=BTN_BORDER
                        )

convert_btn = tk.Button( tab3, 
                        text="Convert CSV", 
                        command=convert_csv, 
                        bg='#9AD259',       # green
                        font=(BTN_FONT_FAMILY, 12, 'bold'),
                        padx=BTN_PADDING,
                        pady=BTN_PADDING,
                        bd=BTN_BORDER
                        )

export_btn = tk.Button( tab3, 
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
bvalues = [ 'Shopify', 'Etsy', 'Wix', 'Square', 'WooCommerce', 'BigCommerce']
build_combobox = ttk.Combobox(  tab2,
                                width=COMBOBOX_WIDTH, 
                                values=bvalues,
                                textvariable=build_var,
                                state='readonly'
                                )


# * * * | | * * *  POSITION WIDGETS  * * * | | * * * #

# TAB BAR
tabControl.grid( row=0, column=0, pady=5, padx=5, sticky=tk.W )

# TAB1
choose_csv_btn.grid( row=1, column=2, pady=65, padx=100 )

# TAB2
brand_label.grid( row=1, column=0, padx=5, pady=15 )
brand_name_field.grid( row=1, column=1, padx=5, pady=15 )

vendor_label.grid( row=2, column=0, padx=5, pady=5 )
vendor_email_field.grid( row=2, column=1, padx=5, pady=5 )

build_label.grid( row=3, column=0, padx=5, pady=15 )
build_combobox.grid( row=3, column=1, padx=5, pady=15, sticky=tk.W )
build_combobox.current(0)   # sets default selection

submit_btn.grid( row=4, column=1, padx=70, pady=8, sticky=tk.W )


# TAB3
convert_btn.grid( row=0, column=0, padx=90, pady=35 )
export_btn.grid( row=1, column=0, padx=90, pady=0 )


root.mainloop()
