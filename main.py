"""
A Tic Tac Toe AI that can be played against in a UI made with Pygame.
"""

__author__ = "Firdavs Nasriddinov"
__versino__ = 1.0

# Import modules
from button import Button
import pygame as pg

# Initialize pygame
pg.init()
pg.font.init()

# Set window title
pg.display.set_caption('Tic-Tac-Toe AI')

# Pygame screen dimensions
WIDTH = 700
HEIGHT = 700

# Variables to represent states of grid boxes
X_VAL = 1
O_VAL = -1
NULL_VAL = 0

# Length and width of grid boxes
GRID_BOX_SIZE = 100

# Offset to display grid from (0, 0) in PyGame screen
OFFSET_X = (WIDTH - 3*GRID_BOX_SIZE)  / 2
OFFSET_Y = (HEIGHT - 3*GRID_BOX_SIZE) / 2

def heuristic(grid: list[list[int]], opp_symbol: int) -> int:
    """Evaluate the value of a grid while moving opp_symbol on the grid.
    
    Heuristic: E(n) = P(n) - O(n)  
        E(n) is the total evaluation
        P(n) is the Player's total possible winning lines
        O(n) is the Opponent's total possible winning lines

    Arguments:
        grid
            contains all grid box values in the tic-tac-toe grid
        opp_symbol
            the opponen'ts symbol to which the heuristic is being calculated
            to win against
    
    Returns:
        score
            heuristic score for the grid when opp_symbol is being tested at
            each grid box
    """

    # Initialize variables to track number of lines for X and O
    x_count = 0
    o_count = 0

    # Check the grid for wins
    # NOTE: not possible with check_winner() because need to count number of 
    # possible winning lines for each symbol

    # Rows
    for r in range(3):
        symbols = [grid[r][0], grid[r][1], grid[r][2]]

        if O_VAL not in symbols and X_VAL not in symbols:
            x_count += 1
            o_count += 1
        if X_VAL in symbols and NULL_VAL in symbols and O_VAL not in symbols:
            x_count += 1
        if O_VAL in symbols and NULL_VAL in symbols and X_VAL not in symbols:
            o_count += 1
        if opp_symbol in symbols and NULL_VAL not in symbols and \
            -opp_symbol not in symbols:
            return -100


    # Cols
    for c in range(3):
        symbols = [grid[0][c], grid[1][c], grid[2][c]]

        if O_VAL not in symbols and X_VAL not in symbols:
            x_count += 1
            o_count += 1
        if X_VAL in symbols and NULL_VAL in symbols and O_VAL not in symbols:
            x_count += 1
        if O_VAL in symbols and NULL_VAL in symbols and X_VAL not in symbols:
            o_count += 1
        if opp_symbol in symbols and NULL_VAL not in symbols and \
            -opp_symbol not in symbols:
            return -100
    

    # Diagonals:
    # tl to br
    symbols = [grid[0][0], grid[1][1], grid[2][2]]

    if O_VAL not in symbols and X_VAL not in symbols:
        x_count += 1
        o_count += 1
    if X_VAL in symbols and NULL_VAL in symbols and O_VAL not in symbols:
        x_count += 1
    if O_VAL in symbols and NULL_VAL in symbols and X_VAL not in symbols:
        o_count += 1
    if opp_symbol in symbols and NULL_VAL not in symbols and \
        -opp_symbol not in symbols:
        return -100

    # bl to tr
    symbols = [grid[0][2], grid[1][1], grid[2][0]]

    if O_VAL not in symbols and X_VAL not in symbols:
        x_count += 1
        o_count += 1
    if X_VAL in symbols and NULL_VAL in symbols and O_VAL not in symbols:
        x_count += 1
    if O_VAL in symbols and NULL_VAL in symbols and X_VAL not in symbols:
        o_count += 1
    if opp_symbol in symbols and NULL_VAL not in symbols and \
        -opp_symbol not in symbols:
        return -100

    # Return the difference of counts based on opp_symbol
    if opp_symbol == X_VAL:
        return o_count - x_count
    elif opp_symbol == O_VAL:
        return x_count - o_count


