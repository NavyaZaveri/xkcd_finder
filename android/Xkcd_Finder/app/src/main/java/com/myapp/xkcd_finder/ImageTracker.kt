package com.myapp.xkcd_finder

class Tracker<T : Comparable<T>> {
    var current = -1
    val images = mutableListOf<T>()
    val seen = mutableListOf<T>()

    fun next(): T {
        if (current <= images.size - 2) {
            return images[current + 1].also { current += 1 }

        } else {
            return images.last()
        }
    }

    fun prev(): T {
        if (current == 0) {
            return images[current]
        }
        return images[current - 1].also { current -= 1 }

    }

    fun current(): T {
        return images[current]
    }

    fun push(img: T) {
        images.add(img)
        current += 1
    }


    fun update(items: List<T>) {
        val prevSize = images.size
        images.addAll(items)
        val newSize = images.size
        if (newSize - prevSize >= 1) {
            current += 1
        }
    }
}