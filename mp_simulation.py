import pygame

from game.utils import Color, WIN_HEIGHT, WIN_WIDTH, RED_TURN, BLUE_TURN
from game.controlPanel import ControlPanel
from game.game import Game
from datetime import datetime
import multiprocessing as mp
from functools import partial


# Increase sharpness
import ctypes

#ctypes.windll.shcore.SetProcessDpiAwareness(1)

# Window's Configuration
WIN_WIDTH = WIN_WIDTH  # height and width of window
WIN_HEIGHT = WIN_HEIGHT

WIN = pygame.display.set_mode(
    (WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE
)  # initilize win form
pygame.display.set_caption("Chinese Chess Game")  # win caption
pygame.font.init()
myfont = pygame.font.SysFont("Comic Sans MS", 15)




def draw(game, controlPanel):
    """
    Drawing the game to window
    """
    WIN.fill(Color.BLACK)
    game.updateGame()

    controlPanel.draw(WIN)
    pygame.display.update()

def randomVSminimax(game, controlPanel):
    """
    Random player vs Minimax player
    """
    
    run = True
    numMoves = 0
    while run:
        # draw(game, controlPanel)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            controlPanel.checkForClick(pos)

        if not game.isOver:
            if game.turn == RED_TURN:

                game.minimaxMove()
            elif game.turn == BLUE_TURN:
                game.randomMove()
        else:
            #Check who is the winner
            if game.turn == RED_TURN:
                
                print("Random Agent wins")
                return "random"
            else:
                print("Minimax Agent wins")
                return "minimax"
        numMoves += 1
        if numMoves >= 200:
            return 'draw'
                
def randomVScmaes(game, controlPanel):
    game = Game(WIN)
    controlPanel = ControlPanel(game)
    
    run = True
    numMoves = 0

    while run:
        # draw(game, controlPanel)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            controlPanel.checkForClick(pos)

        if not game.isOver:
            if game.turn == RED_TURN:

                game.cmaesMove()
            elif game.turn == BLUE_TURN:
                game.randomMove()
        else:
            #Check who is the winner
            if game.turn == RED_TURN:
                print("Random Agent wins")
                return 'random'
            else:
                print("CMA-ES Agent wins")
                return 'cmaes'
        numMoves += 1
        if numMoves >= 200:
            return 'draw'


def cmaseVSminimax(game, controlPanel):
    game = Game(WIN)
    controlPanel = ControlPanel(game)
    
    run = True
    numMoves = 0

    while run:
        # draw(game, controlPanel)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            controlPanel.checkForClick(pos)

        if not game.isOver:
            if game.turn == RED_TURN:

                game.minimaxMove()
            elif game.turn == BLUE_TURN:
                game.cmaesMove()
        else:
            #Check who is the winner
            if game.turn == RED_TURN:
                print("CMA-ES Agent wins")
                return 'cmaes'
            else:
                print("Minimax Agent wins")
                return 'minimax'
                
        numMoves += 1
        if numMoves >= 200:
            return 'draw'


def run_versus(game_func: callable, epochs):
    game = Game(WIN)
    controlPanel = ControlPanel(game)
    with open(f"./outputs/results_{game_func.__name__}.txt", "a") as f:
        f.write(f"Game: {game_func.__name__} with {epochs} epochs\n")
        timestamp = datetime.now().isoformat()
        f.write("Start: " + timestamp)
        f.write("\n")
        for i in range(epochs):
            winner = game_func(game, controlPanel)
            f.write(f"Round {i+15}: {winner}")
            game.resetGame()
            f.write("\n")
            if i % 5 == 0:
                timestamp = datetime.now().isoformat()
                f.write(f"Round {i+15}: " + timestamp)
                f.write("\n")
                f.flush()


def main():
    """
    Main function
    """

    # game = Game(WIN)
    # controlPanel = ControlPanel(game)

    #check if the results file already exists then open that file instead of create a new file


    run_func = partial(run_versus)

    # function, epochs
    args = [
        [randomVSminimax, 50], 
        [randomVScmaes, 50],
        [cmaseVSminimax, 50]
    ]

    with mp.Pool(processes=len(args)) as pool:
        pool.starmap(run_func, args)
    
    pygame.quit()

if __name__ == "__main__":
    main()

