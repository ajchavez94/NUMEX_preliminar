def calculate_iWUE(iWUE):
 """ This script calculates iWUE from a given database"""
 a= 4.4
 b= 27
 f= 12
 cP = 40
 
 delt13Cair = -9.085684858  #data for 2024
 Cair = 423.1142299   #data for 2024 ManuLoa data.
 
 # clean values of C that are incorrect. Too low, less than 35%
 #iWUE = iWUE[iWUE['[C] m/m (%)'] >= 0.35]
 
 print("Delete [C] m/m (%) values lower than 35%")
 #iWUE = iWUE.loc[iWUE['[C] m/m (%)'] >= 35]

 iWUE["t13C_cell"] = (delt13Cair- iWUE["δ13C (‰ v.s.V-PDB)"])/(1+(iWUE["δ13C (‰ v.s.V-PDB)"]/1000)) #HELP
 iWUE["Ci"] = (Cair*(iWUE["t13C_cell"]-a)+f*cP)/(b-a) #all same units %%
 iWUE["Ci/Ca"]= iWUE["Ci"]/Cair #ratio of intercellular CO₂ concentration (Ci) to ambient CO₂ concentration (Ca)
 iWUE["iWUE (μmol/mol)"] = (Cair/1.6)*(1-(iWUE["Ci"]/Cair))

 #Other way to calculate iWUE, gives same result. Bauters formula.
 #iWUE["△13C_cell_2"] = (iWUE["?13Cair"]/1000- iWUE["δ13C (‰ v.s. V-PDB)"]/1000)/(1+(iWUE["δ13C (‰ v.s. V-PDB)"]/1000))
 #iWUE["Ci_2"] = (iWUE["Cair"]*(iWUE["△13C_cell_2"]-a/1000)+(f*cP/1000))/(b/1000-a/1000) #all same units %%
 #iWUE["iWUE (μmol/mol)_m2"] = (iWUE["Cair"]/1.6)*(1-(iWUE["Ci_2"]/iWUE["Cair"]))
 value = len(iWUE)

 print("Cleaning negative values of iWUE (μmol/mol)")
 #iWUE = iWUE[iWUE['iWUE (μmol/mol)'] >= 1]

 print("The length of the df is " + str(value))
 iWUE_clean = iWUE[(iWUE["iWUE (μmol/mol)"].notnull())] #filter the empty rows
 iWUE_clean.head(3)
 #iWUE_clean.to_excel("iWUE_cleaned_"+date_time+".xlsx") #para R 
 return iWUE_clean