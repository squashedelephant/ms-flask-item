
class Item:
    @classmethod
    def calculate_total_price(items):
        total_price = 0
        for item in items:
            sub_price = item['quantity'] * item['price']
            total_price += sub_price
        return total_price

    @classmethod
    def calculate_tax(total_price):
        tax = total_price * 0.08
        return total_price + tax
