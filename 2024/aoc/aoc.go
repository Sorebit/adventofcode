package aoc

import (
    "bufio"
    "log"
    "os"
    "strconv"
    "strings"
)

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
            parsed, _ := strconv.ParseInt(n, 0, 32)
            nums[i] = int(parsed)
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

