import pygame

BLACK    = (   0,   0,   0)
GREEN    = (   0, 150,   0)
WHITE    = ( 200, 200, 200)
WIDTH = 10
HEIGHT = 10
MARGIN = 2

class Cell:
    def __init__(self):
        self.alive = False
        self.near_sum = 0

    def update_near_sum(self, near_sum):
        self.near_sum = near_sum

    def update_state(self, click=False):
        if click:
            self.alive = not self.alive
        elif self.near_sum == 3:
            self.alive = True
        elif self.near_sum < 2 or self.near_sum > 3:
            self.alive = False


class Game:
    def __init__(self, rows=50, cols=50):
        self.rows = rows
        self.cols = cols
        self.grid = [[Cell() for col in range(cols)] for row in range(rows)]
        self.pending = []

    def update_neighborhood(self):
        for i in range(self.rows):
            for j in range(self.cols):
            # I'm sure there is a better way to do this
            # but I don't want to give it that much thought
                neighborhood = []
                if 0 <= i+1 < self.rows:
                    neighborhood.append(self.grid[i+1][j].alive)
                if 0 <= i-1 < self.rows:
                    neighborhood.append(self.grid[i-1][j].alive)
                if 0 <= j+1 < self.cols:
                    neighborhood.append(self.grid[i][j+1].alive)
                if 0 <= j-1 < self.cols:
                    neighborhood.append(self.grid[i][j-1].alive)
                
                if 0 <= i+1 < self.rows:
                    if 0 <= j+1 < self.cols:
                        neighborhood.append(self.grid[i+1][j+1].alive)
                    if 0 <= j-1 < self.cols:
                        neighborhood.append(self.grid[i+1][j-1].alive)
                if 0 <= i-1 < self.rows:
                    if 0 <= j+1 < self.cols:
                        neighborhood.append(self.grid[i-1][j+1].alive)
                    if 0 <= j-1 < self.cols:
                        neighborhood.append(self.grid[i-1][j-1].alive)

                near_sum = sum(neighborhood)

                if self.grid[i][j].near_sum != near_sum:
                    print("Row: {}; Col: {}; Sum: {}".format(i, j, near_sum))
                    self.pending.append((i, j))
                    self.grid[i][j].update_near_sum(near_sum)

    def update_game_state(self):
        for i, j in self.pending:
            self.grid[i][j].update_state()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Game of Life")
    
    rows = 50
    cols = 50
    game = Game(rows, cols)
    size = (rows * (HEIGHT + MARGIN) + MARGIN, cols * (WIDTH + MARGIN) + MARGIN)


    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    done = False
    play = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If user clicked close
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                # Debug prints
                # print("Click ", pos, "Grid coordinates: ", row, column)
                game.grid[row][column].update_state(True)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # print("Pressed spacebar")
                    game.update_neighborhood()
                    game.update_game_state()
                if event.key == pygame.K_RETURN:
                    play = not play
        
        if play:
            game.update_neighborhood()
            game.update_game_state()

        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        
        screen.fill(BLACK)
        
        for row in range(game.rows):
            for column in range(game.cols):
                if game.grid[row][column].alive:
                    color = GREEN
                else:
                    color = WHITE
                pygame.draw.rect(screen, color,
                                 [MARGIN + (MARGIN + WIDTH) * column, 
                                  MARGIN + (MARGIN + HEIGHT) * row,
                                  WIDTH, HEIGHT]
                                )
                
        
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
    
        # --- Limit to 60 frames per second
        clock.tick(20)
    
    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()