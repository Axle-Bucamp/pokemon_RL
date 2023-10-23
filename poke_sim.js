const Sim = require('pokemon-showdown');
const WebSocket = require("ws");

stream = new Sim.BattleStream();

// get the next move and send it to python via socket
const wss = new WebSocket.Server({ port: 9898 });

wss.on("connection", ws => {
    console.log("New player connected!");
    
    ws.on("message", (event) => {
        console.log("Message from client ", event.toString());
        stream.write(event.toString("utf8"))
    });
    
    ws.on("close", () => {
       console.log("player has disconnected!");
    });

});

(async () => {
    for await (const output of stream) {
        console.log(output);
        wss.clients.forEach(client => client.send(output));
    }
})();

// define a function to get the json request after move

stream.write(`>start {"formatid":"gen7randombattle"}`);