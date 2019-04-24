package com.example.myapplication;

import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;


import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;

import android.os.Environment;
import android.provider.MediaStore;
import android.view.View;

import com.google.android.material.navigation.NavigationView;

import androidx.annotation.NonNull;
import androidx.core.view.GravityCompat;
import androidx.drawerlayout.widget.DrawerLayout;
import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import android.hardware.camera2.CameraDevice;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import org.w3c.dom.Text;

import java.io.File;
import java.io.FileOutputStream;

public class MainActivity extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener {
    ImageView imageView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
         super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);



        boolean check=checkCameraHardware(getApplicationContext());
        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.addDrawerListener(toggle);
        toggle.syncState();

        NavigationView navigationView = (NavigationView) findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);
        imageView = (ImageView)findViewById(R.id.imgView);
        Button btn= (Button)findViewById(R.id.button);
        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                File mediaFile =
                        new File(Environment.getExternalStorageDirectory().getAbsolutePath()
                                + "/myvideo.mp4");


                Uri videoUri = Uri.fromFile(mediaFile);
                Intent intent = new Intent(MediaStore.ACTION_VIDEO_CAPTURE);
//                intent.putExtra(MediaStore.EXTRA_OUTPUT, videoUri);
                if (intent.resolveActivity(getPackageManager()) != null) {
                    startActivityForResult(intent,
                            0);
                }
//                startActivityForResult(intent,0);
            }
        });
        System.out.println("In the end");
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {


        Toast.makeText(this, "Video saved to:\n" +
                data.getData(), Toast.LENGTH_LONG).show();
        System.out.println(data.getData());
        //        File file = new File();
//          Context context=getApplicationContext();
//          File directory=context.getFilesDir();
//          FileOutputStream outputStream;
//          System.out.println("Data===="+data);
//        try {
//            outputStream = openFileOutput(directory+"/vid1.mp4", Context.MODE_PRIVATE);
//            outputStream.write(data);
//            outputStream.close();
//        } catch (Exception e) {
//            e.printStackTrace();
//        }
//        System.out.println(directory);
//        System.out.println(directory);
//        System.out.println(directory);
//        System.out.println(directory);
//        System.out.println(directory);
//        System.out.println(directory);
//        System.out.println(directory);
//        super.onActivityResult(requestCode, resultCode, data);
//        Bitmap bitmap = (Bitmap)data.getExtras().get("data");
//        imageView.setImageBitmap(bitmap);
//        Uri videoUri = data.getData();
//        path = Utils.getRealPathFromURI(videoUri, this);
//        manageVideo(path);
    }
    /** Check if this device has a camera */
    private boolean checkCameraHardware(Context context) {
        if (context.getPackageManager().hasSystemFeature(PackageManager.FEATURE_CAMERA)){
            // this device has a camera
            System.out.println("This guy has camera!!!");
            return true;
        } else {
            // no camera on this device
            return false;
        }
    }

    public String getEmojiByUnicode(int unicode){
        return new String(Character.toChars(unicode));
    }

//    private boolean safeCameraOpen(int id) {
//        boolean qOpened = false;
//
//        try {
//            releaseCameraAndPreview();
//            camera = Camera.open(id);
//            qOpened = (camera != null);
//        } catch (Exception e) {
//            Log.e(getString(R.string.app_name), "failed to open Camera");
//            e.printStackTrace();
//        }
//
//        return qOpened;
//    }
//
//    private void releaseCameraAndPreview() {
//        preview.setCamera(null);
//        if (camera != null) {
//            camera.release();
//            camera = null;
//        }
//    }
    public void doSomething()
    {
        System.out.println("In DO SOMETHING");
        checkCameraHardware(getApplicationContext());
//        setContentView(R.layout.activity_main);
//        TextView txtV=(TextView) findViewById(R.id.textView2);
//        txtV.setText( getEmojiByUnicode(0x1F44C) );
//        System.out.println(7+8);
    }
    @Override
    public void onBackPressed() {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();

        if (id == R.id.nav_camera) {
            // Handle the camera action
        } else if (id == R.id.nav_gallery) {

        } else if (id == R.id.nav_slideshow) {

        } else if (id == R.id.nav_manage) {

        } else if (id == R.id.nav_share) {

        } else if (id == R.id.nav_send) {

        }

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }
}
