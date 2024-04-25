import game_rules, random
###########################################################################
# Explanation of the types:
# The board is represented by a row-major 2D list of characters, 0 indexed
# A point is a tuple of (int, int) representing (row, column)
# A move is a tuple of (point, point) representing (origin, destination)
# A jump is a move of length 2
###########################################################################

# I will treat these like constants even though they aren't
# Also, these values obviously are not real infinity, but close enough for this purpose
NEG_INF = -1000000000
POS_INF = 1000000000

class Player(object):
    """ This is the player interface that is consumed by the GameManager. """
    def __init__(self, symbol): self.symbol = symbol # 'x' or 'o'

    def __str__(self): return str(type(self))

    def selectInitialX(self, board): return (0, 0)
    def selectInitialO(self, board): pass

    def getMove(self, board): pass

    def h1(self, board):
        return -len(game_rules.getLegalMoves(board, 'o' if self.symbol == 'x' else 'x'))


# This class has been replaced with the code for a deterministic player.
class MinimaxPlayer(Player):
    def __init__(self, symbol, depth): super(MinimaxPlayer, self).__init__(symbol)

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    # Edit this one here. :)
    def getMove(self, board):
        return findMax(board, self.depth, self.symbol)[1] # do we have a self.depth??

    def findMax(self, board): # do we need depth and symbol as arguments?
        legalMoves = gameRules.getLegalMoves(board, symbol)
        if len(legalMoves) == 0 or depth == 0:
            return (self.h1(board), None)

        bestMove = (NEG_INF, None)

        for i in range(len(legalMoves)):
            nextBoard = game_rules.makeMove(board, legalMoves[i])
            if symbol == 'o':
                value = self.findMin(nextBoard, depth - 1, 'x')[0]
            else:
                value = self.findMin(nextBoard, depth - 1, 'o')[0]

            if bestMove[0] < value:
                bestMove = (value, legalMoves[i])

            return bestMove

    def findMin(self, board):  # same issue??
        legalMoves = game_rules.getLegalMoves(board, symbol)
        if len(legalMoves) == 0 or depth == 0:
            return (self.h1(board), None)

        bestMove = (POS_INF, None)

        for i in range(len(legalMoves)):
            nextBoard = game_rules.makeMove(board, legalMoves[i])
            if symbol == 'o':
                value = self.findMax(nextBoard, depth - 1, 'x')[0]
            if symbol === 'x':
                value = self.findMax(nextBoard, depth - 1, 'x')[0]
            
            if bestMove[0] < value:
                bestMove = (value, legalMoves[i])

        return bestMove


    ''' def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return legalMoves[0]
        else: return None '''



# This class has been replaced with the code for a deterministic player.
class AlphaBetaPlayer(Player):
    def __init__(self, symbol, depth): super(AlphaBetaPlayer, self).__init__(symbol)

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    # Edit this one here. :)
    def getMove(self, board):
        searching = self.findMax(board, NEG_INF, POS_INF)
        return searching[1]

    def findMax(self, board, mini, maxi):
        legalMoves = game_rules.getLegalMoves(board)
        bestMove = (NEG_INF, None)
        if len(legalMoves) == 0 or depth == 0:
            return (self.h1(board), None)
        for i in range(len(legalMoves)):
            nextBoard = game_rules.makeMove(board, legalMoves[i])
            if symbol == 'o':
                value = self.findMin(nextBoard, mini, maxi, depth - 1, 'x')[0]
            else:
                value = self.findMin(nextBoard, mini, maxi, depth - 1, 'o')[0]

            if bestMove[0] < value:
                bestMove = (value, legalMoves[i])
            
            if bestMove[0] >= maxi:
                return bestMove

            if mini < bestMove[0]:
                mini = bestMove[0]

        return bestMove

    def findMin(self, board, mini, maxi):
        legalMoves = game_rules.getLegalMoves(board)
        best = (POS_IN, None)
        if len(legalMoves) == 0 or depth == 0:
            return (self.h1(board), None)
        for i in range(len(legalMoves)):
            nextBoard = game_rules.makeMove(board, legalMoves[i])
            if symbol == 'o':
                value = self.findMax(nextBoard, mini, maxi, depth - 1, 'x')[0]
            else:
                value = self.findMax(nextBoard, mini, maxi, depth - 1, 'o')[0]

            if bestMove[0] > value:
                bestMove = (value, legalMoves[i])

            if bestMove[0] > maxi:
                maxi = bestMove[0]

            if bestMove[0] <= mini:
                return bestMove

        return bestMove


    """ def getMove(self, board):a
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return legalMoves[0]
        else: return None """



class RandomPlayer(Player):
    def __init__(self, symbol):
        super(RandomPlayer, self).__init__(symbol)

    def selectInitialX(self, board):
        validMoves = game_rules.getFirstMovesForX(board)
        return random.choice(list(validMoves))

    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return random.choice(list(validMoves))

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return random.choice(legalMoves)
        else: return None


class DeterministicPlayer(Player):
    def __init__(self, symbol): super(DeterministicPlayer, self).__init__(symbol)

    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return legalMoves[0]
        else: return None


class HumanPlayer(Player):
    def __init__(self, symbol): super(HumanPlayer, self).__init__(symbol)
    def selectInitialX(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def selectInitialO(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def getMove(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')


def makePlayer(playerType, symbol, depth=1):
    player = playerType[0].lower()
    if player   == 'h': return HumanPlayer(symbol)
    elif player == 'r': return RandomPlayer(symbol)
    elif player == 'm': return MinimaxPlayer(symbol, depth)
    elif player == 'a': return AlphaBetaPlayer(symbol, depth)
    elif player == 'd': return DeterministicPlayer(symbol)
    else: raise NotImplementedException('Unrecognized player type {}'.format(playerType))

def callMoveFunction(player, board):
    if game_rules.isInitialMove(board): return player.selectInitialX(board) if player.symbol == 'x' else player.selectInitialO(board)
    else: return player.getMove(board)