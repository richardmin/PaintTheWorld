Endpoints: 

debug 
* GET only, renders debug data
game_data
* POST only, send GPS coordinates here, it returns grid deltas.
join_lobby
* POST sends a request to join the lobby, lobby id and user id returned
* GET should include your lobby id and user id, and will return your lobby status (whether the game should start, and if so, when)

