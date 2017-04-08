#!/usr/bin/python3
# -*- coding: utf8 -*-

import pickle

if __name__ == '__main__' :

    class GameState(object) :
        def __init__(self, **kwargs) :
            self.level = 0
            self.lives = 4

    state = GameState()
    print("origin : ", state.__dict__)
    print()

    #pick to object
    obj = pickle.dumps(state)
    print("type(obj) : ", type(obj), obj)
    print()
    obj_after = pickle.loads(obj)
    print("obj_after : ", type(obj_after), obj_after.__dict__)
    print()
    
    #pick to file
    state_path = '_Output/pickle_game_state.bin'
    with open(state_path, "wb") as f :
        pickle.dump(state, f)

    with open(state_path, "rb") as f :
        state_after = pickle.load(f)

    print("pickle after : ", type(state_after), state_after.__dict__)    
