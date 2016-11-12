Endpoints: 

debug 
* GET only, renders debug data
game_data
* POST only, send GPS coordinates here, it returns grid deltas. Also include your user id, and your game id
** Example Input: {user: 1, game: 1, lat: 38.8719, long: 77.0563}
join_lobby
* POST sends a request to join the lobby, lobby id and user id returned
* GET should include your lobby id and user id, and will return your lobby status (whether the game should start, and if so, when)
* Note if there is a game in progress, or the users are already maxed out we return an error in the format
