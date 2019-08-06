package com.myapp.xkcd_finder

import Xkcd
import XkcdClient
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.util.Log
import android.view.View
import android.widget.Toast
import com.ablanco.zoomy.Zoomy
import com.squareup.picasso.Picasso
import kotlinx.android.synthetic.main.activity_main.*


class MainActivity : AppCompatActivity() {
    val xkcdClient = XkcdClient(this)
    val tracker = Tracker<Xkcd>()


    fun displayImgFromUrl(link: String) {
        Picasso.get().load(link).fit().into(imageView)
    }

    private fun makeZoomable(v: View) {
        val builder = Zoomy.Builder(this).enableImmersiveMode(false)
            .animateZooming(false)
            .target(imageView)
        builder.register()
    }


    private fun displayComic(xkcd: Xkcd) {
        comicTitle.visibility = View.VISIBLE
        urlDisplay.visibility = View.VISIBLE
        recommender.visibility = View.VISIBLE
        displayImgFromUrl(xkcd.link)
        setComicLink(xkcd.link)
        setComicTitle(xkcd.title)
    }

    private fun setComicLink(link: String) {
        urlDisplay.text = link
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        makeZoomable(imageView)

        submit.setOnClickListener {
            println("clicked")
            val query = getUserQuery()
            Log.i("query", query.length.toString())
            xkcdClient.search(listOf("query" to query)) { comics ->
                if (comics.isEmpty()) {
                    Toast.makeText(this, "Couldn't find any comics!", Toast.LENGTH_SHORT).show()
                }
                tracker.update(comics.toList())
                val currentComic = tracker.current()
                if (currentComic != null) {
                    displayComic(currentComic)
                }
                rerfreshTextView()

            }
        }
        back.setOnClickListener { goBack() }
        forward.setOnClickListener { goForward() }
    }

    private fun getUserQuery(): String {
        return floating_search_view.query
    }

    private fun rerfreshTextView() {
    }

    private fun goBack() {
        val prevComic = tracker.prev()
        if (prevComic != null) {
            displayComic(prevComic)
        }
    }

    private fun goForward() {
        val nextComic = tracker.next()
        if (nextComic != null) {
            displayComic(nextComic)
        }
    }

    private fun setComicTitle(title: String) {
        comicTitle.text = title
    }
}

