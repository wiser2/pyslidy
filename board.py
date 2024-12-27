import pygame
from timer import Timer
import random
from colour import Color

class Board:
    def __init__(self, size, tile_size=100) -> None:
        self.size = size
        self.boardstate = []
        for i in range(size):
            self.boardstate.append(make_row(i*size+1, i*size+size))

        self.boardstate[-1][-1] = 0
        self.solved_state = self.boardstate
        self.empty_tile = self.find_empty_tile(self.boardstate)

        self.tile_size = tile_size

        self.colours = self.fringe_colour_scheme()

        self.movecount = 0

        self.timer = Timer()
        self.current_time = 0

        self.last_solve_time = 0
        self.current_mvc = 0
        self.current_tps = 0

    def find_empty_tile(self, boardstate):
        for row in boardstate:
            if 0 in row:
                return [boardstate.index(row), row.index(0)]

    def move_tile(self, direction):
        self.movecount += 1

        if self.movecount == 0:
            self.timer.start()

        target_coords = [0, 0]
        if direction == 'u' and self.empty_tile[0] != 0:
            target_coords = [self.empty_tile[0]-1, self.empty_tile[1]]
        elif direction == 'd' and self.empty_tile[0] != self.size-1:
            target_coords = [self.empty_tile[0]+1, self.empty_tile[1]]
        elif direction == 'l' and self.empty_tile[1] != 0:
            target_coords = [self.empty_tile[0], self.empty_tile[1]-1]
        elif direction == 'r' and self.empty_tile[1] != self.size-1:
            target_coords = [self.empty_tile[0], self.empty_tile[1]+1]
        else:
            return

        target_colour = self.colours[target_coords[0]*self.size + target_coords[1]]
        self.colours[self.empty_tile[0]*self.size + self.empty_tile[1]] = target_colour
        self.colours[target_coords[0]*self.size + target_coords[1]] = 0

        target = self.boardstate[target_coords[0]][target_coords[1]]
        self.boardstate[self.empty_tile[0]][self.empty_tile[1]] = target
        self.boardstate[target_coords[0]][target_coords[1]] = 0
        self.empty_tile = target_coords

    def draw(self, screen, font):
        font = pygame.font.Font('freesansbold.ttf', 40*self.tile_size//100)
        for y in range(self.size):
            for x in range(self.size):
                if self.boardstate[y][x] != 0:
                    tile_colour = (self.colours[y*self.size + x].rgb[0] * 255, self.colours[y*self.size + x].rgb[1] * 255, self.colours[y*self.size + x].rgb[2] * 255)
                    pygame.draw.rect(screen, tile_colour, (x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size))
                    text = font.render(str(self.boardstate[y][x]), True, 'black')
                    text_rect = text.get_rect(center=(x*self.tile_size+self.tile_size/2, y*self.tile_size+self.tile_size/2))
                    text_rect.inflate_ip(self.tile_size/100, self.tile_size/100)
                    screen.blit(text, text_rect)
        
        self.draw_stats(screen, font)


    def gen_scramble(self):
        all_numbers = list(range(self.size**2))
        random.shuffle(all_numbers)
        
        while self.parity(all_numbers) % 2 != 1:
            random.shuffle(all_numbers)

        self.boardstate = []
        # split the shuffled all_numbers into rows
        for i in range(0, self.size**2, self.size):
            row = all_numbers[i:i+self.size]
            self.boardstate.append(row)
        
        self.empty_tile = self.find_empty_tile(self.boardstate)

        self.solved_state = []
        for i in range(self.size):
            self.solved_state.append(make_row(i*self.size+1, i*self.size+self.size))

        self.solved_state[-1][-1] = 0

        self.movecount = 0

        self.update_colours()

        print('scrambled')

    def update_colours(self):
        self.solved_colour_scheme = self.fringe_colour_scheme()
        for y in range(self.size):
            for x in range(self.size):
                if self.boardstate[y][x] == 0:
                    self.colours[y*self.size + x] = 0
                else:
                    self.colours[y*self.size + x] = self.solved_colour_scheme[self.boardstate[y][x]-1]

    def parity(self, permutation):
        original_permutation = permutation
        # move the empty tile to the bottom right
        empty_index = permutation.index(0)
        permutation.append(0)
        permutation.pop(empty_index)

        # calculate the parity of the permutation
        already_seen = []
        cycles = []
        for start_index in permutation:
            if start_index in already_seen:
                continue

            path = [start_index]
            next_index = permutation[start_index]

            while start_index != next_index:
                path.append(next_index)
                next_index = permutation[next_index]

            else:
                cycles.append(path)
                already_seen.extend(path)

        permutation = original_permutation
        return len(cycles) % 2
    
    def hover_control(self):
        mouse_pos = (pygame.mouse.get_pos()[0]//self.tile_size, pygame.mouse.get_pos()[1]//self.tile_size)

        if (mouse_pos[0] < self.size) and (mouse_pos[1] < self.size):
            if (mouse_pos[1] < self.empty_tile[0]) and (mouse_pos[0] == self.empty_tile[1]):
                self.move_tile('u')
            elif (mouse_pos[1] > self.empty_tile[0]) and (mouse_pos[0] == self.empty_tile[1]):
                self.move_tile('d')
            elif (mouse_pos[0] < self.empty_tile[1]) and (mouse_pos[1] == self.empty_tile[0]):
                self.move_tile('l')
            elif (mouse_pos[0] > self.empty_tile[1]) and (mouse_pos[1] == self.empty_tile[0]):
                self.move_tile('r')
    
    def is_solved(self):
        return self.boardstate == self.solved_state

    def fringe_colour_scheme(self):
        # generate gradient for colours
        red = Color('red')
        violet = Color('violet')
        colour_list = list(red.range_to(violet, self.size*2-2))

        for colour in colour_list:
            colour.set_saturation(0.5)

        solved_state_1d = [tile for row in self.solved_state for tile in row]

        colour_scheme_2d = []
        # split self.colours into rows
        for i in range(0, self.size**2, self.size):
            row = solved_state_1d[i:i+self.size]
            colour_scheme_2d.append(row)

        for i in range(len(colour_scheme_2d)):
            for j in range(len(colour_scheme_2d[i])):
                if self.solved_state[i][j] - i*self.size > i:
                    colour_scheme_2d[i][j] = colour_list[i*2]
        
        for x in range(len(colour_scheme_2d)-1):
            for y in range(len(colour_scheme_2d[x])):
                if type(colour_scheme_2d[y][x]) == int:
                    colour_scheme_2d[y][x] = colour_list[x*2+1]
        
        colour_scheme = []
        for row in colour_scheme_2d:
            colour_scheme.extend(row)
        
        self.solved_colour_scheme = colour_scheme
        
        return colour_scheme

    def draw_stats(self, screen, font):
        font = pygame.font.Font('fonts\\Courier New.ttf', 15)
        time_text = font.render(f'{self.current_time}, {self.current_mvc} moves, {self.current_tps} tps', True, 'black')
        time_text_rect = time_text.get_rect(topleft=(30, screen.get_height()-30))
        time_text_rect.inflate_ip(10, 10)
        screen.blit(time_text, time_text_rect)
    
    def update_stats(self):
        self.current_time = self.timer.current_time()
        self.current_mvc = self.movecount
        self.current_tps = self.current_mvc / self.current_time

def make_row(start, end):
    row = list(range(start, end+1))
    return row