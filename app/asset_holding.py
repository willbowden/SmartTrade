

class AssetHolding:
    def __init__(self):
        self.balance = 0
        self.value = 0
        self.orders = []
        self.totalSpend = 0
        self.profit = 0
        self.profitPercent = 0

    def update(self, price):
        self.value = self.balance * price

    def calculate_profit(self):
        self.profit = self.value - self.totalSpend
        self.profitPercent = (self.profit / self.totalSpend) * 100
    
    def sell(self, quantity, value):
        self.balance -= quantity
        if value > self.totalSpend:
            self.totalSpend = 0
        else:
            self.totalSpend -= value

    def buy(self, quantity, spend):
        self.balance += quantity
        self.totalSpend += spend