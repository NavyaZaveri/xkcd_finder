package com.myapp.xkcd_finder

import Xkcd
import XkcdClient
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.view.View
import android.widget.Toast
import com.ablanco.zoomy.Zoomy
import com.squareup.picasso.Picasso
import kotlinx.android.synthetic.main.activity_main.*

class MainActivity : AppCompatActivity() {
    private val xkcdClient = XkcdClient(this)
    private val tracker = Tracker<Xkcd>()


    private fun displayImgFromUrl(link: String) {
        Picasso.get().load(link).fit().into(comicImg)
    }

    private fun makeZoomable(v: View) {
        val builder = Zoomy.Builder(this)
                .target(v)
                .enableImmersiveMode(false)
                .animateZooming(false)

        builder.register()
    }

    private fun makeVisible(vararg views: View) {
        views.forEach { it.visibility = View.VISIBLE }
    }

    private fun displayComic(xkcd: Xkcd) {
        makeVisible(comicImg, comicTitle, comicUrl, randomComicButton)
        displayImgFromUrl(xkcd.link)
        comicUrl.text = xkcd.link
        comicTitle.text = xkcd.title
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        makeZoomable(comicImg)

        submit.setOnClickListener {
            val query = getSearchQuery()
            xkcdClient.search(listOf("query" to query)) { comics ->
                if (comics.isEmpty()) {
                    Toast.makeText(this, "Couldn't find any comics!", Toast.LENGTH_SHORT).show()
                }
                tracker.update(comics.toList())
                val currentComic = tracker.current()
                if (currentComic != null) {
                    displayComic(currentComic)
                }
            }
        }
        back.setOnClickListener { goBack() }
        forward.setOnClickListener { goForward() }

        xkcdClient.random { tracker.update(listOf(it)); displayComic(it) }

        randomComicButton.setOnClickListener {
            xkcdClient.random { xkcd ->
                tracker.update(listOf(xkcd)); displayComic(xkcd)
            }
        }
    }

    private fun getSearchQuery(): String {
        return floating_search_view.query
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
}

