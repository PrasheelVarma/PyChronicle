def calculate_total(price, quantity):
    total = price * quantity
    return total


name = "Laptop"
price = 500
quantity = 2

total = calculate_total(price, quantity)

discount = 50
final_price = total - discount

for i in range(3):
    final_price += 10

status = "Expensive"

if final_price < 1000:
    status = "Affordable"

print(name)
print(final_price)
print(status)
