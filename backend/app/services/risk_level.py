def get_risk_level(score):
    if score >= 80:
        return "Fresh"
    elif score >= 50:
        return "Warning"
    else:
        return "Spoiled"
