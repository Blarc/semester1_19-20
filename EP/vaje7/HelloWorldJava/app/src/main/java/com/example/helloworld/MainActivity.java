package com.example.helloworld;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.util.Date;

public class MainActivity extends AppCompatActivity {

    private final static String TAG = MainActivity.class.getCanonicalName();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final EditText first = findViewById(R.id.firstEt);
        final EditText second = findViewById(R.id.secondEt);
        final Button button = findViewById(R.id.addBtn);
        final TextView textView = findViewById(R.id.resultTv);

        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final int a = Integer.parseInt(first.getText().toString());
                final int b = Integer.parseInt(second.getText().toString());

                final int result = a + b;

                textView.setText(String.valueOf(result));

            }
        });



    }
}
