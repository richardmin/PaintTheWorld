package jgrrw.painttheworld;

import android.graphics.Color;
import android.os.Bundle;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

public class GameOverActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_game_over);

        Intent intent = getIntent();
        String gameEndStatus = intent.getStringExtra(MapsActivity.GAME_END_STATUS);
        int redScore = intent.getExtras().getInt(MapsActivity.RED_TEAM_SCORE);
        int blueScore = intent.getExtras().getInt(MapsActivity.BLUE_TEAM_SCORE);
        TextView gameEnd = (TextView) findViewById(R.id.WhoWon);
        TextView redScoreText = (TextView) findViewById(R.id.RedScore);
        TextView blueScoreText = (TextView) findViewById(R.id.BlueScore);
        TextView redScoreTextHeader = (TextView) findViewById(R.id.RedScoreHeader);
        TextView blueScoreTextHeader = (TextView) findViewById(R.id.BlueScoreHeader);


        gameEnd.setTextSize(40);
        gameEnd.setText(gameEndStatus);

        redScoreText.setText(String.valueOf(redScore));
        blueScoreText.setText(String.valueOf(blueScore));
        // setPadding(left, top, right, bottom);
        redScoreText.setPadding(0, 300, 400, 100);
        blueScoreText.setPadding(400, 300, 0, 100);
        redScoreText.setTextColor(Color.parseColor("#FF0000"));
        blueScoreText.setTextColor(Color.parseColor("#0000FF"));

        redScoreTextHeader.setText("Red Score");
        blueScoreTextHeader.setText("Blue Score");
        redScoreTextHeader.setPadding(0, 200, 400, 100);
        blueScoreTextHeader.setPadding(400, 200, 0, 100);

    }
}
