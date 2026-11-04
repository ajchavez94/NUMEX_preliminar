import numpy as np
import pandas as pd


def assign_atmospheric_values(df, option="annual"):

    """
    Assign atmospheric CO2 concentration (Cair)
    and atmospheric d13C values according to year
    or elevation.

    Parameters
    ----------
    df : pandas.DataFrame

    option : str
        "annual"     -> assign values by year
        "elevation"  -> assign values by elevation

    Returns
    -------
    pandas.DataFrame
    """
    df["Sampling date"]
    df["year"] = pd.to_datetime(df["Sampling date"]).dt.year
       
    # =========================================================
    # OPTION 1 — ANNUAL VALUES
    # Recommended for long-lived leaves
    # =========================================================

    if option == "annual":
        
    
        conditions = [
            df["year"] == 2023,
            df["year"] == 2024
        ]

        # Atmospheric CO2 concentration (ppm)
        Cair_values = [
            419.3,   # 2023
            421.1    # 2024
        ]

        # Atmospheric δ13C values
        d13Cair_values = [
            -8.70,   # 2023
            -8.64    # 2024
        ]

        df["Cair"] = np.select(
            conditions,
            Cair_values,
            default=np.nan
        )

        df["d13Cair"] = np.select(
            conditions,
            d13Cair_values,
            default=np.nan
        )

    # =========================================================
    # OPTION 2 — ELEVATION-DEPENDENT VALUES
    # =========================================================

    elif option == "elevation":

        conditions = [
            df["elevation_m"] == 1000,
            df["elevation_m"] == 2000,
            df["elevation_m"] == 3000
        ]

        d13Cair_values = [
            -8.714103,
            -9.23,
            -9.5219
        ]

        # You can modify this if you have
        # elevation-specific CO2 concentrations
        Cair_values = [
            421.0,
            421.0,
            421.0
        ]

        df["d13Cair"] = np.select(
            conditions,
            d13Cair_values,
            default=np.nan
        )

        df["Cair"] = np.select(
            conditions,
            Cair_values,
            default=np.nan
        )

    else:
        raise ValueError(
            "option must be either 'annual' or 'elevation'"
        )

    return df


def calculate_iWUE(df):

    """
    Calculate intrinsic Water Use Efficiency (iWUE)
    using Farquhar discrimination model.
    """

    df = df.copy()

    # =========================================================
    # Constants
    # =========================================================

    a = 4.4
    b = 27
    f = 12
    cP = 40

    # =========================================================
    # Carbon isotope discrimination
    # =========================================================

    df["Δ13C_cell"] = (
        (df["d13Cair"] - df["δ13C (‰ v.s.V-PDB)"])
        /
        (1 + (df["δ13C (‰ v.s.V-PDB)"] / 1000))
    )

    # =========================================================
    # Intercellular CO2 concentration (Ci)
    # =========================================================

    df["Ci"] = (
        (
            df["Cair"] *
            (df["Δ13C_cell"] - a)
        )
        +
        (f * cP)
    ) / (b - a)

    # =========================================================
    # Ci/Ca ratio
    # =========================================================

    df["Ci/Ca"] = df["Ci"] / df["Cair"]

    # =========================================================
    # Intrinsic Water Use Efficiency
    # =========================================================

    df["iWUE (μmol/mol)"] = (
        (df["Cair"] / 1.6)
        *
        (1 - (df["Ci"] / df["Cair"]))
    )

    # =========================================================
    # Remove empty rows
    # =========================================================

    df_clean = df[
        df["iWUE (μmol/mol)"].notnull()
    ]

    print("iWUE successfully calculated")
    print("Number of rows:", len(df_clean))

    return df_clean

