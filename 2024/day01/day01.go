package main

import (
    "fmt"
    "sort"
    "helpers/aoc"
)

func one(left []int, right []int) int {
    sort.Ints(left)
    sort.Ints(right)
    sum := 0
    for i, _ := range left {
        sum += aoc.Abs(left[i] - right[i])
    }
    return sum
}

func two(left []int, right []int) int {
    count := make(map[int]int)
    for _, n := range right {
        count[n] += 1
    }
    sum := 0
    for _, n := range left {
        sum += n * count[n]
    }
    return sum
}

func main() {
    nums := aoc.ReadIntsInLines("problem.in")

    left := make([]int, len(nums))
    right := make([]int, len(nums))
    for i, pair := range nums {
        left[i], right[i] = pair[0], pair[1]
    }

    ansTwo := two(left, right)
    ansOne := one(left, right)

    fmt.Printf("Part 1: %v\n", ansOne)
    fmt.Printf("Part 2: %v\n", ansTwo)
}

