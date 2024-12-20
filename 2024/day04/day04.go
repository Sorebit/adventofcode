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

    columns := aoc.Group(puzzle, aoc.GroupingColumns)
    total += count(columns)

    diagsD := aoc.Group(puzzle, aoc.GroupingDiagForward)
    total += count(diagsD)

    diagsU := aoc.Group(puzzle, aoc.GroupingDiagBackward)
    total += count(diagsU)
    return total
}

func two(puzzle [][]byte) int {
    extract := func(x1, y1, x2, y2 int) string {
        b := []byte{puzzle[y1][x1], puzzle[y2][x2]}
        return string(b)
    }

    total := 0
    for y := range len(puzzle) - 2 {
        for x := range len(puzzle[y]) - 2 {
            if string(puzzle[y+1][x+1]) != "A" {
                continue
            }
            down := extract(x, y, x+2, y+2)
            up := extract(x, y+2, x+2, y)
            if down != "MS" && down != "SM" {
                continue
            }
            if up != "MS" && up != "SM" {
                continue
            }
            total += 1
        }
    }

    return total
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
    //show(puzzle)

    ansOne := one(puzzle)
    ansTwo := two(puzzle)
    fmt.Printf("Part 1: %v\n", ansOne)
    fmt.Printf("Part 2: %v\n", ansTwo)
}
