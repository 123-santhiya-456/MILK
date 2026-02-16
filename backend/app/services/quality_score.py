def calculate_quality(ph: float, temperature: float):
    score = 100

    # pH Ideal range: 6.5 – 6.8
    if ph < 6.5 or ph > 6.8:
        score -= 30

    # Temperature ideal < 10°C
    if temperature > 10:
        score -= 20

    return max(score, 0)
