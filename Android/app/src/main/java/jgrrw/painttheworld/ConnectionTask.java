package jgrrw.painttheworld;

import android.os.AsyncTask;
import android.util.Log;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLEncoder;

public class ConnectionTask extends AsyncTask<String, Void, String> {


    @Override
    protected String doInBackground(String... params) {
        URL myUrl = null;
        HttpURLConnection conn = null;
        String response = "";
        String lat = params[0];
        String lon = params[1];

        try {
            myUrl = new URL("http://ec2-54-153-39-233.us-west-1.compute.amazonaws.com/join_lobby");
            conn = (HttpURLConnection) myUrl.openConnection();
            conn.setReadTimeout(10000);
            conn.setConnectTimeout(15000);
            conn.setRequestMethod("POST");
            conn.setDoInput(true);
            conn.setDoOutput(true);

            //one long string, first encode is the key to get the  data on your web
            //page, second encode is the value, keep concatenating key and value.
            //theres another ways which easier then this long string in case you are
            //posting a lot of info, look it up.
            String postData = URLEncoder.encode("lat", "UTF-8") + "=" +
                    URLEncoder.encode(lat, "UTF-8") + "&" +
                    URLEncoder.encode("long", "UTF-8") + "=" +
                    URLEncoder.encode(lon, "UTF-8");
            OutputStream os = conn.getOutputStream();

            BufferedWriter bufferedWriter = new BufferedWriter(new OutputStreamWriter(os, "UTF-8"));
            bufferedWriter.write(postData);
            bufferedWriter.flush();
            bufferedWriter.close();

            InputStream inputStream = conn.getInputStream();
            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream, "UTF-8"));
            String line = "";
            while ((line = bufferedReader.readLine()) != null) {
                response += line;
            }
            bufferedReader.close();
            inputStream.close();
            conn.disconnect();
            os.close();
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return response;
    }

    @Override
    protected void onPostExecute(String result) {
        //do what ever you want with the response

        Log.d("Result: ", result);
    }

}
