# builder.py

import pandas as pd
import sys

import formatter as form
import shopify.shopify_builder
import etsy.etsy_builder

###############################################################

def build(build_type=''):
  if(build_type == 'Shopify'):
    shopify_builder()
  elif(build_type == 'Etsy'):
    etsy_builder()
  else:
    pass #TODO: Add Popup Message for 'Not yet implemented...'


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

# TODO: Add Text Fields to Take in email and brand name
    
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

