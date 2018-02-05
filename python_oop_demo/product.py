class Product(object):
    def __init__(self, name, price, weight, brand):
        self.name = name
        self.price = price
        self.weight = weight
        self.brand = brand
        self.status = "for sale"

    def sell(self):
        self.status = "sold"

    def add_tax(self, rate):
        return rate*self.price

    def return_product(self, reason):
        if reason == "defective":
            self.status = reason
            self.price = 0
        elif reason == "opened":
            self.status = "used"
            self.price *= .8
        else:
            self.status = "for sale"
        return self

    def display_info(self):
        print "Product Name: {}".format(self.name)
        print "Price: {}".format(self.price)
        print "Weight: {}".format(self.weight)
        print "Brand: {}".format(self.brand)
        print "Status: {}".format(self.status)
        return self

    def __repr__(self):
        return "<Product object {}, price {}>".format(self.name, self.price)

if __name__ == "__main__":
    PROD1 = Product("apple", 100, "10 lb", "honeydew").return_product("opened").display_info()
    