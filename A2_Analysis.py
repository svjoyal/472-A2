# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 14:12:22 2022

@author: Sarah Joyal
"""
import pandas as pd
import A2_functions as func
import A2_SearchFunctions as search

def analyze(analysis_dict):
    xlwriter = pd.ExcelWriter('Analysis.xlsx', engine='xlsxwriter')
    df = pd.DataFrame(analysis_dict)
    df.to_excel(xlwriter,sheet_name='Analysis',index=False)
    xlwriter.close()

analysisboards = func.parse_file('Analysis_Tests.txt')
h = [search.NA, search.h1, search.h2, search.h3, search.h4]

analysis_dict = {
    "Puzzle Number":[],
    "Algorithm":[],
    "Heuristic":[],
    "Length of the Solution":[],
    "Length of the Search Path":[],
    "Execution Time (in seconds)":[]
    }

for i in range(len(analysisboards)):
    
    sol = search.Search('ucs', analysisboards[i], h[0], i+1)
    analysis_dict["Puzzle Number"].append(sol[1])
    analysis_dict["Algorithm"].append(sol[0].upper())
    analysis_dict["Heuristic"].append(h[0].__name__)
    analysis_dict["Length of the Solution"].append(len(sol[4][0]))
    analysis_dict["Length of the Search Path"].append(sol[3])
    analysis_dict["Execution Time (in seconds)"].append(sol[2])
    
    for v in range(1,5):
        sol = search.Search('gbfs', analysisboards[i], h[v], i+1)
        analysis_dict["Puzzle Number"].append(sol[1])
        analysis_dict["Algorithm"].append(sol[0].upper())
        analysis_dict["Heuristic"].append(h[v].__name__)
        analysis_dict["Length of the Solution"].append(len(sol[4][0]))
        analysis_dict["Length of the Search Path"].append(sol[3])
        analysis_dict["Execution Time (in seconds)"].append(sol[2])
        
        sol = search.Search('a', analysisboards[i], h[v], i+1)
        analysis_dict["Puzzle Number"].append(sol[1])
        analysis_dict["Algorithm"].append(f'{sol[0].upper()}/A*')
        analysis_dict["Heuristic"].append(h[v].__name__)
        analysis_dict["Length of the Solution"].append(len(sol[4][0]))
        analysis_dict["Length of the Search Path"].append(sol[3])
        analysis_dict["Execution Time (in seconds)"].append(sol[2])
        
analyze(analysis_dict)