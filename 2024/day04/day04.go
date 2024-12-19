package main

import (
    "fmt"
    "log"
    "os"
    "regexp"

    "helpers/aoc"
)

func show(p [][]byte) {
    for _, r := range p {
        fmt.Println(string(r))
    }
    fmt.Println()
}


func count(puzzle [][]byte) int {
    total := 0
    forward := regexp.MustCompile("XMAS")
    backward := regexp.MustCompile("SAMX")
    for _, line := range puzzle {
        matches := forward.FindAll(line, -1)
        if matches != nil {
            total += len(matches)
        }
        matches = backward.FindAll(line, -1)
        if matches != nil {
            total += len(matches)
        }
    }
    return total
}

func one(puzzle [][]byte) int {
    total := 0
    total += count(puzzle)

    columns := aoc.Group(puzzle, aoc.GroupingRotate)
    total += count(columns)

    diagsD := aoc.Group(puzzle, aoc.GroupingDiagForward)
    total += count(diagsD)

    diagsU := aoc.Group(puzzle, aoc.GroupingDiagBackward)
    total += count(diagsU)
    return total
}


func two(puzzle [][]bytes) int {
    "M.S"
    ".A."
    "M.S"

    "S.M"
    ".A."
    "S.M"

    "M.M"
    ".A."
    "S.S"

    "S.S"
    ".A."
    "M.M"
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

    puzzle := aoc.ReadBytes(inName)
    show(puzzle)

    ansOne := one(puzzle)
    ansTwo := two()
    fmt.Printf("Part 1: %v\n", ansOne)
    fmt.Printf("Part 2: %v\n", ansTwo)
}
