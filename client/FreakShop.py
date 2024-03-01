from client.GameplayInterface import Game
from client.Menu import MenuView
from client.GameplayInfoClasses import GameInfo

if __name__ == "__main__":
    Menu = MenuView()
    CurrentGame = Game(GameInfo( 1, [1, 9, 5], 4, ["Pasha", "Sasha", "Nagibator228", "Боб"]))
    CurrentDisplayStatus = "menu"
    while True:
        if CurrentDisplayStatus == "menu":
            CurrentDisplayStatus = Menu.ShowStartMenu()
        elif CurrentDisplayStatus == "gameplay":
            CurrentGame.StartGame()
