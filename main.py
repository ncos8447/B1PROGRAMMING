#personal expense tracker

#data structure
expense_records = []
category_totals = {}
unique_categories = set()

print("Welcome to Personal Expense Tracker!\n")

#collect data

num_expenses = 0
while num_expenses < 5:
    print(f"Enter Expense {num_expenses + 1}:")
    category = input("Category (e.g., food, transport): ").strip()
    while True:
        try:
            amount = float(input("  Amount ($): "))
            if amount >= 0:
                break
            else:
                print("Amount cannot be negative.")
        except ValueError:
            print("Please enter a valid number.")

    date = input("  Date (YYYY-MM-DD): ").strip()

    expense_records.append((category, amount, date))

    num_expenses += 1

#categorize
for category, amount, _ in expense_records:
    unique_categories.add(category)
    category_totals[category] = category_totals.get(category, 0) + amount

#calculate overall stats
amounts = [amount for _, amount, _ in expense_records]

overall_stats = {
    'total_spending': sum(amounts),
    'average_expense': sum(amounts) / len(amounts) if amounts else 0,
    'highest_expense': max(amounts) if amounts else 0,
    'lowest_expense': min(amounts) if amounts else 0
}

#spending report

print("\n=== OVERALL SPENDING SUMMARY ===")
print(f"Total Spending: ${overall_stats['total_spending']:.2f}")
print(f"Average Expense: ${overall_stats['average_expense']:.2f}")
print(f"Highest Expense: ${overall_stats['highest_expense']:.2f}")
print(f"Lowest Expense: ${overall_stats['lowest_expense']:.2f}")

print("\n=== OVERALL SPENDING SUMMARY ===")
print(unique_categories)
print(f"Total unique categories: {len(unique_categories)}")

print("\n=== OVERALL SPENDING SUMMARY ===")
for category, amount in category_totals.items():
    print(f"{category}: ${amount:.2f}")

