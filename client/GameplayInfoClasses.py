class PlayerInfo:
    def __init__(self):
        self.CardsInHand = [3, 2, 4, 1, 0, 6, 2, 1, 0, 1]
        self.DiscountedCardsInHand = [1, 2, 3, 0, 0, 0, 1, 0, 0, 0]


class ShopInfo:
    def __init__(self):
        self.CardsInShop = [5, 6, 2, 4, 2, 6, 3, 2, 1, 1]
        self.DiscountedCardsInShop = [2, 1, 0, 1, 1, 1, 0, 0, 1, 0]

class GameInfo:
    def __init__(self, gameID, CurrentTasks, AmountOfPlayers, NicknamesOfPlayers):
        self.GameId = gameID
        self.CurrentPlayer = 0
        self.PlayerAmount = AmountOfPlayers
        self.PlayersNicknames = NicknamesOfPlayers
        self.Tasks = CurrentTasks


