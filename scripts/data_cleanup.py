"""
Function to prepare data received from the wearables reaching the API
for consumption by the models
"""

NO_INCAP = 0

def convert_height_in_to_cm(height: float, height_unit: str) -> float:
    if height_unit == "in":
        return height * 2.54
    else:
        return height

def calc_bmi(weight: float, height: float) -> int:
    bmi_categories = [1, 2, 3, 4]
    bmi_bins = [0, 18.5, 25, 30, float("inf")]
    bmi = weight / (height / 100) ** 2
    for i, max_bmi in enumerate(bmi_bins[1:]):
        if bmi < max_bmi:
            return bmi_categories[i]
    return bmi_categories[-1]

def calc_weekly_minutes(minutes: float, frequency: int) -> float:
    return minutes * frequency

def calc_activity_level(minutes: float, activity_type: str) -> str:
    mod_bins = [-0.1, 0, 149, 299, float("inf")]
    vig_bins = [-0.1, 0, 74, 149, float("inf")]
    activity_levels = ["sin", "insuficiente", "minimo", "supera"]

    if activity_type == 'mod':
        bins = mod_bins
    else:
        bins = vig_bins

    for i, max_minutes in enumerate(bins[1:]):
        if minutes <= max_minutes:
            return activity_levels[i]
    return activity_levels[-1]

def build_features(raw_data: dict) -> dict:
    """
    Build features from raw data.

    Args:
        raw_data (dict): Raw data.
    """

    # Calculate weekly minutes for moderate and vigorous activity
    mod_weekly = calc_weekly_minutes(raw_data["MODMIN"], raw_data["MODFREQ"])
    vig_weekly = calc_weekly_minutes(raw_data["VIGMIN"], raw_data["VIGFREQ"])

    return {
        # General
        "SEX_A": raw_data["SEX_A"],
        "AGEP_A": raw_data["AGE"],
        "HEIGHT_CM": convert_height_in_to_cm(raw_data["HEIGHT"], raw_data["HEIGHT_UNIT"]),
        "WEIGHT_A": raw_data["WEIGHT"], # el pipeline no la usa, es para recordar que debo pedir WEIGHT
        "BMICAT_A": calc_bmi(raw_data["WEIGHT"], convert_height_in_to_cm(raw_data["HEIGHT"], raw_data["HEIGHT_UNIT"])),
        "SLPHOURS_A": raw_data["SLPHOURS"],
        # Diagnostics
        "DEPEV_A": raw_data["DEPEV"],
        "ANXEV_A": raw_data["ANXEV"],
        "ASEV_A": raw_data["ASEV"],
        # Activity
        "MODMIN_A": raw_data["MODMIN"],
        "VIGMIN_A": raw_data["VIGMIN"],
        "MODFREQW_A": raw_data["MODFREQ"],
        "VIGFREQW_A": raw_data["VIGFREQ"],
        "STRFREQW_A": raw_data["STRFREQ"],
        "MODMIN_WEEKLY": mod_weekly,
        "VIGMIN_WEEKLY": vig_weekly,
        "MOD_LEVEL": calc_activity_level(mod_weekly, 'mod'),
        "VIG_LEVEL": calc_activity_level(vig_weekly, 'vig'),
        "CANT_MODFREQW_A": NO_INCAP,
        "CANT_VIGFREQW_A": NO_INCAP,
        "CANT_STRFREQW_A": NO_INCAP
    }

def build_features_batch(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Build features from raw data in batch.

    Args:
        df_raw (pd.DataFrame): DataFrame containing raw data.
    """
    return pd.DataFrame(
        list(df_raw.apply(lambda row: build_features(row.to_dict()), axis=1))
    )