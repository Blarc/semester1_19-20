package fri.ep

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import android.view.View
import android.widget.Button
import kotlinx.android.synthetic.main.activity_main.*

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }

    fun addNumber(view: View) {
        val b = view as Button
        val currentValue = textView.text.toString()
        val newValue = currentValue + b.text.toString()

        textView.text = newValue
    }

    fun clear(view: View) {
        textView.text = ""
    }
}
