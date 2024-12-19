package main

import (
    "fmt"
    "log"
    "os"

    "helpers/aoc"
)


func one() int {
    return 0
}


func two() int {
    return 0
}


func main() {
    log.SetPrefix("")
    log.SetFlags(0)
    if len(os.Args) != 2 {
        log.Fatal("Usage: ", os.Args[0], " <filename>\n")
    }
    inName := os.Args[1]
    fmt.Printf("Reading from: %v\n", inName)

    // ...

    ansOne := one()
    ansTwo := two()
    fmt.Printf("Part 1: %v\n", ansOne)
    fmt.Printf("Part 2: %v\n", ansTwo)
}
