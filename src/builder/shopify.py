# shopify.py

import pandas as pd
import formatter as form


def shopify_builder(sticky_note):
    
    # Extract Info From Sticky Note
    brand = sticky_note["BRAND"]
    email = sticky_note["EMAIL"]
    fp = sticky_note["FILEPATH"]
    
    # Create DataFrame
    df = pd.read_csv(fp)
    
    # Simple Columns That Just Need Copied
    name = df['Title']
    desc = df['Body (HTML)']
    varPrice = df['Variant Price']  # TODO: 
    imgs = df['Image Src']          # TODO: Format images to only contain one link, not comma seperated list
    grams = df['Variant Grams']
    opt1Name, opt1Val = df['Option1 Name'], df['Option1 Value']
    opt2Name, opt2Val = df['Option2 Name'], df['Option2 Value']
    opt3Name, opt3Val = df['Option3 Name'], df['Option3 Value']
    
    # TODO: implement 'Variant Inventory Qty'
    
    #################################################################
    
    # Save Some Columns That Require Formatting
    sku = form.format_skus( df['Handle'], name ) # TODO: Fix SKU func
    enabled = form.drop_down_named( name, 'no' )
    weight = form.grams_to_pounds( grams )
    price = form.format_price( name, varPrice )
    meta = form.format_meta( name, brand )

    NUM_ROWS = len(sku)
    vendor = form.drop_down( email, NUM_ROWS )
    cat = form.format_categories( brand, NUM_ROWS )
    

    # Put Together New Formatted DataFrame
    master_df = pd.DataFrame({      'sku': sku,
                                    'name_en': name,
                                    'description_en': desc,
                                    'price': price,
                                    'vendor': vendor,
                                    'categories': cat,
                                    'metaTitle_en': meta,
                                    'enabled': enabled,
                                    'Option1 Name': opt1Name,
                                    'Option1 Value': opt1Val,
                                    'Option2 Name': opt2Name,
                                    'Option2 Value': opt2Val,
                                    'Option3 Name': opt3Name,
                                    'Option3 Value': opt3Val,
                                    'variantPrice': varPrice,
                                    'weight': weight,
                                    'images': imgs
                                })
    
    sku_df = pd.DataFrame({ 'old sku': df['Handle'], 
                            'new sku': sku 
                        })
    
    # TODO: Trim extra rows!!!
    image_df = pd.DataFrame({   'sku': sku, 
                                'name_en': name, 
                                'vendor': vendor, 
                                'categories': cat, 
                                'images': imgs 
                            })
    
    
    # TODO: Add Defaults & Variants Sheet
    return { "MASTER IMPORT": master_df, "SKU KEY": sku_df, "IMAGE IMPORT": image_df } 
    