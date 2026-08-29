#add aditional data
#information sent by Alejandra
#HELP: here I can add other information
def add_site_info(df):
    def fill_info(row):
        if row['Site'] == 'CaNu ':
            row['annual_precipitation_mm'] = 4500
            row['elevation_m'] = 3000
            row['mean_annual_temperature_C'] = 10
        elif row['Site'] == 'BoN':
            row['annual_precipitation_mm'] = 2000
            row['elevation_m'] = 1000
            row['mean_annual_temperature_C'] = 19
        elif row['Site'] == 'SFNu':
            row['annual_precipitation_mm'] = 2000
            row['elevation_m'] = 2000
            row['mean_annual_temperature_C'] = 15
        else:
            row['annual_precipitation_mm'] = None
            row['elevation_m'] = None
            row['mean_annual_temperature_C'] = None
        return row

    df = df.apply(fill_info, axis=1)
    print("Information was added: annual precipitation, elevation, mean annual temperature")
    return df

def add_specie_info(df):
    def fill_info(row):
        if row['genus'] == 'Weinmania ':
            row['WD'] = 0.536
            
        elif row['genus'] == 'Alchornea':
            row['WD'] = 0.523
            
        elif row['genus'] == 'Myrcia':
            row['WD'] = 0.717

        elif row['genus'] == 'Hedyosmum':
             row['WD'] = 0.489

        elif row['genus'] == 'Pouteria':
             row['WD'] = 0.788
        else:
            row['WD'] = 0.585 #Clarisia
            
        return row
    print("Information of the especies was added: WD")

    df = df.apply(fill_info, axis=1)
    return df

import numpy as np
import pandas as pd 

def add_bloque_info(df):
   """Adds information on the bloque based on the Plot ID whith a difference for SFNU where they have Ca"""
   df["Bloque"] = np.nan
   #df["Plot"] = df["Plot"].str.strip()
   #df["Plot"] = pd.to_numeric(df["Plot"])#, errors="coerce")

   # Rule for Site == "SFNU"
   mask_sfnu = df["Site"] == "SFNu" #only apply rule for SF
   df.loc[mask_sfnu & df["Plot"].between(1, 4),  "Bloque"] = 1
   df.loc[mask_sfnu & df["Plot"].between(6, 9),  "Bloque"] = 2
   df.loc[mask_sfnu & df["Plot"].between(11, 14), "Bloque"] = 3
   df.loc[mask_sfnu & df["Plot"].between(15, 20), "Bloque"] = 4
    
   # Rule for all other sites
   mask_other = df["Site"] != "SFNu"
   print("Adding information of the Bloque to SF")
   df.loc[mask_other & df["Plot"].between(1, 4),   "Bloque"] = 1
   df.loc[mask_other & df["Plot"].between(5, 8),   "Bloque"] = 2
   df.loc[mask_other & df["Plot"].between(9, 12),  "Bloque"] = 3
   df.loc[mask_other & df["Plot"].between(13, 16), "Bloque"] = 4

   print("Information of the bloque was added")
   return df