def minmax(grid: list[list[int]], comp_symbol=X_VAL) -> list[int]:
    """Find the best ply for the computer using the minmax algorithm.
    
    Arguments:
        grid
            contains all grid box values in the tic-tac-toe grid
        comp_symbol : int
            symbol used by computer
    
    Returns:
        i, j
            row and column of best ply for computer
    """

    # Making a new copy of grid to alter
    new_grid = grid.copy()
    
    """Ply: first half of a move in a turn-based, two player game"""

    # List to append computer plies
    comp_plies = []

    # List to store all lists of evaluations generated by computer ply
    all_evals = []

    # Loop through each box in grid
    for i in range(3):
        for j in range(3):
            # If grid box is empty
            if grid[i][j] == NULL_VAL:
                evaluations = []

                # Make a computer ply
                new_grid[i][j] = comp_symbol
                comp_plies.append([i, j])

                # If computer won, return i, j as the best ply for computer
                if check_winner(new_grid) == comp_symbol:
                    return i, j

                # Loop through each box in grid again to evaluate all 
                # evaluations for computer ply
                for r in range(3):
                    for c in range(3):
                        # if grid box is empty
                        if new_grid[r][c] == NULL_VAL:
                            # Make a human ply
                            new_grid[r][c] = -comp_symbol

                            # Evaluate heuristic of this ply
                            evaluation = heuristic(new_grid, -comp_symbol)

                            # Append evalutions
                            evaluations.append(evaluation)

                            # Reset human ply
                            new_grid[r][c] = NULL_VAL
                        
                        # If there are no possible plies left, i, j is the only 
                        # possible ply
                        else:
                            if r == 2 and c == 2 and len(evaluations) == 0:
                                return i, j

                all_evals.append(evaluations)

                # Reset computer ply
                new_grid[i][j] = NULL_VAL

    # List to store minimum evaluation of all evaluationsi in allEvals
    mins = []
    
    # Appending to mins
    for evaluations in all_evals:
        mins.append(min(evaluations))

    # Find the max of min
    maxmin = max(mins)
    
    # Best ply for computer is the compPly with index of where maxmin is 
    # located in min
    best_ply = comp_plies[mins.index(maxmin)]
    
    return best_ply[0], best_ply[1]


def check_winner(grid: list[list[int]]) -> list[int, list[tuple[int]]]:
    """Check for winners in grid.
    
    If there is a winner, returns value of symbol. If there is no winner, 
    returns None. If there are no winners and no available moves, 
    return nullVal.

    Arguments:
        grid
            contains all grid box values in the tic-tac-toe grid
    
    Returns:
        winner_symbol
            the winning symbol
    """

    # Rows
    for r in range(3):
        if grid[r][0] == grid[r][1] == grid[r][2]:
            if grid[r][0] != NULL_VAL:
                return grid[r][0], [(r, 0), (r, 1), (r, 2)]

    # Cols
    for c in range(3):
        if grid[0][c] == grid[1][c] == grid[2][c]:
            if grid[0][c] != NULL_VAL:
                return grid[0][c], [(0, c), (1, c), (2, c)]
    

    # Diagonals
    # tl to br
    if grid[0][0] == grid[1][1] == grid[2][2]:
        if grid[0][0] != NULL_VAL:
            return grid[0][0], [(0, 0), (1, 1), (2, 2)]

    # bl to tr
    if grid[0][2] == grid[1][1] == grid[2][0]:
        if grid[0][2] != NULL_VAL:
            return grid[0][2], [(0, 2), (1, 1), (2, 0)]
    
    # Check for ties
    for r in range(3):
        for c in range(3):
            if grid[r][c] == NULL_VAL:
                return None, None

    return NULL_VAL, None


def draw_grid(screen: pg.surface, grid: list[list[int]], font: pg.font):
    """Draw grid on PyGame screen
    
    Arguments:
        screen
            pygame screen to display contents
        grid
            contains all grid box values in the tic-tac-toe grid
        font
            pygame font to render symbols on screen
    """

    # Dist to store String of symbol and corresponding text color
    symbols = {1: ['X', (0, 0, 255)], -1: ['O', (255, 0, 0)]}

    # Draw lines to represetn Tic Tac Toe grid
    pg.draw.line(screen, (0, 0, 0), (  GRID_BOX_SIZE + OFFSET_X, OFFSET_Y), 
                  (  GRID_BOX_SIZE + OFFSET_X, 3*GRID_BOX_SIZE + OFFSET_Y), 5)
    pg.draw.line(screen, (0, 0, 0), (2*GRID_BOX_SIZE + OFFSET_X, OFFSET_Y), 
                  (2*GRID_BOX_SIZE + OFFSET_X, 3*GRID_BOX_SIZE + OFFSET_Y), 5)
    pg.draw.line(screen, (0, 0, 0), (OFFSET_X,   GRID_BOX_SIZE + OFFSET_Y), 
                  (3*GRID_BOX_SIZE + OFFSET_X,   GRID_BOX_SIZE + OFFSET_Y), 5)
    pg.draw.line(screen, (0, 0, 0), (OFFSET_X, 2*GRID_BOX_SIZE + OFFSET_Y), 
                  (3*GRID_BOX_SIZE + OFFSET_X, 2*GRID_BOX_SIZE + OFFSET_Y), 5)

    # Loop through each grid box
    for r in range(3):
        for c in range(3):
            val = grid[r][c]

            # If grid box is not empty, display its value
            if val != NULL_VAL:
                valText = font.render(symbols[val][0], True, symbols[val][1])

                x = c*GRID_BOX_SIZE + 50 - valText.get_size()[0]/2 + OFFSET_X
                y = r*GRID_BOX_SIZE + 50 - valText.get_size()[1]/2 + OFFSET_Y

                screen.blit(valText, (x, y))


