# builder.py

# Package Imports:
import pandas as pd
import sys

# Import Functions Module:
import formatter as form

###############################################################

# -- CATCH: Bad Headers
try:
  #) Number of Rows Based on Rows Containing SKUs
  NUM_ROWS = len( df['Handle'] )
  #) Save EZ Columns as Pandas Series Objects
  name, desc, varPrice, imgs, grams = df['Title'], df['Body (HTML)'], df['Variant Price'], df['Image Src'], df['Variant Grams']
except KeyError:
  print("ERROR:  The CSV is missing a required column!  Please check your CSV file's header names for:" +
        "\n\t\t+++ 'Handle' \n\t\t+++ 'Title' \n\t\t+++ 'Body (HTML)' \n\t\t+++ 'Variant Price' " + 
        "\n\t\t+++ 'Image Src'\n\t\t+++ 'Variant Grams'\n " )
  sys.exit(0)


# Save Some Columns That Require Formatting
sku = form.format_skus( df['Handle'], name ) # TODO: Fix SKU func
enabled = form.drop_down_named( name, 'no' )
weight = form.grams_to_pounds( grams )
###price = # NEEDS SPECIAL FUNCTION...

#################################################################
# TODO: Add Text Fields to Take in this Data

# Accept User Input From Console For Email & Brand Name
while ( True ):
  email = str(input("Enter Vendor's Email: "))  or  'email@email.com'
  brand = str(input("Enter Vendor's Brand Name: "))  or  'BRAND NAME'
  print("\nVendor's Data Received...\n")

  #) Confirmation Before Moving On
  print("Email: {e}\nBrand: {b}\n".format(e=email, b=brand))
  resp = str(input("Is this correct? [y/n] : "))

  #) Handle Response...
  if ( resp == 'y' ): 
    print("Thank you. Continuing...\n")
    break
  elif ( resp == 'n' ): 
    print("Sorry, please try again.\n")
    continue
  else:
    print("Sorry, invalid response. Please resubmit input.\n")
    continue
    
###################################################################

# Continue Once Confirmed..
vendor = form.drop_down( email, NUM_ROWS )
cat = form.format_categories( brand, NUM_ROWS )
meta = form.format_meta( name, brand )


# Create New Formatted DataFrame
formatted_df = pd.DataFrame({ 'sku': sku,
                              'name_en': name,
                              'description_en': desc,
                              #"price": price,
                              'vendor': vendor,
                              'categories': cat,
                              'metaTitle_en': meta,
                              'enabled': enabled,
                              ### OPTIONS WILL GO HERE...
                              'variantPrice': varPrice,
                              'weight': weight,
                              'images': imgs
                            })

