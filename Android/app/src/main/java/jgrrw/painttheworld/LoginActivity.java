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

import org.json.*;

public class LoginActivity extends AppCompatActivity implements
        com.google.android.gms.location.LocationListener,
        GoogleApiClient.ConnectionCallbacks,
        GoogleApiClient.OnConnectionFailedListener{
    Button b1;
    TextView tx1;
    private GoogleApiClient mGoogleApiClient;
    private LocationRequest locationRequest;
    private LocationListener locationListener;
    public static final int MY_PERMISSIONS_REQUEST_ACCESS_FINE_LOCATION = 0;
    private com.google.android.gms.location.FusedLocationProviderApi fusedLocationProviderApi;
    private android.location.Location mLocation = new android.location.Location("");
    private boolean locationIsValid = false;

    public final static String USER_ID = "painttheworld.USER_ID";
    public static final int LOCATION_INTERVAL = 100;
    private static final String TAG = "LoginActivity";

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
        tx1.setText("\nHello!\n\nWelcome to\nPaintTheWorld!");
        mLocation.set(location);
        Log.d("LOCATION:", mLocation.getLatitude() + ", " + mLocation.getLongitude());
    }


    public void joinGame(View view) throws JSONException
    {
        if (!locationIsValid) {
            return;
        }
        ConnectionTask task = new ConnectionTask();
        String[] params = new String[2];
        params[0] = String.valueOf(mLocation.getLatitude());
        params[1] = String.valueOf(mLocation.getLongitude());
        task.execute(params);
        waitForGame();
    }

    private void waitForGame() {
        RequestQueue queue = Volley.newRequestQueue(this);
        String url ="http://ec2-54-153-39-233.us-west-1.compute.amazonaws.com/join_lobby";

        // Request a string response from the provided URL.
        JsonObjectRequest jsonRequest = new JsonObjectRequest(Request.Method.GET, url, null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        // Do stuff here, successful request
                        try {
                            String gameStartTime = response.getString("game_start_time");
                            String now = ISO8601.now();
                            Calendar gameStartCalendar = Calendar.getInstance();
                            Calendar nowCalendar = Calendar.getInstance();
                            try {
                                gameStartCalendar = ISO8601.toCalendar(gameStartTime);
                                nowCalendar = ISO8601.toCalendar(now);
                            } catch (ParseException e) {
                                //Handle error???
                            }

                            if (nowCalendar.after(gameStartCalendar)) {
                                //Go to MapsActivity
                            }
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
        queue.add(jsonRequest);
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


