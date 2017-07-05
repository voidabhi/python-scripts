def add_milk(func):
    def actual(*args, **kwargs):
        return func(*args, **kwargs) + 25
    return actual

def add_cinnamon(func):
    def actual(*args, **kwargs):
        return func(*args, **kwargs) + 10
    return actual

@add_milk
@add_cinnamon
def buy_mixed_coffee():
    return 50

price = buy_mixed_coffee()
print("mixed price: %s" % price)

# add milk again
price = add_milk(buy_mixed_coffee)()
print("double milk price: %s" % price)

# the same as buy_mixed_coffee
def buy_coffee():
    return 50

price = add_milk(add_cinnamon(buy_coffee))()
print("mixed price: %s" % price)
