import numpy as np

def formula_iWUE(iWUE,delt13Cair,Cair):
  print("No Delete [C] m/m (%) values lower than 35%")
  #iWUE = iWUE.loc[iWUE['[C] m/m (%)'] >= 35]
  a= 4.4
  b= 27
  f= 12
  cP = 40
  iWUE["△13C_cell"] = (delt13Cair- iWUE["δ13C (‰ v.s.V-PDB)"])/(1+(iWUE["δ13C (‰ v.s.V-PDB)"]/1000)) #HELP
  iWUE["Ci"] = (Cair*(iWUE["△13C_cell"]-a)+f*cP)/(b-a) #all same units %%
  iWUE["Ci/Ca"]= iWUE["Ci"]/Cair #ratio of intercellular CO₂ concentration (Ci) to ambient CO₂ concentration (Ca)
  iWUE["iWUE (μmol/mol)"] = (Cair/1.6)*(1-(iWUE["Ci"]/Cair))

  #Other way to calculate iWUE, gives same result. Bauters formula.
  #iWUE["△13C_cell_2"] = (iWUE["?13Cair"]/1000- iWUE["δ13C (‰ v.s. V-PDB)"]/1000)/(1+(iWUE["δ13C (‰ v.s. V-PDB)"]/1000))
  #iWUE["Ci_2"] = (iWUE["Cair"]*(iWUE["△13C_cell_2"]-a/1000)+(f*cP/1000))/(b/1000-a/1000) #all same units %%
  #iWUE["iWUE (μmol/mol)_m2"] = (iWUE["Cair"]/1.6)*(1-(iWUE["Ci_2"]/iWUE["Cair"]))
  value = len(iWUE)
  print("No Cleaning negative values of iWUE (μmol/mol)")
  #iWUE = iWUE[iWUE['iWUE (μmol/mol)'] >= 1]

  print("The length of the df is " + str(value))
  iWUE_clean = iWUE[(iWUE["iWUE (μmol/mol)"].notnull())] #filter the empty rows
  #iWUE_clean.to_excel("iWUE_cleaned_"+date_time+".xlsx") #para R 
  return iWUE_clean
   
def calculate_iWUE(iWUE,CO2):
    """ This script calculates iWUE from a given database. Only ask which source of CO2 we want to use.
    Marijn advice: Use CO2 observation from Manu Lloa and delta13C from site"""
     #HELP: Once I have the results then maybe correct. 

 #Ask the user if we want Manu Lloa, if yes = 1, if No, observation = 0, 
    if CO2 == "option_1":
        # ---- on_site code ----
        print("You choose on d13C site and CO2 obs Manu Lloa")
        delt13Cair = -9.15 #9.22 ### data from Observations in the North. 
        Cair = 423.1142299   #data mean for Ecuador samples 458.9521799015872 but I am using the one for Manu Lloa and delta13 from mean observations.
        # data for 2024 Napo mean is 458. Why is it so high?
        iWUE = formula_iWUE(iWUE,delt13Cair,Cair)
        print("iWUE añadida")

        return iWUE
    
    elif CO2 == "option_2":
        # ---- manuloa code ----
        print("You choose observatory data both CO2 and d13C")
        delt13Cair = -8.6  #data for 2024 manu lloa. si cambia con elevacion. 
        Cair = 423.1142299 
        iWUE = formula_iWUE(iWUE,delt13Cair,Cair)
        print("iWUE añadida")

        return iWUE


    elif CO2 == "option_3":
         print("Using elevation-dependent values")

         df = iWUE.copy()

         conditions = [
            df["elevation_m"] == 1000,
            df["elevation_m"] == 2000,
            df["elevation_m"] == 3000
        ]

         delta_values = [-8.714103, -9.23, -9.5219]
         Cair = 455

         df["delt13Cair"] = np.select(conditions, delta_values, default=np.nan)

         return formula_iWUE(df, df["delt13Cair"], Cair)

    else:
        raise ValueError(
            "argument must be either 'option_1"
        )

    return iWUE