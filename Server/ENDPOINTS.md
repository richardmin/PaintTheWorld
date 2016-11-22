Endpoints: 

1. debug 
    * GET only, renders debug data

2. game_data
    * POST only, send GPS coordinates here, it returns grid deltas. 
        * Input Keys: user-id, lat, long. How post requests are formatted: http://stackoverflow.com/questions/14551194/how-are-parameters-sent-in-an-http-post-request
        * Please ensure that the lat and long degrees have no extra markings (i.e. they're just raw numbers. Do _NOT_ include °N, for example.)

3. join_lobby
    * POST sends a request to join the lobby, user-id (yours), as well as the remainder of the GET data 
    * GET should returns game_start_time in ISO 8601, if the game is starting. It will also have the central GPS location. 
    * Note if there is a game in progress, or the users are already maxed out we return an error in the format. What this effectively means is that you get user-id is -1 and not anything.
    * To speed up development, we'll do our lobby joining process through a web-page.
