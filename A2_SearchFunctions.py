# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 00:05:53 2022

@author: Sarah Joyal

TODO: Stop the looping
"""
import PriorityQueue as pq
import A2_functions as func
import time

"""
SEARCH:
    Takes a single puzzle as input.
    Generates PQ of opened puzzle configurations, then moved into the closed set once deemed not solved
    Returns unsolvable if opened PQ is empty
    Returns path of solved puzzle if deemed solved
    Adds each puzzle config to closed set, adds puzzles' children to opened PQ and loops
    Loop proceeds until either: opened PQ is empty, target puzzle is solved
    
    Priority in PQ is determined by:
        g(n) if using UCS search
        h(n) if using GBFS search
        f(n) if using A/A* search
"""


def Search(searchtype, puzzle, h, num):
    #Start timer and lists of open/visited states
    start = time.time()
    openlist = pq.PriorityQueue()
    closed = set()
    
    #Place the head node in each list
    path = []; moves = []
    openlist.push(h(puzzle), [puzzle, path, moves])
    closed.add(str(puzzle))

    #Closed dict to facilitate heuristic comparison for best-case
    closed_dict = {}
    closed_dict[str(puzzle)] = 0
    
    while True:
        if openlist.empty(): #If open queue is empty, we have exhausted the search with no solution found
            break
        
        #Pop the next node for solution check
        priority, popped_data = openlist.pop()
        data = popped_data[0]
        path = popped_data[1]
        moves = popped_data[2]
        
        hval = h(data)
        gval = len(path)
        fval = gval + hval
        
        search_output = (f'{data} {func.fuel_updates(data.carlist, moves)}') #Search file output
        if searchtype == 'ucs':
            func.doc_search(f'{searchtype}', num, fval, gval, hval, search_output)
        elif searchtype == 'gbfs':    
            func.doc_search(f'{searchtype}-{h.__name__}', num, fval-gval, 0, hval, search_output)
        else:
            func.doc_search(f'{searchtype}-{h.__name__}', num, fval, gval, hval, search_output)
        
        if data.is_solved(): #Check if popped node is solved
            break

        next_moves, next_puzzles = data.possible_moves() #If not, generate the children nodes to visit
        
        for p in next_puzzles: 
            child_path = path + [p]
            child_moves = moves + [next_moves[next_puzzles.index(p)]]
            c_priority = 0
            if searchtype == 'ucs':
                c_priority = len(child_path)
            elif searchtype == 'gbfs':    
                c_priority = h(p)
            else:
                c_priority = h(p) + len(child_path)

            if str(p) not in closed:
                openlist.push(c_priority, [p, child_path, child_moves])
                closed.add(str(p))
                
            elif c_priority < closed_dict[str(p)]:
                openlist.push(c_priority, [p, child_path, child_moves])
                
            closed_dict[str(p)] = c_priority
                    
    end = time.time()
    time_taken = end - start
    
    print(f'{searchtype.upper()} search with heuristic {h.__name__} for board #{num} done')
    #Generate solution file
    return searchtype,num,round(time_taken,2),len(closed),[moves,path],puzzle,openlist.empty()
    


#UCS heuristic
def h0(n):
    return 0

#Blocking cars
def h1(n):
    blocking_cars = set()
    A_found = False
    board = n.get_puzzle()[1]
    for i in board[2]:
        if A_found:
            if i != '.' and i != 'A':
                blocking_cars.add(i)
            continue
        if i == 'A':
            A_found = True
    
    return len(blocking_cars)
   
#Blocking positions 
def h2(n):
    blocking_pos = []
    A_found = False
    board = n.get_puzzle()[1]
    for i in board[2]:
        if A_found:
            if i != '.' and i != 'A':
                blocking_pos.append(i)
            continue
        if i == 'A':
            A_found = True
    
    return len(blocking_pos)
    
#h1*3
def h3(n):
    return h1(n)*3

#All positions between A and exit
def h4(n):
    pos_to_exit = -1
    A_found = False
    board = n.get_puzzle()[1]
    for i in board[2]:
        if A_found:
            pos_to_exit += 1
        if i == 'A':
            A_found = True
    
    return pos_to_exit
