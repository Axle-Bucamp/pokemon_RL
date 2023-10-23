# make the loop
# compute the gradient
# make the policy
from websocket import create_connection
import preprocessing as pr
import model 
import battle
import viz
import pandas as pd
import numpy as np
import random
import tensorflow as tf

episode = 10
over = False
max_turn = 100
number_of_agent = 4
models = []
possible_action = ["move 1", "move 2", "move 3", "move 4", "switch 1", "switch 2", "switch 3", "switch 4", "switch 5", "switch 6"]

for i in range(number_of_agent):
    models.append(model.get_new_player_model())

# get a random seed for each AI (so team is fixed ?)

# get a list of playable model
for i in range(episode):
    # create a game instance
    ws = create_connection("ws://localhost:9898")
    ws.send('>start {"formatid":"gen7randombattle"}')
    ws.send('>player p1 {"name":"Alice"}')
    ws.send('>player p2 {"name":"bob"}')

    ws.send('>p2 switch 1')
    print(ws.recv())
    ws.send('>p1 switch 1')
    print(ws.recv())

    # préprocess the first state of the battle
    player_data = pr.get_players_data(ws, 2)
    state_player_one = pr.preprocess_to_stochastic(player_data)
    state_player_two = pd.concat([state_player_one.iloc[0:6], state_player_one.iloc[6:]] )
    
    # load the model that will fight one against the other
    model_players = random.choices(models, k=2)
  
    nb_turn = 0
    while not over or nb_turn != max_turn:

        # choose a move
        move_player_one = model_players[0].predict(state_player_one.to_numpy().astype('float32').reshape(1, 12, 38))
        move_player_two = model_players[1].predict(state_player_two.to_numpy().astype('float32').reshape(1, 12, 38))

        # make them fight one turn
        indices, values = tf.nn.top_k(move_player_one, k=10)
   
        ## make a function : choice action
        ws.send('>p1 ' + possible_action[values.numpy()[0][0]])
        error_player_one = 0
        i = 1
        while "error" in ws.recv():
            error_player_one += 1
            ws.send('>p1 ' + possible_action[values.numpy()[0][i]])


        indices, values = tf.nn.top_k(move_player_two, k=10)
        error_player_two = 0
        i = 1
        while "error" in ws.recv():
            error_player_two += 1
            ws.send('>p1 ' + possible_action[values.numpy()[0][i]])
        
        break
        # preprocess the new state (update life and status, turn to zeros dead poke)
        # compute policy after a turn
        # compute reward reward
        # apply gradient 
        nb_turn += 1
    
    ws.close()
    break
