package ep.rest

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.TextView
import java.util.*

// iz seznama objektov povemo kako se posamezna vrstica prikaže
class BookAdapter(context: Context) : ArrayAdapter<Book>(context, 0, ArrayList()) {

    // position 0..1 kje v tem seznami risemo
    // view je listView je posamezna vrstica če ne obstaja jo naredimo z layoutInflatejrem
    override fun getView(position: Int, convertView: View?, parent: ViewGroup): View {
        // Check if an existing view is being reused, otherwise inflate the view
        val view = if (convertView == null)
            LayoutInflater.from(context).inflate(R.layout.booklist_element, parent, false)
        else
            convertView

        // dobimo text viewe
        val tvTitle = view.findViewById<TextView>(R.id.tvTitle)
        val tvAuthor = view.findViewById<TextView>(R.id.tvAuthor)
        val tvPrice = view.findViewById<TextView>(R.id.tvPrice)

        // dobimo knjigo
        val book = getItem(position)

        tvTitle.text = book?.title
        tvAuthor.text = book?.author
        tvPrice.text = String.format(Locale.ENGLISH, "%.2f EUR", book?.price)

        // lepše
        getItem(position)?.let {
            tvTitle.text = it.title
            tvAuthor.text = it.author
            tvPrice.text = String.format(Locale.ENGLISH, "%.2f EUR", it.price)
        }

        return view
    }
}