def make_ply(grid: list[list[int]], mouse_pressed: bool) -> list[int]:
    """Make ply for human.
    
    Arguments:
        grid
            contains all grid box values in the tic-tac-toe grid
        mouse_pressed
            whether or not left click is pressed
        
    Returns:
        r, c
            row and column of ply
    """

    # (x, y) position of mouse on screen
    mouse_pos = pg.mouse.get_pos()

    # Determine the row and column of mouse_pos on grid
    r = int((mouse_pos[1] - OFFSET_X)/GRID_BOX_SIZE)
    c = int((mouse_pos[0] - OFFSET_Y)/GRID_BOX_SIZE)

    # If mouse clicked a valid, empty grid box, return r, c of ply
    if mouse_pressed and r in [0, 1, 2] and c in [0, 1, 2]:
        if grid[r][c] == NULL_VAL:
            return r, c

    # Else return None
    return None, None


def print_grid(grid):
    """Helper function to print grid as a serious of Strings in terminal.
    
    Arguments:
        grid
            contains all grid box values in the tic-tac-toe grid
    """

    for i in range(3):
        for j in range(3):
            print(grid[i][j], end='\t')
        print()


def reset() -> list[list[list[int]], int, None]:
    """Reset the program to be able to play again.
    
    Returns:
        grid
            contains all grid box values in the tic-tac-toe grid
        current_player
            current player
        winner
            the current winner which is now None
    """

    # Blank 2D list to store grid
    grid = [[], [], []]

    # Initialize grid with null_vals
    for r in range(3):
        for c in range(3):
            grid[r].append(NULL_VAL)
    
    # Which player computer gets to play as
    current_player = X_VAL

    # Reset winner to None
    winner = None

    return grid, current_player, winner 


def draw_winner_line(screen: pg.surface, win_coords: list[tuple[int]]):
    """Draw line for the winner.
    
    Arguments:
        screen
            pygame screen to display contents
        win_coords
            coords of the winning line
    """

    # The first coord to draw line from
    box_1 = win_coords[0]

    # The second coord to draw line to
    box_2 = win_coords[2]

    # Convert from row and column to screen pixel coordinates
    pos_1 = (box_1[1]*GRID_BOX_SIZE + OFFSET_X + box_1[1]*GRID_BOX_SIZE/2,
             box_1[0]*GRID_BOX_SIZE + OFFSET_Y + box_1[0]*GRID_BOX_SIZE/2)
    pos_2 = (box_2[1]*GRID_BOX_SIZE + OFFSET_X + box_2[1]*GRID_BOX_SIZE/2,
             box_2[0]*GRID_BOX_SIZE + OFFSET_Y + box_2[0]*GRID_BOX_SIZE/2)

    # Draw line
    pg.draw.line(screen, 'black', pos_1, pos_2, 5)


def main():
    """Main function to run program."""

    # Pygame screen to display contents
    screen = pg.display.set_mode([WIDTH, HEIGHT])

    # Size 100 font
    font_100 = pg.font.SysFont('Koulen', 100)

    # Size 40 font
    font_40 = pg.font.SysFont('Koulen', 40)

    play_again_button = Button(screen,
                               pos=(350, 550),
                               dims=(170, 40),
                               font=font_40,
                               text='Play Again',
                               bg_color=(128, 128, 128),
                               text_color=(0, 0, 0))

    # Blank 2D list to store grid
    grid = [[], [], []]

    # Initialize grid with null_vals
    for r in range(3):
        for c in range(3):
            grid[r].append(NULL_VAL)

    # Which symbol computer gets to play as
    comp_symbol = X_VAL

    # Which symbol player gets to play as
    player_symbol = O_VAL

    # X always goes first
    current_player = X_VAL

    # Variable to represent winner
    # If not none, then there is a winner or a tie
    winner = None

    running = True
    while running:
        # Whether or not left click is pressed
        mouse_pressed = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pressed = True

        # Make background white
        screen.fill((255, 255, 255))

        draw_grid(screen, grid, font_100)
        
        if winner is None:
            if current_player == comp_symbol:
                # Get coordinates of best ply for computer
                r, c = minmax(grid, comp_symbol)
                # Make ply
                grid[r][c] = comp_symbol

                # Swap current player
                current_player *= -1
            elif current_player == player_symbol:
                # Get ply coordinates at clicked grid box
                r, c = make_ply(grid, mouse_pressed)

                # Make ply if valid coords
                if r is not None and c is not None:
                    grid[r][c] = player_symbol

                    # Swap current_player
                    current_player *= -1
        else:
            # If there is a winner then draw line to display winner
            if win_coords:
                draw_winner_line(screen, win_coords)
            
            # Draw "play again" button
            play_again_button.draw()

        # Check for a winner
        winner, win_coords = check_winner(grid)

        # Text to display on screen regarding the winner
        text = ''

        if winner == O_VAL:
            text = 'O wins!'
        elif winner == X_VAL:
            text = 'X wins!'
        elif winner == NULL_VAL:
            text = 'It is a tie.'
            
        # Reset game if play again button is pressed
        if play_again_button.is_pressed():
            grid, current_player, winner = reset()

        # Display winner text
        textRender = font_100.render(text, True, (0, 0, 0))

        x = WIDTH/2 - textRender.get_size()[0]/2
        y = 200 - textRender.get_size()[0]/2

        screen.blit(textRender, (x, y))

        # Update screen
        pg.display.flip()

    pg.quit()


if __name__ == '__main__':
    main()