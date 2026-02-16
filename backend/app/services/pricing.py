def calculate_price(score: float, weight: float):
    if score >= 80:
        price_per_liter = 50
        status = "Accept"
    elif score >= 50:
        price_per_liter = 35
        status = "Warning"
    else:
        price_per_liter = 0
        status = "Reject"

    total_amount = price_per_liter * weight

    return status, price_per_liter, total_amount
