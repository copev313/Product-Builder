# etsy.py

import pandas as pd
#import formatter as form


def etsy_builder(sticky_note):
    
    # Extract Info From Sticky Note
    brand = sticky_note["BRAND"]
    email = sticky_note["EMAIL"]
    fp = sticky_note["FILEPATH"]
    
    # Create DataFrame
    df = pd.read_csv(fp)
    
    
    pass