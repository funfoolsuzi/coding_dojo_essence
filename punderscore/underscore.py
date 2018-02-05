class Underscore(object):
    def map(self, lis, func):
        newlis = []
        for item in lis:
            newlis.append(func(item))
        return newlis
    def reduce(self, lis, func):
        accum = ""
        for item in lis:
            accum += func(item)
        return accum
    def find(self, lis, func):
        for item in lis:
            if func(item):
                return item
    def filter(self, lis, func):
        newlis = []
        for item in lis:
            if func(item):
                newlis.append(item)
        return newlis
    def reject(self, lis, func):
        newlis = []
        for item in lis:
            if not func(item):
                newlis.append(item)
        return newlis

_ = Underscore()

if __name__ == "__main__":
    print _.filter([1, 2, 3, 4, 5, 6], lambda x: x%2 == 0)
