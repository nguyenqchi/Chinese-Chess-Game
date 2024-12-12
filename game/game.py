from copy import deepcopy
from pprint import pprint

from .utils import RED_TURN, BLUE_TURN
from .board import BoardGame
import random
import time
from .pieces import Soldier
from cma import CMAEvolutionStrategy

class Game:
    def __init__(self, win):
        self.win = win
        self._init()

    def updateGame(self):
        self.board.drawGrid(self.win)
        time.sleep(2)

    def _init(self):
        """
        Initilize new board
        """
        self.board = BoardGame()
        self.tempBoard = self.board
        self.gameover = False
        self.turn = RED_TURN
        self.selectedPiece = None
        self.enemyPieces = []

        #assign id to each piece
        for i, piece in enumerate(self.board.activePices):
            piece.id = i
        # Track the number of moves for each piece
        self.piece_move_count = {piece.id: 0 for piece in self.board.activePices}


    @property
    def isOver(self):
        return self.gameover

    def resetGame(self):
        """
        Reset the game
        """
        self._init()

    def undo(self):
        """
        Undo a move
        """

        if not self.isOver:
            self.board.deselectPiece(self.selectedPiece.position)
            self.board = self.tempBoard
            self.turn = self.board.turn

    def switchTurn(self):
        """
        Switching side
        """
        self.turn = RED_TURN if self.turn == BLUE_TURN else BLUE_TURN
        self.enemyPieces = [
            piece for piece in self.board.activePices if piece.side != self.turn
        ]

    def checkForMove(self, clickedPos):
        """
        Check for click event to move pieces around in the game
        """
        # Check if any position in the board is clicked
        if self.board.isClicked(clickedPos):
            postion = self.board.getPositionFromCoordinate(clickedPos)
            piece = self.board.getPiece(postion)

            if not self.selectedPiece:
                if piece is not None and piece.side == self.board.turn:
                    self.selectedPiece = piece
                    self.selectedPiece.makeSelected()
                    self.board.movables = self.selectedPiece.possibleMoves

            else:
                if piece == self.selectedPiece:
                    self.board.deselectPiece(postion)
                    self.selectedPiece = None
                # if another position is clicked
                else:
                    # if piece can move to that position
                    moved = self.move(postion)

                    if not moved:
                        self.board.deselectPiece(self.selectedPiece.getPosition())
                        self.selectedPiece = None
                        self.checkForMove(clickedPos)

        else:  # If something else other than the board is not clicked, diselect any selected piece
            if self.selectedPiece is not None:
                self.board.deselectPiece(self.selectedPiece.getPosition())
                self.selectedPiece = None

    def move(self, postion):
        """
        Moving the piece
        position: args tuple
        """
        # print("Active Red Pieces: ", self.board.getActiveRed())
        # print("Active Blue Pieces: ", self.board.getActiveBlue())
        # print(f"Moving {self.selectedPiece} to {postion}")
        if postion in self.board.movables:
            self.tempBoard = deepcopy(self.board)
            self.board.movePiece(self.selectedPiece.position, postion)
            self.selectedPiece = None
            self.switchTurn()
            self.checkForMated()

            if self.calculateNextMoves() == 0:
                self.gameover = True
    
            return True
        else:
            print(f"Cant move there {postion}")
            return False

    def checkForMated(self):
        """
        Check if the lord is under attack
        """
        lordPiece = self.board.getLord(self.turn)
        enemyMoves = []
        for p in self.enemyPieces:
            enemyMoves += p.checkPossibleMove(self.board.grid)

        lordPiece.mated = True if tuple(lordPiece.position) in enemyMoves else False

    def calculateNextMoves(self):
        """
        Calcalate the next moves for every piece
        """
        piecesInTurn = [
            piece for piece in self.board.activePices if piece.side == self.turn
        ]  # get all pieces that in the turn to move

        nextMoves = 0

        totalPiecesCheck = 0

        for piece in piecesInTurn:
            moves = piece.checkPossibleMove(self.board.grid)
            validMoves = []

            for move in moves:
                tempBoard = deepcopy(self.board)
                tempPiece = tempBoard.getPiece(piece.getPosition())

                tempBoard.movePiece(tempPiece.position, move)
                lordPiece = tempBoard.getLord(self.turn)

                enemyMoves = []
                for p in tempBoard.activePices:
                    if p.getSide() != self.turn and p.attackingPiece:
                        enemyMoves += p.checkPossibleMove(tempBoard.grid)
                        totalPiecesCheck += 1

                if tuple(lordPiece.position) in enemyMoves or tempBoard.lordTolord():
                    continue

                validMoves.append(move)

            nextMoves += len(validMoves)
            piece.possibleMoves = validMoves
        return nextMoves
    
    def randomMove(self):
        """
        Automatically move a piece
        """
        if not self.isOver:
            # Choose a random enemy piece and move it to its first possible move
            activeBlues = self.board.getActiveBlue()
            piece = activeBlues[random.randint(0, len(activeBlues) - 1)]
            self.selectedPiece = piece
            while not piece.possibleMoves:
                piece = activeBlues[random.randint(0, len(activeBlues) - 1)]
            self.board.movables = self.selectedPiece.possibleMoves
            self.selectedPiece.makeSelected()
            
            move = piece.possibleMoves[random.randint(0, len(piece.possibleMoves) - 1)]
            print(f"Random move {piece} to {move}")
        
            self.move(move)
            self.updateGame()  # Ensure the UI is updated after the move


    
    # def minimaxMove(self):
    #     """
    #     Minimax algorithm to move pieces
    #     """
    #     if not self.isOver:
    #         best_move = None
    #         best_score = float('-inf') if self.turn == RED_TURN else float('inf')

    #         for piece in self.board.getActivePieces(self.turn):
    #             for move in piece.checkPossibleMove(self.board.grid):
    #                 tempBoard = deepcopy(self.board)
    #                 tempPiece = tempBoard.getPiece(piece.getPosition())
    #                 tempBoard.movePiece(tempPiece.position, move)
    #                 score = self.evaluateBoard(tempBoard)
                
                    
    #                 if (self.turn == RED_TURN and score > best_score) or (self.turn == BLUE_TURN and score < best_score):
    #                     best_score = score
    #                     best_move = (piece, move)

    #         if best_move:
    #             piece, move = best_move
    #             self.selectedPiece = piece
    #             self.board.movables = self.selectedPiece.possibleMoves
    #             self.selectedPiece.makeSelected()
    #             print(f"Minimax moving {piece} to {move}")
    #             time.sleep(0.5)
    #             self.move(move)
    #             # Check if the lord has been captured
    #             if not self.board.getLord(RED_TURN) or not self.board.getLord(BLUE_TURN):
    #                 self.gameover = True



    # def minimaxMove(self):
    #     """
    #     Minimax algorithm to move pieces with depth = 3.
    #     """
    #     if not self.isOver:
    #         best_move = None
    #         best_score = float('-inf') if self.turn == RED_TURN else float('inf')

    #         # Start the minimax search with depth = 2
    #         for piece in self.board.getActivePieces(self.turn):
    #             for move in piece.possibleMoves:
    #                 tempBoard = deepcopy(self.board)
    #                 tempPiece = tempBoard.getPiece(piece.getPosition())
    #                 tempBoard.movePiece(tempPiece.position, move)
                    
    #                 # Perform a recursive minimax search with depth 2 remaining
    #                 score = self.minimax(tempBoard, 0, False if self.turn == RED_TURN else True)

    #                 # Update the best move based on the score
    #                 if (self.turn == RED_TURN and score > best_score) or (self.turn == BLUE_TURN and score < best_score):
    #                     best_score = score
    #                     best_move = (piece, move)

    #         if best_move:
    #             piece, move = best_move
    #             self.selectedPiece = piece
    #             self.board.movables = self.selectedPiece.possibleMoves
    #             self.selectedPiece.makeSelected()
    #             print(f"Minimax moving {piece} to {move}")
    #             time.sleep(0.5)
    #             self.move(move)

    #             # Check if the lord has been captured
    #             if not self.board.getLord(RED_TURN) or not self.board.getLord(BLUE_TURN):
    #                 self.gameover = True

    # def minimax(self, board, depth, is_maximizing):
    #     """
    #     Recursive Minimax algorithm to evaluate board states.
    #     """
    #     # Base case: if game is over or depth limit is reached
    #     if depth == 0 or self.isGameOver(board):
    #         return self.evaluateBoard(board)

    #     if is_maximizing:
    #         max_score = float('-inf')
    #         for piece in board.getActivePieces(RED_TURN):
    #             for move in piece.checkPossibleMove(board.grid):
    #                 tempBoard = deepcopy(board)
    #                 tempPiece = tempBoard.getPiece(piece.getPosition())
    #                 tempBoard.movePiece(tempPiece.position, move)

    #                 score = self.minimax(tempBoard, depth - 1, False)
    #                 max_score = max(max_score, score)
    #         return max_score

    #     else:  # Minimizing player (BLUE_TURN)
    #         min_score = float('inf')
    #         for piece in board.getActivePieces(BLUE_TURN):
    #             for move in piece.checkPossibleMove(board.grid):
    #                 tempBoard = deepcopy(board)
    #                 tempPiece = tempBoard.getPiece(piece.getPosition())
    #                 tempBoard.movePiece(tempPiece.position, move)

    #                 score = self.minimax(tempBoard, depth - 1, True)
    #                 min_score = min(min_score, score)
    #         return min_score



    def minimaxMove(self):
        """
        Minimax algorithm to move pieces with depth = 3 and Alpha-Beta Pruning.
        """
        if not self.isOver:
            best_move = None
            best_score = float('-inf') if self.turn == RED_TURN else float('inf')

            active_pieces = self.board.getActivePieces(self.turn)
            random.shuffle(active_pieces)

            # Start the minimax search with depth = 2
            for piece in active_pieces:
    
                moves = piece.possibleMoves
                
                if not moves:
                    continue  # Skip pieces with no possible moves
            
               
                else:
                    for move in moves:
                        tempBoard = deepcopy(self.board)
                        tempPiece = tempBoard.getPiece(piece.getPosition())
                        tempBoard.movePiece(tempPiece.position, move)

                        # Perform a recursive minimax search with alpha-beta pruning
                        score = self.minimax(
                            tempBoard, 1, float('-inf'), float('inf'), 
                            False if self.turn == RED_TURN else True
                        )

                        # Update the best move based on the score
                        if (self.turn == RED_TURN and score > best_score) or \
                        (self.turn == BLUE_TURN and score < best_score):
                            best_score = score
                            best_move = (piece, move)

        if best_move:
            piece, move = best_move
            self.selectedPiece = piece
            self.board.movables = self.selectedPiece.possibleMoves
            self.selectedPiece.makeSelected()
            print(f"Minimax moving {piece} to {move}")
            time.sleep(0.5)
            self.move(move)

            
            # Check if the lord has been captured
            if not self.board.getLord(RED_TURN) or not self.board.getLord(BLUE_TURN):
                self.gameover = True

    # def minimax(self, board, depth, alpha, beta, is_maximizing):
    #     """
    #     Recursive Minimax algorithm with Alpha-Beta Pruning to evaluate board states.
    #     """
    #     # Base case: if game is over or depth limit is reached
    #     if depth == 0 or self.isGameOver(board):
    #         return self.evaluateBoard(board)

    #     if is_maximizing:
    #         max_score = float('-inf')
    #         for piece in board.getActivePieces(RED_TURN):
    #             for move in piece.checkPossibleMove(board.grid):
    #                 tempBoard = deepcopy(board)
    #                 tempPiece = tempBoard.getPiece(piece.getPosition())
    #                 tempBoard.movePiece(tempPiece.position, move)

    #                 score = self.minimax(tempBoard, depth - 1, alpha, beta, False)
    #                 max_score = max(max_score, score)
    #                 alpha = max(alpha, score)

    #                 # Alpha-Beta Pruning: Stop searching if beta <= alpha
    #                 if beta <= alpha:
    #                     break
    #             if beta <= alpha:
    #                 break  # Break outer loop if pruning occurs
    #         return max_score

    #     else:  # Minimizing player (BLUE_TURN)
    #         min_score = float('inf')
    #         for piece in board.getActivePieces(BLUE_TURN):
    #             for move in piece.checkPossibleMove(board.grid):
    #                 tempBoard = deepcopy(board)
    #                 tempPiece = tempBoard.getPiece(piece.getPosition())
    #                 tempBoard.movePiece(tempPiece.position, move)

    #                 score = self.minimax(tempBoard, depth - 1, alpha, beta, True)
    #                 min_score = min(min_score, score)
    #                 beta = min(beta, score)

    #                 # Alpha-Beta Pruning: Stop searching if beta <= alpha
    #                 if beta <= alpha:
    #                     break
    #             if beta <= alpha:
    #                 break  # Break outer loop if pruning occurs
    #         return min_score


    def isGameOver(self, board):
        """
        Check if the game is over (either lord has been captured).
        """
        return not board.getLord(RED_TURN) or not board.getLord(BLUE_TURN)



    def minimax(self, board, depth, alpha, beta, is_maximizing):
        """
        Recursive Minimax algorithm with Alpha-Beta Pruning to evaluate board states.
        """
        
        # Base case: if game is over or depth limit is reached
        if depth == 0 or self.isGameOver(board):
            return self.evaluateBoard(board)

        if is_maximizing:
            max_score = float('-inf')
            for piece in board.getActivePieces(RED_TURN):
        
                moves = piece.checkPossibleMove(board.grid)
                if not moves:  # Skip if no moves available
                    continue
                for move in moves:
                    tempBoard = deepcopy(board)
                    tempPiece = tempBoard.getPiece(piece.getPosition())
                    tempBoard.movePiece(tempPiece.position, move)

                    score = self.minimax(tempBoard, depth - 1, alpha, beta, False)
                    max_score = max(max_score, score)
                    alpha = max(alpha, score)

                    # Alpha-Beta Pruning: Stop searching if beta <= alpha
                    if beta <= alpha:
                        break
                if beta <= alpha:
                    break  # Break outer loop if pruning occurs
            return max_score

        else:  # Minimizing player (BLUE_TURN)
            min_score = float('inf')
            for piece in board.getActivePieces(BLUE_TURN):
            
                moves = piece.checkPossibleMove(board.grid)
                if not moves:  # Skip if no moves available
                    continue
                for move in moves:
                    tempBoard = deepcopy(board)
                    tempPiece = tempBoard.getPiece(piece.getPosition())
                    tempBoard.movePiece(tempPiece.position, move)

                    score = self.minimax(tempBoard, depth - 1, alpha, beta, True)
                    min_score = min(min_score, score)
                    beta = min(beta, score)

                    # Alpha-Beta Pruning: Stop searching if beta <= alpha
                    if beta <= alpha:
                        break
                if beta <= alpha:
                    break  # Break outer loop if pruning occurs
            return min_score


    def cmaesMove(self, max_iterations=20, population_size=5): 
        """
        Use CMA-ES to improve the minimax algorithm.
        """
        if not self.isOver:
            

            # Define the objective function for CMA-ES
            def objective_function(weights):
                score = 0
                active_pieces = self.board.getActivePieces(self.turn)
                random.shuffle(active_pieces)
                for piece in active_pieces:
                    if self.piece_move_count[piece.id] >= 5:
                        continue  # Skip pieces that have been moved 5 times in a row (to avoid infinite loops)
                    # Check if the soldier has reached the end of the board
                    if isinstance(piece, Soldier) and (piece.position or piece.position == self.board.height - 1):
                        continue  # Skip further moves for this piece if it has reached the end of the board
                    for move in piece.possibleMoves:
                        tempBoard = deepcopy(self.board)
                        tempPiece = tempBoard.getPiece(piece.getPosition())
                        tempBoard.movePiece(tempPiece.position, move)
                        score += self.minimax(tempBoard, 1, float('-inf'), float('inf'), False if self.turn == RED_TURN else True)
                return -score  # CMA-ES minimizes the objective function

            # Initialize CMA-ES with random weights
            es = CMAEvolutionStrategy([0] * len(self.board.activePices), 1, {'maxiter': max_iterations, 'popsize': population_size})
            es.optimize(objective_function)

            # Get the best weights from CMA-ES
            best_weights = es.result.xbest

            for i, piece in enumerate(self.board.activePices):
                piece.weight = best_weights[i]
        

            #print("Best Weights: ", best_weights)

            # Use the best weights to perform the minimax move
            best_move = None
            best_score = float('-inf') if self.turn == RED_TURN else float('inf')
            active_pieces = self.board.getActivePieces(self.turn)
            random.shuffle(active_pieces)
            for piece in active_pieces:
                if self.piece_move_count[piece.id] >= 10:
                    continue  # Skip pieces that have been moved 3 times
                for move in piece.possibleMoves:
                    tempBoard = deepcopy(self.board)
                    tempPiece = tempBoard.getPiece(piece.getPosition())
                    tempBoard.movePiece(tempPiece.position, move)
                    score = self.minimax(tempBoard, 1, float('-inf'), float('inf'), False if self.turn == RED_TURN else True)
                    if (self.turn == RED_TURN and score > best_score) or (self.turn == BLUE_TURN and score < best_score):
                        best_score = score
                        best_move = (piece, move)

            if best_move:
                piece, move = best_move
                self.selectedPiece = piece
                self.board.movables = self.selectedPiece.possibleMoves
                self.selectedPiece.makeSelected()
                print(f"CMA-ES moving {piece} to {move}")
                self.move(move)

                # Check if the lord has been captured
                if not self.board.getLord(RED_TURN) or not self.board.getLord(BLUE_TURN):
                    self.gameover = True

    def evaluateBoard(self, board):
        """
        Evaluate the board and return a score
        """
        score = 0
        for piece in board.activePices:
            if piece.side == RED_TURN:
                score += piece.weight * (piece.value)
            else:
                score -= piece.weight * (piece.value)
        return score