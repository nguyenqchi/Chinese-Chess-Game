import pygame

from game.utils import Color, WIN_HEIGHT, WIN_WIDTH, RED_TURN, BLUE_TURN
from game.controlPanel import ControlPanel
from game.game import Game
from datetime import datetime



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
        draw(game, controlPanel)
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
    
    run = True
    numMoves = 0

    while run:
        draw(game, controlPanel)
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
    
    run = True
    numMoves = 0

    while run:
        draw(game, controlPanel)
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



def main():
    """
    Main function
    """

    game = Game(WIN)
    controlPanel = ControlPanel(game)

    # #check if the results file already exists then open that file instead of create a new file

    # with open("results.txt", "a") as f:
    #     f.write("Random Agent vs Minimax Agent\n")
    #     timestamp = datetime.now().isoformat()  
    #     f.write("timestamp: " + timestamp)
    #     f.write("\n")
    #     for i in range(15):
    #         f.write(randomVSminimax(game, controlPanel))
    #         game.resetGame()
    #         f.write("\n")
    #         if i % 5 == 0:
    #             f.flush()
    #             timestamp = datetime.now().isoformat()  
    #             f.write("timestamp: " + timestamp)
    #             f.write("\n")
    #     timestamp = datetime.now().isoformat()  
    #     f.write("timestamp: " + timestamp)
    #     f.write("\n")
    #     f.write("Random Agent vs CMA-ES Agent\n")  
    #     for i in range(50):
    #         f.write(randomVScmaes(game, controlPanel))
    #         game.resetGame()
            
    #         f.write("\n")
    #         if i % 5 == 0:
    #             f.flush()
    #             timestamp = datetime.now().isoformat()  
    #             f.write("timestamp: " + timestamp)
    #             f.write("\n")
    #     timestamp = datetime.now().isoformat()  
    #     f.write("timestamp: " + timestamp)
    #     f.write("\n")
    #     f.write("CMAES Agent vs Minimax Agent\n")  
    #     for i in range(50):
    #         f.write(cmaseVSminimax(game, controlPanel))
    #         game.resetGame()
            
    #         f.write("\n")
    #         if i % 5 == 0:
    #             f.flush()
    #             timestamp = datetime.now().isoformat()  
    #             f.write("timestamp: " + timestamp)
    #             f.write("\n")
        
            

    # pygame.quit()

    randomVSminimax(game, controlPanel)
    game.resetGame()

if __name__ == "__main__":
    main()
