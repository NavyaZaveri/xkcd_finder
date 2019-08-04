package com.myapp.xkcd_finder

import XkcdClient
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.view.MotionEvent
import android.widget.Toast
import com.github.pwittchen.swipe.library.rx2.Swipe
import com.squareup.picasso.Picasso
import kotlinx.android.synthetic.main.activity_main.*


class MainActivity : AppCompatActivity() {
    val xkcdClient = XkcdClient(this)
    val tracker = Tracker<String>()
    val swipe = Swipe()

    fun displayImgFromUrl(link: String) {
        Picasso.with(this).load(link).into(imageView)
    }


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        submitButton.setOnClickListener {
            val query = getUserQuery()
            xkcdClient.search(listOf("query" to query)) { comics ->
                if (comics.isEmpty()) {
                    Toast.makeText(this, "Couldn't find any comics!", Toast.LENGTH_SHORT).show()
                }
                tracker.update(comics.map { it.link })
                val link = tracker.current()
                displayImgFromUrl(link)
            }
        }

        back.setOnClickListener {
            goBack()
        }
    }

    private fun getUserQuery(): String {
        return editText.text.toString()
    }


    private fun rerfreshTextView() {
        editText.setText("")
    }

    private fun goBack() {
        val prevComicLink = tracker.prev()
        displayImgFromUrl(prevComicLink)

    }

    private fun goForward() {
        val nextComicLink = tracker.next()
        displayImgFromUrl(nextComicLink)

    }

    override fun dispatchTouchEvent(event: MotionEvent): Boolean {
        return super.dispatchTouchEvent(event)
    }
}



