from collections import deque
from random import shuffle, randint


class Deck:
    def __init__(self):
        """Data structure that stores its owner's cards and quickly checks if the goals are completed."""
        self.card_ids = []
        self.vals = [0] * 11
        self.merch_vals = [0] * 11
        self.cats = {Items: 0, Pets: 0, Employees: 0}

    def add_cards(self, *_card_ids):
        """Add cards with the given ids to the deck."""
        self.card_ids += list(_card_ids)
        self.card_ids.sort()
        for card_id in _card_ids:
            card = CARDS[card_id]
            self.vals[card.value] += 1
            if card.is_merch:
                self.merch_vals[card.value] += 1
            self.cats[card.category] += 1

    def sell_cards(self, *_card_ids):
        """Delete cards with the given ids from the deck."""
        for card_id in _card_ids:
            self.card_ids.remove(card_id)
            card = CARDS[card_id]
            self.vals[card.value] -= 1
            if card.is_merch:
                self.merch_vals[card.value] -= 1
            self.cats[card.category] -= 1

    def check_a_tidy_mansion(self):
        """Return number of points earned through the goal "A tidy mansion".

        Description of the goal can be found in the rulebook."""
        points = 0
        _vals = [val for val in self.vals]
        val = 8
        while val > 0:
            if _vals[val] > 0 and _vals[val + 1] > 0 and _vals[val + 2] > 0:
                _vals[val] -= 1
                _vals[val + 1] -= 1
                _vals[val + 2] -= 1
                if val >= 6:
                    points += 7
                elif val >= 3:
                    points += 5
                else:
                    points += 3
            else:
                val -= 1
        return points

    def check_obsessed_by_arrangement(self):
        """Return number of points earned through the goal "Obsessed be arrangement".

        Description of the goal can be found in the rulebook."""
        mx_run = 0
        cur_run = 0
        for val in range(1, 11):
            if self.vals[val] > 0:
                cur_run += 1
            else:
                mx_run = max(mx_run, cur_run)
                cur_run = 0
        return 3 * mx_run

    def check_gem_of_my_collection(self):
        """Return number of points earned through the goal "Gem of my collection".

        Description of the goal can be found in the rulebook."""
        return 3 * self.vals.index(max(self.vals))

    def check_collector(self):
        """Return number of points earned through the goal "Collector".

        Description of the goal can be found in the rulebook."""
        return 10 - self.vals.count(0)

    def check_seeing_double(self):
        """Return number of points earned through the goal "Seeing double".

        Description of the goal can be found in the rulebook."""
        return 2 * (self.cats[Items] // 2) + \
               4 * (self.cats[Pets] // 2) + \
               5 * (self.cats[Employees] // 2)

    def check_three_is_better_than_two(self):
        """Return number of points earned through the goal "Three is better than two".

        Description of the goal can be found in the rulebook."""
        return 2 * (self.cats[Items] // 3) + \
               4 * (self.cats[Pets] // 3) + \
               5 * (self.cats[Employees] // 3)

    def check_the_sum_of_all_fears(self):
        """Return number of points earned through the goal "The sum of all fears".

        Description of the goal can be found in the rulebook."""
        return 3 * (sum(val * self.vals[val] for val in range(1, 11)) // 10)

    def check_too_snob(self):
        """Return number of points earned through the goal "Too snob".

        Description of the goal can be found in the rulebook."""
        points = 0
        for val in range(1, 11):
            points += (self.vals[val] > 0 and not self.merch_vals[val])
        return points

    def check_the_art_of_bargaining(self):
        """Return number of points earned through the goal "The art of bargaining".

        Description of the goal can be found in the rulebook."""
        return 10 - self.merch_vals.count(0)

    def get_cards(self):
        return self.card_ids

    def get_val_cnt(self, val):
        """Return the current number of cards with the given value."""
        return self.vals[val]

    def get_merch_cnt(self):
        """Return the current number of cards marked as merchandise."""
        return sum(self.merch_vals)


class Player:
    def __init__(self, player_id):
        """Class that handles operations with a single player."""
        self.id = player_id
        self.decks = {}
        self.goals = {}
        self.ready = {}

    def join_game(self, game_id):
        """Create a new deck, point counters and readiness status for the new game."""
        self.decks[game_id] = Deck()
        self.goals[game_id] = {
            a_tidy_mansion: 0,
            obsessed_by_arrangement: 0,
            gem_of_my_collection: 0,
            collector: 0,
            seeing_double: 0,
            three_is_better_than_two: 0,
            neighbors_festival: 0,
            the_sum_of_all_fears: 0,
            too_snob: 0,
            the_art_of_bargaining: 0,
            not_the_same_values: 0,
            fashion_at_lowest_price: 0,
        }
        self.ready[game_id] = False

    def change_readiness(self, game_id):
        """Change the readiness status. 'Ready' changes into 'not ready' and vice versa."""
        self.ready[game_id] += 1
        self.ready[game_id] %= 2

    def is_ready(self, game_id):
        """Return the readiness status. True if ready, False otherwise."""
        return self.ready[game_id]

    def leave_game(self, game_id):
        """Remove data from the game."""
        self.decks.pop(game_id)
        self.goals.pop(game_id)
        self.ready.pop(game_id)

    def add_cards(self, game_id, *card_ids):
        """Add cards to the deck used in the given game."""
        self.decks[game_id].add_cards(card_ids)

    def sell_cards(self, game_id, *card_ids):
        """Remove cards from the deck used in the given game."""
        self.decks[game_id].sell_cards(card_ids)

    def get_cards(self, game_id):
        deck = self.decks[game_id]
        return deck.get_cards()

    def get_val_cnt(self, game_id, val):
        """Return the current number of cards with the given value."""
        return self.decks[game_id].get_val_cnt(val)

    def get_merch_cnt(self, game_id):
        """Return the current number of cards marked as merchandise."""
        return self.decks[game_id].get_merch.cnt()

    def update_neighbors_festival(self, game_id, points):
        """Set points for the goal "Neighbors' festival" in the given game to the 'points' argument."""
        self.goals[game_id][neighbors_festival] = points

    def update_not_the_same_values(self, game_id, points):
        """Set points for the goal "Not the same values" in the given game to the 'points' argument."""
        self.goals[game_id][not_the_same_values] = points

    def update_fashion_at_lowest_price(self, game_id, points):
        """Set points for the goal "Fashion at lowest price" in the given game to the 'points' argument."""
        self.goals[game_id][fashion_at_lowest_price] = points

    def update_goals(self, game_id):
        """Update the point counters."""
        self.goals[game_id][a_tidy_mansion] = self.decks[game_id].check_a_tidy_mansion()
        self.goals[game_id][obsessed_by_arrangement] = self.decks[game_id].check_obsessed_by_arrangement()
        self.goals[game_id][gem_of_my_collection] = self.decks[game_id].check_gem_of_my_collection()
        self.goals[game_id][collector] = self.decks[game_id].check_collector()
        self.goals[game_id][seeing_double] = self.decks[game_id].check_seeing_double()
        self.goals[game_id][three_is_better_than_two] = self.decks[game_id].check_three_is_better_than_two()
        self.goals[game_id][the_sum_of_all_fears] = self.decks[game_id].check_the_sum_of_all_fears()
        self.goals[game_id][too_snob] = self.decks[game_id].check_too_snob()
        self.goals[game_id][the_art_of_bargaining] = self.decks[game_id].check_the_art_of_bargaining()


class Game:
    def __init__(self, game_id):
        """Class that handles the gameplay."""
        self.id = game_id
        self.players = []
        self.shop = []
        self.cur_player = 0
        self.stage = WAITING
        self.unused = deque()

    def get_players(self):
        """Return list of players

        Output:

        - list[player_id]"""
        return self.players

    def get_stage(self):
        """Return current game stage

        Output:

        - 0: WAITING
        - 1: RUNNING
        - 2: RESULTS"""
        return self.stage

    def add_player(self, player_id):
        """Add player."""
        self.players.append(player_id)
        PLAYERS[player_id].join_game(self.id)

    def change_player_readiness(self, player_id):
        """Change the readiness status of the player with the given id.
        'Ready' changes into 'not ready' and vice versa.

        If after the change all the players are ready, the game starts."""
        PLAYERS[player_id].change_readiness(self.id)
        if all(PLAYERS[player_id].is_ready()):
            self.start()

    def kick_player(self, player_id):
        """Remove player from the game."""
        self.players.remove(player_id)
        PLAYERS[player_id].leave_game(self.id)
        if not self.players:
            GAMES.pop(self.id)

    def start(self):
        """Start the game."""
        if self.stage != WAITING:
            return
        self.stage = RUNNING
        for i, player in enumerate(self.players):
            last_card = (10, 12, 14, 16, 18)
            player.add_cards(game_id=self.id, cards=(2, 4, 6, last_card[i]))
        all_cards = [1] * 4 + [2] * (7 - len(self.players)) + \
                    [3] * 3 + [4] * (7 - len(self.players)) + \
                    [5] * 3 + [6] * (6 - len(self.players)) + \
                    [7] * 3 + [8] * 5 + \
                    [9] * 2 + [10] * 4 + \
                    [11] * 2 + [12] * (4 - (len(self.players) >= 1)) + \
                    [13] * 2 + [14] * (3 - (len(self.players) >= 3)) + \
                    [15] + [16] * (3 - (len(self.players) >= 4)) + \
                    [17] + [18] * (2 - (len(self.players) >= 5)) + \
                    [19] + [20]
        shuffle(all_cards)
        all_cards.insert(randint(len(all_cards) - 7, len(self.players) - 1), 0)
        self.unused = deque(all_cards)

    def finish(self):
        """End the game and show the results."""
        self.stage = RESULTS

    def move(self, player_id, sold_cards_ids, bought_cards_ids):
        """Handle a player's move. Restock the shop after a valid move
        and finish game if the "Closed Shop" card is pulled."""
        if player_id == self.cur_player and sold_cards_ids and bought_cards_ids:
            return
        good_deal = True
        val0 = CARDS[sold_cards_ids[0]].value
        for card_id in sold_cards_ids:
            if CARDS[card_id].value != val0:
                good_deal = False
                break
        if good_deal:
            val0 = CARDS[bought_cards_ids[0]].value
            for card_id in bought_cards_ids:
                if CARDS[card_id].value != val0:
                    good_deal = False
                    break
            if good_deal:
                good_deal = (len(sold_cards_ids) == len(bought_cards_ids))
        sum_sold = sum(CARDS[card_id].value for card_id in sold_cards_ids)
        sum_bought = sum(CARDS[card_id].value for card_id in bought_cards_ids)
        fair_price = (sum_sold == sum_bought)
        if good_deal or fair_price:
            PLAYERS[player_id].sell_cards(self.id, sold_cards_ids)
            PLAYERS[player_id].add_cards(self.id, bought_cards_ids)

        if not self.restock():
            self.finish()

    def get_current_player(self):
        """Returns id of the current player."""
        return self.players[self.cur_player]

    def get_shop_cards(self):
        return self.shop

    def add_card_to_shop(self):
        """Add a new card from the queue to the shop."""
        new_card = self.unused.popleft()
        self.shop.append(new_card)

    def restock(self):
        """Restock the shop with new cards from the queue."""
        for _ in range(1 + (len(self.players) <= 3)):
            if not self.add_card_to_shop():
                return False
        while len(self.shop) < 5:
            if not self.add_card_to_shop():
                return False

    def check_neighbors_festival(self):
        """Give players points earned through the goal "Neighbors' festival".

        Description of the goal can be found in the rulebook."""
        for val in range(1, 11):
            mx_copies = max(PLAYERS[player_id].get_val_cnt(val) for player_id in self.players)
            for player_id in self.players:
                player = PLAYERS[player_id]
                if player.get_val_cnt(val) == mx_copies:
                    player.update_neighbors_festival(self.id, 5)

    def check_not_the_same_values(self):
        """Give players points earned through the goal "Not the same values".

        Description of the goal can be found in the rulebook."""
        mn_merch = sorted(PLAYERS[player_id].get_merch_cnt(self.id) for player_id in self.players)
        for player_id in self.players:
            player = PLAYERS[player_id]
            player_merch = player.get_merch_cnt(self.id)
            if player_merch == mn_merch[0]:
                player.update_not_the_same_values(self.id, 10)
            elif player_merch == mn_merch[1]:
                player.update_not_the_same_values(self.id, 6)
            elif player_merch == mn_merch[2]:
                player.update_not_the_same_values(self.id, 3)

    def check_fashion_at_lowest_price(self):
        """Give players points earned through the goal "Fashion at lowest price".

        Description of the goal can be found in the rulebook."""
        mx_merch = sorted([PLAYERS[player_id].get_merch_cnt(self.id) for player_id in self.players], reverse=True)
        for player_id in self.players:
            player = PLAYERS[player_id]
            player_merch = player.get_merch_cnt(self.id)
            if player_merch == mx_merch[0]:
                player.update_not_the_same_values(self.id, 10)
            elif player_merch == mx_merch[1]:
                player.update_not_the_same_values(self.id, 6)
            elif player_merch == mx_merch[2]:
                player.update_not_the_same_values(self.id, 3)


class Card:
    def __init__(self, card_id, value, is_merch, category):
        """Class that stores the properties of a certain card."""
        self.id = card_id
        self.value = value
        self.is_merch = is_merch
        self.category = category


# Handles for the cards' categories
Items = "Items"
Pets = "Pets"
Employees = "Employees"
Closed = "Closed"

# Handles for the goals
a_tidy_mansion = "a tidy mansion"
obsessed_by_arrangement = "obsessed by arrangement"
gem_of_my_collection = "gem of my collection"
collector = "collector"
seeing_double = "seeing_double"
three_is_better_than_two = "three is better than two"
neighbors_festival = "neighbors' festival"
the_sum_of_all_fears = "the sum of all fears"
too_snob = "too snob"
the_art_of_bargaining = "the art of bargaining"
not_the_same_values = "not the same values"
fashion_at_lowest_price = "fashion at lowest price"

# Handles for the game stages
WAITING = 0
RUNNING = 1
RESULTS = 2

GAMES = {}
PLAYERS = {}
CARDS = [Card(card_id=0, value=0, is_merch=False, category=Closed),
         Card(card_id=1, value=1, is_merch=True, category=Items),
         Card(card_id=2, value=1, is_merch=False, category=Items),
         Card(card_id=3, value=2, is_merch=True, category=Items),
         Card(card_id=4, value=2, is_merch=False, category=Items),
         Card(card_id=5, value=3, is_merch=True, category=Items),
         Card(card_id=6, value=3, is_merch=False, category=Items),
         Card(card_id=7, value=4, is_merch=True, category=Pets),
         Card(card_id=8, value=4, is_merch=False, category=Pets),
         Card(card_id=9, value=5, is_merch=True, category=Pets),
         Card(card_id=10, value=5, is_merch=False, category=Pets),
         Card(card_id=11, value=6, is_merch=True, category=Pets),
         Card(card_id=12, value=6, is_merch=False, category=Pets),
         Card(card_id=13, value=7, is_merch=True, category=Employees),
         Card(card_id=14, value=7, is_merch=False, category=Employees),
         Card(card_id=15, value=8, is_merch=True, category=Employees),
         Card(card_id=16, value=8, is_merch=False, category=Employees),
         Card(card_id=17, value=9, is_merch=True, category=Employees),
         Card(card_id=18, value=9, is_merch=False, category=Employees),
         Card(category=19, value=10, is_merch=True, card_id=Employees),
         Card(category=20, value=10, is_merch=False, card_id=Employees)]

MX_GAME_ID = 50


class Core:
    def __init__(self):
        pass

    def create_game(self):
        """Start new game session.

        Output:

        - -1:               server can't host more games

        - positive number:  game_id"""
        if len(GAMES) == MX_GAME_ID:
            return -1
        new_game_id = randint(1, MX_GAME_ID)
        while new_game_id in GAMES.keys():
            new_game_id = randint(1, MX_GAME_ID)
        new_game = Game(new_game_id)
        GAMES[new_game_id] = new_game
        return new_game_id

    def join_game(self, game_id, player_id):
        """Add player to a game.

        Output:

         - 0:   ok

         - -1:  game not found

         - -2:  player not found

         - -3:  player is already in this game

         - -4:  game has already started

         - -5:  game is already over

         - -6:  maximum number of players are in the game"""
        if game_id not in GAMES:
            return -1
        if player_id not in PLAYERS:
            return -2
        game = GAMES[game_id]
        if player_id in game.get_players():
            return -3
        if game.get_stage() == RUNNING:
            return -4
        if game.get_stage() == RESULTS:
            return -5
        if len(game.get_players()) == 5:
            return -6
        game.add_player(player_id)
        return 0

    def leave_game(self, game_id, player_id):
        """Kick player from a game.

        Output:

         - 0:   ok

         - -1:  game not found

         - -2:  player not found

         - -3:  player is not in this game"""
        if game_id not in GAMES:
            return -1
        if player_id not in PLAYERS:
            return -2
        game = GAMES[game_id]
        if player_id not in game.get_players():
            return -3
        game.kick_player(player_id)
        return 0

    def change_readiness(self, game_id, player_id):
        """Add player to a game.

        Output:

         - 0:   ok

         - -1:  game not found

         - -2:  player not found

         - -3:  game has already started

         - -4:  game is already over"""
        if game_id not in GAMES:
            return -1
        if player_id not in PLAYERS:
            return -2
        game = GAMES[game_id]
        if game.get_stage() == RUNNING:
            return -3
        if game.get_stage() == RESULTS:
            return -4
        game.change_player_readiness(player_id)
        return 0

    def current_player(self, game_id):
        """Return id of the player that is currently making a move.

        Output:

        - positive number: player_id

        - -1: game not found"""

        if game_id not in GAMES:
            return -1
        game = GAMES[game_id]
        return game.get_current_player()

    def get_shop_cards(self, game_id):
        """Return list of cards currently in the shop

        Output:

        - tuple(0, list[int]): ok and list of card ids

        - tuple(-1, []): game not found

        - tuple(-2, []): game hasn't started yet

        - tuple(-3, []): game is already over"""

        if game_id not in GAMES:
            return -1, []
        game = GAMES[game_id]
        if game.get_stage == WAITING:
            return -2, []
        if game.get_stage == RESULTS:
            return -3, []
        return game.get_shop_cards()

    def get_player_cards(self, game_id, player_id):
        """Return list of player's cards

        Output:

        - tuple(0, list[int]): ok and list of card ids

        - tuple(-1, []): game not found

        - tuple(-2, []): player not found

        - tuple(-3, []): player not in the game

        - tuple(-4, []): game hasn't started yet

        - tuple(-5, []): game is already over"""

        if game_id not in GAMES:
            return -1, []
        game = GAMES[game_id]
        if player_id not in PLAYERS:
            return -2, []
        player = PLAYERS[player_id]
        if player_id not in game.get_players():
            return -3, []
        if game.get_stage == WAITING:
            return -4, []
        if game.get_stage == RESULTS:
            return -5, []
        return player.get_cards(game_id)