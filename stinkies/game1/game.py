from random import choice, shuffle

from game1.words import adjectives, things


def pick_random_thing():
    return " ".join((choice(adjectives), choice(things)))


class Bag:
    def __init__(self, name):
        self.name = name
        self.contents = []
        self.coins = 0

    def load_random_things(self, n=1):
        for i in range(n):
            self.contents.append(pick_random_thing())
            self.coins += 2

    def __str__(self):
        contents = ", ".join(self.contents)
        return "{} ({})\n{}".format(self.name, self.coins, contents)

    def __repr__(self):
        return str(self)

    def trade(self, bag, thing=None):
        old_thing = thing or choice(self.contents)
        self.contents.remove(old_thing)
        new_thing = choice(bag.contents)
        bag.contents.remove(new_thing)
        self.contents.append(new_thing)
        bag.contents.append(old_thing)
        return (old_thing, new_thing)

    def buy_new_thing(self):
        if self.coins >= 2:
            self.contents.append(pick_random_thing())
            self.coins -= 2

    def buy_from(self, bag, thing, coins=2):
        if self.coins >= coins:
            bag.contents.remove(thing)
            self.contents.append(thing)
            self.coins -= coins

    def sell_back(self, thing):
        self.contents.remove(thing)
        self.coins += 1


michelle = Bag("Michelle")
michelle.load_random_things(n=6)
bea = Bag("Bea")
bea.load_random_things(n=6)
daddy = Bag("Daddy")
daddy.load_random_things(n=6)
mummy = Bag("Mum")
mummy.load_random_things(n=6)
