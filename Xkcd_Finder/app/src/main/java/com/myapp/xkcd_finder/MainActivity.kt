package com.myapp.xkcd_finder

import XkcdClient
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.view.View
import android.widget.EditText
import android.widget.Toast
import com.squareup.picasso.Picasso
import kotlinx.android.synthetic.main.activity_main.*


class MainActivity : AppCompatActivity() {
    val xkcd_client = XkcdClient(this)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        submitButton.setOnClickListener {
            val query = getUserQuery()
            xkcd_client.search(listOf("query" to query)) { comics ->

                if (comics.size == 0) {
                    Toast.makeText(this, "Couldn't find any comics!", Toast.LENGTH_SHORT).show()
                }

                comics.forEach {
                    displayImgFromUrl(it.link)
                }
            }
            rerfreshTextView()
        }
    }


    fun displayImgFromUrl(link: String) {
        Picasso.with(this).load(link).into(imageView)
    }

    private fun getUserQuery(): String {
        return editText.text.toString()
    }


    private fun rerfreshTextView() {
        editText.setText("")
    }

    private fun setCurrent(link: String) {

    }

    private fun getPrevious(link: String) {

    }

    private fun getNext(link: String) {

    }

    private fun kaboom(v: View) {
        val editText = findViewById<EditText>(R.id.editText)
        val stuff = editText.text.toString()
        println(stuff)
    }
}



