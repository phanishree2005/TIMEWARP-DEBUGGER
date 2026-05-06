def calculate_total(prices, discount):
    total = sum(prices)
    # BUG: Discount is meant to be subtracted, but here it's added
    final_price = total + discount
    return final_price

prices = [10, 20, 30]
# Should be 50, but because of bug, it becomes 70
print(calculate_total(prices, 10))

# Note: In the debugger, you can step into calculate_total and see
# final_price change to 70 instead of 50.
