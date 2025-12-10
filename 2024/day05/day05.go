package main

import (
    "fmt"
    "log"
    "os"

    "helpers/aoc"
)

var permament [99]bool
var temporary [99]bool
var unmarked map[int]bool = make(map[int]bool)

func visit(n int, graph map[int][]int) {
    if permament[n] {
        return
    }
    fmt.Printf("visit %v\n", n)
    if temporary[n] {
        log.Fatal("cycle")
    }
    delete(unmarked, n)
    temporary[n] = true
    for _, m := range graph[n] {
        visit(m, graph)
    }
    permament[n] = true
    fmt.Println(n)
}

func one(rules, queries [][]int) int {
    // Pomysł jest taki, że sortujemy topologicznie wierzchołki
    // I potem porównujemy query do posortowanych wierzchołków i sprawdzamy czy to podciąg
    // To będzie działać jeśli WSZYSTKIE wierzchołki będą połączone
    // Czyli będzie ile krawędzi? N*(N-1)/2 ?
    // Przykład na to wskazuje, ale opis nie do końca
    graph := make(map[int][]int)
    inDegrees := make(map[int]int)
    for _, rule := range rules {
        src, dst := rule[0], rule[1]
        graph[src] = append(graph[src], dst)
        inDegrees[dst] += 1
        if _, exists := inDegrees[src]; !exists {
            inDegrees[src] = 0
        }
    }
    for n, _ := range graph {
        unmarked[n] = true
    }
    fmt.Println(len(rules))
    fmt.Println(len(graph))
    //fmt.Println(graph)
    fmt.Println(inDegrees)

    for {
        if len(unmarked) <= 0 {
            return 0
        }
        for n, _ := range unmarked {
            visit(n, graph)
            break
        }
    }
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

    lines := aoc.ReadLines(inName)
    rulesRead := false
    var rules [][]int = make([][]int, 0)
    var rule []int
    var queries [][]int = make([][]int, 0)
    var query []int
    for _, l := range lines {
        if l == "" {
            rulesRead = true
        } else if !rulesRead {
            rule = aoc.AllInts(l, "|")
            rules = append(rules, rule)
        } else {
            query = aoc.AllInts(l, ",")
            queries = append(queries, query)
            //fmt.Println(query)
        }
    }

    ansOne := one(rules, queries)
    ansTwo := two()
    fmt.Printf("Part 1: %v\n", ansOne)
    fmt.Printf("Part 2: %v\n", ansTwo)
}
