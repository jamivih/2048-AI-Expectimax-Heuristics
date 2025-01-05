from tkinter import Frame, Label, CENTER
import statistics as st
import random
import logic
import constants as c
import sys
# import AI_heuristics as AI
# import AI_minimax as AI
import AI_both as AI

points_list = []

def gen():
    return random.randint(0, c.GRID_LEN - 1)

def points_calculation(points_list):
    avg = st.mean(points_list)
    print(f'points from 10 rounds: {points_list}')
    print(f'avg: {avg:.2f}')

class GameGrid(Frame):
    def __init__(self):
        for _ in range(10): # Loops the game x amount of times, stores the points and counts the avg
            Frame.__init__(self) # Initializes the Tkinter frame (the main window for the game)
            self.game_over = False
            self.start = True
            self.points = 0

            self.grid() # Places the frame into the window using a grid layout
            self.master.title('2048') # Sets the window title to "2048"
            #self.master.bind("<Key>", self.key_down) # Binds the keyboard input to the key_down function, which will handle player movement
            
            self.done = False

            # A dictionary mapping the four movement keys (up, down, left, right) to the respective functions in logic.py (e.g., logic.up, logic.down)
            self.commands = {
                c.KEY_UP: logic.up,
                c.KEY_DOWN: logic.down,
                c.KEY_LEFT: logic.left,
                c.KEY_RIGHT: logic.right,
                c.KEY_UP_ALT1: logic.up,
                c.KEY_DOWN_ALT1: logic.down,
                c.KEY_LEFT_ALT1: logic.left,
                c.KEY_RIGHT_ALT1: logic.right,
                c.KEY_UP_ALT2: logic.up,
                c.KEY_DOWN_ALT2: logic.down,
                c.KEY_LEFT_ALT2: logic.left,
                c.KEY_RIGHT_ALT2: logic.right,
            }

            self.grid_cells = [] # An empty list to store the GUI cells
            self.init_grid() # Initializes the grid in the GUI
            self.matrix = logic.new_game(c.GRID_LEN) # Initializes the game's board matrix
            self.history_matrixs = []
            self.update_grid_cells() # Updates the grid cells visually according to the current state of the game

            #self.update_view()
            self.game_loop()
            self.mainloop() # Starts the Tkinter main loop, making the window interactive

            # If game is over, points append to the points_list variable
            if self.game_over is True:
                points_list.append(self.points)

        points_calculation(points_list)


    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,width=c.SIZE, height=c.SIZE) # Creates a Frame that serves as the background for the game grid
        background.grid() # Places the Frame in the window

        # Iterates over the grid (which is 4x4 by default), creating a Frame for each cell. 
        # Each cell is represented as a smaller Frame with padding (padx, pady) between them
        for i in range(c.GRID_LEN): 
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(
                    background,
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    width=c.SIZE / c.GRID_LEN,
                    height=c.SIZE / c.GRID_LEN
                )
                cell.grid(
                    row=i,
                    column=j,
                    padx=c.GRID_PADDING,
                    pady=c.GRID_PADDING
                )
                #  Each cell contains a Label, which displays the number (tile) in that position. 
                # The Label's background color and text will be updated based on the game state (empty, 2, 4, 8, etc.)
                t = Label(
                    master=cell,
                    text="",
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    justify=CENTER,
                    font=c.FONT,
                    width=5,
                    height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row) # Stores the grid of Label widgets so the program can update their contents dynamically

    # This function updates the visual representation of the grid.
    def update_grid_cells(self): # Iterates over the matrix (the game state) and updates each corresponding Label in the GUI
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="",bg=c.BACKGROUND_COLOR_CELL_EMPTY) # Changes the text, background color, and foreground color of each Label based on the tile value (constants.py)
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number]
                    )
        self.update_idletasks() # Ensures the UI is updated right away after each move

    def key_down(self, event):
        key = event.keysym # Get the name of the key pressed
        #print(event)
        if key == c.KEY_QUIT: exit() # Exits the game if the quit key is pressed
        # KEY_BACK adds a backtracking feature, where the user can undo a move if there's more than one previous move stored in history_matrixs
        if key == c.KEY_BACK and len(self.history_matrixs) > 1: 
            self.matrix = self.history_matrixs.pop()
            self.update_grid_cells()
            print('back on step total step:', len(self.history_matrixs))        
        elif key in self.commands:
            # Moves the board as per the key command. 
            # If a valid move is made (done == True), a new tile is added using logic.add_two(), and the new state is recorded in history_matrixs
            self.matrix, done = self.commands[key](self.matrix)
            if done:
                self.matrix = logic.add_two(self.matrix)
                # record last move
                self.history_matrixs.append(self.matrix)
                self.update_grid_cells()
                # Check the game state once to avoid redundant calls
                game_state = logic.game_state(self.matrix)

                if game_state == 'win':
                    self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                if game_state == 'loses':
                    self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    
                    return

    def generate_next(self): # Gnerates a new '2' tile at a random empty position after each valid move
        index = (gen(), gen())
        while self.matrix[index[0]][index[1]] != 0: # Ensures that the new tile is placed in an empty cell
            index = (gen(), gen())
        self.matrix[index[0]][index[1]] = 2

    def update_view(self): # Updates the view with a specific focus on handling the AI and game state updates
        weights = {
        'corner_weight': .5,
        'monotonicity_weight': 1.2,
        'merging_weight': 1.2,
        'empty_tiles_weight': 0.5,
        'clustering_weight': 0,
        'smoothness_weights': 0
    } 
        # AI takes over if the game is not over
        if not self.game_over and self.start:
            self.start = False
            self.update_grid_cells()
            self.update()
        # AI makes its move using the AI_play(self.matrix) function, which returns the best move (key) according to the AI's strategy
        
        elif not self.game_over:
            key = AI.AI_play(self.matrix, weights)
            self.commands[key](self.matrix) # commands[key] function executes the AI's move

            self.matrix, done, points = self.commands[key](self.matrix)
            self.points += points # The points for the current move are calculated and added to 
            if done:
                self.done = True # A new tile is added 
                self.matrix = logic.add_two(self.matrix)
                # record last move
                self.history_matrixs.append(self.matrix)
                # The view is updated, and if the player wins or loses, the game-over message is displayed with the points
                self.update_grid_cells()
                self.update()
                if logic.game_state(self.matrix) == 'win':
                    self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[2][1].configure(text="Points:", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[2][2].configure(text=self.points, bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.game_over = True
                    print(self.points)  
                    self.master.destroy() # Closes the window

                if logic.game_state(self.matrix) == 'lose':
                    self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[2][1].configure(text="Points:", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[2][2].configure(text=self.points, bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.game_over = True                        
                    print(self.points)
                    self.master.destroy() # Closes the window                                 
            pass
    
    # The main loop of the game
    def game_loop(self):
        while not self.game_over:
            #print("Your point so far : " + str(self.points))
            self.after(1, self.update_view) # A Tkinter method that schedules the update_view() function to be called after 1 millisecond. This essentially runs the main game loop, with regular updates
            self.update_grid_cells()
            self.update() # Updates the graphical user interface
            #self.update_idletasks()

game_grid = GameGrid()