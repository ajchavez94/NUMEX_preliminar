def add_info_bloque(df):
   """Adds information on the bloque based on the Plot ID whith a difference for SFNU where they have Ca"""
   df["Bloque"] = np.nan

   # Rule for Site == "SFNU"
   mask_sfnu = df["Site"] == "SFNU"
   df["Plot"].astype("int64")
   
   df.loc[mask_sfnu & df["Plot"].between(1, 4),  "Bloque"] = 1
   df.loc[mask_sfnu & df["Plot"].between(6, 9),  "Bloque"] = 2
   df.loc[mask_sfnu & df["Plot"].between(11, 14), "Bloque"] = 3
   df.loc[mask_sfnu & df["Plot"].between(16, 19), "Bloque"] = 4

   # Rule for all other sites
   mask_other = df["Site"] != "SFNU"
   df.loc[mask_other & df["Plot"].between(1, 4),   "Bloque"] = 1
   df.loc[mask_other & df["Plot"].between(5, 8),   "Bloque"] = 2
   df.loc[mask_other & df["Plot"].between(9, 12),  "Bloque"] = 3
   df.loc[mask_other & df["Plot"].between(13, 16), "Bloque"] = 4

   return df