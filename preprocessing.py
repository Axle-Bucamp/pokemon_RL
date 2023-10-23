import pandas as pd
import numpy as np
import json

poke_data_path = "C:\\Users\\Megaport\\Downloads\\pokemon.json"
moves_data = json.load(open(poke_data_path + "\\moves.json"))
pokedata_data = json.load(open(poke_data_path + "\\pokedex.json", encoding="utf8"))
poke_types = ["Normal", "Fire", "Water", "Grass", "Flying", "Fighting", "Poison", "Electric", "Ground", "Rock", "Psychic", "Ice", "Bug", "Ghost", "Steel", "Dragon", "Dark", "Fairy"]

def get_players_data(ws, nb_player):
    players_data = []
    for i in range(nb_player):
        ws.send('request p' + str(i + 1))
        result =  ws.recv()
        while not '{' in result :
            ws.send('request p' + str(i + 1))
            result =  ws.recv()
        json_index = result.index('{')
        json_status = json.loads(result[json_index:])

        players_data.append(pd.json_normalize(json_status["side"]["pokemon"], max_level=3))
    return pd.concat(players_data)

def get_player_data(player_id, df):
    if player_id == 1:
        return df[0:6]
    else :
        return df[6:]

# diviser par fonction pour mieux comprendre
def preprocess_to_stochastic(df):
    # make the pokemon moves more understandable to the AI
    df.index = [0,1,2,3,4,5,6,7,8,9,10,11]
    df[["move_1", "move_2", "move_3", "move_4"]] = df['moves'].to_list()

    for move in moves_data:
        curent = move["ename"].replace(" ", "").replace("-", "").replace("_", "").lower()
        updated = curent == df[["move_1", "move_2", "move_3", "move_4"]]
    
        for key in ["move_1", "move_2", "move_3", "move_4"]:
            df.loc[updated[key], key] = str([move["power"], move["accuracy"], move["pp"], move["type"]])
    
    for i in range(df.shape[0]):
        for key in ["move_1", "move_2", "move_3", "move_4"]:
            move = str(df.iloc[i][key])
            if '[' not in move:
                if "hiddenpower" in move:
                    df.loc[i, [key]] = str([60, 100, 15, move.replace("hiddenpower", "").replace("60", "").capitalize()])
                else:
                    df.loc[i, [key]] = str([0, 100, 20, 'Normal'])


    for i in ["move_1", "move_2", "move_3", "move_4"]:
        df[[i + "power", i + "accuracy", i + "pp", i + "type"]] = df[i].str.replace("'", "").str.replace("[", "").str.replace("]", "").str.split(',').to_list()
    
    # make the pokemon type one hot encoded so the AI understand it
    df[poke_types] = 0
    for poke in pokedata_data:
        name = poke["name"]["english"].lower()
        for i in range(df.shape[0]):
            current_name = df.iloc[i]['details'].replace(", F", "").replace(", M", "").lower()
            if  name == current_name:
                df.loc[i, poke["type"]] = np.ones((len(poke["type"])))

    # normalize the health point and max hp
    df["condition"] = df["condition"].str.split("/").str[0].astype(int)
    df["condition"] = df["condition"] /  df["condition"].max()
    df["hp"] = 100 

    # transform the is active to int
    df["active"] = df["active"].astype(int)

    # replace none to 0
    df = df.replace("None", 0, regex=True)


    # change poke type in move collumn to integer (see later if sparse 1 or 0 value are better with relu)
    # to sparse
    key = []
    for col in key:
        move_type = [col + ptype for ptype in poke_types] 
        df[move_type] = 0
    
    for col in key:
        for i in range(df.shape[0]):
            df.loc[i, [col + df.iloc[i][col].replace(" ", "")]]  = 1

    # to int
    #for typeP in poke_types:
    #    df = df.replace(typeP, poke_types.index(typeP), regex=True)
    
    # drop useless column
    df.to_csv("data.csv")
    key = ["move_1", "move_2", "move_3", "move_4", "details", "item", "ability", "baseAbility", "ident", "pokeball", "moves", "move_1type", "move_2type", "move_3type", "move_4type"]
    df = df.drop(key, axis=1)

    # min max scalling of positive value (min must stay 0)
    df = df.fillna(0)
    key_min_max = ["stats.atk", "stats.def", "stats.spa", "stats.spd", "stats.spe"]
    for column in key_min_max:
        df[column] = df[column].astype(int)
        df[column] = df[column] / df[column].max()
    df.to_csv("state.csv")
    return df
    


