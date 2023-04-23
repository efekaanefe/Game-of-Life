import pygame

pygame.init()

ROW = 42
COL = 42
SQ_SIZE = 20
WIDTH = COL * SQ_SIZE
HEIGHT = ROW * SQ_SIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")

FPS = 60

BLACK = (30, 30, 30)
WHITE = (180, 180, 180)


def main():
    grid = Grid(ROW, COL, SQ_SIZE, WIN)
    clock = pygame.time.Clock()
    running = True
    game_start = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_SPACE:
                    game_start = not game_start

                if event.key == pygame.K_r:
                    grid.grid = grid.get_default_grid()
                    game_start = False

            if event.type == pygame.MOUSEMOTION:
                if not game_start:
                    mx, my = pygame.mouse.get_pos()
                    i = my // SQ_SIZE
                    j = mx // SQ_SIZE
                    if event.buttons[0]:  # left mouse button down
                        grid.grid[i][j] = 1
        if game_start:
            grid.update()
        grid.draw()

        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    quit()


class Grid:
    def __init__(self, row, col, sq_size, win):
        self.row = row
        self.col = col
        self.sq_size = sq_size
        self.win = win
        self.grid = self.get_default_grid()

    def get_default_grid(self):
        return [[0 for _ in range(self.col)] for _ in range(self.row)]

    def update(self):
        updated_grid = self.get_default_grid()

        for i in range(self.row):
            for j in range(self.col):
                value = self.grid[i][j]
                live_neighbours = self.count_live_neighbours(i, j)
                if value == 1 and live_neighbours in range(2, 4):
                    updated_grid[i][j] = 1
                elif value == 0 and live_neighbours == 3:
                    updated_grid[i][j] = 1
                else:
                    updated_grid[i][j] = 0
        self.grid = updated_grid

    def count_live_neighbours(
        self, i, j
    ):  # returns # of live neighbours (dead = 8 - live)
        live = 0
        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
        for di, dj in directions:
            i_neigh = (i + di + self.row) % self.row
            j_neigh = (j + dj + self.col) % self.col
            live += self.grid[i_neigh][j_neigh]  # neighbour_value
        return live

    def draw(self):
        for i in range(self.row):
            for j in range(self.col):
                value = self.grid[i][j]
                color = BLACK if value == 1 else WHITE
                rect = pygame.Rect(
                    j * self.sq_size, i * self.sq_size, self.sq_size, self.sq_size
                )
                pygame.draw.rect(WIN, color, rect)
        for i in range(ROW):
            pygame.draw.line(
                WIN,
                (0, 0, 0),
                (i * self.sq_size - 1, 0),
                (i * self.sq_size - 1, HEIGHT),
                2,
            )
            pygame.draw.line(
                WIN,
                (0, 0, 0),
                (0, i * self.sq_size - 1),
                (WIDTH, i * self.sq_size - 1),
                1,
            )


if __name__ == "__main__":
    main()
