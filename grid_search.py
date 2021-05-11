import time
import copy
import random
import string

class Word:

    def __init__(self, word, grid, positions, directions):
        self.word = word
        self.grid = grid
        self.positions = copy.deepcopy(positions)
        random.shuffle(self.positions)
        self.directions = copy.deepcopy(directions)
        random.shuffle(self.directions)

def try_word(grid, word, pos, dir):
    x, y = pos

    delta_x = dir & 0x1
    delta_y = (dir >> 1) & 0x1

    if x + (delta_x * len(word)) > len(grid) or y + (delta_y * len(word)) > len(grid):
        return None
    temp_grid = copy.deepcopy(grid)
    cur_x = x
    cur_y = y


    
    for c in word:
        if cur_x >= len(temp_grid) or cur_y >= len(temp_grid):
            return None

        if temp_grid[cur_y][cur_x] is None or temp_grid[cur_y][cur_x] == c:

            temp_grid[cur_y][cur_x] = c
            cur_x += delta_x
            cur_y += delta_y
        else:
            return None
    
    return temp_grid

def generate(words, grid_size):
    random.shuffle(words)
    cur_word = 0

    positions = [[x, y] for y in range(grid_size) for x in range(grid_size)]


    directions = [i for i in range(1, 4)]

    word_stack = []
    word_stack.append(Word(words[0], [[None for _ in range(grid_size)] for _ in range(grid_size)], positions, directions))

    while True:
        if not len(word_stack):
            raise Exception("Word does not fit on the grid")

        if not len(word_stack[-1].directions):
            word_stack[-1].positions.pop()
            word_stack[-1].directions = copy.deepcopy(directions)
            random.shuffle(word_stack[-1].directions)
        
        dir = word_stack[-1].directions.pop()

        if not len(word_stack[-1].positions):
            word_stack.pop()
            cur_word -= 1
        else:
            pos = word_stack[-1].positions[-1]
            
            
            grid = try_word(word_stack[-1].grid, word_stack[-1].word, pos, dir)

            if grid is not None:
                

                if len(word_stack) < len(words):
                    word_stack.append(Word(words[len(word_stack)], grid, positions, directions))
                else:
                    word_stack.append(Word(words[0], grid, positions, directions))
                    break

    for y in range(grid_size):
        for x in range(grid_size):
            if word_stack[-1].grid[y][x] is None:
                word_stack[-1].grid[y][x] = "0"
    
    return word_stack[-1].grid


def compare(str1, str2):
    return -1 if str1 > str2 else 0 if str1 == str2 else 1


def binary_search_prefix(arr, prefix):
    l = 0
    r = len(arr) - 1
    while l <= r:
        mid = int(l + (r - l) / 2)

        res = compare(prefix, arr[mid])

        if res == 0:
            return mid

        # Checks if the word starts with the given prefix
        if arr[mid].startswith(prefix):
            return -2
        else:
            if res > 0:
                l = mid + 1
            else:
                r = mid - 1

    return -1

def naive(grid, words):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            for dir in range(1, 4):
                deltaX = dir & 0x01
                deltaY = (dir >> 1) & 0x01

                curX = x
                curY = y

                prefix = ""

                result = -1
                while True:
                    if (curX + deltaX > len(grid) or curY + deltaY > len(grid)):
                        break

                    prefix += grid[curY][curX]

                    curX += deltaX
                    curY += deltaY

                    result = binary_search_prefix(words, prefix)

                    if result != -2:
                        break

                if result >= 0:
                    words.pop(result)
                    
                    if not len(words):
                        print("SUCCESS")
                        return True
    print("FAILED")
    return False

def optimized(grid, words, arr=[], depth=0, dir=0, pos=(0, 0), forceDir=False):
    if depth >= len(grid):
        return

    if not len(words):
        print("SUCCESS")
        return
    
    if not dir:
        optimized(grid, words, arr, depth, 0x1, pos, forceDir)
        optimized(grid, words, arr, depth, 0x2, pos, forceDir)
    else:
        dir_x = dir & 0x1
        dir_y = (dir >> 1) & 0x1

        pos_x, pos_y = pos

        char = grid[pos_y][pos_x]

        for i in range(len(arr) - 1, -1, -1):
            result = binary_search_prefix(words, arr[i] + char)

            if result == -2:
                arr[i] += char
            elif result == -1:
                arr.pop(i)
            else:
                words.pop(result)
                arr[i] += char
                if not len(words):
                    return

        arr += char

        if not forceDir:
            optimized(grid, words, depth=0, dir=(~dir) & 0x3, pos=pos, forceDir=True)
            optimized(grid, words, depth=depth, dir=0x3, pos=pos, forceDir=True)
        
        pos = (pos[0] + dir_x, pos[1] + dir_y)

        optimized(grid, words, arr, depth + 1, dir, pos, forceDir)

if __name__ == "__main__":
    grid = [
        ['N', 'K', 'L', 'L', 'K', 'C'],
        ['R', 'B', 'S', 'L', 'K', 'A'],
        ['E', 'L', 'I', 'L', 'C', 'N'],
        ['D', 'I', 'F', 'R', 'N', 'D'],
        ['Y', 'K', 'C', 'U', 'D', 'Y'],
        ['Y', 'E', 'F', 'K', 'N', 'N']
    ]

    words = ["BIRD", "CANDY", "FUN", "LIKE", "RED"]

    #grid = generate(words, 15)
    words.sort()
    print(words)
    for row in grid:
        print(" ".join(row))

    words_copy = copy.copy(words)

    #start = time.perf_counter()
    #naive(grid, words_copy)
    #end = time.perf_counter()

    #print(f"The naive algorithm took {end - start:0.7f} seconds")

    #start = time.perf_counter()
    naive(grid, words_copy)

    print(words_copy)
    for row in grid:
        print(" ".join(row))
    #end = time.perf_counter()
    #print(f"The optimized algorithm took {end - start:0.7f} seconds")