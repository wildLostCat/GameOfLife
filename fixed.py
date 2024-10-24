import sys
import pygame
import random

GREY = (144, 144, 144)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

WIDTH, HEIGHT = 800, 800
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()


def gen(num):
    return set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num)])


def draw_grid(positions):
    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, BLACK, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))
    for col in range(GRID_WIDTH):
        pygame.draw.line(screen, BLACK, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))
    for position in positions:
        pygame.draw.rect(screen, YELLOW, (position[0] * TILE_SIZE, position[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))


def adjust_grid(positions):
    new_positions = set()
    all_neighbors = set()

    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        neighbors = list(filter(lambda x:x in positions, neighbors))

        if len(neighbors) in [2, 3]:
            new_positions.add(position)

    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x:x in positions, neighbors))

        if len(neighbors) == 3:
            new_positions.add(position)

    return new_positions


def get_neighbors(pos):
    x, y = pos
    neighbors = []

    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx > GRID_WIDTH:
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy > GRID_HEIGHT:
                continue
            if dx == 0 and dy == 0:
                continue

            neighbors.append((x + dx, y + dy))

    return neighbors


def main():
    running = True
    playing = False
    positions = set()

    count = 0
    generation = 0
    update_freq = 90

    while running:
        clock.tick(FPS)
        alive_cells_count = len(positions)

        if playing:
            count += 1

        if count >= update_freq:
            count = 0
            positions = adjust_grid(positions)
            generation += 1
            alive_cells_count = len(positions)

        pygame.display.set_caption(f"state:Running, generation:{generation}, alive cells:{alive_cells_count}" if playing else f"state:Paused, generation:{generation}, alive cells:{alive_cells_count}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                pos = (x // TILE_SIZE, y // TILE_SIZE)
                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing
                    count = 0
                if event.key == pygame.K_c:
                    positions = set()
                    count = 0
                if event.key == pygame.K_g:
                    positions = gen(random.randrange(4, 7) * GRID_WIDTH)

        screen.fill(GREY)
        draw_grid(positions)
        pygame.display.update()


if __name__ == '__main__':
    main()