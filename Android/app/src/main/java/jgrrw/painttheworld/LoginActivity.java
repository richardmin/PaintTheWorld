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

    public void joinGame(View view) throws JSONException {
        String UserLocationLat = Double.toString(34.070098);
        String UserLocationLong = Double.toString(-118.440700); //Testing Inverted Fountain Coordinates

        ConnectionTask task = new ConnectionTask();
        String[] params = new String[2];
        params[0] = UserLocationLat;
        params[1] = UserLocationLong;
        task.execute(params);
    }


}


