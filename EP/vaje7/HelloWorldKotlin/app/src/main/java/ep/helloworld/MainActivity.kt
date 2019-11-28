package ep.helloworld

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle

import kotlinx.android.synthetic.main.activity_main.*

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        addBtn.setOnClickListener {
            val a = firstEt.text.toString().toIntOrNull() ?: 0
            val b = secondEt.text.toString().toIntOrNull() ?: 0
            val result = a + b

            resultTv.text = result.toString()
        }


    }
}
