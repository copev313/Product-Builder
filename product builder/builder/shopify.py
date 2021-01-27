# shopify.py

import pandas as pd

from utils import formatter as frm

# - - - - - - - - - - - - - - - - - - - -


def shopify_builder(sticky_note):
    """
    The main driver function for creating a product build from a Shopify CSV.

    Parameters
    ----------
    sticky_note : dict
        A dictionary object containing required product build information.

    Returns
    -------
    dict
        A dictionary containing necessary CSV formats as values (ex: Master,
        Sku Key, Defaults, etc.)
    """
    # Extract Info From Sticky Note
    brand = sticky_note["BRAND"]
    email = sticky_note["EMAIL"]
    fp = sticky_note["FILEPATH"]

    # Create DataFrame
    df = pd.read_csv(fp)

    # Columns That Just Need Copied
    name = df['Title']
    desc = df['Body (HTML)']
    # TODO: Format images to only contain one link, not a comma seperated list
    imgs = frm.format_images(df['Image Src'])
    # TODO: Handle this steaming pile of garbage...
    opt1Name, opt1Val = df['Option1 Name'], df['Option1 Value']
    opt2Name, opt2Val = df['Option2 Name'], df['Option2 Value']
    opt3Name, opt3Val = df['Option3 Name'], df['Option3 Value']

    # COMING SOON: Inventory Tracking Columns . . .
    '''
    try:
        variantQty = df['Variant Inventory Qty']

    except:

    '''
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Columns That Require Some Formatting

    sku = frm.format_skus(df['Handle'], name)
    enabled = frm.drop_down_named(name, 'no')
    weight = frm.grams_to_pounds(df['Variant Grams'])
    varPrice = frm.format_varprice(df['Variant Price'])
    price = frm.format_price(name, varPrice)
    meta = frm.format_meta(name, brand)

    NUM_ROWS = len(sku)
    print("DEBUG: NUM_ROWS: " + str(NUM_ROWS))  # debug

    vendor = frm.drop_down(email, NUM_ROWS)
    cat = frm.format_categories(brand, NUM_ROWS)

    # Put Together New Formatted DataFrame
    master_import_df = pd.DataFrame({'sku': sku,
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
                                     'images': imgs})

    sku_key_df = pd.DataFrame({'old sku': df['Handle'],
                               'new sku': sku})

    image_key_df = pd.DataFrame({'sku': sku,
                                 'name_en': name,
                                 'vendor': vendor,
                                 'categories': cat,
                                 'images': imgs})

    # Trim Rows w/o a Name Value
    names_only = frm.trim_empty(image_key_df, name)

    # Now Trim Rows w/o an Image Value
    image_import_df = frm.trim_empty(names_only, imgs)

    # defaults_df = pd.DataFrame({ })
    # variants_df = pd.DataFrame({ })

    # TODO: Add Defaults & Variants Sheet
    return {"MASTER IMPORT": master_import_df,
            "SKU KEY": sku_key_df,
            "IMAGE KEY": image_key_df,
            "IMAGE IMPORT": image_import_df,
            # "DEFAULTS": defaults_df,
            # "VARIANTS": variants_df
            }
