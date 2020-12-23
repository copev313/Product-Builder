# app.py

# Imports:
import pandas as pd
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog
import json, re


filepath = ''
buildtype = ''

# Create Window
root = tk.Tk()
root.geometry('400x300')
root.title("Product Builder -- (version: 0.1.2)")

# * * * MENU COMMAND FUNCTIONS * * * #

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


# About Me Event:
def about_me():
    messagebox.showinfo('About Me', "I do stuff" )


# Instructions Event:
def instructions():
    messagebox.showinfo('Instructions', "Coming soon..." )

# * * * * * * * * * * * * * * * * * #

# Build Menu
menubar = tk.Menu(root)
filemenu = tk.Menu( menubar, tearoff=0 )
filemenu.add_command( label="Instructions", command=instructions )
filemenu.add_command( label="Choose CSV File", command=select_csv )
filemenu.add_command( label="About Me", command=about_me )
filemenu.add_separator()
filemenu.add_command( label="Exit", command=root.quit )

menubar.add_cascade( label="Options Menu", menu=filemenu )
root.config(menu=menubar)


# Labels
build_label = tk.Label( root, text="Build Type: " )
brand_label = tk.Label( root, text="Brand: ")
vendor_label = tk.Label( root, text="Email: ")

# Fields
brand_name_var = tk.StringVar( root, value="MY SOCKS")                     # Default Text Entry Values
vendor_email_var = tk.StringVar( root, value="eatmysocks@yahoo.org")

brand_name_field = tk.Entry( root, width=35, textvariable=brand_name_var )
vendor_email_field = tk.Entry( root, width=35, textvariable=vendor_email_var )                               


# * * * BUTTON COMMAND FUNCTIONS * * * #

# Submit Input Event
def submit_input():
    global buildtype
    brand = brand_name_var.get()
    email = vendor_email_var.get()
    buildtype = build_var.get()
    
    def return_input(brand='', email='', buildtype='', filepath=''):
        return {'brand':brand, 'email':email, 'buildtype':buildtype, 'filepath':filepath}
    
    def check_email(email=''):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        return True if re.search(regex, email) else False
    
    
    # CASE: No CSV Path Selected
    if(filepath == ""):
        messagebox.showwarning("More Info Required", "No CSV file path selected.")
    
    # CASE: Email Invalid
    elif(!check_email(email)):    
        messagebox.showwarning("Input Validation", "The email entered is not valid.")
    
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
            messagebox.showinfo('Complete', 'Information Submitted!')
            brand_name_var.set('')      # Clear Fields
            vendor_email_var.set('')
            return_input(brand, email, buildtype, filepath)
        
        # NO --
        else:
            messagebox.showinfo('Submission Cancelled', 
                                'Please make the proper changes and try again.')


# Export CSV Event:      
def export_csv(df):
    export_path = filedialog.asksaveasfilename(defaultextention='.csv')
    df.to_csv( export_path, index=False, header=True )


# temp func for test runs
def dothething():
    pass


# * * * * * * * * * * * * * * * * * #

# Buttons
submit_btn = tk.Button( root, 
                        text="Submit",
                        command=submit_input,
                        bg='red',        
                        bd=5
                        )

convert_btn = tk.Button( root, 
                        text="Convert CSV", 
                        command=dothething, 
                        bg='#4CAF50',       # green
                        bd=5
                        )

export_btn = tk.Button( root,  
                        text="Export CSV", 
                        command=export_csv, 
                        bg='#3AAFFF',       # light blue
                        bd=5
                        )


# Dropdown Menu
build_var = tk.StringVar()
build_combobox = ttk.Combobox(  root,
                                width=18, 
                                values=[ 'Shopify', 'Etsy', 'Wix', 'Square', 'WooCommerce', 'BigCommerce'],
                                textvariable=build_var,
                                state='readonly'
                                )


# * * * | | * * *  POSITION WIDGETS  * * * | | * * * #
brand_label.grid( row=0, column=0, pady=15, sticky=tk.E )
brand_name_field.grid( row=0, column=1 )

vendor_label.grid( row=1, column=0, padx=5, pady=5, sticky=tk.E )
vendor_email_field.grid( row=1, column=1 )

build_label.grid( row=2, column=0, padx=5, pady=5, sticky=tk.E )
build_combobox.grid( row=2, column=1, padx=5, pady=5, sticky=tk.W )
build_combobox.current(0)                               # sets default selection

submit_btn.grid( row=2, column=2, padx=25, pady=5 )

# convert_btn.grid( )
# export_btn.grid( )

root.mainloop()
