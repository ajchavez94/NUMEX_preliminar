

def kruskal_por_especie_y_tratamiento(df, variable):
    """
    Aplica el test de Kruskal-Wallis por especie, comparando tratamientos para cada una.
     The Kruskal-Wallis Test uses the following null and alternative hypotheses:

     The null hypothesis (H0): The median is equal across all groups.

     The alternative hypothesis: (Ha): The median is not equal across all groups.
     If p-value is less than 0.05, we can reject the null hypothesis. 
     
    Parámetros:
    - df: DataFrame con columnas 'name', 'tratamiento' y la variable numérica.
    - variable: str, nombre de la variable numérica (ej: 'iWUE', 'delta13C', etc.)

    Retorna:
    - Lista de diccionarios con resultados por especie.
    """
    from scipy.stats import kruskal
    from scipy.stats import f_oneway

    resultados = []

    for especie in df['name'].unique():
        sub_df = df[df['name'] == especie] #filtra por especie
        # Crear lista de valores por tratamiento (ignorando NaNs)
        grupos = [sub_df[sub_df['Sub'] == tr][variable].dropna() #luego selecciona el tratamiento y forma grupos
                  for tr in sub_df['Sub'].unique()]         
        print("Comparacion entre tratamientos")
        print(variable)
        # Solo si hay al menos dos tratamientos con datos
        if sum([len(g) > 0 for g in grupos]) >= 2:
            h_stat, p_val = kruskal(*grupos) #aplica el test de grupos para cada uno
            print(f"\nTEST KRUSKALL")
            df_libertad = len(grupos) - 1

            print(f"\nEspecie: {especie}")
            print(f"H = {h_stat:.3f}, p = {p_val:.4f}, df = {df_libertad}")

            resultados.append({
                "especie": especie,
                "H": h_stat,
                "p": p_val,
                "df": df_libertad
            })

            print(f"\nTEST ANOVA DE UNA VIA")
            print(f"\nEspecie: {especie}")

            f_statistic, p_value = f_oneway(*grupos)

            print(f"F-statistic: {f_statistic}")
            print(f"P-value: {p_value}")

        else:
            print(f"\nEspecie: {especie} - Datos insuficientes para el test.")
    
    return resultados
