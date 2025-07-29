condition_mapping = {
    "Platform X": {"Like New": "New", "Good": "Good", "Fair": "Scrap"},
    "Platform Y": {"Like New": "3 Stars", "Good": "2 Stars", "1 Star": "Usable"}, # Corrected "1 Star" mapping
    "Platform Z": {"Like New": "As New", "Good": "Good", "Fair": "Good"},
}

fees = {
    "Platform X": lambda price: round(price * 0.10, 2),
    "Platform Y": lambda price: round((price * 0.08) + 2, 2),
    "Platform Z": lambda price: round(price * 0.12, 2),
}

# Added a minimum profit threshold
MIN_PROFIT_THRESHOLD = 5.0 
def calculate_selling_price(cost_price, platform):
    margin = 1.12  # 12% default markup
    price = cost_price * margin
    fee = fees[platform](price)
    final_price = round(price + fee, 2)
    return final_price, fee

def map_condition(cond, platform):
    return condition_mapping.get(platform, {}).get(cond, "Unknown")