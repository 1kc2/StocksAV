from stock import Stock

class Position:
    def __init__(self, symbol, quantity, avg_price):
        self.symbol = symbol
        self.quantity = quantity
        self.avg_price = avg_price
        self.stock = Stock("SHOP.TO", "2019-11-04")

    def open_pnl(self):
        print(self.stock.current_price())
        return (self.stock.current_price() - self.avg_price) * self.quantity

    def total_cost(self):
        return self.avg_price * self.quantity

    def current_value(self):
        return self.stock.current_price() * self.quantity

if __name__ == '__main__':
    td = Position("TD.TO", 13, 73.95)
    shop = Position("SHOP.TO", 10, 133.93)
    print(td.open_pnl()+shop.open_pnl())
