#!/usr/bin/python3
# -*- coding: utf8 -*-

import copyreg
import pickle

if __name__ == '__main__' :
    #better way to use pickle
    better_state_path = '_Output/pickle_better_game_state.bin'

    class BetterGameState(object) :
        def __init__(self, level = 0, lives = 4) :
            self.level = level
            self.lives = lives

    def unpickle_game_state(kwargs) :
        return BetterGameState(**kwargs)
    
    def pickle_game_state(game_state) :
        kwargs = game_state.__dict__
        return unpickle_game_state, (kwargs,)
       
    copyreg.pickle(BetterGameState, pickle_game_state)
    betterState = BetterGameState()
    
    with open(better_state_path, "wb") as f :
        pickle.dump(betterState, f)

    with open(better_state_path, "rb") as f :
        better_after = pickle.load(f)

    print("origin: ", type(betterState), betterState.__dict__)
    print("after: ", type(better_after), better_after.__dict__)
    print()

    #remove level add point to object
    class BetterGameState(object) :
        def __init__(self, lives = 4, point = 5) :
            self.lives = lives
            self.point = point
    
    def unpickle_game_state(kwargs) :
        version = kwargs.pop('version', 1)
        if version == 1 :
            kwargs.pop('level')
        return BetterGameState(**kwargs)
    
    def pickle_game_state(game_state) :
        kwargs = game_state.__dict__
        kwargs['version'] = 2
        return unpickle_game_state, (kwargs,)

    copyreg.pickle(BetterGameState, pickle_game_state)
    state = BetterGameState()
    print("origin : ", type(state), state.__dict__)

    serialize = pickle.dumps(state)
    obj_after = pickle.loads(serialize)
    print("after dump : ", type(state), state.__dict__)
    print(type(obj_after), obj_after.__dict__)

    with open(better_state_path, 'rb') as f :
        better_after = pickle.load(f)

    print(type(better_after), better_after.__dict__)