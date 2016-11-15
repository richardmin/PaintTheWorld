package jgrrw.painttheworld;

import android.support.v4.app.FragmentActivity;
import android.os.Bundle;
import android.view.View;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import android.content.Intent;

public class MapsActivity extends FragmentActivity implements OnMapReadyCallback {
    public final static String GAME_END_STATUS = "painttheworld.GAME_END_STATUS";
    public final static String RED_TEAM_SCORE = "painttheworld.RED_TEAM_SCORE";
    public final static String BLUE_TEAM_SCORE = "painttheworld.BLUE_TEAM_SCORE";
    private GoogleMap mMap;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps);
        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);
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
        mMap.setMapType(GoogleMap.MAP_TYPE_HYBRID);

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
    }

    /**
     * Prepares data to be displayed in GameOverActivity and changes to GameOverActivity
     * @param view
     */
    public void gameOver(View view){
        Intent intent = new Intent(this, GameOverActivity.class);
        //TODO: Get meaningful end game status from server. Possibly score as well?
        //Current it just puts some meaningless placeholders
        String status = "Victory!";
        intent.putExtra(GAME_END_STATUS, status);
        intent.putExtra(RED_TEAM_SCORE, 100);
        intent.putExtra(BLUE_TEAM_SCORE, 150);
        startActivity(intent);
    }
}