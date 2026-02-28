#product Pricing Manager

#sample product data (name, base price, category, tier)
products_data = [
    "Laptop,1200,Electronics,Premium",
    "Jeans,80,Clothing,Standard",
    "Book,25,Books,Budget",
    "Coffee Maker,150,Home,Premium"
]

def calculate_discount(category, tier):
    category_discounts = {
        "Electronics": 10,
        "Clothing": 15,
        "Books": 5,
        "Home": 12
    }
    tier_discounts = {
        "Premium": 5,
        "Standard": 0,
        "Budget": 2
    }

    category_discount = category_discounts.get(category, 0)
    tier_discount = tier_discounts.get(tier, 0)

    return category_discount + tier_discount

products = []
total_discount_percentages = []

for line_num, line in enumerate(products_data, start=1):
    try:
        name, base_price_str, category, tier = line.split(',')
        base_price = float(base_price_str)

        #discounts
        discount_pct = calculate_discount(category, tier)
        discount_amt = base_price * (discount_pct / 100)
        final_price = base_price - discount_amt

        #store the data
        products.append({
            'name': name,
            'base_price': base_price,
            'discount_pct': discount_pct,
            'discount_amt': discount_amt,
            'final_price': final_price
        })
        total_discount_percentages.append(discount_pct)

    except ValueError:
        print(f"Line {line_num}: Invalid format or price '{line}' skipped.")

#report
try:
    with open('pricing_report.txt', 'w') as report:
        report.write("PRICING REPORT\n")
        report.write("="*75 + "\n")
        report.write(f"{'Product Name':30} {'Base Price':>12} {'Discount %':>12} "
                     f"{'Discount $':>12} {'Final Price':>12}\n")
        report.write("-"*75 + "\n")

        for product in products:
            report.write(f"{product['name']:30} "
                         f"${product['base_price']:>10.2f} "
                         f"{product['discount_pct']:>10.2f}% "
                         f"${product['discount_amt']:>10.2f} "
                         f"${product['final_price']:>10.2f}\n")

except IOError:
    print("Error: Could not write to 'pricing_report.txt'.")
    exit(1)

#summary
if products:
    total_products = len(products)
    avg_discount = sum(total_discount_percentages) / total_products
    print(f"Total products processed: {total_products}")
    print(f"Average discount applied: {avg_discount:.2f}%")
else:
    print("No products were processed.")
