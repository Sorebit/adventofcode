package main

import (
    "fmt"
    "log"
    "os"

    "helpers/aoc"
)

func inRange(v int, a int, b int) bool {
    return a <= v && v <= b
}


func flip(r []int) {
    // Flip slice left-to-right
    for i := 0; i < len(r) / 2; i += 1 {
        r[i], r[len(r) - 1 - i] = r[len(r) - 1 - i], r[i]
    }
}

func one(reports [][]int) int {
    checkInc := func(r []int) int {
        // Check if r is strictly increasing within range of increments
        for i := 0; i < len(r) - 1; i += 1 {
            if !inRange(r[i+1] - r[i], 1, 3) {
                return 0
            }
        }
        return 1
    }

    sum := 0
    for _, r := range reports {
        if r[0] > r[1] {
            flip(r)
        }
        sum += checkInc(r)
    }
    return sum
}


func two(reports [][]int) int {
    // This problem can be viewed as checking for strictly incrementing elemements left
    // to right, then right to left.
    // The cases are short (N <= 8), so even a brute-force approach would be fine
    // I think that checking the levels only without 1 of 2 mismatched elements is better
    // There probably is some more complicated logic to do it in 1 pass
    checkWithout := func(levels []int, skip int) bool {
        // assumes len >= 2
        l, r := 0, 1
        for l < len(levels) && r < len(levels) {
            if r == skip {
                r += 1
            }
            if l == skip {
                l += 1
            }
            if l == r {
                r += 1
            }
            if r >= len(levels) || l >= len(levels) {
                break
            }

            if inRange(levels[r] - levels[l], 1, 3) {
                l += 1
                r += 1
            } else {
                return false
            }
        }
        return true
    }

    check := func(levels []int) int {
        l, r := 0, 1
        for l < len(levels) && r < len(levels) {
            if inRange(levels[r] - levels[l], 1, 3) {
                l, r = l + 1, r + 1
            } else if checkWithout(levels, l) || checkWithout(levels, r) {
                return 1
            } else {
                return 0
            }
        }
        return 1
    }

    twoWay := func(levels []int) int {
        leftToRight := check(levels)
        flip(levels)
        rightToLeft := check(levels)
        return leftToRight | rightToLeft
    }

    sum := 0
    for _, r := range reports {
        sum += twoWay(r)
    }
    return sum
}


func main() {
    log.SetPrefix("")
    log.SetFlags(0)
    if len(os.Args) != 2 {
        log.Fatal("Usage: ", os.Args[0], " <filename>\n")
    }
    inName := os.Args[1]
    fmt.Printf("Reading from: %v\n", inName)

    reports := aoc.ReadIntsInLines(inName)

    ansOne := one(reports)
    ansTwo := two(reports)
    fmt.Printf("Part 1: %v\n", ansOne)
    fmt.Printf("Part 2: %v\n", ansTwo)
}
