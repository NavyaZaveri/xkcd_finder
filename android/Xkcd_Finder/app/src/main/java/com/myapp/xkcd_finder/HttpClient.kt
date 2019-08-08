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
    private val API = "https://34379f3f.ngrok.io"

    fun search(p: Parameters, callback: (Array<Xkcd>) -> Unit) {
        makeRequest("$API/search", p, callback)
    }

    private inline fun <reified T> makeRequest(url: String, p: Parameters, crossinline callback: (T) -> Unit) {
        buildPath(url, p)
            .httpGet()
            .responseJson { _, _, result ->
                when (result) {
                    is Result.Failure -> {
                        Log.i("failed", "request failed")
                        main.runOnUiThread {
                            Toast.makeText(
                                main,
                                "Request Failed!",
                                Toast.LENGTH_LONG
                            ).show()
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
}

inline fun <reified T> deserialize(content: String): T {
    return Gson().fromJson(content, T::class.java)
}

fun buildPath(url: String, params: Parameters): String {
    var url = url

    if (params.isNotEmpty()) {
        url += "?"
    }
    for ((p, v) in params) {
        url += "$p=$v&"
    }
    return url.substring(0, url.lastIndex)
}


