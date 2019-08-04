package com.myapp.xkcd_finder

import XkcdClient
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.util.Log
import android.widget.Toast
import com.squareup.picasso.Picasso
import kotlinx.android.synthetic.main.activity_main.*


class MainActivity : AppCompatActivity() {
    val xkcdClient = XkcdClient(this)
    val tracker = Tracker<String>()

    fun displayImgFromUrl(link: String) {
        Picasso.get().load(link).into(imageView)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        submitButton.setOnClickListener {
            val query = getUserQuery()
            Log.i("query", query.length.toString())
            xkcdClient.search(listOf("query" to query)) { comics ->
                if (comics.isEmpty()) {
                    Toast.makeText(this, "Couldn't find any comics!", Toast.LENGTH_SHORT).show()
                }
                tracker.update(comics.map { it.link })
                val link = tracker.current()
                if (link != null)
                    displayImgFromUrl(link)
                rerfreshTextView()
            }
        }

        back.setOnClickListener {
            goBack()
        }
        forward.setOnClickListener {
            goForward()
        }
    }

    private fun getUserQuery(): String {
        return editText.text.toString().trim()
    }

    private fun rerfreshTextView() {
        editText.setText("")
    }

    private fun goBack() {
        val prevComicLink = tracker.prev()
        if (prevComicLink != null) {
            displayImgFromUrl(prevComicLink)
        }
    }

    private fun goForward() {
        val nextComicLink = tracker.next()
        if (nextComicLink != null) {
            displayImgFromUrl(nextComicLink)
        }
    }
}



