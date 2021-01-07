# formatter.py

import numpy as np
import pandas as pd
import random
import string

###################################################

def drop_down(data, num_rows):
  new_list = [data] * num_rows
  return pd.Series(new_list)



def format_skus(sku_col, name_col):
  new_list = []
  bool_name = pd.notnull(name_col)
  formatted = ""

  for i, sku in enumerate(sku_col):

    # Force SKU to string
    sku = str(sku)    

    # CASE: SKU is acceptable
    if ( len(sku) <= 30 and len(sku) > 0 ):
      new_list.append(sku)
    
    # CASE: SKU too long  
    elif ( len(sku) > 30 ):
      # Does row contain a name?
      if ( bool_name[i] ):
        trim = sku[:24]                     # Trim to 24 characters
        five = "".join([ random.choice(string.ascii_lowercase) for i in range(5) ])  # Generate String of 5 Random Lowercase Letters
        formatted = trim +"-"+ str(five)    # Form New SKU
      else:
        pass
      new_list.append(formatted)            # Add SKU to List

    # CASE: SKU has no length
    else:                                       
      raise Exception("A sku was too short to process.")

  return pd.Series(new_list)



def grams_to_pounds(grams_col):
  to_edit = grams_col * 0.00220462
  rounded = round( to_edit, 4 )
  return pd.Series(rounded)   



def format_categories(brand_name, num_rows, category="Coming Soon"):
  cat_str = "{cat} >>> {name}".format(cat=category, name=brand_name)
  return drop_down(cat_str, num_rows)



def drop_down_named(name_col, data):
  dlist = []
  bool_array = pd.isnull(name_col)
  for b in bool_array:
    if (b):                       # CASE: Name is empty
      dlist.append(np.nan)
    else:                         # CASE: Name has a value
      dlist.append(data)
  return pd.Series(dlist)



def format_meta(name_col, brand):
  meta_list = []
  bool_array = pd.isnull(name_col)
  for i, name in enumerate(list(name_col)):
    if (bool_array[i]):   # CASE: Name is empty
      meta_list.append(np.nan)
    else:                 # CASE: Name has a value
      metatitle = "Wholesale {name} | {brand}".format(name=name, brand=brand)
      meta_list.append(metatitle)
  return pd.Series(meta_list)



def format_price(name_col, vprice_col):
  price_list = []
  bool_array = pd.isnull(name_col)
  for i, price in enumerate(list(name_col)):
    if (bool_array[i]):   # CASE: Name is empty
      price_list.append(np.nan)
    else:                 # CASE: Name has value
      price_list.append(price)
  return pd.Series(price_list)