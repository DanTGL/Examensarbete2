import time
import copy

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

                result = 0
                while True:
                    if (curX + deltaX > len(grid) or curY + deltaY > len(grid)):
                        result = -1
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
                        return True

    return False

def optimized(grid, words, arr=[], depth=0, dir=0, pos=(0, 0), forceDir=False):
    if depth >= len(grid):
        return
    
    if dir == (0, 0):
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
                arr.pop(i)
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

    words_copy = copy.copy(words)

    start = time.perf_counter()
    naive(grid, words_copy)
    end = time.perf_counter()

    print(f"The naive algorithm took {end - start:0.7f} seconds")

    words_copy = copy.copy(words)

    start = time.perf_counter()
    optimized(grid, words_copy)
    end = time.perf_counter()
    print(f"The optimized algorithm took {end - start:0.7f} seconds")