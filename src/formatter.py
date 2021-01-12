# formatter.py

import numpy as np
import pandas as pd
import random
import string

###################################################

def drop_down(data, num_rows):
  """
  Fills a pandas Series object with a single piece of data.

  Parameters
  ----------
  data : any
      The data used to fill the column.
  num_rows : int
      The number of rows that need to be filled.

  Returns
  -------
  pandas.Series
      The required pandas Sereis object filled with 'data'.
  """
  new_list = [data] * num_rows
  return pd.Series(new_list)



def format_skus(sku_col, name_col):
  """
  Formats the sku column based on length the sku value's length.
  If longer than 30 characters this function will trim and append five random letters.

  Parameters
  ----------
  sku_col : pandas.Series
      The sku column to be formatted.
  name_col : pandas.Series
      The name column used as reference.

  Returns
  -------
  pandas.Series
      The properly formatted sku column.

  Raises
  ------
  Exception
      Handler for sku values with no length.
  """
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
      raise Exception("A sku was too short to check formatting!")

  return pd.Series(new_list)



def grams_to_pounds(grams_col):
  """
  Converts a weight column in grams to a weight column in pounds.
  Rounds to 4 decimal places (saves X-Cart some work).

  Parameters
  ----------
  grams_col : pandas.Series
      The weight column in grams.

  Returns
  -------
  pandas.Series
      The weight column coverted to pounds.
  """
  to_edit = grams_col * 0.00220462
  rounded = round( to_edit, 4 )
  return pd.Series(rounded)   



def format_categories(brand_name, num_rows, category="Coming Soon"):
  """
  Formats the data required for the categories column.

  Parameters
  ----------
  brand_name : str
      The brand name.
  num_rows : [type]
      The number of rows to create/fill.
  category : str, optional
      The category the brand is currently located in, by default "Coming Soon"

  Returns
  -------
  pandas.Series
      Uses the 'drop_down' function to return a column filled with the proper category data.
  """
  cat_str = "{cat} >>> {name}".format(cat=category, name=brand_name)
  return drop_down(cat_str, num_rows)



def drop_down_named(name_col, data):
  """
  Takes a piece of data and creates a column with it dropped down only rows containing a name value.

  Parameters
  ----------
  name_col : pandas.Series
      The name column used as reference.
  data : any
      The fill data.

  Returns
  -------
  pandas.Series
      The required column with no data in rows not containing a name value.
  """
  dlist = []
  bool_array = pd.isnull(name_col)
  for b in bool_array:
    if (b):                       # CASE: Name is empty
      dlist.append(np.nan)
    else:                         # CASE: Name has a value
      dlist.append(data)
  return pd.Series(dlist)



def format_meta(name_col, brand):
  """
  Formats the metaTitle column using the product's name and the brand's name.
  This column will only contain data in the rows containing a name value.
  
  Parameters
  ----------
  name_col : pandas.Series
      The name column used as reference.
  brand : str
      The brand name.

  Returns
  -------
  pandas.Series
      The properly formatted metaTitle column.
  """
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
  """
  Creates the default price column based on the name and variantPrice columns.
  This column will only contain a price in rows containing a name value.

  Parameters
  ----------
  name_col : pandas.Series
      The name column as reference.
  vprice_col : pandas.Series
      The variantPrice column.

  Returns
  -------
  pandas.Series
      The properly formatted price column.
  """
  price_list = []
  bool_array = pd.isnull(name_col)
  for i, price in enumerate(list(vprice_col)):
    if (bool_array[i]):   # CASE: Name is empty
      price_list.append(np.nan)
    else:                 # CASE: Name has value
      price_list.append(price)
  return pd.Series(price_list)



def format_varprice(vprice_col):
  """
  Checks the variantPrice column to make sure it doesn't contain any dollar-signs and that the values are floats.

  Parameters
  ----------
  vprice_col : pandas.Series
      The variantPrice column to check.

  Returns
  -------
  pandas.Series
      The cleaned and formatted variantPrice column.
  """
  formatted_list = []
  for vp in vprice_col:
    as_string = str(vp)
    no_symbol = as_string.replace('$', "")
    as_float = float(no_symbol)
    formatted_list.append(as_float)
  return pd.Series(formatted_list)



def trim_empty(df, ref_col):
  bool_array = pd.isnull(ref_col)     # boolean array - True when value is empty
  index_list = []                     # store a list of indices with an empty value
  for index, value in enumerate(df):
    # CASE: empty value
    if (bool_array[i]):
      index_list.append(i)
    else:
      pass
    
  return df.drop(index=index_list, axis=0)

