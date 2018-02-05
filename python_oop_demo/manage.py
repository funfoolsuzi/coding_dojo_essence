from store import Store
from product import Product

s1 = Store("Lynnwood", "Li")
s1.add_product(Product("banana", 10, "1 lb", "sun"))
s1.add_product(Product("watermelon", 3, "1.5 lb", "west"))
s1.inventory()
print s1
