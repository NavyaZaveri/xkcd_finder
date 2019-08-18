import android.app.Activity
import android.util.Log
import android.widget.Toast
import com.github.kittinunf.fuel.core.Parameters
import com.github.kittinunf.fuel.httpGet
import com.github.kittinunf.fuel.json.responseJson
import com.github.kittinunf.result.Result
import com.google.gson.Gson


data class Xkcd(val id: Int, val content: String, val link: String, val title: String)


class XkcdClient(private val main: Activity) {
    private val API = "https://79fe3009.ngrok.io"


    fun search(p: Parameters, callback: (List<Xkcd>) -> Unit) {
        makeRequest("$API/search", p, callback)
    }


    private inline fun <reified T> makeRequest(url: String, p: Parameters, crossinline callback: (T) -> Unit) {
        buildPath(url, p)
            .httpGet()
            .responseJson { _, _, result ->
                when (result) {
                    is Result.Failure -> {
                        main.runOnUiThread {
                            Toast.makeText(main, "Oops, something went wrong!", Toast.LENGTH_LONG).show()
                        }
                    }
                    is Result.Success -> {
                        val json = result.get().obj()
                        Log.i("json", json.toString())
                        val res = deserialize<T>(json.get("results").toString())
                        main.runOnUiThread { callback(res) }
                    }
                }
            }
    }


    fun random(callback: (Xkcd) -> Unit) {
        makeRequest("$API/random", mutableListOf(), callback)
    }
}


private inline fun <reified T> deserialize(content: String): T {
    return Gson().fromJson(content, T::class.java)
}


/*
Hacky solution used as a drop-in replacement until https://github.com/kittinunf/fuel/issues/666 is fixed
 */
private fun buildPath(url: String, params: Parameters): String {
    var url = url
    if (params.isEmpty()) {
        return url
    }

    if (params.isNotEmpty()) {
        url += "?"
    }
    for ((p, v) in params) {
        url += "$p=$v&"
    }
    return url.substring(0, url.lastIndex)
}


