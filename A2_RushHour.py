# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 18:59:33 2022

@author: Sarah Joyal
"""
import A2_functions as func
from copy import deepcopy    
EXIT = {'x': 5, 'y': 2}

#============================ CAR CLASS ============================
class Car(object): 
    """
    Attributes:
        name = AKA car colour (char)
        coord = coordinates on the board (matrix size 2)
        length = Length of the car (int)
        orientation = Orientation of the car (int 0 = H, 1 = V)
        fuel = Fuel available for the car (int)
        is_A = Whether the car is to be freed (bool)
    """
    
    def __init__(self, name, xcoord, ycoord, length, orientation, fuel, is_A):
        
        self.name = name
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.length = length
        self.orientation = orientation
        self.fuel = fuel
        self.is_A = is_A

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return str(self.__dict__)
    
    def __hash__(self):
        return hash(self.__repr__())
    
    def __repr__(self):
        return "Car({0}, [{1}, {2}], {3}, {4}, {5})".format(self.name, self.xcoord, self.ycoord,
                                                     self. length, self.orientation,
                                                     self.fuel)
        
#============================ BOARD CLASS ============================
class Board(object):
    
    """
    Attributes:
        cars = Cars still on board
    """
    
    def __init__(self, cars):
        self.size = {'x': 6, 'y': 6}
        self.carlist = cars
        
    def __eq__(self, other):
        return self.carlist == other.carlist

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __str__(self):
        return str(self.get_puzzle()[0])

    def __hash__(self):
        return hash(self.__repr__())
    
    
    def get_puzzle(self):
        str_board, board = func.gen_board(self.carlist)
        return str_board, board

    def is_solved(self):
        solved = False
        for car in self.carlist:
            if car.is_A and car.xcoord + car.length == EXIT['x']: solved = True
        return solved
    
    def possible_moves(self):
        
        matrix_puzzle = self.get_puzzle()[1]
        
        moves = []
        boards = []
                
        for car in self.carlist:
            if car.fuel > 0:
                new_fuel = car.fuel - 1
                if car.orientation == 0:
                    if car.xcoord > 0 and matrix_puzzle[car.ycoord][car.xcoord - 1] == '.':
                        newcar = Car(car.name, car.xcoord - 1, car.ycoord, car.length, car.orientation, new_fuel, car.name == 'A')
                        newcarlist = self.carlist.copy()
                        newcarlist.remove(car)
                        newcarlist.add(newcar)
                        move_str = 'left'
                        moves.append([car.name, move_str, 1])
                        boards.append(Board(newcarlist))
                        
                    if car.xcoord + car.length < self.size['x']-1 and matrix_puzzle[car.ycoord][car.xcoord + car.length + 1] == '.':
                        if car.xcoord + car.length + 1 ==  EXIT['x'] and car.ycoord == EXIT['y'] and not car.name == 'A':
                            newcarlist = self.carlist.copy()
                            newcarlist.remove(car)
                        else:
                            newcar = Car(car.name, car.xcoord + 1, car.ycoord, car.length, car.orientation, new_fuel, car.name == 'A')
                            newcarlist = self.carlist.copy()
                            newcarlist.remove(car)
                            newcarlist.add(newcar)
                        move_str = 'right'
                        moves.append([car.name, move_str, 1])
                        boards.append(Board(newcarlist))
                else:
                    if car.ycoord > 0 and matrix_puzzle[car.ycoord - 1][car.xcoord] == '.':
                        newcar = Car(car.name, car.xcoord, car.ycoord - 1, car.length, car.orientation, new_fuel, car.name == 'A')
                        newcarlist = self.carlist.copy()
                        newcarlist.remove(car)
                        newcarlist.add(newcar)
                        move_str = 'up'
                        moves.append([car.name, move_str, 1])
                        boards.append(Board(newcarlist))
                    if car.ycoord + car.length < self.size['y']-1 and matrix_puzzle[car.ycoord + car.length + 1][car.xcoord] == '.':
                        newcar = Car(car.name, car.xcoord, car.ycoord + 1, car.length, car.orientation, new_fuel, car.name == 'A')
                        newcarlist = self.carlist.copy()
                        newcarlist.remove(car)
                        newcarlist.add(newcar)
                        move_str = 'down'
                        moves.append([car.name, move_str, 1])
                        boards.append(Board(newcarlist))
            else:
                continue
        return moves, boards