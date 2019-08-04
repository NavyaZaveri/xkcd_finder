import android.app.Activity
import android.util.Log
import com.github.kittinunf.fuel.core.Parameters
import com.github.kittinunf.fuel.httpGet
import com.github.kittinunf.fuel.json.FuelJson
import com.github.kittinunf.fuel.json.responseJson
import com.github.kittinunf.result.Result
import com.google.gson.Gson


class XkcdClient(val main: Activity) {
    val API = "https://c7eb1043.ngrok.io"

    fun get_random_comic(p: Parameters = mutableListOf(), callback: (Array<Xkcd>) -> Unit) {
        makeRequest(API, p, callback)
    }

    fun get_all_comics(p: Parameters = mutableListOf(), callback: (Array<Xkcd>) -> Unit) {
        makeRequest("$API/all", p, callback)
    }


    fun search(p: Parameters, callback: (Array<Xkcd>) -> Unit) {
        makeRequest("$API/search", p, callback)
    }


    private inline fun <reified T> makeRequest(url: String, p: Parameters, crossinline callback: (T) -> Unit) {
        buildPath(url, p)
            .httpGet(mutableListOf())
            .responseJson { _, _, result ->
                when (result) {
                    is Result.Failure -> {
                        Log.i("", "whoops!")
                    }
                    is Result.Success -> runCallbackOn(result, callback)
                }
            }
    }

    inline fun <reified T> runCallbackOn(
        successfulResponse: Result.Success<FuelJson, *>,
        crossinline callback: (T) -> Unit
    ) {
        val json = successfulResponse.get().obj()
        Log.i("json", json.toString())
        val res = deserialize<T>(json.get("results").toString())
        main.runOnUiThread {
            callback(res)
        }
    }
}

inline fun <reified T> deserialize(content: String): T {
    return Gson().fromJson(content, T::class.java)
}


data class Xkcd(val id: Int, val content: String, val link: String, val title: String)


fun buildPath(url: String, params: Parameters): String {
    var url = url
    if (params.isNotEmpty()) {
        url += "?"

    }
    for ((p, v) in params) {
        url += "$p=$v&"
    }

    //remove the trailing &'
    return url.substring(0, url.lastIndex)
}


