package jgrrw.painttheworld;

import android.support.v4.app.FragmentActivity;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.os.Bundle;
import android.graphics.Color;
import android.widget.TextView;
import android.widget.Toast;
import android.view.ViewGroup;
import android.util.Log;
import android.content.Intent;
import android.provider.Settings;
import android.Manifest;
import android.content.pm.PackageManager;

import java.util.TimerTask;
import java.util.Timer;
import java.util.List;
import java.util.ArrayList;

import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationListener;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.PolygonOptions;
import com.google.android.gms.maps.model.Polygon;

public class MapsActivity extends FragmentActivity implements
        OnMapReadyCallback, GoogleApiClient.ConnectionCallbacks,
        GoogleApiClient.OnConnectionFailedListener,
        com.google.android.gms.location.LocationListener{

    private GoogleMap mMap;
    private TimerTask timerTask;
    private Timer timer;
    private GoogleApiClient mGoogleApiClient;
    private android.location.Location mLastLocation;
    private static final String TAG = "MapsActivity";
    private LocationRequest locationRequest;
    private LocationListener locationListener;
    public static final int MY_PERMISSIONS_REQUEST_ACCESS_FINE_LOCATION = 0;
    private com.google.android.gms.location.FusedLocationProviderApi fusedLocationProviderApi;

    public String latitude_string = "";
    public String longitude_string = "";

    //This constant is how often the post to game_data occurs/main game logic loops
    public static final long GAME_LOOP_INCREMENT = 250;
    //Update location every 100 milliseconds
    public static final int LOCATION_INTERVAL = 100;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps);

        //Ask user for location permissions
        // Here, thisActivity is the current activity
        if (ContextCompat.checkSelfPermission(this,
                Manifest.permission.ACCESS_FINE_LOCATION)
                != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this,
                        new String[]{Manifest.permission.ACCESS_FINE_LOCATION},
                        MY_PERMISSIONS_REQUEST_ACCESS_FINE_LOCATION);
        }

        getLocation();

        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);

        final TextView textView = new TextView(this);


        timer = null;

        //Main game logic loop
        timerTask = new TimerTask() {

            @Override
            public void run() {
                //Put game logic here...like the posting to server/updates/whatever

            }
        };
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
        Log.d("LOCATION:", location.getLatitude() + ", " + location.getLongitude());
    }

    //Methods for connecting to Google Play Services API
    @Override
    public void onConnected(Bundle bundle) {
        try {
            fusedLocationProviderApi.requestLocationUpdates(mGoogleApiClient, locationRequest, this);
        } catch (SecurityException e) {
            Log.e("GET LOCATION", e.toString());
        }

        //Start main game logic loop
        timerStart();
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
    protected void onStart() {
        super.onStart();
    }

    @Override
    protected void onStop() {
        super.onStop();
        if (mGoogleApiClient.isConnected()) {
            mGoogleApiClient.disconnect();
        }
    }

    public void timerStart() {
        if(timer != null) {
            return;
        }
        timer = new Timer();
        timer.scheduleAtFixedRate(timerTask, 0, GAME_LOOP_INCREMENT);
    }

    public void timerStop() {
        timer.cancel();
        timer = null;
    }

    /**
     * Manipulates the map once available.
     * This callback is triggered when the map is ready to be used.
     * This is where we can add markers or lines, add listeners or move the camera. In this case,
     * we just add a marker near Sydney, Australia.
     * If Google Play services is not installed on the device, the user will be prompted to install
     * it inside the SupportMapFragment. This method will only be triggered once the user has
     * installed Google Play services and returned to the app.
     */
    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;
        mMap.setMapType(GoogleMap.MAP_TYPE_NORMAL);

        int choice = 1;
        LatLng InvertedFountainCenter = new LatLng(34.070098, -118.440700);
        LatLng DicksonCenter = new LatLng(34.072201, -118.442165);
        LatLng Battleground = new LatLng(0, 0);
        float zoomLevel = 19;
        switch (choice){
            case 0:
                Battleground = InvertedFountainCenter;
                zoomLevel = 19.6f;
                break;
            case 1:
                Battleground = DicksonCenter;
                zoomLevel = 19.1f;
                break;
        }
        mMap.addMarker(new MarkerOptions().position(Battleground).title("Center of battleground."));
        mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(Battleground, zoomLevel));
        mMap.getUiSettings().setScrollGesturesEnabled(false); //Disable camera movement
        mMap.getUiSettings().setZoomControlsEnabled(false); //Disable camera zoom? doesnt seem to work
        mMap.getUiSettings().setAllGesturesEnabled(false);
        mMap.getUiSettings().setRotateGesturesEnabled(false);

        String red = "#77FF0000";
        //Drawing a test rectangle
        double top_lat = Battleground.latitude + 0.0001;
        double bottom_lat = Battleground.latitude - 0.0001;
        double top_long = Battleground.longitude + 0.0001;
        double bottom_long = Battleground.longitude - 0.0001;

        PolygonOptions polygonOptions = new PolygonOptions()
                .add(new LatLng(top_lat, top_long), new LatLng(top_lat, bottom_long),
                        new LatLng(bottom_lat, bottom_long), new LatLng(bottom_lat, top_long))
                .strokeWidth(0)
                .fillColor(Color.parseColor(red));

        Polygon square = mMap.addPolygon(polygonOptions);
    }
}