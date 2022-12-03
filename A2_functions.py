# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 13:21:26 2022

@author: Sarah Joyal, ID 40083642
"""
import A2_RushHour as game
#============================ FREE FUNCTIONS ============================
def parse_file(filename):
    
    file = open(filename, 'r')
    
    puzzles = []
    
    for line in file:
        
        if line[0] == "#" or line[0] == "\n":
            continue

        puzzles.append(extract_board(line.split()))

    file.close()
    
    return puzzles
    
    
def extract_board(raw):
    
    puzzle = [['']*6 for _ in range(6)]
    
    fuel_list = []
    raw_puzzle = raw[0]
    
    if len(raw) > 1:
        fuel_list = raw[1:]
        
    #Format puzzle
    for i in range(0, len(raw_puzzle)):
        x = i%6
        y = i//6
        item = raw_puzzle[i]
        puzzle[y][x] = item
    

    carlist = extract_cars(puzzle, fuel_list)
    
    return game.Board(carlist)
                    

def extract_cars(puzzle, fuel_list):
    register_cars = puzzle
    car_list = set()
    
    #Register list of cars
    for y in range(0, 6):
        for x in range(0, 6):
            element = register_cars[y][x]
            if element == '.':
                continue
            n = element; cx = x; cy = y; l = -1; o = -1
            f = extract_fuel(n, fuel_list)
            
            #Check for horizontal cars
            if x < 5:
                if x < 4: 
                    if register_cars[y][x + 1] == element and register_cars[y][x + 2] == element:
                        l = 3
                        o = 0
                        register_cars[y][x + 1] = '.'
                        register_cars[y][x + 2] = '.'
                        
                if register_cars[y][x + 1] == element:
                    l = 2
                    o = 0
                    register_cars[y][x + 1] = '.'
                    
            #Check for vertical cars
            if y < 5:
                if y < 4: 
                    if register_cars[y+1][x] == element and register_cars[y+2][x] == element:
                        l = 3
                        o = 1
                        register_cars[y+1][x] = '.'
                        register_cars[y+2][x] = '.'
                if register_cars[y+1][x] == element:
                    l = 2
                    o = 1
                    register_cars[y+1][x] = '.'
            
            car_list.add(game.Car(n, cx, cy, l-1, o, f, n=='A'))
    
    return car_list
    
def extract_fuel(name, fuel_list):
    # print(f'looking for {name} in:s\n{fuel_list}')
    fuel_level = 100
    
    if len(fuel_list) == 0:
        return fuel_level

    for fuel in fuel_list:
        if fuel[0] == name:
            fuel_level = int(fuel[1])

    return fuel_level

def gen_board(carlist):
    board = [['.', '.', '.', '.', '.', '.'],
             ['.', '.', '.', '.', '.', '.'],
             ['.', '.', '.', '.', '.', '.'],
             ['.', '.', '.', '.', '.', '.'],
             ['.', '.', '.', '.', '.', '.'],
             ['.', '.', '.', '.', '.', '.']]
    
    for car in carlist:
        x, y = car.xcoord, car.ycoord
        if car.orientation == 0:
            for i in range(car.length+1):
                board[y][x+i] = car.name
        else:
            for i in range(car.length+1):
                board[y+i][x] = car.name
                
    str_board = ''
    for y in board:
        for x in y:
            str_board += x
            
    return str_board, board
    
def fuel_updates(carlist, moves):
    output = ''
    
    for c in carlist:
            for m in moves:
                if c.name == m[0]:
                    output += f' {c.name}{c.fuel}'
                    break
                
    return output

def trim(movelist, boardconfig):
    
    car = movelist[0][0]; direction = movelist[0][1]; distance = movelist[0][2]
    
    trimmed_movelist = [[car, direction, distance]]
    trimmed_boardconfig = [f'{boardconfig[0]} {fuel_updates(boardconfig[0].carlist, trimmed_movelist)}']
    
    for i in range(1, len(movelist)):
        car = movelist[i][0]; direction = movelist[i][1]; distance = movelist[i][2]
        if trimmed_movelist[-1][0] == car and trimmed_movelist[-1][1] == direction:
            
            del trimmed_movelist[-1]
            trimmed_movelist.append([car, direction, distance+1])
            
            del trimmed_boardconfig[-1]
            
        else:
            trimmed_movelist.append([car, direction, distance])
            
        trimmed_boardconfig.append(f'{boardconfig[i]} {fuel_updates(boardconfig[i].carlist, trimmed_movelist)}')

            
    return trimmed_movelist, trimmed_boardconfig

def doc_solution(searchType, num, runtime, search_length, solution_path, init_puzzle, no_sol):
    
    moves_path, sol_path = trim(solution_path[0], solution_path[1])
    
    start_puzzlestr, start_puzzleboard = init_puzzle.get_puzzle()
    
    file = f'{searchType}-sol-{num}.txt'
    
    with open(f'A2output/{file}', 'w') as f:
        print('-'*100 + '\n', file=f)
        
        print(f'Initial board configuration: {start_puzzlestr}\n', file=f)
        
        for line in start_puzzleboard:
            for e in line:
                print(f'{e}', end="", file=f)
            print('', file=f)
            
        print('\nCar fuel available: ', end="", file=f)
        for c in init_puzzle.carlist:
            if c == list(init_puzzle.carlist)[-1]:
                print(f'{c.name}:{c.fuel}\n', file=f)
            else:
                print(f'{c.name}:{c.fuel}, ', end="", file=f)
        
        if no_sol:
            print("Sorry, could not solve the puzzle as specified.\nError: no solution found\n", file=f)
            print(f'Runtime: {runtime} seconds', file=f)
            print('-'*100, file=f)
            return

        print(f'Runtime: {runtime} seconds', file=f)
        print(f'Search path length: {search_length} states', file=f)
        print(f'Solution path length: {len(moves_path)} moves', file=f)
        print('Solution path: ', end="", file=f)
        moves_output = []
        
        for entry in moves_path:
            moves_output.append(f'{entry[0]} {entry[1]} {entry[2]}')
            if entry == moves_path[-1]:
                print(f'{moves_output[-1]}', file=f)
            else:
                print(f'{moves_output[-1]}; ', end="", file=f)
                
        print("", file=f)
        
        for i in range(len(sol_path)):
            print(f'{moves_output[i]}\t{sol_path[i]}', file=f)
            
        print("", file=f)
        
        for line in solution_path[1][-1].get_puzzle()[1]:
            for e in line:
                print(f'{e}', end="", file=f)
            print('', file=f)
            
        print("", file=f)
        
        print('-'*100, file=f)

def doc_search(searchType, num, fnum, gnum, hnum, state):
    file = f'A2output/{searchType}-search-{num}.txt'
    with open(file, 'a') as f:
        print(f'{fnum} {gnum} {hnum} {state}', file=f)
