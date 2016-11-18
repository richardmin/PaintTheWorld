package jgrrw.painttheworld;

import android.support.v4.app.FragmentActivity;
import android.os.Bundle;
import android.graphics.Color;

import java.util.TimerTask;
import java.util.Timer;
import java.util.List;
import java.util.ArrayList;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.PolygonOptions;
import com.google.android.gms.maps.model.Polygon;

public class MapsActivity extends FragmentActivity implements OnMapReadyCallback {

    private GoogleMap mMap;
    private TimerTask timerTask;
    private Timer timer;

    //This constant is how often the post to game_data occurs/main game logic loops
    public static final long GAME_LOOP_INCREMENT = 250;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps);

        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);

        timer = null;
        //Main game logic loop
        timerTask = new TimerTask() {

            @Override
            public void run() {

            }
        };
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

        // TODO: Disable camera movement. Maybe by using Lite mode?
        // TODO: For Dickson court to work, landscape mode required. Is there a way to force this?
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
        /*
        for (int i = -5;  i < 5; i++) {
            PolylineOptions options = new PolylineOptions();
            options.add(new LatLng(top_lat, top_long));
            options.add(new LatLng(bottom_lat, bottom_long));
            top_lat += radius;
            bottom_lat += radius;
            mMap.addPolyline(options.width(3));

        }*/
        //Start main game logic loop
        timerStart();
    }
}