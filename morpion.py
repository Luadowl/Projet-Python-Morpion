import random
import tools

# Fonction pour afficher le plateau
def displayBoard(board):
    for row in board:
        print(" ".join(str(cell) if cell is not None else "_" for cell in row))
    print()

# Fonction pour le tour du joueur
def pPlay(board, pSymbol, size):
    while True:
        displayBoard(board)
        print("Tour du joueur.")
        row = tools.AskIntInRange(f"Choisissez la ligne où vous voulez jouer (0 = première ligne et {size-1} = dernière ligne)", 0, len(board) - 1)
        column = tools.AskIntInRange(f"Choisissez la colonne où vous voulez jouer (0 = première colonne et {size-1} = dernière colonne)", 0, len(board) - 1)

        if board[row][column] is None:
            board[row][column] = pSymbol
            return True
        else:
            print("Cette case est prise. Réessayez")

def cPlay(board, cSymbol, pSymbol):

    def findMove(symbol, check_symbol):
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] is None:
                    board[i][j] = symbol
                    if checkWinner(board, pSymbol, cSymbol) == check_symbol:
                        return (i, j)
                    board[i][j] = None
        return None

    def playRandom(empty_cells):
        random_row, random_col = random.choice(empty_cells)
        board[random_row][random_col] = cSymbol

    def countSymbolsInLine(line, symbol):
        return line.count(symbol)

    def countEmptyInLine(line):
        return line.count(None)

    def canWinOrBlock(symbol, check_symbol):
        for i in range(len(board)):
            row = board[i]
            col = [board[j][i] for j in range(len(board))]
            if countSymbolsInLine(row, symbol) == len(board) - 1 and countEmptyInLine(row) == 1:
                return True if check_symbol == symbol else False
            if countSymbolsInLine(col, symbol) == len(board) - 1 and countEmptyInLine(col) == 1:
                return True if check_symbol == symbol else False
        return False

    #joue au centre
    if board[len(board)//2][len(board)//2] is None:
        board[len(board)//2][len(board)//2] = cSymbol
        return

    # Vérifier si l'ordinateur peut gagner
    if canWinOrBlock(cSymbol, cSymbol):
        winning_move = findMove(cSymbol, cSymbol)
        if winning_move:
            row, col = winning_move
            board[row][col] = cSymbol
            return

    # Vérifier si l'adversaire peut gagner et bloquer
    if canWinOrBlock(pSymbol, cSymbol):
        blocking_move = findMove(pSymbol, cSymbol)
        if blocking_move:
            row, col = blocking_move 
            board[row][col] = cSymbol
            return

    # Si aucun mouvement gagnant ou bloquant, jouer aléatoirement
    empty_cells = [(i, j) for i in range(len(board)) for j in range(len(board)) if board[i][j] is None]
    if empty_cells:
        playRandom(empty_cells)


# Fonction pour vérifier si c'est un match nul
def checkDraw(board):
    emptyCells = sum(row.count(None) for row in board)
    return emptyCells == 0

# Fonction pour vérifier s'il y a un gagnant

def checkWinner(board, pSymbol, cSymbol):
    for symbol in [pSymbol, cSymbol]:
        for i in range(len(board)):
            if all(board[i][j] == symbol for j in range(len(board))) or \
               all(board[j][i] == symbol for j in range(len(board))) or \
               (all(board[j][j] == symbol for j in range(len(board))) or \
               all(board[j][len(board) - j - 1] == symbol for j in range(len(board)))):

                return symbol

    return None

def ticTacToe():
    while True:
        
        size = tools.AskIntInRange("Choisissez la taille du plateau (minimum 3, maximum 100) :", 3 , 100)
        pSymbol = tools.AskInputs("Choisissez un symbole (X ou O) :", ["x", "o"])
        cSymbol = "o" if pSymbol == "x" else "x"

        # Crée un plateau vide avec la taille spécifiée
        board = [[None for _ in range(size)] for _ in range(size)]

        print("Tour de l'ordinateur :")
        cPlay(board, cSymbol, pSymbol)
    
        while True:
            if pPlay(board, pSymbol, size):
                winner = checkWinner(board, pSymbol, cSymbol)
                if winner:
                    displayBoard(board)
                    print(f"Le joueur {winner} a gagné !")
                    break
                elif checkDraw(board):
                    displayBoard(board)
                    print("Match nul !")
                    break

            cPlay(board, cSymbol, pSymbol)
            winner = checkWinner(board, pSymbol, cSymbol)
            if winner:
                displayBoard(board)
                print(f"L'ordinateur {winner} a gagné !")
                break
            elif checkDraw(board):
                displayBoard(board)
                print("Match nul !")
                break

        if not tools.Retry():
            return False

ticTacToe()
