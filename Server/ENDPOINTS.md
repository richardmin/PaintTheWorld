Endpoints: 

1. debug 
    * GET only, renders debug data

2. game_data
    * POST only, send GPS coordinates here, it returns grid deltas. Also include your user id, and your game id
        * Example Input: {user: 1, game: 1, lat: 38.8719, long: 77.0563}

3. join_lobby
    * POST sends a request to join the lobby, user-id (yours), as well as the remainder of the GET data 
    * GET should returns game_start_time in ISO 8601, if the game is starting. It will also have the central GPS location. 
    * Note if there is a game in progress, or the users are already maxed out we return an error in the format. What this effectively means is that you get user-id is -1 and not anything.
    * Note if there is a game in progress, or the users are already maxed out we return an error in the format. What this effectively means is that you get user-id is -1 and not anything. 
    * To speed up development, we'll do our lobby joining process through a web-page.
