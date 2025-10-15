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
