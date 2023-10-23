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

