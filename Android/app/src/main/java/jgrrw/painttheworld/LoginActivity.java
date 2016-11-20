package jgrrw.painttheworld;

import android.*;
import android.content.pm.PackageManager;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import java.util.Map;
import java.util.HashMap;

import android.widget.Button;
import android.widget.TextView;
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
        tx1.setText("\nHello!\n\nWelcome to\nPaintTheWorld!");
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
        mLocation.set(location);
        Log.d("LOCATION:", mLocation.getLatitude() + ", " + mLocation.getLongitude());
    }

    public void joinGame(View view) throws JSONException
    {
        RequestQueue queue = Volley.newRequestQueue(this);
        String url ="http://ec2-54-153-39-233.us-west-1.compute.amazonaws.com/join_lobby";
        Map<String, String> jsonParams = new HashMap<String, String>();

        jsonParams.put("lat", String.valueOf(mLocation.getLatitude()));
        jsonParams.put("long", String.valueOf(mLocation.getLongitude()));

        JsonObjectRequest postRequest = new JsonObjectRequest( Request.Method.POST, url,

                new JSONObject(jsonParams),
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        Integer UserID = 0;
                        try {
                            UserID = response.getInt("user-id");
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                        tx1.setText("Joining game: Welcome User " + UserID.toString());
                        if (UserID != -1) {
                            Intent intent = new Intent(LoginActivity.this, MapsActivity.class);
                            intent.putExtra(USER_ID, UserID);
                            //poll until game is ready to start
                            startActivity(intent);
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        tx1.setText("Post unsuccessful, please try again.");
                    }
                }) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<String, String>();
                headers.put("Content-Type", "application/json; charset=utf-8");
                headers.put("User-agent", System.getProperty("http.agent"));
                return headers;
            }
        };
        queue.add(postRequest);
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


