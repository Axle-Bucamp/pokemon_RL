# make the loop
# compute the gradient
# make the policy
from websocket import create_connection
import preprocessing as pr
import model 
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
# last issue, sometime player get inverted for some reason in the curent value cycle so probably same in the rest

# get a list of playable model
model_players = random.choices(models, k=2) # must save the progress also car about unique tf function
optimizer_p1 = tf.keras.optimizers.Adam() 
optimizer_p2 = tf.keras.optimizers.Adam() 
loss_object = tf.keras.losses.CategoricalCrossentropy()

for i in range(episode):
    # create a game instance
    ws = create_connection("ws://localhost:9898")
    ws.send('>start {"formatid":"gen7randombattle"}')
    ws.send('>player p1 {"name":"Alice"}')
    ws.send('>player p2 {"name":"bob"}')

    ws.send('>p2 switch 1')
    ws.send('>p1 switch 1')

    # préprocess the first state of the battle
    player_data = pr.get_players_data(ws, 2)
    curent_life = pr.get_total_life(player_data.copy())
    # make a function to get specific critere from team
    state_player_one = pr.preprocess_to_stochastic(player_data)
    state_player_two = pd.concat([state_player_one.iloc[6:], state_player_one.iloc[0:6]] )
    
    # load the model that will fight one against the other
    nb_turn = 0
    while not over or nb_turn != max_turn:
        move_player_one = model_players[0](state_player_one.to_numpy().astype('float32').reshape(1, 12, 38), training=True)
        move_player_two = model_players[1](state_player_two.to_numpy().astype('float32').reshape(1, 12, 38), training=True)

        # make them fight one turn
        indices, values = tf.nn.top_k(move_player_one, k=10)
        ## make a function : choice action
        ws.send('>p1 ' + possible_action[values.numpy()[0][0]])
        error_player_one = 0
        i = 1
        ret = ws.recv() 
        while "error" in ret or "Can't" in ret:
            print(ret)
            error_player_one += 1
            ws.send('>p1 ' + possible_action[values.numpy()[0][i] ])
            ret = ws.recv() 
            i += 1

        penalty_p1 = error_player_one / 10
        if "switch" in possible_action[values.numpy()[0][i] ] :
            penalty_p1+= 0.1

        indices, values = tf.nn.top_k(move_player_two, k=10)
        ws.send('>p2 ' + possible_action[values.numpy()[0][0] ])
        error_player_two = 0
        z = 1
        ret = ws.recv() 
        while "error" in ret or "Can't" in ret:
            print(ret)
            error_player_two += 1
            ws.send('>p2 ' + possible_action[values.numpy()[0][z] ])
            ret = ws.recv() 
            z += 1

        penalty_p2 = error_player_two / 10
        if "switch" in possible_action[values.numpy()[0][z] - 1] :
            penalty_p2+= 0.1
        
        # add penalty on switch
        
        
        penalty_p2
        # add penalty on error

        # get the next state
        player_data = pr.get_players_data(ws, 2)
        new_curent_life = pr.get_total_life(player_data.copy())
        state_player_one = pr.preprocess_to_stochastic(player_data)
        state_player_two = pd.concat([state_player_one.iloc[6:], state_player_one.iloc[0:6]] )
            
        # compute the reward
        cur_arr_p1, cur_arr_p2, new_arr_p1, new_arr_p2 = np.zeros((1,10)), np.zeros((1,10)), np.zeros((1,10)), np.zeros((1,10))
        cur_arr_p1[0][i] = curent_life[0]
        cur_arr_p2[0][z] = curent_life[1]
        new_arr_p2[0][z] = new_curent_life[1]
        new_arr_p1[0][i] = new_curent_life[0]

        # train
        model.train_p1(state_player_one.to_numpy().astype('float32').reshape(1, 12, 38), model_players[0], loss_object, optimizer_p1, cur_arr_p1, cur_arr_p2, new_arr_p1, new_arr_p2, penalty_p1)
        model.train_p2(state_player_two.to_numpy().astype('float32').reshape(1, 12, 38), model_players[1], loss_object, optimizer_p2, cur_arr_p1, cur_arr_p2, new_arr_p1, new_arr_p2, penalty_p2)
        curent_life = new_curent_life
        nb_turn += 1
        print(curent_life)
        # préprocess the first state of the battle
        player_data = pr.get_players_data(ws, 2)
        curent_life = pr.get_total_life(player_data.copy())
        # make a function to get specific critere from team
        state_player_one = pr.preprocess_to_stochastic(player_data)
        state_player_two = pd.concat([state_player_one.iloc[6:], state_player_one.iloc[0:6]] )

    ws.close()