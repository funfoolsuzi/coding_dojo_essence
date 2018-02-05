from product import Product

class Store(object):
    def __init__(self, location, owner):
        self.location = location
        self.owner = owner
        self.products = []

    def add_product(self, prod):
        self.products.append(prod)
        return self

    def remove_product(self, prodname):
        for p in self.products:
            if p.name == prodname:
                self.products.remove(p)
        return self

    def inventory(self):
        for p in self.products:
            p.display_info()
            print

    def __repr__(self):
        return "<Store object {}, owner {}>".format(self.location, self.owner)

if __name__ == "__main__":
    s1 = Store("Lynnwood", "Li")
    s1.add_product(Product("banana", 10, "1 lb", "sun"))
    s1.add_product(Product("watermelon", 3, "1.5 lb", "west"))
    s1.inventory()
