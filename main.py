import pygame
from pygame.locals import *
import sys
from board import Board

pygame.init()

screen = pygame.display.set_mode((800, 800), RESIZABLE)
font = pygame.font.Font('freesansbold.ttf', 32)


def solving():
    print('solving')
    board.current_time = 0
    board.timer.start()

    solved = False
    if control_mode == 'kb':
        while not solved:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        board.move_tile('u')
                    elif event.key == pygame.K_DOWN:
                        board.move_tile('d')
                    elif event.key == pygame.K_LEFT:
                        board.move_tile('l')
                    elif event.key == pygame.K_RIGHT:
                        board.move_tile('r')
                    
            screen.fill('white')
            if board.movecount > 0:
                board.update_stats()
            else:
                board.timer.start()
            board.draw(screen, font)
            pygame.display.flip()
            solved = board.is_solved()
    
    elif control_mode == 'hover':
        while not solved:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    board.hover_control()


            screen.fill('white')
            if board.movecount > 0:
                board.update_stats()
            else:
                board.timer.start()
            board.draw(screen, font)
            pygame.display.flip()    
            solved = board.is_solved()

    final_time = board.timer.current_time()
    board.last_solve_time = final_time
    board.current_mvc = board.movecount
    board.current_tps = board.movecount/final_time


boardsize = 4
tilesize = 100
board = Board(boardsize, tilesize)
board.fringe_colour_scheme()

settings = open('settings.txt', 'r')
for line in settings:
    if 'control mode' in line:
        control_mode = line.split(': ')[1].strip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                board.gen_scramble()
                solving()

            if event.key == pygame.K_EQUALS:
                boardsize += 1
                board = Board(boardsize, tilesize)
            elif event.key == pygame.K_MINUS:
                boardsize -= 1
                board = Board(boardsize, tilesize)

            if event.key == pygame.K_PAGEUP:
                board.tile_size += 10
            elif event.key == pygame.K_PAGEDOWN:
                board.tile_size -= 10
            elif event.key == pygame.K_HOME:
                board.tile_size = 100
            elif event.key == pygame.K_END:
                board.tile_size = (min(screen.get_width(), screen.get_height()))/board.size
            if control_mode == 'kb':
                if event.key == pygame.K_UP:
                    board.move_tile('u')
                elif event.key == pygame.K_DOWN:
                    board.move_tile('d')
                elif event.key == pygame.K_LEFT:
                    board.move_tile('l')
                elif event.key == pygame.K_RIGHT:
                    board.move_tile('r')

    screen.fill((255, 255, 255))
    if control_mode =='hover':
        board.hover_control()

    board.draw(screen, font)

    pygame.display.flip()

pygame.quit()
