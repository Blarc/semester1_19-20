package ep.ws

import android.os.AsyncTask
import android.os.Bundle
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_main.*
import org.json.JSONObject
import java.lang.Exception
import java.net.HttpURLConnection
import java.net.URL
import java.util.*

class MainActivity : AppCompatActivity() {
    companion object {
        private const val API_KEY = ""
        const val WS_URL = "https://www.omdbapi.com/?s=%s&apikey=$API_KEY"
        val TAG: String = MainActivity::class.java.canonicalName!!
    }

    var task: LookUp? = null

    override fun onStop() {
        task?.cancel(true)
        task = null
        super.onStop()
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        search_btn.setOnClickListener {
            Log.i(TAG, "Searching ...")
            task = LookUp(this)
            task?.execute(query.text.toString())
            query.setText("")
        }
    }

    class LookUp(val activity: MainActivity) : AsyncTask<String, Unit, JSONObject>() {
        override fun doInBackground(vararg params: String?): JSONObject {
            try {
                val url = URL(String.format(WS_URL, params[0]))
                // as == CASTING
                val conn = url.openConnection() as HttpURLConnection


                // krajse
                conn.apply {
                    doInput = true
                    requestMethod = "GET"
                    setRequestProperty("accept", "application/json")
                }

                // conn.doInput = true
                // conn.requestMethod = "GET"
                // conn.setRequestProperty("accept", "application/json")

                val scanner = Scanner(conn.inputStream).useDelimiter("\\A")
                return if (scanner.hasNext()) {
                    JSONObject(scanner.next())
                } else {
                    JSONObject()
                }

            } catch (e: Exception) {
                Log.w(TAG, "Exception: ${e.localizedMessage}")
                return JSONObject()
            }
        }

        override fun onPostExecute(result: JSONObject) {
            // Log.i(TAG, "Rezultat: ${result.toString(2)}")
            activity.results.text = result.toString(2)
        }
    }
}
