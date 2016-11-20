Endpoints: 

1. debug 
    * GET only, renders debug data

2. game_data
    * POST only, send GPS coordinates here, it returns grid deltas. 
        * Input Keys: user-id, lat, long. 
        * Please ensure that the lat and long degrees have no extra markings (i.e. they're just raw numbers. Do _NOT_ include °N, for example.)

3. join_lobby
    * POST sends a request to join the lobby, user-id (yours), as well as the remainder of the GET data 
    * GET should returns game_start_time in ISO 8601, if the game is starting. It will also have the central GPS location. 
    * Note if there is a game in progress, or the users are already maxed out we return an error in the format. What this effectively means is that you get user-id is -1 and not anything.


How to format data
In general, to send data we need the INTERNET permission. 
Add android.permission.INTERNET to the app manifest.

1. HTTP GET: 
    *   To make a GET request, you put parameters in the URL after the endpoint such as: ?field=value&field2=value2 à la youtube

        We shouldn't be using this at all, so you don't need the ? and things afterwards.
    
        In Android, this looks like (on the join_lobby endpoint)
        ```
        RequestQueue queue = Volley.newRequestQueue(this);
        String url ="http://our_url.com/join_lobby";

        // Request a string response from the provided URL.
        StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
                    new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
                // Do stuff here, successful request
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                // Unsuccessful request. 
            }
        });
        // Add the request to the RequestQueue.
        queue.add(stringRequest);
        ```

        Read more here: https://developer.android.com/training/volley/simple.html
2. HTTP POST:
    *   To make a POST request, you need to place the parameters in the body. Android volley will manage this for you.

        If you are interested in how the raw binary data is formatted, How post requests are formatted: http://stackoverflow.com/questions/14551194/how-are-parameters-sent-in-an-http-post-request is a good resource.

        In Android this looks like (on the join_lobby endpoint)
        ```
        RequestQueue queue = Volley.newRequestQueue(this);
        String url ="http://our_url.com/join_lobby";

        final JSONObject jsonBody = new JSONObject("{\"type\":\"example\"}");
        // Request a string response from the provided URL.
        JsonObjectRequest jsonRequest = new JsonObjectRequest(url, jsonBody
                    new Response.Listener<JsonObject>() {
            @Override
            public void onResponse(String response) {
                // Do stuff here, successful request
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                // Unsuccessful request. 
            }
        });
        // Add the request to the RequestQueue.
        queue.add(stringRequest);
        ```

3. Json Data:
    *   This is placed in the body of the data. It looks like a dict or map, with keys and values.

        For example, it looks like {key: value}, where value can be an integer, array, json object, or string.

        More information on json.org for the format precise specifications. How we are going to use it in the project is a non-string delimited key along with the data.

        For example {error: 'invalid parameter'}.

        To parse a JSON request in Android, you can simply use the JSONObject

        ``` JSONObject obj = new JSONObject(string); ``` 

        To access data in JSONObject, take the appropriate type. 

        ``` String jsonString = obj.getString("stringkey"); ```
        ``` boolean jsonBoolean = obj.getBoolean("booleankey"); ```
        ``` int jsonInt = obj.getInt("intkey"); ```
        ``` JSONArray jsonArray = obj.getJSONArray("arraykey"); ```

        More info here: http://stackoverflow.com/questions/9605913/how-to-parse-json-in-android
