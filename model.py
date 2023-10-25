import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, optimizers

# add layer config etc
def get_new_player_model(possible_action=10, nb_layer = 5, neuron_per_layer = 32, learning_rate=0.01):
    
    # define the model
    model = keras.Sequential()
    model.add(keras.Input(shape=(12,38)))
    model.add(layers.Flatten())
    for i in range(nb_layer):
        model.add(layers.Dense(neuron_per_layer, activation="relu", name="layer_" + str(i)))

    model.add(layers.Dense(possible_action, activation='softmax'))
    
    # choose the optimizer
    return model

@tf.function
def train_p1(input, model, loss, optimizer, cur_arr_p1, cur_arr_p2, new_arr_p1, new_arr_p2, penalty):
    with tf.GradientTape() as gradien_P1_tape, tf.GradientTape() as gradien_P2_tape:
        # choose a move
        move = model(input, training=True)
            
        # compute the reward
        # minimiser l'entropie de la vie perdu d'un tour à l'autre  et augmenter celle de l'adversaire
        # on peut ajouter N tour avant le calcul de la future value si nécessaire
        # (lifePF - log(lifeP) - (lifeE - log(lifeEF)) / 2 
        # check the need, do we need to compare model output in loss disc_real_output
        loss_total =  1 + ( loss(cur_arr_p1, new_arr_p1)   - loss(cur_arr_p2, new_arr_p2 )) * tf.cast(move,dtype=tf.float64) + penalty
        
        # apply the gradient
        gradient = gradien_P1_tape.gradient(loss_total,
                                          model.trainable_variables)
            
        optimizer.apply_gradients(zip(gradient,
                                          model.trainable_variables))
            
        

@tf.function
def train_p2(input, model, loss, optimizer, cur_arr_p1, cur_arr_p2, new_arr_p1, new_arr_p2, penalty):
    with tf.GradientTape() as gradien_P1_tape, tf.GradientTape() as gradien_P2_tape:
        # choose a move
        move = model(input, training=True)
            
        # compute the reward
        # minimiser l'entropie de la vie perdu d'un tour à l'autre  et augmenter celle de l'adversaire
        # on peut ajouter N tour avant le calcul de la future value si nécessaire
        # (lifePF - log(lifeP) - (lifeE - log(lifeEF)) / 2 
        # check the need, do we need to compare model output in loss disc_real_output
        loss_total =  1 + ( loss(cur_arr_p2, new_arr_p2 )  - loss(cur_arr_p1, new_arr_p1 ) ) * tf.cast(move,dtype=tf.float64) + penalty
        
        # apply the gradient
        gradient = gradien_P1_tape.gradient(loss_total,
                                          model.trainable_variables)
            
        optimizer.apply_gradients(zip(gradient,
                                          model.trainable_variables))
            