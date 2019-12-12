package fri.ep

import android.os.AsyncTask
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import android.util.Log
import kotlinx.android.synthetic.main.activity_main.*

class MainActivity : AppCompatActivity() {
    private val tag = MainActivity::class.java.canonicalName
    var task: MyAsyncTask? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        progressBar.max = 100

        btnStart.setOnClickListener {
            task = MyAsyncTask(this)
            task?.execute(50)
        }

        Log.i(tag, "Metode GUI poganja nit " + Thread.currentThread())
    }

    override fun onStop() {
        task?.cancel(true)
        task = null
        super.onStop()
    }


    class MyAsyncTask(val activity: MainActivity) : AsyncTask<Int, Double, Unit>() {
        val tag = MyAsyncTask::class.java.canonicalName

        override fun doInBackground(vararg params: Int?): Unit {
            for (i in 0 until params[0]!!) {
                if (isCancelled) {
                    break
                }

                simulateWork()
                publishProgress(i.toDouble() / params[0]!!.toDouble())
            }
        }

        override fun onProgressUpdate(vararg values: Double?) {
            // Log.i(tag, "Sporocamo napredek (${values[0]}) ... Nit = ${Thread.currentThread()}")
            activity.tvProgress.text = String.format("%.2f %%", values[0])
            activity.progressBar.progress = values[0]!!.toInt()
        }

        private fun simulateWork() {
            Log.i(tag, "Simuliramo opravilo ... čakamo 1 sekundo. Nit = ${Thread.currentThread()}")
            try {
                Thread.sleep(1000)
            } catch (e: InterruptedException) {
                Log.e(tag, "Interrupted", e)
            }
        }
    }

}
