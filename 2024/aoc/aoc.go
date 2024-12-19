package aoc

import (
    "bufio"
    "log"
    "os"
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
