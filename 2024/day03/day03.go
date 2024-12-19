package main

import (
    "fmt"
    "log"
    "os"
    "regexp"
    "sort"

    "helpers/aoc"
)


func one(memory string) int {
    re := regexp.MustCompile("mul\\(([0-9]+),([0-9]+)\\)")
    matches := re.FindAllStringSubmatch(memory, -1)

    if matches == nil {
        log.Fatal("No matches for ", re)
        // return 0
    }

    total := 0
    for _, match := range matches {
        // fmt.Printf("%v %v %v\n", match, match[1], match[2])
        a, b := aoc.Int(match[1]), aoc.Int(match[2])
        total += a * b
    }

    return total
}

type Command struct {
    Kind string
    I []int
}

func two(memory string) int {
    // this was the easiest to write. I'm probably gonna regret it later though
    var commands []Command = make([]Command, 0)
    mark := func(re *regexp.Regexp, kind string) {
        //fmt.Printf("%v %v\n", re, kind)
        matches := re.FindAllStringSubmatchIndex(memory, -1)
        if matches == nil {
            log.Fatal("No matches for ", re)
        }
        for _, match := range matches {
            c := Command{kind, match}
            commands = append(commands, c)
        }
    }

    reMul := regexp.MustCompile("mul\\(([0-9]+),([0-9]+)\\)")
    reDo := regexp.MustCompile("do\\(\\)")
    reDont := regexp.MustCompile("don't\\(\\)")

    mark(reDo, "do")
    mark(reDont, "dont")
    mark(reMul, "mul")

    sort.SliceStable(commands, func(i, j int) bool {
        return commands[i].I[0] < commands[j].I[0]
    })
    // fmt.Printf("%v\n", commands)

    total := 0
    enabled := true
    for _, c := range commands {
        if c.Kind == "do" {
            enabled = true
            continue
        } else if c.Kind == "dont" {
            enabled = false
            continue
        }
        if !enabled {
            continue
        }
        a := memory[c.I[2]:c.I[3]]
        b := memory[c.I[4]:c.I[5]]
        total += aoc.Int(a) * aoc.Int(b)
        //fmt.Printf("%v * %v\n", a, b)
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

    memory := aoc.ReadFile(inName)

    ansOne := one(memory)
    ansTwo := two(memory)
    fmt.Printf("Part 1: %v\n", ansOne)
    fmt.Printf("Part 2: %v\n", ansTwo)
}
