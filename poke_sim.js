const Sim = require('pokemon-showdown');
const WebSocket = require("ws");
// import {Dex, BattleStreams, RandomPlayerAI, Teams} from '@pkmn/sim';

stream = new Sim.BattleStream();
// get the next move and send it to python via socket
const wss = new WebSocket.Server({ port: 9898 });

wss.on("connection", ws => {
    console.log("New player connected!");
    
    ws.on("message", (event) => {
        console.log("Message from client ", event.toString());
        if (event.toString().includes("request")){
            
            if (event.toString().includes("p1")){
                const team = JSON.stringify(stream.battle.sides[0].getRequestData(true)['pokemon']);
                ws.send(team.toString());
            }else{

                const team = JSON.stringify(stream.battle.sides[1].getRequestData(true)['pokemon']);
                ws.send(team.toString());
            }
        }else{
            stream.write(event.toString("utf8"));
        }
    });
    
    ws.on("close", () => {
       console.log("player has disconnected!");
    });

});

(async () => {
    for await (const output of stream) {   
        // sometime cause trouble with fainted poke 
        if(output.includes("error")){
            wss.clients.forEach(client => client.send("error"));
        }else{
            wss.clients.forEach(client => client.send("ok"));
        }
        console.log(output);
    }
})();

// define a function to get the json request after move
console.log("|error|[Invalid choice] Can't switch: You can't switch to a fainted Pokémon".includes("error"))
stream.write(`>start {"formatid":"gen7randombattle"}`);