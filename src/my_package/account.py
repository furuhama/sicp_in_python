"""
every Account instance has its holder & balance
"""


class Account(object):
    def __init__(self, account_holder):
        self.balance = 0
        self.holder = account_holder

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            return 'Insufficient funds'
        self.balance -= amount
        return self.balance

    def status(self):
        print("====== basic info ======\n{}\nholder: {}\nbalance: {}".format(
            self, self.holder, self.balance))
