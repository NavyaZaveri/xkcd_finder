package com.myapp.xkcd_finder

class Tracker<T> {
    private var current = -1
    private val history = mutableListOf<T>()

    fun next(): T? {
        if (hasNext()) {
            return history[current + 1].also { current += 1 }

        }
        return null
    }

    fun prev(): T? {
        if (hasPrev()) {
            return history[current - 1].also { current -= 1 }
        }
        return null
    }

    private fun hasPrev(): Boolean {
        return current > 0
    }

    private fun hasNext(): Boolean {
        return current <= history.size - 2
    }

    fun current(): T? {
        if (current < 0) {
            return null
        }
        return history[current]
    }


    fun update(items: List<T>) {
        val prevSize = history.size
        history.addAll(items)
        if (history.size == prevSize) {
            current = prevSize - 1
        } else {
            current = prevSize
        }
    }
}