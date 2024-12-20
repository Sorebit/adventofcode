package aoc

import (
    "bufio"
    "log"
    "os"
    "sort"
    "strconv"
    "strings"
)

func ReadFile(filename string) string {
    content, err := os.ReadFile(filename)
    if err != nil {
        log.Fatal(err)
    }
    return string(content)
}

func ReadBytes(filename string) [][]byte {
    lines := ReadLines(filename)
    b := make([][]byte, len(lines))
    for i, line := range lines {
        b[i] = []byte(line)
    }
    return b
}

func ReadLines(filename string) []string {
    f, err := os.Open(filename)
    if err != nil {
        log.Fatal(err)
    }
    defer f.Close()

    lines := []string{}
    scanner := bufio.NewScanner(f)

    for scanner.Scan() {
        lines = append(lines, scanner.Text())
    }

    if err := scanner.Err(); err != nil {
        log.Fatal(err)
    }

    return lines
}

func ReadIntsInLines(filename string) [][]int {
    lines := ReadLines(filename)
    result := make([][]int, len(lines))

    for line_idx, line := range lines {
        fields := strings.Fields(line)
        nums := make([]int, len(fields))
        for i, n := range fields {
            nums[i] = Int(n)
        }

        result[line_idx] = nums
    }
    return result
}

func Abs(v int) int {
    if v < 0 {
        return -v
    }
    return v
}

func Int(v string) int {
    n, err := strconv.ParseInt(v, 0, 32)
    if err != nil {
        log.Fatal(err)
    }
    return int(n)
}


type Grouping func(int, int) int

func GroupingColumns(x, y int) int {
    return x
}

func GroupingDiagForward(x, y int) int {
    return x + y
}

func GroupingDiagBackward(x, y int) int {
    return x - y
}

func Group(puzzle [][]byte, key Grouping) [][]byte {
    // Given a 2D-array of bytes and a Grouping fn, return an
    // array of slices, where elements in each slice
    // Ex. if the grouping is by diagonal, each slice contains all
    //     elements of n-th diagonal
    groups := make(map[int][]byte)
    keys := make([]int, 0)
    for y, row := range puzzle {
        for x, b := range row {
            k := key(x, y)
            _, ok := groups[k]
            if !ok {
                groups[k] = []byte{b}
                keys = append(keys, k)
            } else {
                groups[k] = append(groups[k], b)
            }
        }
    }

    sort.Ints(keys)
    result := make([][]byte, len(keys))
    for i, k := range keys {
        result[i] = groups[k]
    }
    return result
}
