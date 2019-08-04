package com.myapp.xkcd_finder

class Tracker<T : Comparable<T>> {
    var current = -1
    val images = mutableListOf<T>()
    val seen = mutableListOf<T>()

    fun next(): T {
        return if (current <= images.size - 2) {
            seen.add(images[current + 1])
            images[current + 1].also { current += 1 }

        } else {
            images.last()
        }
    }

    fun prev(): T {
        if (current == 0) {
            return images[current]
        }
        return images[current - 1].also { current -= 1 }

    }

    fun current(): T {
        seen.add(images[current])
        return images[current]
    }

    fun push(img: T) {
        images.add(img)
        current += 1
    }


    fun update(items: List<T>) {
        val prevSize = images.size
        val unseenItems = items.filter { it !in seen }
        images.addAll(unseenItems)
        val newSize = images.size
        if (newSize - prevSize >= 1) {
            current += 1
        }
    }
}