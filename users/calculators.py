def calculate_bmi(weight_kg, height_cm):
    if not weight_kg or not height_cm or height_cm == 0:
        return None
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)

def calculate_bmr_mifflin_st_jeor(weight_kg, height_cm, age_years, sex):
    if not weight_kg or not height_cm or not age_years or not sex:
        return None

    # Mifflin-St Jeor Formula
    # Men: (10 * weight (kg)) + (6.25 * height (cm)) - (5 * age (years)) + 5
    # Women: (10 * weight (kg)) + (6.25 * height (cm)) - (5 * age (years)) - 161

    bmr_calc = (10 * float(weight_kg)) + (6.25 * float(height_cm)) - (5 * int(age_years))

    if sex.upper() == 'M': # Male
        bmr_calc += 5
    elif sex.upper() == 'F': # Female
        bmr_calc -= 161
    else: # 'Other' or 'Prefer not to say' - cannot accurately calculate without binary sex for this formula
        return None

    return round(bmr_calc, 2)

ACTIVITY_LEVELS = {
    'SEDENTARY': 1.2,       # Sedentary (little or no exercise)
    'LIGHT': 1.375,         # Lightly active (light exercise/sports 1-3 days/week)
    'MODERATE': 1.55,       # Moderately active (moderate exercise/sports 3-5 days/week)
    'ACTIVE': 1.725,        # Very active (hard exercise/sports 6-7 days a week)
    'VERY_ACTIVE': 1.9      # Super active (very hard exercise/physical job & exercise 2x/day)
}

ACTIVITY_LEVEL_CHOICES = [
    ('SEDENTARY', 'Sedentary (little or no exercise)'),
    ('LIGHT', 'Lightly active (light exercise 1-3 days/week)'),
    ('MODERATE', 'Moderately active (moderate exercise 3-5 days/week)'),
    ('ACTIVE', 'Very active (hard exercise 6-7 days/week)'),
    ('VERY_ACTIVE', 'Super active (very hard exercise/job & exercise 2x/day)'),
]

def calculate_daily_calorie_needs(bmr, activity_level_key):
    if not bmr or not activity_level_key or activity_level_key not in ACTIVITY_LEVELS:
        return None
    multiplier = ACTIVITY_LEVELS[activity_level_key]
    return round(bmr * multiplier, 0) # Calories often rounded to nearest whole number
