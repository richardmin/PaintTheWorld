package jgrrw.painttheworld;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.view.View;

import android.widget.Button;
import android.widget.TextView;
import android.content.Intent;
import com.android.volley.*;
import com.android.volley.toolbox.*;
import org.json.*;

public class LoginActivity extends AppCompatActivity {
    Button b1;
    TextView tx1;
    public final static String USER_ID = "painttheworld.USER_ID";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        b1 = (Button) findViewById(R.id.JoinButton);
        tx1 = (TextView) findViewById(R.id.AboutText);
        tx1.setText("Hello, welcome to PaintTheWorld!");
    }

    public void joinGame(View view) throws JSONException
    {
        RequestQueue queue = Volley.newRequestQueue(this);
        String url ="http://our_url.com/join_lobby";

        try {
            final JSONObject jsonBody = new JSONObject("{\"lat\":\"37.014298129\", \"long\":\"50.0:w\"}");
            // Request a string response from the provided URL.
            JsonObjectRequest jsonRequest = new JsonObjectRequest(url, jsonBody,
            new Response.Listener<JSONObject>() {

                @Override
                public void onResponse(JSONObject response) {
                    // Do stuff here, successful request
                    try {
                        int UserID = response.getInt("user-id");
                        if (UserID != -1) {
                            Intent intent = new Intent(LoginActivity.this, MapsActivity.class);
                            intent.putExtra(USER_ID, UserID);
                            startActivity(intent);
                        }
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }
            }, new Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError error) {
                    // Unsuccessful request.
                    tx1.setText("Join unsuccessful, please try again.");
                }
            });
            // Add the request to the RequestQueue.
            queue.add(jsonRequest);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
}


