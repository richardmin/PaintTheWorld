package jgrrw.painttheworld;

import android.content.pm.PackageManager;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import android.util.Log;
import android.view.View;
import java.util.Calendar;
import java.text.ParseException;

import android.widget.Button;
import android.widget.TextView;
import android.text.format.Time;
import android.icu.text.DateFormat;
import android.content.Intent;
import com.android.volley.*;
import com.android.volley.toolbox.*;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.location.LocationListener;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationServices;
import java.util.HashMap;
import android.os.Handler;
import java.lang.Runnable;

import org.json.*;

public class LoginActivity extends AppCompatActivity implements
        com.google.android.gms.location.LocationListener,
        GoogleApiClient.ConnectionCallbacks,
        GoogleApiClient.OnConnectionFailedListener{
    Button b1;
    View b;
    TextView tx1;
    private GoogleApiClient mGoogleApiClient;
    private LocationRequest locationRequest;
    private LocationListener locationListener;
    public static final int MY_PERMISSIONS_REQUEST_ACCESS_FINE_LOCATION = 0;
    private com.google.android.gms.location.FusedLocationProviderApi fusedLocationProviderApi;
    private android.location.Location mLocation = new android.location.Location("");
    private boolean locationIsValid = false;
    private boolean buttonVisible = false;
    private Handler pollingHandler = new Handler();
    private Calendar gameStartCalendar;
    private Calendar nowCalendar;
    private Intent switchToMaps;
    private int user_id;
    private String gameStartTime;

    public final static String USER_ID = "painttheworld.USER_ID";
    public final static String GAME_ISO_TIME = "painttheworld.GAME_ISO_TIME";
    public static final int LOCATION_INTERVAL = 100;
    private static final String TAG = "LoginActivity";

    final Runnable pollServerForStartTime = new Runnable() {
        public void run() {
            waitForGame();
            pollingHandler.postDelayed(pollServerForStartTime, 1400);
        }
    };
    final Runnable pollToSeeIfGameHasStarted = new Runnable() {
        public void run() {
            String now = ISO8601.now();
            try {
                nowCalendar = ISO8601.toCalendar(now);
            } catch (ParseException e) {
                e.printStackTrace();
            }
            if (nowCalendar.after(gameStartCalendar)) {
                //Go to MapsActivity
                switchToMaps = new Intent(LoginActivity.this, MapsActivity.class);
                switchToMaps.putExtra(USER_ID, user_id);
                switchToMaps.putExtra(GAME_ISO_TIME, gameStartTime);
                startActivity(switchToMaps);
                pollingHandler.removeCallbacks(pollToSeeIfGameHasStarted);
            }
            else {
                pollingHandler.postDelayed(pollToSeeIfGameHasStarted, 500);
            }
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);


        //Get location
        if (ContextCompat.checkSelfPermission(this,
                android.Manifest.permission.ACCESS_FINE_LOCATION)
                != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this,
                    new String[]{android.Manifest.permission.ACCESS_FINE_LOCATION},
                    MY_PERMISSIONS_REQUEST_ACCESS_FINE_LOCATION);
        }
        getLocation();

        b1 = (Button) findViewById(R.id.JoinButton);
        b = findViewById(R.id.JoinButton);
        tx1 = (TextView) findViewById(R.id.AboutText);
        tx1.setTextSize(30);
        tx1.setText("Loading...");
    }

    //Methods for Google Play Services Location
    private void getLocation() {
        locationRequest = LocationRequest.create();
        locationRequest.setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY);
        locationRequest.setInterval(LOCATION_INTERVAL);
        locationRequest.setFastestInterval(LOCATION_INTERVAL);
        fusedLocationProviderApi = LocationServices.FusedLocationApi;
        mGoogleApiClient = new GoogleApiClient.Builder(this)
                .addApi(LocationServices.API)
                .addConnectionCallbacks(this)
                .addOnConnectionFailedListener(this)
                .build();
        if (mGoogleApiClient != null) {
            mGoogleApiClient.connect();
        }
    }

    @Override
    public void onLocationChanged(android.location.Location location) {
        locationIsValid = true;
        if (!buttonVisible) {
            b.setVisibility(View.VISIBLE);
            buttonVisible = true;
        }
        tx1.setText("\nHello!\n\nWelcome to\nPaintTheWorld!");
        mLocation.set(location);
        Log.d("LOCATION:", mLocation.getLatitude() + ", " + mLocation.getLongitude());
    }


    public void joinGame(View view) throws JSONException
    {
        if (!locationIsValid) {
            return;
        }
        final String URL = "http://ec2-54-153-39-233.us-west-1.compute.amazonaws.com/join_lobby";
        // Post params to be sent to the server
        HashMap<String, Double> params = new HashMap<String, Double>();
        params.put("lat", mLocation.getLatitude());
        params.put("long", (mLocation.getLongitude()));

        JsonObjectRequest req = new JsonObjectRequest(URL, new JSONObject(params),
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            user_id = response.getInt("user-id");
                            if (user_id != -1) {
                                pollingHandler.post(pollServerForStartTime);
                            }
                            else {
                                Log.d("User_id", String.valueOf(user_id));
                                tx1.setText("Please try again later.");
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
            }
        });

        // add the request object to the queue to be executed
        ApplicationController.getInstance().addToRequestQueue(req);
    }

    private void waitForGame() {
        b.setVisibility(View.GONE);
        RequestQueue queue = Volley.newRequestQueue(this);
        String url ="http://ec2-54-153-39-233.us-west-1.compute.amazonaws.com/join_lobby";

        // Request a string response from the provided URL.
        JsonObjectRequest jsonRequest = new JsonObjectRequest(Request.Method.GET, url, null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        // Do stuff here, successful request
                        try {
                            if (!response.has("game-start-time")) {
                                Log.d("Continuing to poll", "hi");
                                return;
                            }
                            pollingHandler.removeCallbacks(pollServerForStartTime);
                            gameStartTime = response.getString("game-start-time");
                            String now = ISO8601.now();
                            gameStartCalendar = Calendar.getInstance();
                            nowCalendar = Calendar.getInstance();
                            try {
                                gameStartCalendar = ISO8601.toCalendar(gameStartTime);
                                nowCalendar = ISO8601.toCalendar(now);
                            } catch (ParseException e) {
                                //Handle error???
                            }
                            pollingHandler.post(pollToSeeIfGameHasStarted);

                        } catch (JSONException e) {
                            //idk but it died
                            e.printStackTrace();
                        }
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                // Unsuccessful request.
            }
        });
        // Add the request to the RequestQueue.
        ApplicationController.getInstance().addToRequestQueue(jsonRequest);
    }

    //Methods for connecting to Google Play Services API
    @Override
    public void onConnected(Bundle bundle) {
        try {
            fusedLocationProviderApi.requestLocationUpdates(mGoogleApiClient, locationRequest, this);
        } catch (SecurityException e) {
            Log.e("GET LOCATION ERROR", e.toString());
        }
    }

    @Override
    public void onConnectionSuspended(int i) {
        Log.i(TAG, "Connection Suspended");
        mGoogleApiClient.connect();
    }

    @Override
    public void onConnectionFailed(ConnectionResult connectionResult) {
        Log.i(TAG, "Connection failed. Error: " + connectionResult.getErrorCode());
    }

    @Override
    protected void onStop() {
        super.onStop();
        if (mGoogleApiClient.isConnected()) {
            mGoogleApiClient.disconnect();
        }
    }


}


