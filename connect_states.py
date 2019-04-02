# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 14:05:34 2019

@author: Victor Zuanazzi
"""
from quantity import Quantity
from itertools import product
from copy import deepcopy

#not used yet to keep the data structure consistent.
class State:  
    def __init__(self, s_id, s_desc):
        self.id =  s_id    
        self.description = s_desc
        self.previous = {}
        self.next = {}
    
    def add_next_state(self, next_id):
        self.previous.add(next_id)
    
    def add_previous_state(self, prev_id):
        self.next.add(prev_id)
        

def state_copy(state):
    """copy quantities of the state.
    Not entities that have no quantity are ignored.
    """
    c_s = {}
    
    for entity in state:
        
        if (entity == "id") | (entity == "prev") | (entity == "next"):
            #c_s[entity] = state[entity].copy()
            continue
        
        c_s[entity] = {}
        
        for q in state[entity]:
            c_s[entity][q] = state[entity][q].copy()

    return c_s
        
        
        
def add_directional_connection(prev_s, next_s):
    """makes the directional connections between states.
    Inputs:
        prev_s: (dict state format) the previous state.
        next_s: (dict state format) the next state.
    Result:
        prev_s["next"] = next_s["id"] adds the id of the next state to the 
            previous state
        next_s["prev"] = prev_s["id"] adds the id of the previous state to the 
            next state.
    """
    
    #add the id of the next state to the previous state.
    if prev_s.get("next"):
        prev_s["next"].add(next_s["id"])
    else:
        prev_s["next"] = {next_s["id"]}
        
    #add the id of the previous state to the next state.
    if next_s.get("prev"):
        next_s["prev"].add(prev_s["id"])
    else:
        next_s["prev"] = {prev_s["id"]}
        
    

def connect_states(unconnected_states):
    """create phisically possible connection between states.
    NOT FULLU WORKING YET"""
    
    #add an id to each state.
    for i, s in enumerate(unconnected_states.copy()):
        s["id"] = i
        
    #For each state, check if it is possible to transition to the other state.
    for s_1 in unconnected_states:
        
        #gets all the possibilities of transitions considering all quantities 
        #of entities.
        quantities = []
        for entity_1 in s_1.copy():
            
            if (entity_1 == "id") | (entity_1 == "prev") | (entity_1 == "next"):
                continue
            
            for q in s_1[entity_1]:       
                #!!! applyDerivative changes the upper bound of inflow !!!
                quantities.append(Quantity.applyDerivative(s_1[entity_1][q]))
          
        
        all_poss = list(product(*quantities))
        
        #compares all_possibilities of next states with the posssible next states.
        for maybe_next_state in all_poss:
            #converts the list into a state description
            
            for s_2 in unconnected_states:
                
                #it is slow, but it works!
                new_s = list_to_state(maybe_next_state, s_2)

                if new_s == s_2:
                    add_directional_connection(s_1, s_2)
                    
                    
                    
#                
#                #check all quantities of the state before making the connection
#                for entity_2 in s_2:
#                    
#                    if (entity_2 == "id") | (entity_2 == "prev") | (entity_2 == "next"):
#                        continue
#                    
#                    for q_2 in s_2[entity_2]:
#                        print("generated state:\n" new_s[entity_2][q_2])
#                        print("compared state:\n" s_2[entity_2][q_2])
#                        if s_2[entity_2][q_2] == new_s[entity_2][q_2]:
#                            continue
#                        else:
#                            connect = False
#                            
#                if connect:
#                    add_directional_connection(s_1, s_2)
                            
        
        
    return unconnected_states
        
        
        
        
        
        
        
        
        
        
        
        
        