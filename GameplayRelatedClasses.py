class PlayerInfo:
    def __init__(self):
        self.CardsInHand = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
        self.DiscountedCardsInHand = [4, 4, 3, 3, 3, 2, 2, 2, 1, 1]


class GameInfo:
    def __init__(self, playerID, gameID, CurrentTasks, AmountOfPlayers, NicknamesOfPlayers):
        self.PlayerID = playerID
        self.GameId = gameID
        self.CurrentPlayer = 0
        self.PlayerAmount = AmountOfPlayers
        self.PlayersNicknames = NicknamesOfPlayers
        self.Tasks = CurrentTasks


