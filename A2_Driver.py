# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 11:32:33 2022

@author: Sarah Joyal
"""
import A2_functions as func
import A2_SearchFunctions as search

testboard = func.parse_file('sample-input.txt')

h = [search.h0, search.h1, search.h2, search.h3, search.h4]

for i in range(len(testboard)):
    
    sol = search.Search('ucs', testboard[i], h[0], i+1)
    func.doc_solution(sol[0], sol[1], sol[2], sol[3], sol[4], sol[5], sol[6])
    
    for v in range(1,5):
        sol = search.Search('gbfs', testboard[i], h[v], i+1)
        func.doc_solution(sol[0], sol[1], sol[2], sol[3], sol[4], sol[5], sol[6])
    
        sol = search.Search('a', testboard[i], h[v], i+1)
        func.doc_solution(sol[0], sol[1], sol[2], sol[3], sol[4], sol[5], sol[6])
    
   